"""Publish the deck to Firebase (project ateno-pitch, https://pitch.ateno.co) behind an email sign-in.

Usage:
  python3 build.py en && python3 translate_ru.py && python3 thumbs.py deck_ru   # build first
  python3 publish.py              # upload decks + deploy pages and rules
  python3 publish.py --rotate     # also change the secret path of images/thumbnails

How it is protected:
- /en/ and /ru/ are a sign-in form (gate/gate.html). Firebase emails a one-time link that opens /auth/,
  which proves the visitor owns that address.
- Only addresses on the access list can open the deck. The admin (ADMIN below, also in firestore.rules)
  manages the list at /admin/: add, remove, approve requests, see who opened the deck.
- The deck itself (slide text and speaker notes) is stored in Firestore (decks/en, decks/ru); firestore.rules
  let only listed, verified emails read it.
- Images, videos and thumbnails are static files under /d/<random token>/; the token appears only inside
  the protected deck HTML and is kept in .deck-token (not in git).
- In the browser: email watermark on every slide, printing/saving/copying disabled, the screen goes black on
  screenshot shortcuts. A determined viewer can still photograph the screen; the watermark shows who it was.

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
    "en": dict(TITLE="Ateno — Pitch Deck", T_TITLE="Ateno pitch deck",
               T_LEAD="Enter your email. We'll send you a sign-in link.",
               T_SEND="Send link", T_SENT_TITLE="Check your inbox", T_SENT="We sent a sign-in link to",
               T_SPAM="It can take a minute. If you don't see it, check spam.",
               T_LOADING="Opening the deck…", T_FOOT="Confidential", T_SIGNOUT="Sign out",
               T_DENIED_TITLE="Access requested", T_DENIED="This deck is shared by invitation. We've let Ateno know; you'll be able to open it once they add you.",
               T_SEND_FAIL="Couldn't send the link. Check the address and try again.",
               T_ERROR="Couldn't open the deck. Try again in a moment.",
               T_SHIELD="Screenshots are not allowed", T_PRINT="Printing and saving are disabled",
               OTHER_HREF="/ru/", OTHER_LABEL="Русский"),
    "ru": dict(TITLE="Ateno — питч-дек", T_TITLE="Питч-дек Ateno",
               T_LEAD="Введите email. Мы пришлём ссылку для входа.",
               T_SEND="Получить ссылку", T_SENT_TITLE="Проверьте почту", T_SENT="Мы отправили ссылку для входа на",
               T_SPAM="Письмо может прийти через минуту. Если его нет, проверьте спам.",
               T_LOADING="Открываем дек…", T_FOOT="Конфиденциально", T_SIGNOUT="Выйти",
               T_DENIED_TITLE="Запрос отправлен", T_DENIED="Дек открыт только по приглашению. Мы сообщили Ateno; вы сможете открыть его, когда вас добавят.",
               T_SEND_FAIL="Не удалось отправить ссылку. Проверьте адрес и попробуйте ещё раз.",
               T_ERROR="Не удалось открыть дек. Попробуйте чуть позже.",
               T_SHIELD="Скриншоты запрещены", T_PRINT="Печать и сохранение отключены",
               OTHER_HREF="/en/", OTHER_LABEL="English"),
}
COMMON = {"SDK": SDK, "CONFIG": json.dumps(CONFIG), "HOST": HOST, "ADMIN": ADMIN}


def fill(text, values):
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    assert "{{" not in text, re.findall(r"\{\{\w+\}\}", text)
    return text


def auth_settings(access):
    """HOST may sign in, and email links sign in without a password."""
    # (the link itself still goes through Firebase's page, which forwards to /auth/; Firebase does not let the API change it)
    url = f"https://identitytoolkit.googleapis.com/admin/v2/projects/{PROJECT}/config?updateMask=authorizedDomains,signIn.email"
    body = {"authorizedDomains": [f"{PROJECT}.firebaseapp.com", f"{PROJECT}.web.app", HOST],
            "signIn": {"email": {"enabled": True, "passwordRequired": False}}}
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


def upload(lang, html, access):
    url = (f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents/decks/{lang}")
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
        upload(lang, html, access)
        (site / lang).mkdir(parents=True, exist_ok=True)
        (site / lang / "index.html").write_text(fill(gate, {**TEXT[lang], **COMMON, "LANG": lang}), encoding="utf-8")
        print(f"{lang}: deck uploaded ({len(html)//1024} KB, {n} paths rewritten)")
    # public pages: sign-in landing, admin, shared code (none of them knows the secret folder)
    (site / "static").mkdir()
    for f in ("logo.png", "favicon.png"):
        shutil.copy(ROOT / "deck_en/assets" / f, site / "static" / f)
    shutil.copy(ROOT / "gate/gate.css", site / "static/gate.css")
    (site / "static/app.js").write_text(fill((ROOT / "gate/app.js").read_text(encoding="utf-8"), COMMON), encoding="utf-8")
    for page in ("auth", "admin"):
        (site / page).mkdir()
        (site / page / "index.html").write_text(fill((ROOT / f"gate/{page}.html").read_text(encoding="utf-8"), COMMON), encoding="utf-8")
    (site / "404.html").write_text("<!DOCTYPE html><meta charset=utf-8><title>Not found</title><meta http-equiv=refresh content=\"0;url=/en/\">")
    subprocess.run(["firebase", "deploy", "--only", "hosting,firestore", "--project", PROJECT, "--non-interactive"], check=True)
    auth_settings(access)
    print(f"live: https://{HOST}/en/  ·  admin: https://{HOST}/admin/")


if __name__ == "__main__":
    main()
