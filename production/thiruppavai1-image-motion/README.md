# Thiruppavai 1: Margazhi Thingal cinematic image film

This full-song film uses the unchanged audio of Guru Kula Desam's original
`RDcw0Bol-cE` upload. The visuals are image-derived: controlled 24 fps camera
reframing of 25 approved temple stills and four newly generated group scenes.
The people and temple elements within each still do not have native motion.

The four new scenes were generated with `S07-imagegen-doorway.png` as the
continuity reference. Each final group scene depicts Andal in a burgundy sari
with eight adult companions. A tenth person generated in the walking and
offering drafts was removed before the final assets were accepted.

`render.py` creates the 1280x720 H.264 film, copies the original AAC audio,
and puts the official Guru Kula Desam channel avatar in the lower left of
every frame. `review-manifest.json` records the frame boundaries and source
image for every shot. Run from the repository root with Pillow, NumPy, and
imageio-ffmpeg installed:

```powershell
python production/thiruppavai1-image-motion/render.py
```

The film follows the gathering at Margazhi dawn, tank, collective pilgrimage,
temple approach, conch and chakra, and offering at the Vishnu sanctum. Cuts
are placed within 0.75 seconds of an even shot grid using nearby audio energy
minima. That method does not establish word-level lyric synchronization.

## Technical review

The completed 5:31.04 export decoded without error. The AAC payload remuxed
to ADTS is byte-for-byte identical to the original song (SHA-256
`64c3c627283059e39ef5810b0ab2216efe6fb6c7ad544e397bdd52da562b71b9`).
`review_contact.py` sampled twelve points from the encoded film into
`review-contact-sheet.jpg`, including the group, walk, offering, ending, and
lower-left channel logo. This is a still-derived film; human motion and exact
lyric-to-cut timing are not certified by these technical checks.
