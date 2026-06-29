#!/usr/bin/env python3
"""Generate TG6-dev branded capability graphics (dashboard / security scan / AI).

Owned, license-free panels rendered locally in the TG6-dev palette. Rendered at
2x and downscaled (LANCZOS) for crisp anti-aliasing. Output -> ../assets/img/.
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 2  # supersample factor
W, H = 1200, 760
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")

# ---- palette ----
BG     = (10, 14, 12)
PANEL  = (17, 23, 20)
PANEL2 = (13, 18, 15)
INK    = (238, 243, 238)
MUTED  = (139, 163, 149)
DIM    = (90, 110, 99)
LIME   = (163, 230, 53)
LIMEd  = (101, 163, 13)
CYAN   = (34, 211, 238)
AMBER  = (245, 191, 66)
LINE   = (34, 48, 42)

FONTS = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size * S)
MONO   = lambda s: font("DejaVuSansMono.ttf", s)
MONOB  = lambda s: font("DejaVuSansMono-Bold.ttf", s)
SANS   = lambda s: font("DejaVuSans.ttf", s)
SANSB  = lambda s: font("DejaVuSans-Bold.ttf", s)

def canvas():
    img = Image.new("RGB", (W * S, H * S), BG)
    return img, ImageDraw.Draw(img)

def px(v):  # scale helper
    return v * S

def rrect(d, box, r, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = [px(v) for v in box]
    d.rounded_rectangle([x0, y0, x1, y1], radius=px(r), fill=fill,
                        outline=outline, width=max(1, width * S))

def glow(img, draw_fn, blur=18, alpha=255):
    """Draw on a transparent layer, blur it, composite back for a glow."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    draw_fn(ld)
    layer = layer.filter(ImageFilter.GaussianBlur(blur * S))
    img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"), (0, 0))

def window_chrome(d, title):
    rrect(d, (0, 0, W, H), 22, fill=PANEL, outline=LINE, width=1)
    # title bar
    d.line([(0, px(56)), (px(W), px(56))], fill=LINE, width=S)
    cx = px(34)
    for col in [(255, 95, 86), (255, 189, 46), (39, 201, 63)]:
        dim = tuple(int(c * 0.65) for c in col)
        d.ellipse([cx, px(22), cx + px(13), px(22) + px(13)], fill=dim)
        cx += px(22)
    tf = MONO(13)
    tw = d.textlength(title, font=tf)
    d.text(((px(W) - tw) / 2, px(20)), title, font=tf, fill=MUTED)

def save(img, name):
    img = img.resize((W, H), Image.LANCZOS)
    path = os.path.abspath(os.path.join(OUT, name))
    img.save(path, "PNG")
    print("wrote", path)

