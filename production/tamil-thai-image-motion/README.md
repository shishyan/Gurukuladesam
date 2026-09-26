# Tamil Thai Vazhthu cinematic image film

This 4:11 full-song film uses Guru Kula Desam's original `ETELjf0OTi4` AAC
recording unchanged. It has 21 distinct image-derived shots: seventeen
previously approved Tamil landscape and heritage plates, plus four new scenes
of poetry, music, Bharatanatyam, and handloom weaving. No source image is used
twice in the shot plan.

`render.py` uses the shared image-film renderer in
`production/thiruppavai1-image-motion/render.py`. It makes a 1280x720, 24 fps
H.264 film with slow camera movement, cuts near nearby music energy minima,
and the Guru Kula Desam avatar at lower left. People and objects within an
image remain still. `review-manifest.json` records all shot sources and frame
boundaries. Run from the repository root:

```powershell
python production/tamil-thai-image-motion/render.py
python production/film_contact.py production/tamil-thai-image-motion/TAMIL-THAI-VAZHTHU-CINEMATIC-v1.mp4
```

The completed video decoded without error. Its AAC payload remuxed to ADTS
matched the original audio byte for byte (SHA-256
`603925be8fe0d8bb78fe292de896fac65c636ba70e9e1643d219a8884745d0b3`).
The 12-frame contact sheet samples the encoded film and logo. Exact lyric and
phrase timing is not established by the automated cut placement.

## Publication

Published September 27, 2026: https://youtu.be/isCeNcUwBTw

YouTube Studio reported public visibility, no copyright issues, and selection
of both `Discography` and `Other Songs`.
