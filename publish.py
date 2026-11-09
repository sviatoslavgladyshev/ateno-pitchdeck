"""Publish the deck to Firebase (project ateno-pitch, https://pitch.ateno.co) behind an email sign-in.

Usage:
  python3 build.py en && python3 translate_ru.py && python3 thumbs.py deck_ru   # build first
  python3 publish.py              # upload decks + deploy pages and rules
  python3 publish.py --rotate     # also change the secret path of images/thumbnails

How it is protected (the site sends no email):
- The admin creates invitations at /admin/ (admin_link.py gives the admin link) and sends each link himself.
  A link opens the deck only after the visitor confirms the invited email, and only on at most N devices
  (anonymous Firebase session per browser). The rules are in firestore.rules.
- The deck HTML is stored in Firestore: decks/<lang> for viewers (speaker notes removed), decksFull/<lang> for the admin.
- Images, videos and thumbnails are static files under /d/<random token>/; the token appears only inside
  the protected deck HTML and is kept in .deck-token (not in git).
- In the browser: invisible view code in every slide, presenter tools for the admin only, printing/saving/copying
  disabled, 3 screenshot attempts block access. A phone camera can't be blocked.

Needs: firebase CLI and gcloud, both logged in to an owner account of the project.
"""
import datetime, json, pathlib, re, secrets, shutil, subprocess, sys, urllib.request

ROOT = pathlib.Path(__file__).parent
PROJECT = "ateno-pitch"
SDK = "13.2.0"
CONFIG = {"apiKey": "AIzaSyCgPlU6KZ5hgeOhvAvDX64_f6YFL9rUJFk", "authDomain": "ateno-pitch.firebaseapp.com",
          "projectId": "ateno-pitch", "appId": "1:328461271072:web:129e66d17890400a89fc45"}

HOST = "pitch.ateno.co"
ADMIN = "glsvyatoslav@gmail.com"   # also hard-coded in firestore.rules

TEXT = {
    "en": dict(TITLE="Ateno — Pitch Deck",
               T_CONFIRM_TITLE="Confirm your email", T_CONFIRM="Enter the email address this invitation was sent to.",
               T_OPEN="Open the deck", T_LOADING="Opening the deck…", T_FOOT="Confidential",
               T_INVITE_TITLE="Invitation only", T_INVITE="This deck is shared by personal invitation. Open the link from your invitation email.",
               T_NO_MATCH="This email doesn't match the invitation.",
               T_USED="This invitation is already in use on other devices. Ask Ateno to reset it.",
               T_ERROR="Something went wrong. Try again in a moment.",
               T_SHIELD="Screenshots, printing and saving are not allowed", T_STRIKE="Attempt {n} of {max}. At {max}, access to the deck is blocked.",
               T_BLOCKED_TITLE="Access blocked", T_BLOCKED="Too many screenshot or print attempts. Contact Ateno to restore access.",
               OTHER_HREF="/ru/", OTHER_LABEL="Русский"),
    "ru": dict(TITLE="Ateno — питч-дек",
               T_CONFIRM_TITLE="Подтвердите email", T_CONFIRM="Введите адрес, на который пришло приглашение.",
               T_OPEN="Открыть дек", T_LOADING="Открываем дек…", T_FOOT="Конфиденциально",
               T_INVITE_TITLE="Только по приглашению", T_INVITE="Дек открывается по личному приглашению. Откройте ссылку из письма с приглашением.",
               T_NO_MATCH="Этот email не совпадает с приглашением.",
               T_USED="Это приглашение уже используется на других устройствах. Попросите Ateno сбросить его.",
               T_ERROR="Что-то пошло не так. Попробуйте чуть позже.",
               T_SHIELD="Скриншоты, печать и сохранение запрещены", T_STRIKE="Попытка {n} из {max}. После {max} доступ к деку будет заблокирован.",
               T_BLOCKED_TITLE="Доступ заблокирован", T_BLOCKED="Слишком много попыток скриншота или печати. Чтобы восстановить доступ, свяжитесь с Ateno.",
               OTHER_HREF="/en/", OTHER_LABEL="English"),
}
COMMON = {"SDK": SDK, "CONFIG": json.dumps(CONFIG), "HOST": HOST, "ADMIN": ADMIN}


def fill(text, values):
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    assert "{{" not in text, re.findall(r"\{\{\w+\}\}", text)
    return text


