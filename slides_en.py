# Ateno pitch deck slides, in the viewer's slide format (1920x1080, inline px styles).
F = "font-family:'Inter', -apple-system, Arial, sans-serif"
DARK = "#05050a"; DARK2 = "#08080f"; LIGHT = "#07070d"
INK_D = "#f5f5f7"; SUB_D = "#86868b"; EYE_D = "#a593f5"
INK_L = "#f5f5f7"; SUB_L = "#a1a1a6"; EYE_L = "#a593f5"; CARD_L = "rgba(255,255,255,.045)"
GRAD = "linear-gradient(90deg, #a78bfa, #60a5fa 55%, #34d399)"
MONO = "font-family:'JetBrains Mono', ui-monospace, monospace"
BORDER = "border:1px solid rgba(255,255,255,.09)"
GT = f"background:{GRAD};-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent"

N_TOTAL = 19
_n = [0]

import random, hashlib, re
SPLAT_COLORS = ["#a78bfa", "#60a5fa", "#34d399", "#8b5cf6"]
def splats(seed, n=4):
    """Soft Gaussian 'splats' behind each slide: the product's own primitive, used as the brand texture."""
    r = random.Random(int(hashlib.md5(seed.encode()).hexdigest()[:8], 16))
    defs, els = "", ""
    for i in range(n):
        c = r.choice(SPLAT_COLORS)
        gid = f"sp-{seed}-{i}"
        defs += f'<radialGradient id="{gid}"><stop offset="0" stop-color="{c}" stop-opacity="{r.uniform(.16,.26):.2f}"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
        corner = i % 4
        cx = r.uniform(-120, 520) if corner in (0, 3) else r.uniform(1400, 2040)
        cy = r.uniform(-140, 360) if corner in (0, 1) else r.uniform(720, 1220)
        rx, ry, rot = r.uniform(360, 720), r.uniform(160, 340), r.uniform(0, 180)
        els += f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="url(#{gid})" transform="rotate({rot:.0f} {cx:.0f} {cy:.0f})"/>'
    return (f'<svg aria-hidden="true" width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;left:0;top:0;width:1920px;height:1080px">'
            f'<defs>{defs}</defs>{els}</svg>'
            '<div style="position:absolute;left:0;top:0;width:1920px;height:1080px;background-image:radial-gradient(rgba(255,255,255,.07) 1.2px, transparent 1.6px);background-size:36px 36px"></div>')

def foot(dark):
    _n[0] += 1
    cross = ('<svg aria-hidden="true" width="26" height="26" viewBox="0 0 26 26" style="width:26px;height:26px">'
             '<g fill="none" stroke="#8b7cf6" stroke-width="1.6"><circle cx="13" cy="13" r="7"/><path d="M13 0v7M13 19v7M0 13h7M19 13h7"/></g></svg>')
    left = (f'<p style="position:absolute;left:72px;bottom:52px;{MONO};font-size:19px;letter-spacing:1px;color:#6e6e73">Pre-seed · November 2026</p>')
    return left + (f'<div style="position:absolute;right:72px;bottom:52px;display:flex;align-items:center;gap:16px">'
            f'<p style="{MONO};font-size:19px;letter-spacing:1px;color:#6e6e73">{_n[0]:02d} / {N_TOTAL:02d}</p>'
            f'<img src="assets/logo.png" alt="Ateno" style="width:30px;height:auto;opacity:.9"></div>')

def sec(id, body, notes, dark=True, bg=None, trans="push", section=None, extra=""):
    light = id in LIGHT_IDS
    if light:
        body = to_light(body); bg = "#fbfbfd"; col = "#1d1d1f"
    else:
        bg = bg or DARK; col = INK_D
    ds = f' data-section="{section}"' if section else ""
    cls = "slide" if light else "slide dk"
    body = re.sub(r'<div([^>]*?)style="([^"]*?border-radius:3[26]px[^"]*?padding[^"]*?)"', lambda m: f'<div{m.group(1)}class="card{" hi" if "ede9fe" in m.group(2) or "139,124,246" in m.group(2) else ""}" style="{m.group(2)}"', body)
    return (f'<section class="{cls}" id="{id}" data-transition="{trans}"{ds} style="background:{bg};color:{col};{F};{extra}">\n'
            f'{body}\n{foot(dark) if id != 'cover' else re.sub(r'^<p[^>]*>Pre-seed · November 2026</p>', '', foot(dark))}\n<aside>{notes}</aside>\n</section>\n')

# Mostly light deck; dark only for the key statement slides.
LIGHT_IDS = {"problem", "today", "product", "speed", "bottleneck", "training", "roadmap",
             "applications", "model", "competition", "traction", "team", "ask"}
LIGHT_MAP = [
    ("#f5f5f7", "#1d1d1f"), ("#a1a1a6", "#6e6e73"), ("#7c7c85", "#86868b"), ("#a593f5", "#6d4fe0"),
    ("rgba(255,255,255,.045)", "#f2f2f5"), ("border:1px solid rgba(255,255,255,.09)", "border:1px solid rgba(0,0,0,.04)"),
    ("rgba(139,124,246,.14)", "#ede9fe"), ("rgba(139,124,246,.16)", "#ede9fe"), ("rgba(139,124,246,.10)", "#f4f1fe"),
    ("rgba(255,255,255,.05)", "#ffffff"), ("rgba(255,255,255,.14)", "#e5e5ea"), ("rgba(255,255,255,.03)", "#f5f5f7"),
    ("linear-gradient(#0d0d16,#0d0d16) padding-box", "linear-gradient(#fbfbfd,#fbfbfd) padding-box"),
    ("#c4b5fd", "#5b3fd6"), ("#c7c7cc", "#4b4b52"), ("#2c2c2e", "#e5e5ea"), ("#3a3a3c", "#d2d2d7"),
    ("#1c1c1e", "#ececf0"), ("#636366", "#aeaeb2"), ("border:2px solid rgba(167,139,250,.6)", "border:2px solid #c4b5fd"),
]
def to_light(h):
    for a, b in LIGHT_MAP:
        h = h.replace(a, b)
    return h

