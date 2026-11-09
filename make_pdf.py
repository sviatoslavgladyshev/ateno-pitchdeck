"""Export a deck folder to a pixel-perfect PDF.
Usage: python3 make_pdf.py ateno-pitch Ateno_Pitch_Deck_EN.pdf
Each slide is rendered at 3840x2160 (2x) in its final state: animations finished,
bars filled, video posters shown. Requires: pip install playwright pillow && playwright install chromium
"""
import io, re, sys, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright

deck = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "ateno-pitch").resolve()
out = sys.argv[2] if len(sys.argv) > 2 else "deck.pdf"
html = (deck / "index.html").read_text(encoding="utf-8")
first = re.search(r'<section class="slide', html).start()
head = html[:first]
head = head[: head.index("<body")]
sections = re.findall(r'<section class="slide[^"]*"[\s\S]*?</section>', html)

pages = []
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)
    tmp = deck / "_export.html"
    for sec in sections:
        sec = re.sub(r'class="slide', 'class="active slide', sec, count=1)
        tmp.write_text(head + '<body style="margin:0;background:#000"><div id="deck" style="position:absolute;left:0;top:0;transform:none;opacity:1;border-radius:0">'
                       + sec + "</div></body></html>", encoding="utf-8")
        pg.goto(tmp.as_uri())
        pg.evaluate("""() => {
          document.querySelectorAll('video').forEach(v => { const im = document.createElement('img');
            im.src = v.getAttribute('poster'); im.setAttribute('style', v.getAttribute('style') || ''); v.replaceWith(im); });
          document.querySelectorAll('[data-build-in]').forEach(e => { e.style.opacity = 1; e.style.transform = 'none'; });
          document.querySelectorAll('.grow,.shrink,.growh').forEach(e => e.style.transition = 'none');
        }""")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        pages.append(Image.open(io.BytesIO(pg.screenshot(type="png"))).convert("RGB"))
    tmp.unlink()
    br.close()
pages[0].save(out, save_all=True, append_images=pages[1:], resolution=200.0, quality=92)
print(f"saved {out}: {len(pages)} slides")
