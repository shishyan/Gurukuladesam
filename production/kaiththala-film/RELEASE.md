# Kaiththala Niraigani cinematic film

- Original Guru Kula Desam song: https://youtu.be/IhE1OvdIBKs
- Public ritual edition: https://youtu.be/hKkmbQ9TIaU
- Playlists selected in YouTube Studio: Discography; Lord Murugar Songs
- Studio status on September 27, 2026: video published; checks complete with no issues

This film uses twelve distinct imagegen scenes cropped from three saved contact sheets. The original song audio is copied into the camera-motion render and then the ritual-effects render. The channel emblem appears at lower left. The final film frames both lower sides with dheepam and four burning agarbatti, and adds restrained drizzle to the rainy outdoor courtyard scene.

From this folder, run `python prepare.py`, `python render.py manifest.json`, then `python ../next-five-image-motion/ritual_effects.py manifest.json --rain-shots 9`. Run `python verify.py` to check scene uniqueness, exact decoded audio, and full media decode. The final file is `KAITHTHALA-NIRAIGANI-CINEMATIC-ritual-v2.mp4`.
