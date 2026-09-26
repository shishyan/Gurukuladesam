# Vaan Sirappu image-motion study

This is an **18-second production study**, timed to original source audio at
161.25–179.25 seconds. It is not a completed film or an approved addition to
the existing 161.25-second moving-footage edit.

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
