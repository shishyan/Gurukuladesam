# Kalvi image-motion film — review cut

## Published unique-image film

`KALVI-CINEMATIC-v3-UNIQUE-IMAGES.mp4` is the final published cut:
https://youtu.be/KZxknhbVIk0 (published 2026-09-27). It begins with a new
wide landscape for the orchestral opening and uses 24 distinct source images
for 24 shots, with the Guru Kula Desam logo at bottom left. The manifest
enforces unique image filenames. Full video/audio decode passed, no black
intervals were detected at a 0.02-second threshold, and the AAC audio payload
matches the original channel source byte-for-byte. YouTube's upload check
reported no copyright issue. It was added to the Thirukkural Master Collection
and Discography playlists.

Earlier v1 and v2 files below are superseded review cuts that repeat artwork.

The full-length review film is `KALVI-FULL-IMAGE-MOTION-REVIEW-v1.mp4`.
`KALVI-CINEMATIC-v2.mp4` is the presentation cut matched to the published
Gana Natha Om reference: it adds the same circular channel emblem at the lower
left and has no review label. It remains unpublished pending audiovisual review.
It uses the original Guru Kula Desam recording `_Ceq0AzIQ9c` (6:03.26),
12 new ImageGen artworks, and 24 slow camera framings. The imagery follows
learning, demonstration, practical application, and knowledge shared with a
community. No new voice or music was generated.

Run `python production/kalvi-image-motion/render.py` from the repository root
to reproduce the film. `review-manifest.json` records the exact shot order and
frame boundaries; `contact-sheet.jpg` shows all source plates, and
`review-contact-sheet.jpg` samples the output.

Technical verification: 1280 x 720, 24 fps, 8,718 video frames, full video
and audio decode passed, no black intervals found at a 0.02-second threshold.
The AAC payload in the MP4 is byte-identical to the original channel audio
after ADTS remux (SHA-256
`2afa3e786e09e037dbff1e71204f25779e586782220d980e523f1d24840b1bb8`).
The branded cut also passed full decode and black-frame checks, and its AAC
payload is byte-identical to the source. `branded-check.jpg` records a visual
check of the emblem placement.

This is an image-motion treatment: people and objects within each artwork are
still. Cuts were placed near low-energy audio points and have not been checked
against the exact sung Tamil lines. Full-speed audiovisual review is needed
before publication.

Image prompts were created for the 12 roles named by the artwork files, with
the common specification: historically grounded Tamil village learning scenes,
cinematic photoreal 16:9 composition, natural anatomy, maintained environments,
and no readable text, modern objects, or watermarks. The built-in ImageGen tool
created the plates; the copies used by the render are stored in this directory.
