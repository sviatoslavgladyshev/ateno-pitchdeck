"""Render grid/presenter thumbnails for any built deck folder: python3 thumbs.py deck_ru"""
import io, re, sys, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
deck = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "deck_en").resolve()
html = (deck / "index.html").read_text(encoding="utf-8")
pre = html[: re.search(r'<section class="slide', html).start()]
pre = pre[: pre.index("<body")]
secs = re.findall(r'<section class="slide[^"]*"[\s\S]*?</section>', html)
(deck / "thumbs").mkdir(exist_ok=True)
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={"width": 1920, "height": 1080})
    tmp = deck / "_thumb.html"
    for sec in secs:
        sid = re.search(r'id="([^"]+)"', sec).group(1)
        tmp.write_text(pre + '<body style="margin:0;background:#000"><div id="deck" style="position:absolute;left:0;top:0;transform:none;opacity:1;border-radius:0">'
                       + re.sub(r'class="slide', 'class="active slide', sec, count=1) + "</div></body></html>", encoding="utf-8")
        pg.goto(tmp.as_uri())
        pg.evaluate("""() => { document.querySelectorAll('video').forEach(v => v.pause());
          document.querySelectorAll('[data-build-in]').forEach(e => { e.style.opacity = 1; e.style.transform = 'none'; });
          document.querySelectorAll('.grow,.shrink,.growh').forEach(e => e.style.transition = 'none'); }""")
        pg.wait_for_timeout(400)
        png = pg.screenshot(type="png", clip={"x": 0, "y": 0, "width": 1920, "height": 1080})
        Image.open(io.BytesIO(png)).convert("RGB").resize((960, 540), Image.LANCZOS).save(deck / "thumbs" / f"{sid}.jpg", quality=85)
    tmp.unlink(); br.close()
print("thumbnails:", len(secs))