# ============================================================ DASHBOARD
def gen_dashboard():
    img, d = canvas()
    # top glow
    glow(img, lambda l: l.ellipse([px(700), px(-160), px(1300), px(260)],
         fill=(163, 230, 53, 36)), blur=60)
    d = ImageDraw.Draw(img)
    window_chrome(d, "tg6 · analytics — live")

    pad = 40
    # ---- stat tiles ----
    tiles = [("UPTIME", "99.98%", LIME), ("REQ / MIN", "12.4k", CYAN),
             ("P95 LATENCY", "38ms", LIME)]
    tw = (W - pad * 2 - 2 * 20) / 3
    ty = 84
    for i, (label, val, col) in enumerate(tiles):
        x = pad + i * (tw + 20)
        rrect(d, (x, ty, x + tw, ty + 118), 14, fill=PANEL2, outline=LINE, width=1)
        d.text((px(x + 22), px(ty + 24)), label, font=MONO(12), fill=MUTED)
        d.text((px(x + 22), px(ty + 50)), val, font=SANSB(40), fill=col)

    # ---- big area chart ----
    cx0, cy0, cx1, cy1 = pad, 240, W - pad, H - 56
    rrect(d, (cx0, cy0, cx1, cy1), 16, fill=PANEL2, outline=LINE, width=1)
    d.text((px(cx0 + 24), px(cy0 + 20)), "TRAFFIC · last 30 days", font=MONO(12), fill=MUTED)
    # plot area
    plx0, ply0, plx1, ply1 = cx0 + 24, cy0 + 60, cx1 - 24, cy1 - 36
    # grid
    for i in range(5):
        gy = ply0 + (ply1 - ply0) * i / 4
        d.line([(px(plx0), px(gy)), (px(plx1), px(gy))], fill=LINE, width=1)
    # data
    random.seed(6)
    n = 30
    base = [0.28, 0.30, 0.26, 0.34, 0.31, 0.38, 0.42, 0.39, 0.45, 0.5,
            0.47, 0.55, 0.6, 0.57, 0.63, 0.7, 0.66, 0.72, 0.78, 0.74,
            0.8, 0.86, 0.83, 0.9, 0.88, 0.93, 0.97, 0.94, 0.99, 1.0]
    pts = []
    for i in range(n):
        x = plx0 + (plx1 - plx0) * i / (n - 1)
        jitter = (random.random() - 0.5) * 0.05
        y = ply1 - (ply1 - ply0) * max(0.05, min(1, base[i] + jitter))
        pts.append((px(x), px(y)))
    # gradient fill under the line
    fill_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(fill_layer)
    poly = pts + [(px(plx1), px(ply1)), (px(plx0), px(ply1))]
    fd.polygon(poly, fill=(163, 230, 53, 46))
    img.paste(Image.alpha_composite(img.convert("RGBA"), fill_layer).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)
    # glow line + crisp line
    glow(img, lambda l: l.line(pts, fill=(163, 230, 53, 150), width=3 * S, joint="curve"), blur=8)
    d = ImageDraw.Draw(img)
    d.line(pts, fill=LIME, width=max(1, 3 * S), joint="curve")
    # secondary cyan line
    pts2 = [(x, y + px(46)) for (x, y) in pts]
    d.line(pts2, fill=CYAN, width=max(1, 2 * S), joint="curve")
    # last point marker
    lx, ly = pts[-1]
    d.ellipse([lx - px(6), ly - px(6), lx + px(6), ly + px(6)], fill=LIME)
    d.ellipse([lx - px(11), ly - px(11), lx + px(11), ly + px(11)], outline=LIME, width=S)
    save(img, "cap-dashboard.png")

# ============================================================ SECURITY SCAN
def gen_scan():
    img, d = canvas()
    glow(img, lambda l: l.ellipse([px(-200), px(380), px(420), px(900)],
         fill=(163, 230, 53, 30)), blur=70)
    d = ImageDraw.Draw(img)
    window_chrome(d, "security-scan — zsh")

    m = MONO(15)
    x = 40
    y = 88
    lh = 30
    def line(segs, dy=lh):
        nonlocal y
        cx = px(x)
        for txt, col in segs:
            d.text((cx, px(y)), txt, font=m, fill=col)
            cx += d.textlength(txt, font=m)
        y += dy
    line([("$ ", LIME), ("tg6 scan --target ", INK), ("app.client.com", CYAN), (" --owasp", MUTED)])
    line([("  running OWASP Top-10 + TLS + dependency audit…", DIM)], dy=lh + 8)
    line([("[OK]   ", LIME), ("TLS 1.3 · HSTS · modern cipher suite", INK)])
    line([("[OK]   ", LIME), ("SQLi / XSS / CSRF — ", INK), ("no findings", MUTED)])
    line([("[OK]   ", LIME), ("auth · rate-limiting · session cookies hardened", INK)])
    line([("[WARN] ", AMBER), ("cookie missing ", INK), ("SameSite=Strict", CYAN), (" · auto-fixed", DIM)])
    line([("[OK]   ", LIME), ("dependencies — ", INK), ("0 CVEs", LIME), (" across 142 packages", MUTED)])
    line([("[OK]   ", LIME), ("security headers — CSP enforced, X-Frame DENY", INK)])
    line([("[OK]   ", LIME), ("secrets scan — ", INK), ("clean", MUTED), (" · no keys in tree", DIM)], dy=lh + 14)
    line([("$ ", LIME), ("tg6 harden ", INK), ("--apply", MUTED)])
    line([("  + ", LIME), ("Strict-Transport-Security, CSP, Referrer-Policy", INK)])
    line([("  + ", LIME), ("SameSite cookies · automated backups · WAF rules", INK)])
    line([("[OK]   ", LIME), ("3 fixes applied · re-scan ", INK), ("passed", LIME)], dy=lh + 14)
    # summary bar
    by = y
    rrect(d, (x, by, W - 40, by + 64), 12, fill=PANEL2, outline=LINE, width=1)
    d.text((px(x + 20), px(by + 20)), "==>", font=MONOB(15), fill=MUTED)
    cx = px(x + 70)
    for txt, col in [("0 critical", LIME), ("  ·  ", DIM), ("1 medium", AMBER),
                     ("  ·  ", DIM), ("grade ", INK), ("A", LIME)]:
        d.text((cx, px(by + 19)), txt, font=MONOB(16), fill=col)
        cx += d.textlength(txt, font=MONOB(16))
    y = by + 64 + 26
    # blinking cursor prompt
    d.text((px(x), px(y)), "$", font=m, fill=LIME)
    d.rectangle([px(x + 22), px(y + 2), px(x + 22 + 11), px(y + 22)], fill=LIME)
    save(img, "cap-scan.png")