def eyebrow(t, dark=True, b=None):
    a = f' data-build-in="fade {b}"' if b else ""
    return (f'<div{a} style="display:flex;align-items:center;gap:22px;width:100%">'
            f'<p style="{MONO};font-size:21px;font-weight:500;color:{EYE_D};letter-spacing:3px;text-transform:uppercase;white-space:nowrap">'
            f'<span style="color:#86868b">{_n[0]+1:02d} /</span> {t}</p>'
            f'<div style="flex:1;height:1px;background:rgba(134,134,139,.35)"></div></div>')

def h2(a, b=None, dark=True, size=80, width=None):
    w = f"width:{width}px;" if width else ""
    second = f' <br><span style="color:#7c7c85">{b}</span>' if b else ""
    return f'<h2 style="font-size:{size}px;font-weight:700;letter-spacing:-{size*0.032:.1f}px;line-height:1.05;{w}">{a}{second}</h2>'

def label(t, x, y, w=600, align="left", dark=True, right=None):
    pos = f"right:{right}px;" if right is not None else f"left:{x}px;"
    return f'<p style="position:absolute;{pos}top:{y}px;width:{w}px;font-size:24px;color:{"#86868b" if dark else "#86868b"};text-align:{align}">{t}</p>'

# ---------- icons (simple strokes) ----------
def icon(kind, color):
    p = {
        "patent": '<path d="M14 4h26l12 12v44H14z"/><path d="M40 4v12h12"/><path d="M22 28h22M22 36h22M22 44h12"/>',
        "building": '<rect x="10" y="14" width="44" height="40" rx="3"/><path d="M4 22 32 6l28 16"/><path d="M24 54V38h16v16"/>',
        "tunnel": '<path d="M6 56V34a26 26 0 0 1 52 0v22"/><path d="M18 56V36a14 14 0 0 1 28 0v20"/><path d="M2 56h60"/>',
        "crane": '<path d="M14 58V8h4v50"/><path d="M16 10h40"/><path d="M50 10v14"/><rect x="44" y="24" width="12" height="9" rx="1"/><path d="M16 10 6 20h10"/><path d="M8 58h18"/>',
        "pilot": '<path d="M4 24 32 12l28 12-28 12z"/><path d="M16 30v12c0 4 8 8 16 8s16-4 16-8V30"/><path d="M58 25v14"/>',
        "chip": '<rect x="16" y="16" width="32" height="32" rx="4"/><rect x="25" y="25" width="14" height="14" rx="2"/><path d="M24 8v8M32 8v8M40 8v8M24 48v8M32 48v8M40 48v8M8 24h8M8 32h8M8 40h8M48 24h8M48 32h8M48 40h8"/>',
        "drone": '<circle cx="14" cy="14" r="8"/><circle cx="50" cy="14" r="8"/><circle cx="14" cy="50" r="8"/><circle cx="50" cy="50" r="8"/><path d="M20 20l8 8M44 20l-8 8M20 44l8-8M44 44l-8-8"/><rect x="26" y="26" width="12" height="12" rx="3"/>',
        "box": '<path d="M8 20 32 8l24 12v24L32 56 8 44z"/><path d="M8 20l24 12 24-12M32 32v24"/>',
        "users": '<circle cx="22" cy="22" r="9"/><path d="M6 54c0-10 7-16 16-16s16 6 16 16"/><circle cx="44" cy="24" r="7"/><path d="M42 38c9 0 16 5 16 14"/>',
    }[kind]
    return (f'<div class="ibox"><svg aria-hidden="true" width="44" height="44" viewBox="0 0 64 64" style="width:44px;height:44px">'
            f'<g fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{p}</g></svg></div>')

def card(icon_kind, title, text, b, dark=False):
    bg = CARD_L
    tc = INK_D
    sc = "#a1a1a6"
    ic = icon(icon_kind, EYE_D if dark else EYE_L) if icon_kind else ""
    return (f'<div data-build-in="rise {b}" style="flex:1;background:{bg};{BORDER};border-radius:32px;padding:52px;display:flex;flex-direction:column;gap:20px">'
            f'<p class="tag">0{b}</p>{ic}<h3 style="font-size:40px;font-weight:700;letter-spacing:-1px;color:{tc}">{title}</h3>'
            f'<p style="font-size:28px;line-height:1.4;color:{sc}">{text}</p></div>')

def chip(t, pos="left:16px;top:16px"):
    return (f'<p style="position:absolute;{pos};{MONO};font-size:15px;letter-spacing:2px;text-transform:uppercase;color:#fff;'
            f'background:rgba(0,0,0,.5);padding:6px 12px;border-radius:3px">{t}</p>')

def pcard(img, title, text, b, pos="50% 50%"):
    """Photo card: a website render on top, the claim underneath."""
    return (f'<div data-build-in="rise {b}" style="flex:1;display:flex;flex-direction:column;gap:22px">'
            f'<div style="position:relative;height:300px;border-radius:4px;overflow:hidden;background:#111">'
            f'<img src="assets/{img}" alt="" style="width:100%;height:300px;object-fit:cover;object-position:{pos}">{chip("Illustration")}</div>'
            f'<p class="tag" style="position:static">0{b}</p>'
            f'<h3 style="font-size:40px;font-weight:700;letter-spacing:-1px;margin-top:-12px">{title}</h3>'
            f'<p style="font-size:27px;line-height:1.4;color:#a1a1a6;margin-top:-8px">{text}</p></div>')

slides = []
P128 = "padding:128px;display:flex;flex-direction:column;justify-content:center;gap:72px"

