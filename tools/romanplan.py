"""romanplan.py — a tiny SVG toolkit implementing the Gens Togata diegetic
Roman visual language for floor plans and diagrams.

Palette and conventions are derived from the Tabula Peutingeriana / OmnesViae
aesthetic and tied to the Gens Togata rulebook (same parchment / maroon / gold).
Everything is original vector art — no third-party image is copied.
"""

# --- palette (shared with the Gens Togata rulebook) ---
INK    = "#2a1d0c"   # walls, labels (dark sepia)
PARCH  = "#efe3c6"   # parchment ground
PARCH2 = "#e6d6ac"   # faint room tint
POCHE  = "#3a2a14"   # filled wall thickness
STONE  = "#cdb98a"   # paving / steps
WATER  = "#6f8d7e"   # impluvium, piscina (TP green-water)
WATER2 = "#577567"
GARDEN = "#8a9a62"   # hortus greenery
ACCENT = "#6e1b1b"   # maroon rules / cartouche
GOLD   = "#8a5a12"   # keys, scale, accents

SERIF = "'Gentium Book Basic','Times New Roman','DejaVu Serif',serif"

PES = 12  # user units per Roman foot (pes ~ 0.296 m)


def defs():
    """Reusable <defs>: floor patterns and a column symbol."""
    return f"""<defs>
  <pattern id="mosaic" width="9" height="9" patternUnits="userSpaceOnUse">
    <rect width="9" height="9" fill="{PARCH2}"/>
    <path d="M0 0H9M0 4.5H9M0 0V9M4.5 0V9" stroke="{INK}" stroke-width="0.35" opacity="0.5"/>
    <circle cx="4.5" cy="4.5" r="0.5" fill="{INK}" opacity="0.5"/>
  </pattern>
  <pattern id="water" width="14" height="7" patternUnits="userSpaceOnUse">
    <rect width="14" height="7" fill="{WATER}"/>
    <path d="M0 2 q3.5 -2 7 0 t7 0 M0 5 q3.5 -2 7 0 t7 0" fill="none" stroke="{WATER2}" stroke-width="0.7"/>
  </pattern>
  <pattern id="garden" width="16" height="16" patternUnits="userSpaceOnUse">
    <rect width="16" height="16" fill="{GARDEN}" opacity="0.32"/>
    <path d="M4 11 V6 M2.5 8 L4 6 L5.5 8 M12 13 V8 M10.5 10 L12 8 L13.5 10" stroke="{GARDEN}" stroke-width="0.8" fill="none" opacity="0.9"/>
    <circle cx="9" cy="3" r="0.7" fill="{GARDEN}"/><circle cx="2" cy="14" r="0.7" fill="{GARDEN}"/>
  </pattern>
  <pattern id="hypocaust" width="10" height="10" patternUnits="userSpaceOnUse">
    <rect width="10" height="10" fill="{PARCH2}"/>
    <rect x="3" y="3" width="4" height="4" fill="none" stroke="{INK}" stroke-width="0.4" opacity="0.6"/>
  </pattern>
  <g id="columna">
    <circle r="3.1" fill="{POCHE}"/><circle r="1.4" fill="{PARCH}"/>
  </g>
  <filter id="rough" x="-4%" y="-4%" width="108%" height="108%">
    <feTurbulence type="fractalNoise" baseFrequency="0.013 0.017" numOctaves="3" seed="11" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="roughmap" x="-4%" y="-4%" width="108%" height="108%">
    <feTurbulence type="fractalNoise" baseFrequency="0.016 0.02" numOctaves="3" seed="5" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="3.1" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="mottle">
    <feTurbulence type="fractalNoise" baseFrequency="0.009 0.013" numOctaves="4" seed="8" result="t"/>
    <feColorMatrix in="t" type="matrix" values="0 0 0 0 0.42  0 0 0 0 0.31  0 0 0 0 0.15  0 0 0 1.4 -0.55"/>
  </filter>
  <radialGradient id="age" cx="50%" cy="46%" r="75%">
    <stop offset="50%" stop-color="#6e4a1b" stop-opacity="0"/>
    <stop offset="100%" stop-color="#4e3312" stop-opacity="0.44"/>
  </radialGradient>
  <radialGradient id="stain" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#6b4a1e" stop-opacity="0.26"/>
    <stop offset="65%" stop-color="#6b4a1e" stop-opacity="0.09"/>
    <stop offset="100%" stop-color="#6b4a1e" stop-opacity="0"/>
  </radialGradient>
</defs>"""


