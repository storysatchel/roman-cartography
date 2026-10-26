"""draw_domus.py — re-draws a canonical Roman atrium-peristyle domus in the
Gens Togata diegetic visual language. Original vector art.
Outputs domus.svg.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import romanplan as R
from romanplan import Plan, tabula_ansata, scalebar, groma, page, INK, GOLD, ACCENT, SERIF

# page geometry
W, H = 940, 1240
x0, y0 = 150, 165          # interior origin (pes 0,0 top-left = back of house)
p = Plan(x0, y0)

# solid wall block, then carve rooms out of it (subtractive poche)
p.footprint(-1.2, -1.2, 41.2, 79)

# --- back / top band: peristyle court flanked by reception + service rooms ---
p.room(1.2, 1.2, 13, 13)                 # TRICLINIVM (dining)
p.room(1.2, 14.2, 13, 26)                # CVLINA (kitchen)
p.room(28, 1.2, 38.8, 13)                # OECVS (hall)
p.room(28, 14.2, 38.8, 26)              # CVBICVLVM
p.room(14.2, 1.2, 26.8, 26, "stone")     # PERISTYLIVM ambulatory (paved)
p.room(16, 3.2, 25, 24, "garden")        # HORTVS (garden)
p.pool(18.5, 11, 22.5, 17)               # PISCINA

# peristyle colonnade (ring just inside the court)
cols = []
for px in (15.2, 18.1, 21, 23.9, 25.8):
    cols += [(px, 2.6), (px, 24.6)]
for py in (6, 9.4, 12.8, 16.2, 19.6):
    cols += [(15.2, py), (25.8, py)]
p.colonnade(cols)

# --- middle band: tablinum on the grand axis, alae, cubicula ---
p.room(15, 27.2, 26, 37)                 # TABLINVM
p.room(1.2, 27.2, 8, 33)                 # ALA (sin)
p.room(33, 27.2, 38.8, 33)               # ALA (dex)
p.room(1.2, 34, 8, 40)                   # CVBICVLVM
p.room(33, 34, 38.8, 40)                 # CVBICVLVM

# --- atrium band ---
p.room(9, 38.2, 32, 67)                  # ATRIVM
p.pool(16.5, 47, 24.5, 57)               # IMPLVVIVM
p.room(1.2, 41, 8, 52); p.room(1.2, 53, 8, 66)     # cubicula (sin)
p.room(33, 41, 38.8, 52); p.room(33, 53, 38.8, 66) # cubicula (dex)

# --- entrance band ---
p.room(17.3, 67.2, 22.7, 77.8, "mosaic") # FAVCES (entry corridor, mosaic)
p.room(1.2, 67.2, 15, 77.8)              # TABERNA (shop)
p.room(26, 67.2, 38.8, 77.8)             # TABERNA (shop)

# street
p.room(-1.2, 79, 41.2, 82.5, "stone")

# --- doorways (carve the grand axis + room access) ---
p.door(18.6, 77.6, 21.4, 79.2)           # street -> fauces
p.threshold(18.9, 78.0, 21.1, 78.9)
p.door(18.6, 66.9, 21.4, 67.5)           # fauces -> atrium
p.door(18.5, 36.7, 22.5, 38.5)           # atrium -> tablinum
p.door(18.5, 26.6, 22.5, 27.5)           # tablinum -> peristyle
# cubicula / rooms off atrium
for yy in (44, 56):
    p.door(7.7, yy, 9.3, yy + 3)
    p.door(31.7, yy, 33.3, yy + 3)
# peristyle rooms
p.door(6, 13, 9, 14.6); p.door(30, 13, 33, 14.6)   # culina / cubiculum
p.door(10.5, 6, 12.2, 9); p.door(28, 6, 29.7, 9)   # triclinium / oecus
# tabernae to street
p.door(6, 77.6, 9, 79.2); p.door(31, 77.6, 34, 79.2)

# grand axial sight-line (fauces -> impluvium -> tablinum -> garden)
p.axis(20, 3.5, 77.5)

# --- room labels ---
L = [
 (20, 73, "FAVCES", 8), (8, 73, "TABERNA", 7.5), (32.4, 73, "TABERNA", 7.5),
 (20.5, 44, "ATRIVM", 11), (20.5, 52.5, "IMPLVVIVM", 6.8, R.PARCH),
 (4.6, 47, "CVB.", 6.5), (4.6, 60, "CVB.", 6.5), (35.4, 47, "CVB.", 6.5), (35.4, 60, "CVB.", 6.5),
 (20.5, 32.5, "TABLINVM", 8.5), (4.6, 30.5, "ALA", 6.5), (35.4, 30.5, "ALA", 6.5),
 (4.6, 37.5, "CVB.", 6.5), (35.4, 37.5, "CVB.", 6.5),
 (20.5, 6.5, "PERISTYLIVM", 7), (20.5, 20.5, "HORTVS", 6.5, INK),
 (7, 7.5, "TRICLINIVM", 7), (7, 20.5, "CVLINA", 7.5),
 (33.4, 7.5, "OECVS", 7.5), (33.4, 20.5, "CVBICVLVM", 6.5),
]
for item in L:
    pp, qq, tx, sz = item[0], item[1], item[2], item[3]
    col = item[4] if len(item) > 4 else INK
    p.label(pp, qq, tx, sz, col)

# ---------- assemble page ----------
parts = [p.svg()]
parts.append(tabula_ansata(390, 92, 300, 46, "Domvs Romana", "forma \u00b7 a canonical atrium-peristyle house"))
parts.append(scalebar(55, H - 72, 40, 10))
parts.append(groma(812, 162, 20))

# legend / clavis
lx, ly = 690, 250
leg = [f'<g font-family="{SERIF}" font-size="7.5" fill="{INK}">']
leg.append(f'<rect x="{lx-10}" y="{ly-18}" width="190" height="150" fill="{R.PARCH}" '
           f'stroke="{GOLD}" stroke-width="1"/>')
leg.append(f'<text x="{lx+85}" y="{ly-4}" text-anchor="middle" font-size="9" fill="{GOLD}" '
           f'letter-spacing="1.5" style="text-transform:uppercase">Clavis</text>')
rows = [("paries", R.POCHE, "wall"), ("url(#water)", None, "aqua \u2014 pool"),
        ("url(#garden)", None, "hortus \u2014 garden"), ("url(#mosaic)", None, "opus \u2014 mosaic floor"),
        ("stone", R.STONE, "pavimentum \u2014 paving")]
yy = ly + 12
for fillid, solid, meaning in rows:
    f = solid if solid else f"url(#{fillid.split('#')[1]}" if fillid.startswith("url") else fillid
    f = solid if solid else fillid
    leg.append(f'<rect x="{lx}" y="{yy-8}" width="16" height="11" fill="{f}" stroke="{INK}" stroke-width="0.5"/>')
    leg.append(f'<text x="{lx+24}" y="{yy}" letter-spacing="0.6">{meaning}</text>')
    yy += 20
# column swatch
leg.append(f'<use href="#columna" x="{lx+8}" y="{yy-4}"/>')
leg.append(f'<text x="{lx+24}" y="{yy}">columna \u2014 column</text>')
leg.append('</g>')
parts.append("\n".join(leg))

# credit
parts.append(f'<text x="{W/2}" y="{H-26}" font-family="{SERIF}" font-size="7.5" fill="{INK}" '
             f'text-anchor="middle" letter-spacing="0.8" opacity="0.8">'
             f'Gens Togata \u00b7 diegetic visual language \u00b7 after the Tabula Peutingeriana'
             f'</text>')
parts.append(f'<text x="{W/2}" y="{H-16}" font-family="{SERIF}" font-size="6.5" fill="{INK}" '
             f'text-anchor="middle" opacity="0.6">route data: OmnesViae (CC-derived, MIT) \u00b7 original vector art</text>')

out = page(W, H, "\n".join(parts))
open(os.path.join(os.path.dirname(__file__), "..", "domus.svg"), "w").write(out)
print("wrote domus.svg")