# 1 COVER
slides.append(sec("cover", f'''
<video src="assets/chip-reveal.mp4" poster="assets/chip-poster.jpg" muted loop playsinline autoplay style="position:absolute;left:700px;top:0;width:1220px;height:1080px;object-fit:cover"></video>
<div style="position:absolute;left:700px;top:0;width:560px;height:1080px;background:linear-gradient(90deg,#05050a,rgba(5,5,10,0))"></div>
<div style="position:absolute;left:128px;top:300px;width:700px;display:flex;flex-direction:column;gap:36px">
<img data-build-in="fade 1" src="assets/logo.png" alt="Ateno logo" style="width:120px;height:auto">
<h1 data-build-in="rise 2" style="font-size:150px;font-weight:700;letter-spacing:-5px;line-height:1">Ateno</h1>
<p data-build-in="rise 3" style="font-size:46px;line-height:1.25;color:#a1a1a6;font-weight:500;letter-spacing:-.6px">Navigation that doesn't<br>depend on GPS</p>
</div>
<p style="position:absolute;left:128px;bottom:120px;font-size:24px;color:#6e6e73">Sviatoslav Gladyshev · Co-founder &amp; CEO · info@ateno.co · Pre-seed · November 2026</p>
{label("Concept render", 0, 920, 400, "right", right=72)}
''', "Ateno builds a dedicated chip that lets autonomous systems build 3D maps on board and navigate without GPS. The chip on screen is a concept render, not silicon.", trans="fade", section="Problem"))

# 2 PROBLEM
slides.append(sec("problem", f'''
<div style="display:flex;flex-direction:column;gap:28px">{eyebrow("The problem", False)}{h2("Every autonomous system asks:", "where am I?", False, 84)}</div>
<div style="display:flex;gap:40px">
{pcard("place-bridge.webp", "Denied", "GPS can be jammed, spoofed or simply absent.", 1, "50% 40%")}
{pcard("place-underground.webp", "Underground and indoors", "Tunnels, mines and buildings have no signal at all.", 2)}
{pcard("place-site.webp", "Disconnected", "No reliable link to a server. The map has to be built on board.", 3, "50% 60%")}
</div>''', "GPS answers the question until it doesn't: it can be denied, faked, or never there. And there is often no link to send data anywhere. The machine has to build a 3D map from its own cameras, while it moves, and locate itself in it. The three pictures are illustrations from our website, not field footage.", dark=False, extra=P128.replace("gap:72px", "gap:64px")))

# 3 TODAY
def tstat(num, text, b):
    return (f'<div data-build-in="rise {b}" style="border-top:1px solid #2c2c2e;padding-top:22px">'
            f'<p style="font-size:76px;font-weight:700;letter-spacing:-2.5px;line-height:1">{num}</p>'
            f'<p style="font-size:25px;color:#a1a1a6;margin-top:10px;line-height:1.35">{text}</p></div>')
slides.append(sec("today", f'''
<div style="position:absolute;left:128px;top:128px;width:1664px;display:flex;flex-direction:column;gap:26px">{eyebrow("Today")}{h2("The best 3D maps come from Gaussian Splatting.", "Building one takes a datacenter GPU.", True, 64)}</div>
<div style="position:absolute;left:128px;top:392px;width:920px;height:530px;border-radius:6px;overflow:hidden;background:#000">
<video src="assets/orbit.mp4" poster="assets/orbit-poster.jpg" muted loop playsinline autoplay style="width:1196px;height:689px;object-fit:cover;margin-left:-138px;margin-top:-60px"></video></div>
{label("3DGS scene, shown in a software viewer", 128, 934, 920)}
<div style="position:absolute;left:1120px;top:392px;width:672px;display:flex;flex-direction:column;gap:30px">
{tstat("0.4–5 FPS", "Published Gaussian SLAM on NVIDIA Jetson. Too slow to navigate with.", 1)}
{tstat("4–24 h", "To reconstruct a large scene on GPUs. Record now, map later.", 2)}
{tstat("20–80 GB", "GPU memory for large scenes. Nothing on board comes close.", 3)}
</div>''', "Gaussian Splatting builds photorealistic maps from ordinary cameras. But building one is a training job. Sources: published Gaussian SLAM benchmarks; 30+ practitioner interviews since May 2026."))

# 4 INSIGHT
slides.append(sec("insight", f'''
<div style="position:absolute;left:0;top:0;width:1920px;height:1080px;background:radial-gradient(circle at 50% 70%, rgba(60,40,140,.45) 0%, rgba(0,0,0,0) 60%)"></div>
<div style="position:absolute;left:60px;top:210px;width:1800px;display:flex;flex-direction:column;align-items:center;gap:30px;text-align:center">
{eyebrow("Our insight")}
<h2 style="font-size:94px;font-weight:700;letter-spacing:-3.5px;line-height:1.08">A robot doesn't need to view a map. <br><span style="{GT}">It needs to build one.</span></h2>
</div>
<div data-build-in="rise 1" style="position:absolute;left:360px;top:680px;width:1200px;display:flex;align-items:center;gap:56px">
<p style="font-size:190px;font-weight:800;letter-spacing:-8px;line-height:1;{GT}"><span data-count="77">77</span>%</p>
<p style="font-size:34px;line-height:1.4;color:#a1a1a6;width:640px">of 3DGS training time is the backward pass and optimizer. Our hardware is designed around it.</p>
</div>''', "We profiled the reference pipeline (gsplat on an NVIDIA L4) before writing any RTL. Building the map is training, and training is where the compute goes. Most accelerators stop at rendering.", trans="push"))

# 5 PRODUCT
def spec(k, v, b, hi=False):
    vc = "#c4b5fd" if hi else INK_D
    return (f'<div data-build-in="fade {b}" style="display:flex;gap:28px;align-items:baseline;border-top:1px solid #2c2c2e;padding:16px 0 0">'
            f'<p style="width:170px;flex:none;{MONO};font-size:16px;letter-spacing:2.5px;color:#86868b;text-transform:uppercase">{k}</p>'
            f'<p style="font-size:25px;line-height:1.3;color:{vc}">{v}</p></div>')
