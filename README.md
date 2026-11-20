# World News — Friday 20 November 2026

A newspaper front page of the day's world news, in one 1024×1024 image.
Entry for the make.fun competition `news-image-20261120`.

## Stories (all first reported on 20 November 2026)

- **Lead — Trump puts Iran war decision off until 2027.** The president says
  there is "no rush" and he will "see what happens" after 1 January.
  (Reuters / The Times of India, 20 Nov 2026)
- **Europe "ready for talks" with Russia to end the Ukraine war.**
  (BBC, 20 Nov 2026)
- **300,000 evacuated as Cyclone Akvan strikes India's east coast.**
  Landfall in Odisha, 423 rescue teams deployed. (The Hindu, 20 Nov 2026)
- **Engine fault ends Japan's Hayabusa2 asteroid landing.** (Space.com, 20 Nov 2026)
- **Gen Z walkouts sweep Europe** — International Youth Strike: 200+ British
  schools, 34 German cities, a general strike in Italy. (ZeroFox, 20 Nov 2026)
- **GTA 6 sales already pass $1.8bn**, overtaking The Odyssey's global run.
  (Mezha, 20 Nov 2026)
- **Sport brief — Phillips' 118 makes history in Wellington.** First player to
  score centuries against India in Tests, ODIs and T20s in one calendar year;
  New Zealand pass 300 on day two, Henry Nicholls 146 not out.
  (ICC / Cricbuzz, day two, 20 Nov 2026)

## How it works

`poster.html` is the front page (fresh design: navy masthead band, full-width
lead, three-column grid, tinted lower band). It is rendered once at build time
into `entry.png` (1024×1024 PNG, under 1 MiB). `main.ts` (Node 22, standard
library only, no network) validates the image — PNG magic, at most
1024×1024, whole file with an IEND chunk, at most 1 MiB — and copies it
byte for byte to `/output/entry.png`, so two runs write identical bytes.

Run it outside the grader with:

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
