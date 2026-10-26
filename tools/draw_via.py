"""draw_via.py — a Tabula-Peutingeriana-style route ribbon rendered from real
OmnesViae data (data/omnesviae.json, MIT, (c) Rene Voorburg). Original vector art.

Finds a shortest road path between two places and draws it as a schematic
diegetic strip: red road, station chicanes, twin-tower vignettes, Latin labels,
distances. Outputs via.svg.
"""
import sys, os, json, heapq, unicodedata
sys.path.insert(0, os.path.dirname(__file__))
import romanplan as R
from romanplan import INK, PARCH, PARCH2, ACCENT, GOLD, WATER, SERIF, POCHE, STONE

HERE = os.path.dirname(__file__)
G = json.load(open(os.path.join(HERE, "..", "data", "omnesviae.json")))["@graph"]

places, adj = {}, {}
for n in G:
    t = n.get("@type")
    if t == "Place":
        places[n["@id"]] = n
    elif t == "TravelAction":
        a = n["from"][0]["@id"]; b = n["to"][0]["@id"]; d = n.get("dist", 1) or 1
        adj.setdefault(a, []).append((b, d)); adj.setdefault(b, []).append((a, d))

def norm(s): return "".join(c for c in unicodedata.normalize("NFKD", (s or "").lower())
                             if not unicodedata.combining(c))

def find(q):
    q = norm(q)
    best = None
    for pid, pl in places.items():
        if q == norm(pl.get("modern")) or q == norm(pl.get("label")):
            return pid
        if (best is None) and (q in norm(pl.get("modern")) or q in norm(pl.get("label"))):
            best = pid
    return best

def dijkstra(s, t):
    pq = [(0, s, [s])]; seen = set()
    while pq:
        c, u, path = heapq.heappop(pq)
        if u == t: return path, c
        if u in seen: continue
        seen.add(u)
        for v, d in adj.get(u, []):
            if v not in seen: heapq.heappush(pq, (c + d, v, path + [v]))
    return None, None

START, END = find("Roma"), find("Brundisium")
path, total = dijkstra(START, END)
if not path:
    END = find("Capua"); path, total = dijkstra(START, END)

# full-path per-segment distances, then collapse to a legible number of stops
fullseg = [next((dd for v, dd in adj.get(path[i-1], []) if v == path[i]), 0) for i in range(1, len(path))]
if len(path) > 9:
    keep = sorted(set(round(i * (len(path) - 1) / 8) for i in range(9)))
else:
    keep = list(range(len(path)))
stops = [places[path[k]] for k in keep]
seg_dists = [sum(fullseg[keep[j-1]:keep[j]]) for j in range(1, len(keep))]
print("ROUTE:", " -> ".join(s.get("label", "?") for s in stops), "| total leugae:", total)

# ---- draw the ribbon ----
W, H = 1180, 300
n = len(stops)
mL, mR = 90, 90
span = W - mL - mR
xs = [mL + span * i / (n - 1) for i in range(n)]
ROADY = H / 2 + 18

def twin_tower(x, y, big=False):
    s = 1.5 if big else 1.0
    w, h = 18 * s, 22 * s
    g = [f'<g transform="translate({x:.1f},{y:.1f})">']
    # body
    g.append(f'<rect x="{-w/2:.1f}" y="{-h:.1f}" width="{w:.1f}" height="{h:.1f}" '
             f'fill="{PARCH2}" stroke="{INK}" stroke-width="1.3"/>')
    # two merlon towers
    tw = w * 0.34
    for sx in (-1, 1):
        tx = sx * (w/2 - tw/2)
        g.append(f'<rect x="{tx-tw/2:.1f}" y="{-h-tw*0.9:.1f}" width="{tw:.1f}" '
                 f'height="{tw*1.1:.1f}" fill="{PARCH2}" stroke="{INK}" stroke-width="1.3"/>')
    g.append(f'<line x1="{-w/2:.1f}" y1="{-h*0.5:.1f}" x2="{w/2:.1f}" y2="{-h*0.5:.1f}" '
             f'stroke="{INK}" stroke-width="0.8"/>')
    g.append('</g>')
    return "\n".join(g)

