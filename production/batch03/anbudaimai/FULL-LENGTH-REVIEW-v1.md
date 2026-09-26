# Anbudaimai full-length review candidate — 2026-09-20

**Actual output:** `ANBU-FULL-LENGTH-REVIEW-v1.mp4`,74,285,221 bytes. **5155 picture frames at24fps =214.7916666667sec**,1280x720H.264. This is a full-duration review candidate, NOT release-approved or published. V15 and all original/generated sources preserved. No new end-title wording or freeze introduced; final living scene continues to last selected frame. Review labels explicitly require human audiovisual approval.

## Exact frame ledger

All frame ranges are zero-based, end-exclusive. Source selections are unique, once each; no loops, slowed footage, repeated prefixes or duration-padding. Earlier twelve-frame AN13→AN14 dissolve is retained and accounted for.

| Shot | Source seconds | Film frames [in,out) |
|---|---|---|
|AN01|3.75–9.50|0–138|
|AN02|0.50–9.00|138–342|
|AN03|0.75–8.75|342–534|
|AN07|0.75–8.50|534–720|
|AN04|0.75–8.25|720–900|
|AN05|1.00–8.50|900–1080|
|AN06|0.75–8.25|1080–1260|
|AN09|0.50–8.50|1260–1452|
|AN10|0.50–8.00|1452–1632|
|AN11|1.00–5.50|1632–1740|
|AN12|3.50–8.50|1740–1860|
|AN13|0.50–7.50|1860–2028|
|AN14|0.50–7.50|2016–2184|
|AN16|1.00–5.50|2184–2292|
|AN17|0.50–9.00|2292–2496|
|AN18|0.50–7.50|2496–2664|
|AN19|1.50–7.00|2664–2796|
|AN20|0.50–7.50|2796–2964|
|AN21|0.25–3.75|2964–3048|
|AN22|0.50–8.50|3048–3240|
|AN24|1.00–7.00|3240–3384|
|AN25|0.50–7.50|3384–3552|
|AN26|0.50–8.00|3552–3732|
|AN27|1.00–7.50|3732–3888|
|AN28|3.00–7.50|3888–3996|
|AN29|1.00–6.50|3996–4128|
|AN30|0.25–8.75|4128–4332|
|AN31|0.00–7.00|4332–4500|
|AN32|0.25–9.25|4500–4716|
|AN33|0.25–9.25|4716–4932|
|AN34|0.25–229/24 (=9.541666667)|4932–5155|

26 earlier shots =4140 source frames minus12 dissolve frames =4128 film frames. Five closing shots =204+168+216+216+223=1027frames. Total unique selected source5167frames; occupied picture5155frames. AN08/15/23 failed and absent. AN07 alone retains disclosed16:9 crop1152x648 at128,72 scaled1280x720; provenance retained. Other frames uncropped.

## Complete original audio, unchanged

Entire `source/youtube/lneosghJWgs.m4a` AAC stream copied with `-c:a copy`, no trimming, re-encoding, fading, generated sound or gain changes. Source MP4 declared duration9471859/44100=214.78138321995sec. Identical source/output compressed-audio payload SHA256:

`7a55b37ef6380f8b6f0348db6cc830d9b3f729d5c82062da801111c15995f758`

AAC priming/padding and remux timing must not be confused with added footage: both source and output decode to final PTS9471424 plus1024samples at44100Hz, end214.794739229sec. Output raw audio media duration214.831020408sec includes priming; presentation container duration214.795sec. Picture214.791666667sec is0.00307256sec shorter than decoded AAC endpoint, less than one24fps frame. Full audio payload is intact; no song truncation to rounded214.78.

## Technical and visual checks actually performed

- Successful full audio/video decode,5155frames, no errors.
- Full-film FFmpeg blackdetect at98% black pixels/pixel threshold0.10/minimum0.02sec: no black intervals reported. This does not certify every aesthetic exposure choice.
- Closing cut pairs4127/4128,4331/4332,4499/4500,4715/4716,4931/4932 and lastframe5154 inspected in ANBU-full-review-closing-boundaries.png. Expected garden→seated return→care→outdoor-attention sequence, intact boundaries/end. Sheet's twelfth empty layout cell is not film black.
- Original/output compressed AAC hashes identical. Read-only timing script independently reports5155video samples/214.791666667sec. Source fragmented MP4 has empty stsz table; its zero stsz count is NOT zero audio packets.

Earlier per-version edit/QC notes remain applicable. Closure deliberately restages the known AN09 family already seated, adding host chair/repositioning side table after elapsed time; no invented sitting action or seamless geography claim. AN31 selection excludes later simultaneous re-reach. AN32 actual towel lift/tilt/placement differs from requested supported slide; sampled grip is conditional, not full-speed certification. Final calm motion is actual generated footage, not still extension.

## Mandatory human release review — unresolved

Watch/listen to the entire candidate at normal speed: musical/lyric fit, emotional pacing, same-axis cuts and elapsed-time staging, cloth/towel/basket grips, facial identity, rain contact/occlusion, artificial-looking water, ending cadence. Labels remain because these are not established by numerical checks or contact sheets. No claim of listening/perceived synchronized performance. Fix any flagged timecodes before clean release export/publication. No authorization inferred from full duration or technical checks.

Build: `build-opening-review-v2.ps1 -FullReview`. `inspect_mp4_timing.py` is read-only verification. Initial full-review attempt failed CFR negotiation before writing packets; explicit24fps after trim fixed it, successful candidate verified above.
