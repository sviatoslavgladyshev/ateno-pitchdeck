"""Publish the deck to Firebase (project ateno-pitch) behind an email sign-in.

Usage:
  python3 build.py en && python3 translate_ru.py && python3 thumbs.py deck_ru   # build first
  python3 publish.py              # upload decks + deploy hosting, rules and auth
  python3 publish.py --rotate     # also change the secret path of images/thumbnails

How it is protected:
- The public pages /en/ and /ru/ are only a sign-in form (gate/gate.html). Firebase emails a one-time
  sign-in link; opening it proves the visitor owns that address.
- The deck itself (slide text and speaker notes) is stored in Firestore (decks/en, decks/ru). The rules in
  firestore.rules let only signed-in visitors with a verified email read it.
- Images, videos and thumbnails are static files under /d/<random token>/; the token appears only inside
  the protected deck HTML. It is kept in .deck-token (not in git). --rotate makes old links to files stop working.
- Every opening is logged to Firestore -> views (email, language, time).

Needs: firebase CLI and gcloud, both logged in to an owner account of the project.
"""
import datetime, json, pathlib, re, secrets, shutil, subprocess, sys, urllib.request

ROOT = pathlib.Path(__file__).parent
PROJECT = "ateno-pitch"
SDK = "13.2.0"
CONFIG = {"apiKey": "AIzaSyCgPlU6KZ5hgeOhvAvDX64_f6YFL9rUJFk", "authDomain": "ateno-pitch.firebaseapp.com",
          "projectId": "ateno-pitch", "appId": "1:328461271072:web:129e66d17890400a89fc45"}

TEXT = {
    "en": dict(TITLE="Ateno — Pitch Deck", T_TITLE="Ateno pitch deck",
               T_LEAD="Enter your email. We'll send you a link to open the deck.",
               T_SEND="Send link", T_SENT_TITLE="Check your inbox", T_SENT="We sent a sign-in link to",
               T_SPAM="It can take a minute. If you don't see it, check spam.",
               T_CONFIRM_TITLE="Confirm your email", T_CONFIRM="Enter the address the link was sent to.",
               T_OPEN="Open the deck", T_LOADING="Opening the deck…", T_FOOT="Confidential",
               T_SEND_FAIL="Couldn't send the link. Check the address and try again.",
               T_LINK_FAIL="This link has expired or was already used. Request a new one.",
               T_NO_ACCESS="Couldn't open the deck. Request a new link.",
               OTHER_HREF="/ru/", OTHER_LABEL="Русский"),
    "ru": dict(TITLE="Ateno — питч-дек", T_TITLE="Питч-дек Ateno",
               T_LEAD="Введите email. Мы пришлём ссылку для входа.",
               T_SEND="Получить ссылку", T_SENT_TITLE="Проверьте почту", T_SENT="Мы отправили ссылку для входа на",
               T_SPAM="Письмо может прийти через минуту. Если его нет, проверьте спам.",
               T_CONFIRM_TITLE="Подтвердите email", T_CONFIRM="Введите адрес, на который пришла ссылка.",
               T_OPEN="Открыть дек", T_LOADING="Открываем дек…", T_FOOT="Конфиденциально",
               T_SEND_FAIL="Не удалось отправить ссылку. Проверьте адрес и попробуйте ещё раз.",
               T_LINK_FAIL="Ссылка устарела или уже использована. Запросите новую.",
               T_NO_ACCESS="Не удалось открыть дек. Запросите новую ссылку.",
               OTHER_HREF="/en/", OTHER_LABEL="English"),
}


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
        page = gate
        for k, v in {**TEXT[lang], "LANG": lang, "SDK": SDK, "CONFIG": json.dumps(CONFIG), "ASSETS": "/static/"}.items():
            page = page.replace("{{" + k + "}}", v)
        assert "{{" not in page, re.findall(r"\{\{\w+\}\}", page)
        (site / lang).mkdir(parents=True, exist_ok=True)
        (site / lang / "index.html").write_text(page, encoding="utf-8")
        print(f"{lang}: deck uploaded ({len(html)//1024} KB, {n} paths rewritten)")
    # the public sign-in page must not reveal the secret folder, so it has its own logo and icon
    (site / "static").mkdir()
    for f in ("logo.png", "favicon.png"):
        shutil.copy(ROOT / "deck_en/assets" / f, site / "static" / f)
    (site / "404.html").write_text("<!DOCTYPE html><meta charset=utf-8><title>Not found</title><meta http-equiv=refresh content=\"0;url=/en/\">")
    subprocess.run(["firebase", "deploy", "--only", "hosting,firestore,auth", "--project", PROJECT, "--non-interactive"], check=True)


if __name__ == "__main__":
    main()
