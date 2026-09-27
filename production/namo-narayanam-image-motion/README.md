# Namo Narayanam / Dashavatara cinematic image film

This full-song film uses the unchanged Guru Kula Desam audio from
`4vZEVROZIx8`. The visual sequence follows Vaishnava devotees into a temple,
through the Dashavatara images, and back to collective tulsi offering. The
film is image-derived: camera movement reframes still artworks; people and
objects inside the images do not move independently.

Seventeen previously approved avatar plates and five new ImageGen scenes make
the source set. `NN22-varaha-boar.png` corrects the earlier `N05` plate, which
visibly depicted an elephant rather than the boar avatar. The uncorrected
plate is excluded from this film. Some approved plates recur in a second,
closer framing to carry the 7:35 recording without inventing new footage.

`render.py` runs the shared 1280x720, 24 fps renderer with restrained camera
movement, music-energy-near cuts, the original AAC recording, and the Guru
Kula Desam channel avatar at lower left. `review-manifest.json` lists every
shot and its exact frame boundaries.

```powershell
python production/namo-narayanam-image-motion/render.py
python production/film_contact.py production/namo-narayanam-image-motion/NAMO-NARAYANAM-CINEMATIC-v1.mp4
```

The contact sheet is a visual sample of the encoded film. Automated cuts do
not establish exact lyric or phrase synchronization.

## Review and publication state

The 7:35 export decoded without error. Its remuxed AAC payload is byte-for-byte
the same as the original (SHA-256
`32be2224a97eb1f7a5b8dc6e5f3d87fb70350739955d827cfa289359991651c1`).

This corrected cut is **unpublished**. A separate shared batch published
https://youtu.be/WIDyQVQY2X8 before this cut was ready; publishing this one
would duplicate the song. That live batch film's manifest includes the
elephant-like `N05-imagegen-varaha.png` shot. The corrected `NN22` plate and
this alternate render are retained here for review before any replacement
decision.
