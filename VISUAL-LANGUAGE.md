# Gens Togata — Diegetic Roman Visual Language

A small, reusable system for drawing **maps, itineraries, and architectural
diagrams** that look like they belong *inside* the Roman world rather than in a
modern textbook — for use in the *Gens Togata* Genesys supplement and related
material.

Everything here is **original vector art**. No third-party drawing is copied or
traced. The *aesthetic* is derived from the **Tabula Peutingeriana** (the Roman
world's own schematic road map) and the palette is shared with the *Gens Togata*
rulebook so the diagrams drop in seamlessly.

---

## Provenance & licensing

| Source | Use here | Licence |
|---|---|---|
| **OmnesViae** (`data/omnesviae.json`, © René Voorburg) | Place names, modern names, coordinates, road segments & distances, vignette `symbol` codes | **MIT** — reused with attribution (see `NOTICE`) |
| **Tabula Peutingeriana** | Visual *vocabulary* only (ribbon roads, station chicanes, pictographic vignettes, parchment palette) | Ancient original; a style/idea, not copyrightable |
| Floor-plan *subjects* (Roman building types) | Architectural **facts** redrawn from scratch | Facts aren't copyrightable; art is original |

The OmnesViae dataset is JSON-LD: **3,323 `Place`** nodes (`label` = Peutinger
Latin name, `modern`, `lat`, `lng`, `symbol`) and **3,523 `TravelAction`**
edges (`from`, `to`, `dist` in *leugae*).

---

## Palette (shared with the rulebook)

| Token | Hex | Role |
|---|---|---|
| `INK` | `#2a1d0c` | walls, labels (dark sepia) |
| `PARCH` | `#efe3c6` | parchment ground |
| `PARCH2` | `#e6d6ac` | faint room tint / pattern base |
| `POCHE` | `#3a2a14` | filled wall thickness |
| `STONE` | `#cdb98a` | paving, steps, thresholds |
| `WATER` | `#6f8d7e` | impluvium, piscina (TP green-water) |
| `GARDEN` | `#8a9a62` | hortus greenery |
| `ACCENT` | `#6e1b1b` | maroon frames, roads, cartouches |
| `GOLD` | `#8a5a12` | keys, scale, modern place-names |

Type: a serif (`Gentium Book Basic` / Times / DejaVu Serif), **letter-spaced,
uppercased**, with classical orthography (**V for U, no J**): `ATRIVM`,
`CVBICVLVM`, `FAVCES`.

---

## Conventions — architectural diagrams (floor plans)

- **Walls = poché.** Draw the whole footprint solid (`POCHE`), then *carve*
  rooms as parchment rectangles. Walls are simply the material left between
  rooms — thickness is the gap you leave.
- **Doorways** are parchment bridges carved across a wall; a paved threshold
  (`STONE`) may sit in the opening.
- **Floors** carry meaning by fill pattern: `water` (pool), `garden` (planting),
  `mosaic` (fine *opus* grid), `hypocaust` (pilae grid), `stone` (paving).
- **Columns** are ringed dots (`#columna`), placed as colonnades.
- **The grand axis** (fauces → impluvium → tablinum → peristyle) is marked with
  a faint dashed `ACCENT` sight-line — the signature of the Roman house.
- Furniture of the plate: **tabula ansata** title, **pedes** scale bar,
  **groma** orientation cross (`SEPTENTRIO` north), a **clavis** (legend), and a
  credit line. Double `ACCENT` border frames the sheet.

## Conventions — maps & itineraries

- Roads are **red ribbons**, schematic (not geographic), with a **chicane kink**
  at each station.
- Settlements get **pictographic vignettes** (twin-tower town; larger walled
  vignette for a *great city* at the ends). The OmnesViae `symbol` code is the
  hook for a fuller vignette taxonomy (spa, temple, port — *to build*).
- Latin name **above**, modern name **below** (italic gold), **distance** on each
  leg (in *leugae*). "schematic, not to geographic scale" is stated on the plate.

---

## Toolkit

- `tools/romanplan.py` — the language as code: palette, `defs()` (patterns +
  column symbol), a `Plan` class (`footprint`, `room`, `pool`, `door`,
  `column`/`colonnade`, `label`, `axis`), and page furniture (`tabula_ansata`,
  `scalebar`, `groma`, `page`).
- `tools/draw_domus.py` → `domus.svg` — a canonical atrium-peristyle house.
- `tools/draw_via.py` → `via.svg` — a Tabula-Peutingeriana itinerary built from
  real OmnesViae data (shortest road path, summed leg distances).

Render: `python3 tools/draw_domus.py && rsvg-convert -w 1000 domus.svg -o domus.png`

---

## Roadmap

1. Full **vignette taxonomy** keyed to OmnesViae `symbol` codes (spa / temple /
   port / great city), replacing the single twin-tower.
2. A **regional map** mode (places by lat/lng with a schematic coast & relief),
   not just linear strips.
3. More building types: *insula*, *thermae* (with hypocaust), *castrum*,
   *basilica*, *temple*.
4. Integrate as figures in the *Gens Togata* rulebook (gazetteer & scenarios).