slides.append(sec("product", f'''
<div style="position:absolute;left:1000px;top:0;width:920px;height:1080px;overflow:hidden;background:#1a1a1c">
<img src="assets/chip-silver.jpg" alt="Ateno AX chip, concept render" style="width:920px;height:1080px;object-fit:cover;object-position:46% 50%"></div>
<p style="position:absolute;right:72px;top:64px;font-size:16px;color:#ffffff;background:rgba(0,0,0,.45);padding:7px 14px;border-radius:3px;{MONO};letter-spacing:2px;text-transform:uppercase">Concept render</p>
<div style="position:absolute;left:128px;top:96px;width:800px;height:888px;display:flex;flex-direction:column;justify-content:center;gap:34px">
{eyebrow("The product")}
<div style="display:flex;flex-direction:column;gap:18px">
<h1 style="font-size:124px;font-weight:700;letter-spacing:-5px;line-height:.95">Ateno&nbsp;AX</h1>
<p style="font-size:34px;line-height:1.25;color:#a1a1a6;font-weight:500;letter-spacing:-.4px">One chip that builds the map and renders it.<br>On the device, offline.</p></div>
<div style="display:flex;flex-direction:column;gap:16px">
{spec("Input", "Frames from the robot's own cameras", 1)}
{spec("Builds", "A 3D Gaussian map, trained on the chip", 2)}
{spec("Renders", "Photorealistic views, 1080p today", 3)}
{spec("Link", "None needed. Nothing leaves the device", 4)}
{spec("Ships as", "Compute module, or IP block in an SoC", 5)}
{spec("Poses", "Software today (COLMAP); on-chip next", 6)}
{spec("Status", "Rendering and training run on FPGA", 7, True)}
</div></div>''', "Ateno AX is one chip for one workload: it trains the 3D map and renders it, on the device, with no connection. The chip image is a concept render, not silicon. Be precise about what exists: rendering and training run on our FPGA prototype; camera poses are still computed in software.", bg=DARK2, section="Product"))

# 5b MODULE
slides.append(sec("module", f'''
<img src="assets/device-main.webp" alt="Concept render of the Ateno AX module connected to a laptop by a USB-C cable" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;object-position:30% 50%">
<div style="position:absolute;left:0;top:0;width:1920px;height:1080px;background:linear-gradient(200deg,rgba(5,5,10,.82) 0%,rgba(5,5,10,.35) 38%,rgba(5,5,10,0) 60%)"></div>
<div style="position:absolute;right:120px;top:128px;width:900px;display:flex;flex-direction:column;gap:28px">
{eyebrow("Form factor")}
<h2 data-build-in="rise 1" style="font-size:76px;font-weight:700;letter-spacing:-3px;line-height:1.05">One small module. <br><span style="color:#c7c7cc">Plugs into the robot.</span></h2>
<p data-build-in="rise 2" style="font-size:32px;line-height:1.4;color:#d2d2d7">The first product is an edge module around the chip. Later, the same design as an IP block inside an SoC.</p>
</div>
{chip("Concept render", "left:72px;top:64px")}
''', "This is how the first product would look: a small compute module that sits on the robot. It is a concept render; no module has been built. What exists today is the design running on an FPGA.", bg=DARK))

# 6 PROOF
slides.append(sec("proof", f'''
<div style="position:absolute;left:1032px;top:100px;width:760px;height:760px;border-radius:6px;overflow:hidden;background:#000">
<video src="assets/buildup.mp4" poster="assets/fpga-frame.jpg" muted playsinline autoplay style="width:760px;height:760px;object-fit:cover"></video></div>
{label("Illustrative build-up. The final frame is our FPGA render (AWS F2).", 1032, 876, 760)}
<div style="position:absolute;left:128px;top:150px;width:840px;display:flex;flex-direction:column;gap:28px">{eyebrow("What already runs")}{h2("This frame was rendered by our hardware.", None, True, 80)}</div>
<div style="position:absolute;left:128px;top:560px;width:840px;display:grid;grid-template-columns:1fr 1fr;gap:48px 48px">
<div data-build-in="rise 1"><p style="font-size:84px;font-weight:700;letter-spacing:-3px;line-height:1"><span data-count="173161">173,161</span></p><p style="font-size:26px;color:#a1a1a6;margin-top:10px">Gaussians in the scene</p></div>
<div data-build-in="rise 2"><p style="font-size:84px;font-weight:700;letter-spacing:-3px;line-height:1"><span data-count="2073600">2,073,600</span></p><p style="font-size:26px;color:#a1a1a6;margin-top:10px">pixels, computed by our design</p></div>
<div data-build-in="rise 3"><p style="font-size:84px;font-weight:700;letter-spacing:-3px;line-height:1">1080p</p><p style="font-size:26px;color:#a1a1a6;margin-top:10px">end to end on the FPGA</p></div>
<div data-build-in="rise 4"><p style="font-size:84px;font-weight:700;letter-spacing:-3px;line-height:1">Closed</p><p style="font-size:26px;color:#a1a1a6;margin-top:10px">timing on AWS F2</p></div>
</div>''', "Full 1080p rendering ran end to end on an AWS F2 FPGA, September 2026. The build-up animation is illustrative; the final frame is the FPGA output. If asked about GPUs: today the FPGA is about 70x slower than an NVIDIA L4 on this frame (262 ms vs about 3.7 ms). What carries over to silicon is the cycle count, not FPGA wall-clock.", section="Proof"))

# 7 SPEED
def vbar(h, label, value, grad, b):
    bg = GRAD.replace("90deg", "0deg") if grad else "repeating-linear-gradient(135deg,#c7c7cc 0 3px,#ececf0 3px 12px)"
    vc = INK_L
    return (f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:end;gap:18px;width:220px;height:560px">'
            f'<p data-build-in="fade {b}" style="font-size:44px;font-weight:700;letter-spacing:-1px;color:{vc};white-space:nowrap">{value}</p>'
            f'<div class="growh" style="width:160px;height:{h}px;border-radius:3px;background:{bg}"></div>'
            f'<p style="font-size:26px;color:{SUB_L}">{label}</p></div>')