def auth_settings(access):
    """Visitors get an anonymous Firebase session (one per browser); the site never sends email."""
    url = f"https://identitytoolkit.googleapis.com/admin/v2/projects/{PROJECT}/config?updateMask=authorizedDomains,signIn.anonymous,signIn.email"
    body = {"authorizedDomains": [f"{PROJECT}.firebaseapp.com", f"{PROJECT}.web.app", HOST],
            "signIn": {"anonymous": {"enabled": True}, "email": {"enabled": False}}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="PATCH",
                                 headers={"Authorization": f"Bearer {access}", "Content-Type": "application/json",
                                          "x-goog-user-project": PROJECT})
    urllib.request.urlopen(req).read()


def token():
    f = ROOT / ".deck-token"
    if "--rotate" in sys.argv or not f.exists():
        f.write_text(secrets.token_urlsafe(24))
    return f.read_text().strip()


def protect(html, prefix):
    """Point every asset, thumbnail and the phone remote at the secret folder."""
    html, n = re.subn(r'(["\'`])(assets|thumbs|fonts)/', lambda m: m.group(1) + prefix + m.group(2) + "/", html)
    remote = "${location.pathname.replace(/[^/]*$/, '')}remote.html"
    assert remote in html, "remote.html address not found in the viewer"
    html = html.replace(remote, prefix + "remote.html")
    html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex,nofollow">', 1)
    html = html.replace("</style>\n</head>", "@media print{html,body{display:none!important}}\n</style>\n</head>", 1)
    return html, n


def upload(lang, html, access, coll="decks"):
    url = (f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents/{coll}/{lang}")
    body = {"fields": {"html": {"stringValue": html},
                       "updated": {"timestampValue": datetime.datetime.now(datetime.timezone.utc).isoformat()}}}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="PATCH",
                                 headers={"Authorization": f"Bearer {access}", "Content-Type": "application/json",
                                          "x-goog-user-project": PROJECT})
    urllib.request.urlopen(req).read()


def main():
    tok = token()
    site = ROOT / "site"
    shutil.rmtree(site, ignore_errors=True)
    gate = (ROOT / "gate/gate.html").read_text(encoding="utf-8")
    access = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, check=True).stdout.strip()
    for lang in ("en", "ru"):
        deck = ROOT / f"deck_{lang}"
        prefix = f"/d/{tok}/{lang}/"
        files = site / "d" / tok / lang
        for sub in ("assets", "fonts", "thumbs"):
            shutil.copytree(deck / sub, files / sub)
        shutil.copy(deck / "remote.html", files / "remote.html")
        html, n = protect((deck / "index.html").read_text(encoding="utf-8"), prefix)
        assert len(html.encode()) < 1_000_000, "deck HTML is over Firestore's 1 MB document limit"
        upload(lang, html, access, "decksFull")                    # admin: with speaker notes
        viewer = re.sub(r"<aside>[\s\S]*?</aside>", "<aside></aside>", html)
        assert not re.search(r"<aside>[^<]", viewer), "speaker notes left in the viewer deck"
        upload(lang, viewer, access)                                 # everyone else: no notes
        (site / lang).mkdir(parents=True, exist_ok=True)
        (site / lang / "index.html").write_text(fill(gate, {**TEXT[lang], **COMMON, "LANG": lang}), encoding="utf-8")
        print(f"{lang}: deck uploaded ({len(html)//1024} KB, {n} paths rewritten)")
    # public pages: sign-in landing, admin, shared code (none of them knows the secret folder)
    (site / "static").mkdir()
    for f in ("logo.png", "favicon.png"):
        shutil.copy(ROOT / "deck_en/assets" / f, site / "static" / f)
    shutil.copy(ROOT / "gate/gate.css", site / "static/gate.css")
    (site / "static/app.js").write_text(fill((ROOT / "gate/app.js").read_text(encoding="utf-8"), COMMON), encoding="utf-8")
    for page in ("admin",):
        (site / page).mkdir()
        (site / page / "index.html").write_text(fill((ROOT / f"gate/{page}.html").read_text(encoding="utf-8"), COMMON), encoding="utf-8")
    (site / "404.html").write_text("<!DOCTYPE html><meta charset=utf-8><title>Not found</title><meta http-equiv=refresh content=\"0;url=/en/\">")
    subprocess.run(["firebase", "deploy", "--only", "hosting,firestore", "--project", PROJECT, "--non-interactive"], check=True)
    auth_settings(access)
    print(f"live: https://{HOST}/en/  ·  admin: https://{HOST}/admin/")


if __name__ == "__main__":
    main()
