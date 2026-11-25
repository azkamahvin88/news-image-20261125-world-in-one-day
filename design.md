# Design notes — news-image-20261125

One-page newspaper front page, 1024×1024, cream paper, black serif
headlines, maroon + navy accents, flat original vector illustrations
(no photos). Template follows the winning pattern of news-image-20261120
(top-10 study): kicker → giant date masthead → sub-headline → 6-number
stat strip → colour-coded region bar → 3 lead stories → 10 small stories
→ world map with numbered pins → "ALSO ON…" list → DATE CHECK box → footer.

## Stories (36 total, 7 regions)

Regions: Europe 10, Asia 5, Middle East 7, Africa 4, Americas 5,
Oceania 2, Global 3.

### Featured (13) — numbered, pinned on the map
1. Kyiv's sea drones sink Russian warship off Libya (Reuters)
2. Houthis hit Riyadh's tallest tower; 11 wounded (Reuters)
3. Huawei convicted on 10 of 12 US criminal counts (Reuters)
4. NATO sends early-warning jets to Poland (Reuters)
5. Putin vows retaliation over refinery strikes (Kremlin / X)
6. 700,000+ Russian soldiers killed, leak finds (RFE/RL)
7. Russian strike on Kyiv-region flats kills 11 (RFE/RL)
8. Zelenskyy: US "aligning with Russia" (Bloomberg)
9. Trump pardons turkeys Freedom and Feathers (AP)
10. Fort Hood gunman seeks stay of execution (Reuters)
11. Sarkozy and Bruni ordered to stand trial (Reuters)
12. Indonesia's vice-president resigns (Wire reports)
13. Senegal get AFCON title back after CAS ruling (AFP)

### Also on Wednesday 25 November (23)
14. Iran winter gas shortages (DW) · 15. Iraq seizes Kurdish oilfields
(Reuters) · 16. Israeli strike kills Hamas security chief in Gaza (BBC) ·
17. Israel: Iran building chemical weapons, plotted to kill Trump
(Israel says) · 18. Iran: three oil tankers hit by mines in Hormuz strait
(IRGC claim) · 19. EU 22nd sanctions package (EU) · 20. Denmark upholds
"ghetto" evictions (Reuters) · 21. Cameroon separatist leader war-crimes
trial in Norway (Reuters) · 22. RFE/RL shortwave for Afghan girls
(RFE/RL) · 23. Xiamen Airlines orders 50 Boeing 737-8 (Reuters) ·
24. Nvidia gives back $240bn (Motley Fool) · 25. Bitcoin slips towards
$60,000 (Share-Talk) · 26. England beat Australia by 8 wickets, 2nd T20I
(AP) · 27. Australia ASX +1.82%; layoffs post-Covid high (FNN) ·
28. Colombia car bomb wounds 23; 25 held hostage (Reuters) · 29. FBI crime
database suspected breach (Reuters) · 30. O'Hare radar delays (Reuters) ·
31. US envoy "not certain" Israel military aid ends this year (Reuters) ·
32. NATO vows to defend vs space threats (Reuters) · 33. Asteroid eclipse
imaged; Vera Rubin's first pictures (NASA) · 34. Landmine victims
five-year high (Landmine Monitor) · 35. Nigerian emir suspended
(Reuters) · 36. DR Congo rebels pull back (Reuters)

## DATE CHECK (left out on purpose)
- Champions League results of Tue 24 Nov (Real Madrid 5-1 PSV; Man City
  2-2 Napoli) — Tuesday's news.
- Huawei verdict handed down late Tuesday in New York (reported widely Wed).
- Wed night ties (Liverpool at Club Brugge; PSG v Roma) still to be played
  at press time; results not yet known.
- Nvidia's 31.5% surge was Monday 23 Nov (fell 5.9% Tuesday).

## Build
`draw.py` (Pillow, Liberation fonts) draws entry.png deterministically;
`main.py` copies it to the output dir. Two runs of draw.py produce
identical md5. entry.png: 1024×1024, ~195 KB, under the 1 MiB cap.
