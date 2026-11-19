# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/muradpipit/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/muradpipit/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-page newspaper front page that sums up Thursday 19 November 2026 in a single image: "THE WORLD IN ONE DAY". Hero story is the widening U.S.–Iran exchange of fire across the Gulf (U.S. strike on Qeshm Island, Iranian strikes on U.S. bases in Kuwait and Bahrain, Strait of Hormuz shipping attacked, three U.S. carriers in the region), with panels for the GTA VI global rollout after a 13-year wait, the Trump–Xi–Putin trilateral talks at APEC in Shenzhen, Democrats nominating Hakeem Jeffries (poised to be the first Black Speaker of the House), NASA's Voyager 1 reaching one light-day from Earth, and the EU's proposed 45bn-euro Ukraine loan plus Cyclone Akvan nearing India's coast.

The image is drawn entirely in code: `draw.py` renders the 1024x1024 front page with a hand-built 5x7 bitmap font and a pure-stdlib PNG encoder — no downloaded photos, no external assets. `main.py` copies the image to `/output/entry.png` and verifies it (PNG magic, dimensions, 1 MiB cap, chunk CRCs, round-trip SHA256).

Local verification: `photo.jpg` is 1024x1024, 20,606 bytes (under the 1 MiB limit); two independent `draw.py` runs produce byte-identical output (SHA256 `809292f7928bb80d73983a3c749965eaa40635b98b860d5c532b8ec65bc5df0b`), and two `main.py` runs produce byte-identical `/output/entry.png` files.

## Run it

```sh
python3 main.py
```

To regenerate the image from scratch:

```sh
python3 draw.py photo.jpg
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=16hpme30&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