slides.append(sec("speed", f'''
<div style="position:absolute;left:128px;top:128px;width:900px;display:flex;flex-direction:column;gap:28px">{eyebrow("Progress", False)}{h2("From one second to 262 ms.", "In ten days.", False, 84)}</div>
<div data-build-in="rise 1" style="position:absolute;left:128px;top:520px;width:700px;display:flex;flex-direction:column;gap:18px">
<p style="font-size:220px;font-weight:800;letter-spacing:-9px;line-height:.95;{GT}">3.9×</p>
<p style="font-size:34px;line-height:1.35;color:{SUB_L}">faster frame time, same 1080p scene,<br>173,161 Gaussians, FPGA core at 100 MHz.</p>
</div>
<div style="position:absolute;left:1020px;top:300px;width:772px;height:660px;background:rgba(255,255,255,.045);border-radius:36px;display:flex;align-items:end;justify-content:center;gap:120px;padding:0 0 40px">
{vbar(420, "Aug 31", "1.02 s", False, 2)}
{vbar(108, "Sep 10", "262 ms", True, 3)}
</div>
<p style="position:absolute;left:128px;top:930px;width:860px;font-size:24px;color:#86868b">Not fast yet, and we know exactly why: next slide.</p>
''', "Same scene, same resolution. 1.02 s on August 31, 262 ms on September 10: 3.9 times faster. Not fast yet: the next slide shows exactly where the time goes.", dark=False, trans="push"))

# 8 BOTTLENECK
def stage(name, pct, ms, color, b, hi=False):
    w = int(560 * pct / 100)
    nc = "#c4b5fd" if hi else INK_D
    return (f'<div data-build-in="rise {b}" style="display:flex;flex-direction:column;gap:14px;border-top:1px solid #2c2c2e;padding-top:26px">'
            f'<div style="display:flex;align-items:baseline;justify-content:space-between"><p style="font-size:34px;font-weight:{700 if hi else 600};color:{nc}">{name}</p>'
            f'<p style="font-size:34px;font-weight:700;font-variant-numeric:tabular-nums;color:{nc}">{pct}%<span style="color:#86868b"> · ≈{ms} ms</span></p></div>'
            f'<div style="height:10px;width:560px;border-radius:2px;background:#1c1c1e"><div class="grow" style="height:10px;width:{w}px;border-radius:2px;background:{color}"></div></div></div>')
slides.append(sec("bottleneck", f'''
<div style="position:absolute;left:128px;top:128px;width:1664px;display:flex;flex-direction:column;gap:28px">{eyebrow("Where the time goes")}{h2("Three quarters of every frame is sorting.", "That's what we fix next.", True, 80)}</div>
<div data-build-in="pop 1" style="position:absolute;left:150px;top:400px;width:520px;height:520px">
<svg aria-label="Frame time breakdown: frontend 19%, sorting 75%, render 6%" width="520" height="520" viewBox="0 0 520 520" style="position:absolute;left:0;top:0;width:520px;height:520px"><defs><linearGradient id="sortg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a78bfa"/><stop offset=".55" stop-color="#60a5fa"/><stop offset="1" stop-color="#34d399"/></linearGradient></defs><circle cx="260" cy="260" r="200" fill="none" stroke="#3a3a3c" stroke-width="64" stroke-dasharray="232.8 1256.6" stroke-dashoffset="0.0" transform="rotate(-90 260 260)"/><circle cx="260" cy="260" r="200" fill="none" stroke="url(#sortg)" stroke-width="64" stroke-dasharray="936.5 1256.6" stroke-dashoffset="-238.8" transform="rotate(-90 260 260)"/><circle cx="260" cy="260" r="200" fill="none" stroke="#636366" stroke-width="64" stroke-dasharray="69.4 1256.6" stroke-dashoffset="-1181.2" transform="rotate(-90 260 260)"/></svg>
<p style="position:absolute;left:0;top:200px;width:520px;text-align:center;font-size:76px;font-weight:800;letter-spacing:-2.5px">262 ms</p>
<p style="position:absolute;left:0;top:296px;width:520px;text-align:center;font-size:26px;color:#86868b">per 1080p frame</p>
</div>
<div style="position:absolute;left:1000px;top:440px;width:792px;display:flex;flex-direction:column;gap:34px">
{stage("Sorting", 75, 197, GRAD, 2, True)}
{stage("Frontend", 19, 50, "#8e8e93", 3)}
{stage("Render", 6, 16, "#636366", 4)}
</div>
<p style="position:absolute;left:128px;top:940px;width:1664px;font-size:24px;color:#86868b">Measured on our FPGA (1080p, 100 MHz); ms = share of 262 ms. Our own bottleneck, not a GPU one.</p>
''', "This is our own bottleneck on the FPGA, not a GPU problem: on GPUs, sorting is about 12% of training time. Fixing our sorting engine is the next step. The milliseconds are simply the percentages applied to 262 ms.", bg=DARK))

# 9 TRAINING
def tstep(i, x, name, sub, status, scol, sbg, b, hi=False):
    bg = "rgba(139,124,246,.14)" if hi else CARD_L
    return (f'<div data-build-in="rise {b}" style="position:absolute;left:{x}px;top:430px;width:360px;height:230px;background:{bg};{BORDER};border-radius:32px;padding:30px 30px;display:flex;flex-direction:column;justify-content:space-between">'
            f'<div><p style="{MONO};font-size:18px;letter-spacing:2px;color:#86868b">0{i}</p>'
            f'<h3 style="font-size:40px;font-weight:700;letter-spacing:-1px;margin-top:8px">{name}</h3>'
            f'<p style="font-size:24px;color:#a1a1a6;margin-top:4px">{sub}</p></div>'
            f'<p style="align-self:start;{MONO};font-size:17px;letter-spacing:2px;text-transform:uppercase;color:{scol};background:{sbg};padding:7px 12px;border-radius:3px">{status}</p></div>')
def tnum(n, t, b):
    return (f'<div data-build-in="fade {b}" style="flex:1;display:flex;align-items:baseline;gap:18px;border-top:1px solid #2c2c2e;padding-top:20px">'
            f'<p style="font-size:64px;font-weight:700;letter-spacing:-2px;line-height:1">{n}</p><p style="font-size:24px;color:#a1a1a6;line-height:1.3">{t}</p></div>')