# ============================================================ AI / AUTOMATION
def gen_ai():
    img, d = canvas()
    glow(img, lambda l: l.ellipse([px(420), px(120), px(980), px(640)],
         fill=(34, 211, 238, 26)), blur=90)
    glow(img, lambda l: l.ellipse([px(250), px(260), px(700), px(700)],
         fill=(163, 230, 53, 26)), blur=90)
    d = ImageDraw.Draw(img)
    window_chrome(d, "tg6 · ai + automation")

    d.text((px(40), px(86)), "NEURAL ROUTING", font=MONO(12), fill=MUTED)

    # node graph: 4 layers
    layers = [3, 5, 5, 2]
    gx0, gx1 = 120, W - 120
    gy0, gy1 = 170, H - 150
    cols = []
    for li, count in enumerate(layers):
        x = gx0 + (gx1 - gx0) * li / (len(layers) - 1)
        nodes = []
        for ni in range(count):
            y = gy0 + (gy1 - gy0) * (ni + 0.5) / count
            nodes.append((x, y))
        cols.append(nodes)
    # edges: crisp alpha lines + a soft glow underneath
    def draw_edges(l, boost=0):
        random.seed(3)
        for a, b in zip(cols, cols[1:]):
            for (x0, y0) in a:
                for (x1, y1) in b:
                    on = random.random() > 0.35
                    col = (163, 230, 53) if random.random() > 0.4 else (34, 211, 238)
                    alpha = (95 if on else 38) + boost
                    l.line([(px(x0), px(y0)), (px(x1), px(y1))], fill=col + (alpha,), width=S)
    glow(img, lambda l: draw_edges(l, boost=60), blur=5)
    edge_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_edges(ImageDraw.Draw(edge_layer))
    img.paste(Image.alpha_composite(img.convert("RGBA"), edge_layer).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)
    # nodes
    for li, nodes in enumerate(cols):
        for (x, y) in nodes:
            col = CYAN if li in (0, len(cols) - 1) else LIME
            glow(img, (lambda X, Y, C: lambda l: l.ellipse(
                [px(X) - px(14), px(Y) - px(14), px(X) + px(14), px(Y) + px(14)],
                fill=C + (120,)))(x, y, col), blur=10)
            d = ImageDraw.Draw(img)
            d.ellipse([px(x) - px(9), px(y) - px(9), px(x) + px(9), px(y) + px(9)],
                      fill=PANEL2, outline=col, width=max(1, 2 * S))
            d.ellipse([px(x) - px(3), px(y) - px(3), px(x) + px(3), px(y) + px(3)], fill=col)

    # prompt bar at bottom
    py = H - 96
    rrect(d, (40, py, W - 40, py + 56), 28, fill=PANEL2, outline=LINE, width=1)
    d.text((px(64), px(py + 17)), "summarize today's leads and draft replies", font=MONO(14), fill=MUTED)
    rrect(d, (W - 40 - 116, py + 8, W - 48, py + 48), 20, fill=LIME)
    d.text((px(W - 40 - 92), px(py + 17)), "run →", font=MONOB(14), fill=(12, 18, 10))
    save(img, "cap-ai.png")

