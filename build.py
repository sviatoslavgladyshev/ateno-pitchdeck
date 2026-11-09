"""Build the Ateno pitch deck from the slide sources.

Usage:
  python3 build.py en          # slides_en.py -> deck_en/index.html (+ thumbnails)
  python3 build.py en --no-thumbs

Edit the text and layout of slides in slides_en.py / slides_ru.py. Every slide is one
sec(...) call: an id, the HTML body (1920x1080 canvas, inline px styles), and speaker notes.
Thumbnails (used by the grid and presenter view) need: pip install playwright && playwright install chromium
"""
import importlib, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent
lang = (sys.argv[1] if len(sys.argv) > 1 else "en").lower()
assert lang in ("en", "ru"), "language must be en or ru"
mod = importlib.import_module(f"slides_{lang}")
out_dir = ROOT / f"deck_{lang}"

head = (ROOT / "template/viewer_head.html").read_text(encoding="utf-8")
tail = (ROOT / "template/viewer_tail.html").read_text(encoding="utf-8")
body = "".join(mod.slides)

if lang == "ru":
    head = head.replace('<html lang="en">', '<html lang="ru">')
    head = head.replace("<title>Ateno — Pitch Deck</title>", "<title>Ateno — питч-дек</title>")
    head = re.sub(r'<meta name="description"[^>]*>',
                  '<meta name="description" content="Ateno: чипы для построения 3D-карт прямо на роботах и дронах. Питч-дек pre-seed.">', head)
    body = body.replace(">173,161</span>", ">173 161</span>").replace(">2,073,600</span>", ">2 073 600</span>")
    tail = tail.replace("toLocaleString('en-US')", "toLocaleString('ru-RU')")

(out_dir / "index.html").write_text(head + body + tail, encoding="utf-8")
(out_dir / "remote.html").write_text((ROOT / "template/remote.html").read_text(encoding="utf-8"), encoding="utf-8")
ids = re.findall(r'<section class="slide[^"]*" id="([^"]+)"', body)
print(f"built {out_dir/'index.html'}: {len(ids)} slides")

if "--no-thumbs" not in sys.argv:
    from playwright.sync_api import sync_playwright
    (out_dir / "thumbs").mkdir(exist_ok=True)
    pre = head[: head.index("<body")]
    secs = re.findall(r'<section class="slide[^"]*"[\s\S]*?</section>', body)
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1920, "height": 1080})
        tmp = out_dir / "_thumb.html"
        for sid, sec in zip(ids, secs):
            tmp.write_text(pre + '<body style="margin:0;background:#000"><div id="deck" style="position:absolute;left:0;top:0;transform:none;opacity:1;border-radius:0">'
                           + re.sub(r'class="slide', 'class="active slide', sec, count=1) + "</div></body></html>", encoding="utf-8")
            pg.goto(tmp.as_uri())
            pg.evaluate("""() => { document.querySelectorAll('video').forEach(v => v.pause());
              document.querySelectorAll('[data-build-in]').forEach(e => { e.style.opacity = 1; e.style.transform = 'none'; });
              document.querySelectorAll('.grow,.shrink,.growh').forEach(e => e.style.transition = 'none'); }""")
            pg.wait_for_timeout(400)
            import io
            from PIL import Image
            png = pg.screenshot(type="png", clip={"x": 0, "y": 0, "width": 1920, "height": 1080})
            Image.open(io.BytesIO(png)).convert("RGB").resize((960, 540), Image.LANCZOS).save(
                out_dir / "thumbs" / f"{sid}.jpg", quality=85)
        tmp.unlink()
        br.close()
    print("thumbnails updated")