GREEN = ("#1f8a52", "rgba(48,164,108,.12)"); AMBER = ("#b45309", "rgba(245,165,36,.14)")
slides.append(sec("training", f'''
<div style="position:absolute;left:128px;top:128px;width:1664px;display:flex;flex-direction:column;gap:26px">{eyebrow("Training in hardware", False)}{h2("Most accelerators stop at rendering.", "The whole training loop runs on our FPGA.", False, 72)}</div>
{tstep(1, 128, "Render", "Gaussians → image", "✓ On FPGA", *GREEN, 1)}
{tstep(2, 562, "Compare", "vs the camera frame", "✓ On FPGA", *GREEN, 2)}
{tstep(3, 996, "Backward", "gradients", "✓ On FPGA", *GREEN, 3)}
{tstep(4, 1430, "Adam update", "new Gaussians", "✓ On FPGA", *GREEN, 4, True)}
<svg aria-hidden="true" width="74" height="40" viewBox="0 0 74 40" style="position:absolute;left:488px;top:540px;width:74px;height:40px"><path d="M10 20H60" stroke="#8b7cf6" stroke-width="2.5"/><path d="M52 11L64 20L52 29" fill="none" stroke="#8b7cf6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg><svg aria-hidden="true" width="74" height="40" viewBox="0 0 74 40" style="position:absolute;left:922px;top:540px;width:74px;height:40px"><path d="M10 20H60" stroke="#8b7cf6" stroke-width="2.5"/><path d="M52 11L64 20L52 29" fill="none" stroke="#8b7cf6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg><svg aria-hidden="true" width="74" height="40" viewBox="0 0 74 40" style="position:absolute;left:1356px;top:540px;width:74px;height:40px"><path d="M10 20H60" stroke="#8b7cf6" stroke-width="2.5"/><path d="M52 11L64 20L52 29" fill="none" stroke="#8b7cf6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
<svg aria-hidden="true" width="1664" height="110" viewBox="0 0 1664 110" style="position:absolute;left:128px;top:672px;width:1664px;height:110px"><defs><marker id="lh" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#8b7cf6"/></marker></defs><path d="M1482 4V70H180V12" fill="none" stroke="#8b7cf6" stroke-width="2.5" stroke-dasharray="8 7" marker-end="url(#lh)"/></svg>
<p style="position:absolute;left:128px;top:752px;width:1664px;text-align:center;{MONO};font-size:19px;letter-spacing:2px;color:#6d4fe0;text-transform:uppercase">Repeated thousands of times per scene</p>
<div style="position:absolute;left:128px;top:826px;width:1664px;display:flex;gap:48px">
{tnum("13×", "faster Adam step on FPGA<br>vs our CPU reference (1 Gaussian)", 5)}
{tnum("723", "tests passing<br>in our regression suite", 6)}
{tnum("20", "claims in our UAE<br>patent application", 7)}
</div>''', "This is the standard Gaussian Splatting training step: render, compare with the camera frame, backpropagate, update. All four stages run on our FPGA prototype. The 13x figure is the Adam step benchmarked on a single Gaussian (51 microseconds vs 665 on CPU). Next: large scenes and energy efficiency.", dark=False))

# 10 ROADMAP
def step(tag, title, text, b, hi=False):
    bd = f"border:3px solid transparent;background:linear-gradient(#0d0d16,#0d0d16) padding-box,{GRAD} border-box" if hi else "border:3px solid #2c2c2e;background:rgba(255,255,255,.03)"
    return (f'<div data-build-in="rise {b}" style="flex:1;border-radius:32px;padding:52px;{bd};display:flex;flex-direction:column;gap:18px">'
            f'<p style="font-size:24px;font-weight:600;color:{EYE_D}">{tag}</p><h3 style="font-size:40px;font-weight:700;letter-spacing:-1px">{title}</h3>'
            f'<p style="font-size:28px;line-height:1.4;color:#a1a1a6">{text}</p></div>')
slides.append(sec("roadmap", f'''
<div style="display:flex;flex-direction:column;gap:28px">{eyebrow("Roadmap")}{h2("FPGA proof first.", "Silicon only after.", True, 88)}</div>
<div style="display:flex;gap:32px">
{step("Done · Jun–Nov 2026", "Working prototype", "1080p rendering and full training on FPGA. 723 tests passing.", 1)}
{step("This round", "Scale and efficiency", "Large, real-world scenes. Energy benchmark vs Jetson and GPU.", 2, True)}
{step("After proof", "Silicon", "Pick the process node from measured needs. Tape out with design partners.", 3)}
</div>
<p style="font-size:26px;color:#86868b">No tape-out until performance, power and economics are proven on the FPGA.</p>''', "Tape-out is gated on Phase 2 results. Do not promise a silicon date.", bg=DARK2, extra=P128))

# 11 MARKET
slides.append(sec("market", f'''
<div style="position:absolute;left:0;top:0;width:1920px;height:1080px;background:radial-gradient(circle at 75% 60%, rgba(30,70,130,.45) 0%, rgba(0,0,0,0) 60%)"></div>
<div style="position:absolute;left:128px;top:128px;display:flex;flex-direction:column;gap:28px">{eyebrow("Market")}{h2("Every robot that moves", "needs to see in 3D.", True, 88)}</div>
<div style="position:absolute;left:128px;top:450px;width:1664px;display:flex;gap:96px">
<div data-build-in="rise 1"><p style="font-size:150px;font-weight:800;letter-spacing:-6px;line-height:1">2.8M</p><p style="font-size:30px;color:#a1a1a6;margin-top:16px">mobile robots shipped per year by 2030<br>(ABI Research)</p></div>
<div data-build-in="rise 2"><p style="font-size:150px;font-weight:800;letter-spacing:-6px;line-height:1;{GT}">$170–560M</p><p style="font-size:30px;color:#a1a1a6;margin-top:16px">per year in modules at 20% adoption and<br>$300–1,000 a unit, from mobile robots alone</p></div>
</div>
<p style="position:absolute;left:128px;bottom:120px;font-size:24px;color:#6e6e73">Before drones and other autonomous systems, and IP licensing. A scenario, not a forecast.</p>''', "2.8M times 20% times $300 is about $170M; times $1,000 is about $560M. Drones, other autonomous systems and IP royalties are upside on top.", section="Business"))

