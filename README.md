# The World in One Page — 27 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-bounty-7c3aed)](https://make.fun/competitions/news-image-20261127)
[![Prize $100](https://img.shields.io/badge/prize-%24100-brightgreen)](https://make.fun/competitions/news-image-20261127)
[![Status: Open](https://img.shields.io/badge/status-open-blue)](https://make.fun/competitions/news-image-20261127)

One image that sums up the world's news on **Friday, 27 November 2026** — a
dense one-page newspaper front page, drawn entirely in code.

## How it works

`main.py` (Python 3 + Pillow, no network, no randomness) draws the whole
front page — masthead, headlines, charts and illustrations — and writes a
deterministic 1024×1024 PNG to `/output/entry.png`.

```sh
python3 main.py   # writes /output/entry.png
```

Two runs produce byte-identical output (verified by sha256).

## Stories in the image

| # | Story |
|---|-------|
| 1 | **Lead — Trump: "victory at hand" in Iran war; Putin "wants a deal" on Ukraine.** Trump tells troops victory over Iran is near, offers Tehran a deal after meeting NATO chief Rutte at Mar-a-Lago; Zelensky warns the US not to drift from Ukraine. Hormuz tanker traffic rises despite attacks; Iran rations power. |
| 2 | **Thanksgiving storm batters the US East Coast.** 724,000+ without power, 70 mph gusts; the 100th Macy's Thanksgiving Day Parade postponed for the first time ever; 1,000+ flights hit. |
| 3 | **SpaceX cleared for 1 million satellites.** FCC approves orbital AI data centres in space; Musk pledges 2 SpaceX shares to every US child — an $18bn giveaway. |
| 4 | **Markets: GDP revised up to 4.3%; gold tops $3,600.** US Q3 growth revised from 3.4%; Nasdaq futures +2.5%; Brent ~$96; Tokyo core inflation hits a 16-month high at 2.9%. |
| 5 | **New US tariffs: up to 40% on China.** Duties proposed on 14 partners — 40% China, 35% Vietnam, 10% on Brazilian aircraft; Beijing and Brasilia vow retaliation. |
| 6 | **Houthi strike hits Saudi Aramco refinery.** Attack on the Jazan refinery kills a worker and halts some operations; two Italian technicians die in a drone strike on a Kuwaiti facility. |
| 7 | **Sport: Skubal's $450M Mets deal sets a record.** 9-year, $450m — the richest pitcher contract ever; LeBron James posts his first triple-double for the 76ers. |
| 8 | **World in brief.** NZ coalition one seat short of a majority; UK net migration near a 30-year low; Cloudflare outage before Black Friday; FIFA cyberattack; Anita DeFrantz dies at 74; Kim Jong Un vows to expand the nuclear arsenal. |

Sources: Reuters, AP, BBC, AFP, NYT (27 November 2026).

## License

MIT — see [LICENSE](LICENSE).
