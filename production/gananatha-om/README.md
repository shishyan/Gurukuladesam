# Gana Natha Om image-motion review

This is a full-length, **unpublished review cut** for the original song
"கண நாதா ஓம் (Original)" (`GydxHEmyDPc`). The source audio is 3:47.96.
The 1280 x 720 picture runs 3:48.00 at 24 fps (5,472 frames), with 30
framings made from 15 accepted ImageGen artworks. The source AAC stream is
copied into the MP4 without re-encoding.

`review-manifest.json` lists every image, shot role, and exact frame boundary.
The editor chooses nearby low-RMS points within about one second of evenly
spaced cuts. These points have **not** been approved against the Tamil lyrics
or musical phrases. The camera moves are slow crops of stills; only the tank
shots have composited surface ripples, and a few outdoor shots have subtle
light motes. The flame, bell, incense, foliage, and deity do not have
independent source motion.

Run from the repository root with Python, Pillow, NumPy, and imageio-ffmpeg:

```powershell
python production/gananatha-om/render_review.py
```

Output: `GANA-NATHA-OM-FULL-IMAGE-MOTION-REVIEW-v1.mp4`.
`review-contact-sheet.jpg` shows ten checkpoints across the film.

Technical QC on 2026-09-26: full video/audio decode exit 0; exactly 5,472
frames; no black interval detected at the 0.02-second threshold; AAC payload
byte-identical to `source/youtube/GydxHEmyDPc.m4a` after ADTS remux. The
40 ms picture extension is whole-frame rounding. The contact sheet was
visually inspected. Full-speed human audiovisual review, lyric timing,
iconography approval, and release approval are still needed.

`GN07-banyan-garden-raw.png`, `GN10-idol-close-HOLD.png`, and
`GN16-final-sanctum-HOLD.png` are excluded ImageGen outputs. The first had
black image bands. The second showed a long second tusk and an axe instead
of the requested single broken tusk and goad; its corrected variant is used.
The final sanctum variant retained the tusk/tool inconsistency, so the film
returns to `GN01-sanctum-master.png` instead. `GN01` was also corrected to
remove an erroneous bull-like foreground sculpture. See `ARTWORK-PROMPTS.md`
for scene briefs and visual constraints.
