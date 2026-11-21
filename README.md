# World News — Friday 20 November 2026

A newspaper front page of the day's world news, in one 1024×1024 image.
Entry for the make.fun competition `news-image-20261120`.

## Round 3 (prep only, 21 Nov 2026 — NOT submitted)

Rebuilt around the day's sharpest event instead of adding more stories:
**lead — Russian missiles land on NATO soil in Poland.** Two Kh-101
cruise missiles and a drone crashed in south-east Poland (Nowy Lipowiec,
Rudnik nad Sanem, Mołodycz) during Moscow's biggest strike of the month
on Ukraine (400+ drones, 110 missiles; 8 killed); PM Tusk called it an
"intentional provocation", NATO jets scrambled, Patriots on alert.
The lead is a situation map of the impact zone plus a "The Strike"
numbers rail (3 / 400+ / 8 / 0). Supporting: Wall Street AI rout with a
plunging Nasdaq chart ($4tn wiped out in a week; Nasdaq −5.3%, S&P −3.7%,
Nvidia −14% as the SEC opens a probe), Senate 51–48 backs Trump on the
Iran war, Cyclone Akvan (300,000+ evacuated). Briefs: Peru 6.7 quake,
COP31 draft drops fossil fuels, GTA 6 $3.8bn day one, Phillips makes
history. All figures re-verified against wire/press reports of 20 Nov
2026 (ISW, Reuters, WSJ, Investopedia, Hindu BusinessLine, AFP).

`poster.py` draws the page with PIL (deterministic); `main.ts` copies
`entry.png` byte for byte. Verified: two `main.ts` runs + two
`poster.py` renders all give sha256
`2c93eaa88a348c0b82f457cac6d5347624175527ecb440fe7de2c5ac3f250ec6`
(1024×1024, 146,744 bytes).

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
