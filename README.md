# News Image — 18 November 2026

One image that sums up the world's news of Wednesday 18 November 2026,
entered in the make.fun competition `news-image-20261118`.

The front page covers six stories from that day: the United States striking
an Iranian missile site on Qeshm Island and Iran's drone attacks on Bahrain
and Kuwait; Ukraine's strike partly collapsing the Kerch bridge to Crimea;
Xi Jinping hosting Vladimir Putin in Shenzhen ahead of the first
Trump-Xi-Putin trilateral summit; Mary Peltola winning Alaska's Senate seat
as Democrats reach 56 seats; the Ebola outbreak in DR Congo passing 11,000
cases; and Category 5 Cyclone Xavier striking the Northern Cook Islands.

## How it works

`entry.png` is the front page itself (1024x1024 PNG, drawn with PIL from
the verified wire reports of the day). `main.py` is the entry program: using
only the Python standard library, it reads `entry.png` next to it, checks
that the file is a whole PNG or JPEG within the size and dimension limits,
and writes the bytes unchanged to `entry.png` in the output directory
(`MAKEFUN_OUTPUT_DIR`, or `/output` when unset).

Run it locally with:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The program runs with no network and writes the same bytes on every run.