# 11b APPLICATIONS
slides.append(sec("applications", f'''
<div style="display:flex;flex-direction:column;gap:28px">{eyebrow("Applications", False)}{h2("Built for autonomy", "where GPS can't be trusted.", False, 76)}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:28px">
<div data-build-in="rise 1" style="background:rgba(139,124,246,.14);border:2px solid rgba(167,139,250,.6);border-radius:4px;padding:20px;display:flex;gap:32px;align-items:center"><div style="position:relative;width:300px;height:180px;flex:none;border-radius:3px;overflow:hidden;background:#000"><img src="assets/map-bridge.webp" alt="" style="width:300px;height:180px;object-fit:cover"></div><div><h3 style="font-size:36px;font-weight:700;letter-spacing:-1px">Autonomous drones</h3><p style="font-size:26px;color:#c7c7cc;margin-top:8px;line-height:1.35">Navigation where GPS is jammed, spoofed or unavailable.</p></div></div>
<div data-build-in="rise 2" style="background:{CARD_L};{BORDER};border-radius:4px;padding:20px;display:flex;gap:32px;align-items:center"><div style="position:relative;width:300px;height:180px;flex:none;border-radius:3px;overflow:hidden;background:#000"><img src="assets/map-construction.webp" alt="" style="width:300px;height:180px;object-fit:cover"></div><div><h3 style="font-size:36px;font-weight:700;letter-spacing:-1px">Ground robots</h3><p style="font-size:26px;color:{SUB_L};margin-top:8px;line-height:1.35">Unmapped or changing terrain, with no link to a server.</p></div></div>
<div data-build-in="rise 3" style="background:{CARD_L};{BORDER};border-radius:4px;padding:20px;display:flex;gap:32px;align-items:center"><div style="position:relative;width:300px;height:180px;flex:none;border-radius:3px;overflow:hidden;background:#000"><img src="assets/map-floor.webp" alt="" style="width:300px;height:180px;object-fit:cover"></div><div><h3 style="font-size:36px;font-weight:700;letter-spacing:-1px">Critical infrastructure</h3><p style="font-size:26px;color:{SUB_L};margin-top:8px;line-height:1.35">Security and inspection of sites where data must stay on site.</p></div></div>
<div data-build-in="rise 4" style="background:{CARD_L};{BORDER};border-radius:4px;padding:20px;display:flex;gap:32px;align-items:center"><div style="position:relative;width:300px;height:180px;flex:none;border-radius:3px;overflow:hidden;background:#000"><img src="assets/map-tunnel.webp" alt="" style="width:300px;height:180px;object-fit:cover"></div><div><h3 style="font-size:36px;font-weight:700;letter-spacing:-1px">Tunnels and underground</h3><p style="font-size:26px;color:{SUB_L};margin-top:8px;line-height:1.35">Mines, tunnels and subterranean spaces with no signal at all.</p></div></div>
</div>
<p style="font-size:26px;color:#86868b">Every one of these needs the same thing: a map built on board, in real time, with nothing sent off the device.</p>
<p style="position:absolute;right:72px;top:72px;font-size:20px;color:#86868b">Maps: simulated scenes, illustrations</p>''', "GPS-denied, disconnected operation is the common thread. Drones and ground robots increasingly have to map and localize on board, with no GPS and no link. Elbit Systems' engineering leadership sees strong potential and is interested as we mature; our current stage is early for them. Name Elbit only with their OK. The map pictures are simulated scenes from our website.", dark=False, extra=P128.replace("gap:72px", "gap:52px")))

# 12 MODEL
def mcard(tag, title, text, b):
    return (f'<div data-build-in="rise {b}" style="flex:1;background:{CARD_L};{BORDER};border-radius:32px;padding:52px;display:flex;flex-direction:column;gap:18px">'
            f'<p class="tag">0{b}</p><p style="{MONO};font-size:20px;letter-spacing:2px;text-transform:uppercase;color:{EYE_L}">{tag}</p><h3 style="font-size:40px;font-weight:700;letter-spacing:-1px">{title}</h3>'
            f'<p style="font-size:28px;line-height:1.4;color:{SUB_L}">{text}</p></div>')
slides.append(sec("model", f'''
<div style="display:flex;flex-direction:column;gap:28px">{eyebrow("Business model", False)}{h2("Three ways we make money.", None, False, 88)}</div>
<div style="display:flex;gap:32px">
{mcard("First", "Design partnerships", "Drone and robot platform makers fund the engineering to fit the chip to their system. About $120K each.", 1)}
{mcard("Then", "Compute modules", "An edge module at $300–1,000 a unit, in every robot that maps.", 2)}
{mcard("At scale", "IP licensing", "A per-chip royalty for SoC vendors that integrate our block.", 3)}
</div>
<p style="font-size:26px;color:#86868b">No revenue today. Design partnerships are what we sell first.</p>''', "We start with paid design partnerships, which fund the engineering and validate demand before silicon.", dark=False, extra=P128))

# 13 COMPETITION
def row(a, b, c, hi=False):
    st = f"background:rgba(139,124,246,.14);" if hi else ""
    fw = "font-weight:700;" if hi else ""
    return (f'<div style="display:flex;{st}border-top:1px solid #2c2c2e;padding:30px 28px;border-radius:{"4px" if hi else "0"}">'
            f'<p style="width:30%;font-size:30px;{fw}">{a}</p><p style="width:38%;font-size:30px;color:#c7c7cc;{fw}">{b}</p><p style="width:32%;font-size:30px;color:{"#c4b5fd" if hi else "#a1a1a6"};{fw}">{c}</p></div>')