def stainblobs(w, h, seed=42, n=8):
    import random
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        cx = rnd.uniform(0.06, 0.94) * w
        cy = rnd.uniform(0.06, 0.94) * h
        r = rnd.uniform(0.035, 0.10) * min(w, h)
        out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="url(#stain)"/>')
    return "\n".join(out)


def X(p, x0): return x0 + p * PES
def Y(p, y0): return y0 + p * PES


class Plan:
    def __init__(self, x0, y0):
        self.x0, self.y0 = x0, y0
        self.body = []

    def px(self, p): return self.x0 + p * PES
    def py(self, p): return self.y0 + p * PES

    def footprint(self, x0, y0, x1, y1):
        self.body.append(f'<rect x="{self.px(x0):.1f}" y="{self.py(y0):.1f}" '
                         f'width="{(x1-x0)*PES:.1f}" height="{(y1-y0)*PES:.1f}" fill="{POCHE}"/>')

    def room(self, x0, y0, x1, y1, fill=PARCH):
        f = {"mosaic": "url(#mosaic)", "water": "url(#water)", "garden": "url(#garden)",
             "hypo": "url(#hypocaust)", "stone": STONE}.get(fill, fill)
        self.body.append(f'<rect x="{self.px(x0):.1f}" y="{self.py(y0):.1f}" '
                         f'width="{(x1-x0)*PES:.1f}" height="{(y1-y0)*PES:.1f}" fill="{f}"/>')

    def pool(self, x0, y0, x1, y1):
        self.room(x0, y0, x1, y1, "water")
        self.body.append(f'<rect x="{self.px(x0):.1f}" y="{self.py(y0):.1f}" '
                         f'width="{(x1-x0)*PES:.1f}" height="{(y1-y0)*PES:.1f}" '
                         f'fill="none" stroke="{INK}" stroke-width="1"/>')

    def door(self, x0, y0, x1, y1, fill=PARCH):
        """Carve a doorway (parchment bridge) across a wall."""
        self.room(x0, y0, x1, y1, fill)

    def threshold(self, x0, y0, x1, y1):
        """A paved threshold mark inside a doorway."""
        self.room(x0, y0, x1, y1, "stone")

    def column(self, p, q):
        self.body.append(f'<use href="#columna" x="{self.px(p):.1f}" y="{self.py(q):.1f}"/>')

    def colonnade(self, pts):
        for p, q in pts:
            self.column(p, q)

    def label(self, p, q, text, size=9, color=INK, spacing=1.1):
        self.body.append(
            f'<text x="{self.px(p):.1f}" y="{self.py(q):.1f}" font-family="{SERIF}" '
            f'font-size="{size}" fill="{color}" text-anchor="middle" '
            f'letter-spacing="{spacing}" style="text-transform:uppercase">{text}</text>')

    def axis(self, p, q0, q1):
        self.body.append(f'<line x1="{self.px(p):.1f}" y1="{self.py(q0):.1f}" '
                         f'x2="{self.px(p):.1f}" y2="{self.py(q1):.1f}" stroke="{ACCENT}" '
                         f'stroke-width="0.7" stroke-dasharray="2 3" opacity="0.6"/>')

    def svg(self):
        return "\n".join(self.body)


# ---- page furniture ----