# ============================================================ OG IMAGE
def _bf(path, size, weight=None):
    f = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "fonts", path), size * S)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f

def _mark(d, x, y, s, col):
    """Draw the TG6-dev brand glyph (rounded square + chevron + underscore)."""
    u = s / 36.0
    d.rounded_rectangle([px(x + 1.5 * u), px(y + 1.5 * u), px(x + 34.5 * u), px(y + 34.5 * u)],
                        radius=px(9 * u), outline=col, width=max(1, int(round(2.5 * u * S))))
    w = max(1, int(round(3 * u * S)))
    d.line([(px(x + 11 * u), px(y + 13 * u)), (px(x + 16 * u), px(y + 18 * u)),
            (px(x + 11 * u), px(y + 23 * u))], fill=col, width=w, joint="curve")
    d.line([(px(x + 19 * u), px(y + 24 * u)), (px(x + 26 * u), px(y + 24 * u))], fill=col, width=w)

def gen_og():
    global W, H
    OW, OH = 1200, 630
    W, H = OW, OH
    img = Image.new("RGB", (OW * S, OH * S), BG)
    # glow
    glow(img, lambda l: l.ellipse([px(620), px(-220), px(1320), px(360)], fill=(163, 230, 53, 46)), blur=80)
    glow(img, lambda l: l.ellipse([px(-260), px(380), px(360), px(900)], fill=(34, 211, 238, 24)), blur=90)
    d = ImageDraw.Draw(img)

    # right-side sparkline motif (subtle)
    random.seed(6)
    base = [0.2, 0.28, 0.24, 0.36, 0.32, 0.45, 0.5, 0.46, 0.6, 0.66, 0.62, 0.78, 0.84, 0.8, 0.95, 1.0]
    sx0, sx1, sy0, sy1 = 720, 1180, 250, 520
    pts = [(px(sx0 + (sx1 - sx0) * i / (len(base) - 1)),
            px(sy1 - (sy1 - sy0) * base[i])) for i in range(len(base))]
    fl = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(fl).polygon(pts + [(px(sx1), px(sy1)), (px(sx0), px(sy1))], fill=(163, 230, 53, 26))
    img.paste(Image.alpha_composite(img.convert("RGBA"), fl).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)
    d.line(pts, fill=(163, 230, 53), width=max(1, 3 * S), joint="curve")

    # brand row
    _mark(d, 70, 60, 40, LIME)
    d.text((px(124), px(66)), "TG6", font=_bf("JetBrainsMono.ttf", 24, 700), fill=INK)
    bw = d.textlength("TG6", font=_bf("JetBrainsMono.ttf", 24, 700))
    d.text((px(124) + bw, px(66)), " · dev", font=_bf("JetBrainsMono.ttf", 24, 700), fill=LIME)

    # headline
    hf = _bf("HankenGrotesk.ttf", 86, 800)
    sf = _bf("InstrumentSerif-Italic.ttf", 96)
    x = 70
    y = 168
    lh = 96
    d.text((px(x), px(y)), "Build it.", font=hf, fill=INK)
    # line 2: "Secure" (serif italic lime) + " it."
    d.text((px(x), px(y + lh) - px(8)), "Secure", font=sf, fill=LIME)
    sw = d.textlength("Secure", font=sf)
    d.text((px(x) + sw, px(y + lh)), " it.", font=hf, fill=INK)
    d.text((px(x), px(y + 2 * lh)), "Rank it.", font=hf, fill=INK)

    # subtitle + url
    d.text((px(x), px(y + 3 * lh + 6)), "Full-stack development · Security · SEO · AI",
           font=_bf("JetBrainsMono.ttf", 21, 500), fill=MUTED)
    d.text((px(x), px(OH - 56)), "glitch6-dev.github.io/DigitalServices",
           font=_bf("JetBrainsMono.ttf", 18, 500), fill=DIM)

    img = img.resize((OW, OH), Image.LANCZOS)
    # og-image lives at the repo root (referenced by the page <head>)
    path = os.path.abspath(os.path.join(OUT, "..", "..", "og-image.png"))
    img.save(path, "PNG")
    print("wrote", path)

if __name__ == "__main__":
    gen_dashboard()
    gen_scan()
    gen_ai()
    gen_og()
    print("done")
