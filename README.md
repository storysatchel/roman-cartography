# roman-cartography

A diegetic Roman **visual language** for maps, itineraries, and architectural
diagrams — built for the *Gens Togata* Genesys supplement.

See **[VISUAL-LANGUAGE.md](VISUAL-LANGUAGE.md)** for the full spec (palette,
conventions, provenance, roadmap).

## Quick start

```sh
python3 tools/draw_domus.py && rsvg-convert -w 1000 domus.svg -o domus.png   # floor plan
python3 tools/draw_via.py   && rsvg-convert -w 1180 via.svg   -o via.png     # TP itinerary
```

- `domus.svg` — a canonical atrium-peristyle *domus* floor plan.
- `via.svg` — a Tabula-Peutingeriana route strip from real OmnesViae data.
- `tools/romanplan.py` — the reusable toolkit that *is* the visual language.

## Credits

Route data from **[OmnesViae](https://omnesviae.org)** © René Voorburg (MIT) —
see [`NOTICE`](NOTICE). Aesthetic after the **Tabula Peutingeriana**. All vector
art is original.