slides.append(sec("competition", f'''
<div style="display:flex;flex-direction:column;gap:28px">{eyebrow("Landscape")}{h2("Today's edge chips weren't built", "to make the map.", True, 84)}</div>
<div data-build-in="fade 1" style="display:flex;flex-direction:column">
<div style="display:flex;padding:0 28px 18px"><p style="width:30%;font-size:24px;color:#86868b">Who</p><p style="width:38%;font-size:24px;color:#86868b">What they do</p><p style="width:32%;font-size:24px;color:#86868b">The gap</p></div>
{row("NVIDIA Jetson, Qualcomm", "General-purpose edge compute", "0.4–5 FPS on Gaussian SLAM")}
{row("Edge-AI NPUs", "Accelerate neural networks", "Not the 3DGS dataflow; partners")}
{row("Academic accelerators", "GSCore, StreamingGS and others", "Not products; mostly rendering")}
{row("Ateno", "Training and rendering in hardware", "Built for the robot", True)}
</div>''', "Edge-AI NPU companies accelerate neural nets, so they are potential partners rather than competitors.", bg=DARK2, extra=P128))

# 14 TRACTION
slides.append(sec("traction", f'''
<div style="display:flex;flex-direction:column;gap:28px">{eyebrow("Traction", False)}{h2("Early, and real.", None, False, 92)}</div>
<div style="display:flex;gap:32px">
{card("pilot", "Pilot", "Research pilot with the S.M.A.R.T. Construction Research Group at NYU Abu Dhabi.", 1)}
{card("chip", "Industry", "Elbit Systems' engineering sees strong potential in our technology.", 2)}
{card("users", "Demand", "30+ practitioner interviews; several said they would pay $3–5K per project.", 3)}
{card("patent", "IP", "Patent application submitted in the UAE, with 20 claims on our hardware.", 4)}
</div>
<p style="font-size:26px;color:#86868b">No revenue or LOI yet. The pilot is unpaid; the willingness to pay is verbal.</p>''', "Be honest about the stage: interest and an unpaid pilot, not contracts. Elbit: strong interest in the technology, but our stage is early for them; no commitment.", dark=False, extra=P128.replace("gap:72px","gap:52px"), section="Team and ask"))

# 15 TEAM
def person(ini, name, role, text, b):
    return (f'<div data-build-in="rise {b}" style="flex:1;background:{CARD_L};{BORDER};border-radius:32px;padding:60px;display:flex;flex-direction:column;gap:18px">'
            f'<img src="assets/{ {"SG": "sviat.webp", "AM": "artemii.jpg"}[ini] }" alt="" style="width:210px;height:210px;border-radius:6px;object-fit:cover">'
            f'<h3 style="font-size:48px;font-weight:700;letter-spacing:-1.2px;margin-top:10px">{name}</h3>'
            f'<p style="font-size:30px;font-weight:600;color:{EYE_L}">{role}</p><p style="font-size:28px;line-height:1.4;color:{SUB_L}">{text}</p></div>')
slides.append(sec("team", f'''
<div style="display:flex;flex-direction:column;gap:28px">{eyebrow("Team", False)}{h2("From idea to working hardware", "in five months.", False, 84)}</div>
<div style="display:flex;gap:32px">
{person("SG", "Sviatoslav Gladyshev", "Co-founder &amp; CEO", "Mathematics at NYU; condensed-matter research on excitons in bilayer graphene. Previously co-founder and CTO of LevelUp.", 1)}
{person("AM", "Artemii Mavlitov", "Co-founder &amp; CTO", "Leads RTL design. Data Science and Mathematics at NYU. ICPC and CCPC regional medalist.", 2)}
</div>''', "Rendering and training paths were built in about five months, June to October 2026, by the two of us.", dark=False, extra=P128))

# 16 ASK
def ms(n, t, d, b):
    return (f'<div data-build-in="rise {b}" style="flex:1;border-top:2px solid #3a3a3c;padding-top:34px;display:flex;flex-direction:column;gap:14px">'
            f'<p style="font-size:26px;font-weight:600;color:{EYE_D}">{n}</p><h3 style="font-size:40px;font-weight:700;letter-spacing:-1px">{t}</h3>'
            f'<p style="font-size:28px;line-height:1.4;color:#a1a1a6">{d}</p></div>')
slides.append(sec("ask", f'''
<div style="display:flex;flex-direction:column;gap:28px">{eyebrow("The ask")}<h2 style="font-size:100px;font-weight:700;letter-spacing:-3.5px;line-height:1.05">Raising a pre-seed round <br>of <span style="{GT}">$1.25M</span>.</h2></div>
<div style="display:flex;gap:40px">
{ms("01", "GPU benchmark", "Energy per frame, FPGA vs GPU and Jetson, on real scenes.", 1)}
{ms("02", "Large scenes", "Training and rendering on large, real-world scenes.", 2)}
{ms("03", "Design partners", "First paid engagements with drone and autonomous-system makers.", 3)}
</div>''', "We are raising $1.25M pre-seed. Be ready to say what it buys and for how long: the three milestones on this slide, and the runway in months.", extra="padding:128px;display:flex;flex-direction:column;justify-content:center;gap:110px"))

# 17 CLOSE
slides.append(sec("close", f'''
<div style="position:absolute;left:0;top:0;width:1920px;height:1080px;background:radial-gradient(circle at 50% 45%, rgba(60,40,140,.5) 0%, rgba(0,0,0,0) 62%)"></div>
<div style="position:absolute;left:160px;top:300px;width:1600px;display:flex;flex-direction:column;align-items:center;gap:44px;text-align:center">
<img data-build-in="pop 1" src="assets/logo.png" alt="Ateno logo" style="width:150px;height:auto">
<h2 data-build-in="rise 2" style="font-size:112px;font-weight:700;letter-spacing:-4px;line-height:1.05">Build the map <span style="{GT}">on the device.</span></h2>
<p data-build-in="fade 3" style="font-size:38px;color:#a1a1a6">No GPS. No cloud. info@ateno.co · ateno.co</p>
</div>''', "Thank you."))

assert len(slides) == N_TOTAL, len(slides)