def tabula_ansata(cx, cy, w, h, title, sub=""):
    """A Roman inscription tablet (dovetail handles) for the plan title."""
    x0, y0 = cx - w / 2, cy - h / 2
    ah = h * 0.5
    s = [f'<g>']
    s.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" '
             f'rx="2" fill="{PARCH}" stroke="{ACCENT}" stroke-width="1.6"/>')
    s.append(f'<rect x="{x0+3:.1f}" y="{y0+3:.1f}" width="{w-6:.1f}" height="{h-6:.1f}" '
             f'fill="none" stroke="{ACCENT}" stroke-width="0.6"/>')
    # dovetail ansae
    for sgn, hx in ((-1, x0), (1, x0 + w)):
        tip = hx + sgn * h * 0.55
        s.append(f'<path d="M{hx:.1f} {cy-ah/2:.1f} L{tip:.1f} {cy-ah*0.72:.1f} '
                 f'L{tip:.1f} {cy+ah*0.72:.1f} L{hx:.1f} {cy+ah/2:.1f} Z" '
                 f'fill="{PARCH}" stroke="{ACCENT}" stroke-width="1.2"/>')
    s.append(f'<text x="{cx:.1f}" y="{cy + (2 if not sub else -2):.1f}" font-family="{SERIF}" '
             f'font-size="17" fill="{ACCENT}" text-anchor="middle" letter-spacing="2.5" '
             f'style="text-transform:uppercase">{title}</text>')
    if sub:
        s.append(f'<text x="{cx:.1f}" y="{cy+13:.1f}" font-family="{SERIF}" font-size="8" '
                 f'fill="{INK}" text-anchor="middle" letter-spacing="1.5" '
                 f'font-style="italic">{sub}</text>')
    s.append('</g>')
    return "\n".join(s)


def scalebar(x, y, pedes=40, step=10):
    w = pedes * PES
    s = [f'<g>']
    s.append(f'<text x="{x:.1f}" y="{y-6:.1f}" font-family="{SERIF}" font-size="7.5" '
             f'fill="{INK}" letter-spacing="1.3" style="text-transform:uppercase">pedes romani</text>')
    n = pedes // step
    for i in range(n):
        fill = INK if i % 2 == 0 else PARCH
        s.append(f'<rect x="{x+i*step*PES:.1f}" y="{y:.1f}" width="{step*PES:.1f}" height="6" '
                 f'fill="{fill}" stroke="{INK}" stroke-width="0.8"/>')
    for i in range(n + 1):
        s.append(f'<text x="{x+i*step*PES:.1f}" y="{y+16:.1f}" font-family="{SERIF}" '
                 f'font-size="7" fill="{INK}" text-anchor="middle">{i*step}</text>')
    s.append('</g>')
    return "\n".join(s)


def groma(cx, cy, r=18):
    """Surveyor's cross marking the cardo / decumanus with SEPTENTRIO north."""
    s = [f'<g stroke="{INK}" stroke-width="0.9">']
    s.append(f'<line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}"/>')
    s.append(f'<line x1="{cx}" y1="{cy-r}" x2="{cx}" y2="{cy+r}"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="2.2" fill="{ACCENT}" stroke="none"/>')
    s.append(f'<path d="M{cx} {cy-r-7} L{cx-3} {cy-r} L{cx+3} {cy-r} Z" fill="{INK}" stroke="none"/>')
    s.append('</g>')
    s.append(f'<text x="{cx}" y="{cy-r-10}" font-family="{SERIF}" font-size="7" fill="{INK}" '
             f'text-anchor="middle" letter-spacing="1">SEPTENTRIO</text>')
    return "\n".join(s)


def page(w, h, inner, rough="rough"):
    border = (f'<rect x="12" y="12" width="{w-24}" height="{h-24}" fill="none" '
              f'stroke="{ACCENT}" stroke-width="2.2"/>'
              f'<rect x="17" y="17" width="{w-34}" height="{h-34}" fill="none" '
              f'stroke="{ACCENT}" stroke-width="0.7"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">\n{defs()}\n'
            f'<rect width="{w}" height="{h}" fill="{PARCH}"/>\n'
            f'<rect width="{w}" height="{h}" filter="url(#mottle)" opacity="0.5"/>\n'
            f'{stainblobs(w, h)}\n'
            f'<g filter="url(#{rough})">\n{border}\n{inner}\n</g>\n'
            f'<rect width="{w}" height="{h}" fill="url(#age)"/>\n</svg>')
