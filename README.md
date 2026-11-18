# The World in One Page — 18 November 2026 (v2)

A one-page newspaper front page summarising the eight stories that
defined Wednesday 18 November 2026, drawn entirely with Pillow.

## The eight stories

1. **Gulf strikes (lead)** — U.S. jets hit a Revolutionary Guard
   missile launch site on Qeshm Island; Iran fires drones at Bahrain
   and Kuwait.
2. **Kerch Bridge** — Ukrainian drones and missiles partly collapse
   the bridge to Crimea; one arch falls into the strait.
3. **Shenzhen summit** — Xi hosts Putin ahead of Thursday's first
   Trump–Xi–Putin trilateral.
4. **Alaska** — Democrat Mary Peltola wins the Senate seat; Democrats
   reach a 56-seat majority.
5. **Ebola in DR Congo** — the outbreak passes 11,000 cases and
   5,400 deaths.
6. **Cyclone Xavier** — a Category 5 storm slams the Northern Cook
   Islands.
7. **Also today** — the U.S. loses measles-free status after 26 years
   (5,400+ cases).
8. **Also today** — a Russian military plane crashes in Siberia,
   19 dead.

## Layout (v2 vs v1)

v1 carried six stories in three rows with a small lead illustration.
v2 adds two more verified stories in an "ALSO TODAY" strip, enlarges
the lead explosion illustration (layered burst, smoke rings, four
drones over Qeshm Island), redraws the Kerch Bridge as a proper side
view (intact arch, broken deck segment falling into the strait with a
splash), and redraws the Shenzhen skyline with the red sun disc
behind the towers and the Chinese, Russian and U.S. flags. Type is
larger throughout and the bottom-row icons sit beside the section
kickers instead of crowding the text.

## How it is built

`draw_frontpage.py` (build-time only, not part of the entry) draws
`entry.png` (1024x1024, ~131 KB) with Pillow: paper `#f7f3ea`,
ink `#111111`, red `#b91c1c`, navy `#1e3a5f`. It is deterministic —
two runs produce byte-identical output. The entry program `main.py`
(standard library only) validates the image (PNG, at most 1 MiB, at
most 1024x1024) and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`
(or `/output/entry.png`).

## Run

```sh
python3 draw_frontpage.py   # regenerates entry.png (build time)
python3 main.py             # writes entry.png to the output dir
```