parts = []
parts.append(f'<rect width="{W}" height="{H}" fill="{PARCH}"/>')
parts.append(f'<rect x="10" y="10" width="{W-20}" height="{H-20}" fill="none" stroke="{ACCENT}" stroke-width="2"/>')
parts.append(f'<rect x="15" y="15" width="{W-30}" height="{H-30}" fill="none" stroke="{ACCENT}" stroke-width="0.6"/>')
# title
parts.append(f'<text x="{W/2}" y="46" font-family="{SERIF}" font-size="16" fill="{ACCENT}" '
             f'text-anchor="middle" letter-spacing="2.5" style="text-transform:uppercase">Itinerarivm</text>')
parts.append(f'<text x="{W/2}" y="62" font-family="{SERIF}" font-size="8.5" fill="{INK}" '
             f'text-anchor="middle" font-style="italic" letter-spacing="1">'
             f'{R.html_safe if hasattr(R,"html_safe") else ""}{stops[0].get("modern")} ad {stops[-1].get("modern")} '
             f'\u00b7 {total} leugae</text>')

# the red road with station chicanes
d = [f'M {xs[0]:.1f} {ROADY:.1f}']
for i in range(1, n):
    midx = (xs[i-1] + xs[i]) / 2
    d.append(f'L {midx-7:.1f} {ROADY:.1f} L {midx:.1f} {ROADY-9:.1f} L {midx+7:.1f} {ROADY:.1f} L {xs[i]:.1f} {ROADY:.1f}')
parts.append(f'<path d="{" ".join(d)}" fill="none" stroke="{ACCENT}" stroke-width="2.6" stroke-linejoin="round"/>')

# distance numbers on each segment
for i in range(1, n):
    dist = seg_dists[i-1]
    mx = (xs[i-1] + xs[i]) / 2
    parts.append(f'<text x="{mx:.1f}" y="{ROADY+17:.1f}" font-family="{SERIF}" font-size="8.5" '
                 f'fill="{INK}" text-anchor="middle" font-weight="bold">{dist}</text>')

# vignettes + labels
for i, (x, st) in enumerate(zip(xs, stops)):
    big = i in (0, n - 1)
    parts.append(twin_tower(x, ROADY, big))
    lab = st.get("label", "")
    parts.append(f'<text x="{x:.1f}" y="{ROADY-(36 if big else 30):.1f}" font-family="{SERIF}" '
                 f'font-size="{9 if big else 8}" fill="{INK}" text-anchor="middle" '
                 f'letter-spacing="0.8">{lab}</text>')
    mod = " ".join((st.get("modern") or "").replace("~", " ").split())
    if mod:
        parts.append(f'<text x="{x:.1f}" y="{ROADY+34:.1f}" font-family="{SERIF}" font-size="7" '
                     f'fill="{GOLD}" text-anchor="middle" font-style="italic">{mod}</text>')

# scale note / legend
parts.append(f'<text x="{W/2}" y="{H-24}" font-family="{SERIF}" font-size="7.5" fill="{INK}" '
             f'text-anchor="middle" letter-spacing="0.8" opacity="0.85">'
             f'distances in leugae (Gallic leagues) \u00b7 schematic, not to geographic scale \u2014 after the Tabula Peutingeriana</text>')
parts.append(f'<text x="{W/2}" y="{H-13}" font-family="{SERIF}" font-size="6.5" fill="{INK}" '
             f'text-anchor="middle" opacity="0.6">data: OmnesViae \u00a9 Ren\u00e9 Voorburg (MIT) \u00b7 Gens Togata diegetic visual language</text>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
       f'{R.defs()}\n' + "\n".join(parts) + "\n</svg>")
open(os.path.join(HERE, "..", "via.svg"), "w").write(svg)
print("wrote via.svg")
