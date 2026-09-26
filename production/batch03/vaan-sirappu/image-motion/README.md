# Vaan Sirappu image-motion study

This folder contains an 18-second technique study and a **full-length,
unpublished review cut**. The latter preserves the existing 161.25 seconds of
selected moving footage and adds 151.291667 seconds of image-derived scenes
from 20 distinct stills. It is complete in duration, not approved for release.

## Assets and technique

- `VS40-monsoon-valley.png`: rain/irrigation establishing shot. Prompt: wide
  Tamil Nadu paddy valley at dawn, distant monsoon curtain, irrigation channel,
  restrained 35 mm devotional film look, no text.
- `VS41-rain-fed-paddy.png`: empty close paddy and flowing bund. Prompt: low
  angle rice seedlings rooted in rain-rippled water, deep landscape layers, no
  people or text.
- `VS42-temple-tank.png`: dry South Indian temple veranda looking onto rain
  and a temple tank. Prompt: sheltered brass lamp, wet exterior, physically
  coherent monsoon, no people or text.
- `render_study.py`: controlled slow dolly/truck per shot, location-limited
  animated rain streaks, time-varying non-grid water impacts, hard cuts every
  six seconds, original song audio only. Deterministic render.
- `VAAN-image-motion-study-18s.mp4`: 1280×720 H.264/AAC, 24 fps, 432 frames.

`ARTWORK-PROMPTS.md` records the subject and physical constraints for every
generated frame, including the two held images.

Run with Python, Pillow, and `imageio-ffmpeg` from the repository root:

```powershell
python production/batch03/vaan-sirappu/image-motion/render_study.py
```

Full video and audio decode passed on 2026-09-26. The three midpoint frames
are in `study-contact.jpg`. The effect is strongest on rain and water. The
farmers in VS40 are embedded in the original still and do not move, so that
shot must remain short or be replaced before film integration. The temple
lamp is also a still element. Human motion, iconography, music phrasing, and
full-speed playback need review before expanding this into the remaining
151 seconds. Repeating these three frames to fill the song would not meet the
existing film standard.

## Full-length review

`render_full_review.py` renders the distinct scene tail and joins it to the
prior v15. It chooses cut points near quiet samples in the soundtrack, within
approximately one second of a uniform seven-to-eight-second shot grid. Those
measurements do **not** establish lyric or phrase timing. The 20-shot order is
listed with exact frame boundaries in `full-review-manifest.json`.

Run from the repository root:

```powershell
python production/batch03/vaan-sirappu/image-motion/render_full_review.py
```

Output: `VAAN-FULL-LENGTH-IMAGE-MOTION-REVIEW-v1.mp4`, 1280×720, 24 fps,
7,501 frames, 5:12.54 picture. `VAAN-image-motion-tail-151s.mp4` is a generated
silent intermediate and is not committed. `full-review-contact.jpg` shows ten checkpoints including both
sides of the cut at 161.25 seconds.

Technical QC on 2026-09-26: full video/audio decode exit 0, exactly 7,501
frames, no detected black interval at 0.02-second threshold, and extracted
AAC payload SHA-256 identical to the original `tX4JtRSOuxE.m4a` (both
`87d5f7d614311eefb27c4e528e89ae05182eda4d13f3d87913229be491dce750`
when remuxed as ADTS). The final picture extends approximately 0.02 second
beyond the source audio because of whole-frame rounding.

Review limits: no full-speed human audiovisual approval, lyric cut approval,
or publication. Camera motion, rain and water impacts are composited from
still artwork; the water and foliage pictured within those stills do not have
true source motion. VS40 has small static farmers. The prior v15 footage has
an upper-left provisional review overlay; the new tail has a matching review
label added at assembly. Two
generated temple frames, `VS53-temple-passage-HOLD.png` and
`VS56-gratitude-offering.png`, were excluded for wet-looking sheltered stone.
Avoid treating this as 312 seconds of accepted moving footage. Review the
entire cut at normal speed with sound before deciding whether still-derived
shots meet the film's standard or need replacement.

## Channel and production improvements

The channel's Videos tab showed 38 uploads on 2026-09-26, including cinematic
versions of Anbudaimai, Thiruppavai 2, Mahaganesa Pancharatnam, and other
songs. Its public Playlists tab showed devotional and Discography collections,
but no dedicated playlist for the cinematic films. A public film playlist
would give viewers a clear route through those works and separate them from
the audio-release versions. Select the canonical film for each song to avoid
clustering duplicate audio and film uploads.

For production, keep a single ledger per song with source audio ID/duration,
film status, exact coverage seconds, approved shot IDs, lyric or musical cue,
and release gates. The current `ACTIVE-BATCH.md` calls Anbudaimai unpublished
while the channel already has a published cinematic upload; that status needs
reconciliation before it drives further work. For future still-derived scenes,
prefer environments, objects, rain, water, smoke, and light with physically
bounded animation. Use actual moving footage for prominent people, gestures,
and ritual actions whenever possible. Review at normal speed with the song,
then run technical decode, black-frame, audio continuity, and cut-boundary QC.

## Clean branded cut

`render_branded.py` rebuilds the first 3,870 frames directly from the 24
director-selected source ranges in `batch-v15.json`, omitting the provisional
upper-left review text. It regenerates the 20-shot image-motion tail without
that text, joins both sections, and overlays the official Guru Kula Desam
channel emblem at the lower left (102 x 102 pixels, 24-pixel margin). The
avatar source is `production/gananatha-om/channel-avatar-reference.jpg`.

Run from the repository root after materializing the source clips with Git LFS:

```powershell
python production/batch03/vaan-sirappu/image-motion/render_branded.py
```

The resulting `VAAN-SIRAPPU-CINEMATIC-v2.mp4` has 7,501 frames at 24 fps,
1280 x 720, and uses the original AAC stream byte-for-byte. Full video/audio
decode passed on 2026-09-27, blackdetect found zero intervals at the
0.02-second threshold, and `branded-contact-sheet.jpg` was inspected at 12
points including both sides of the 161.25-second join. The first section
contains actual selected moving footage; the final 151.29 seconds use still
artwork with camera and bounded environmental animation. These technical
checks do not prove lyric timing or full-speed human audiovisual approval.

The clean 161-second section, silent image-motion tail, and small logo PNG are
generated intermediates and are not committed.

Published on the official Guru Kula Desam channel on 2026-09-27:
https://youtu.be/f1jxgAbXcdE . YouTube reported no copyright issue during
upload. Live playlist enumeration confirmed membership in `Discography` and
`திருக்குறள் | Thirukkural — Master Collection`. YouTube processing may
continue after publication; the local technical checks above cover the
uploaded source file.
