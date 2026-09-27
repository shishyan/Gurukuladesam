# Guru Kula Desam: ten song film batch

All films use the channel emblem at lower left, a wide opening composition, the source song's original audio, and a distinct image for each shot. The batch contains 144 shots with 144 distinct image files by content hash. Each rendered file passed a full media decode and an exact decoded-audio comparison with its source. YouTube Studio confirmed all ten films as **Public / Published** on September 27, 2026.

| Song | Scenes | Source audio | Published film |
|---|---:|---|---|
| Porai Udaimai | 20 | [Original](https://youtu.be/aSQrSHA4YtU) | [Film](https://youtu.be/R82hz_s2YGQ) |
| Maasil Veenaiyum | 23 | [Original](https://youtu.be/cKyT1Cv7zEA) | [Film](https://youtu.be/KQpDmHooEh8) |
| Thennadudaiya Sivaney Potri | 12 | [Original](https://youtu.be/mb-lljpUJ5g) | [Film](https://youtu.be/Z9GnvOMjDjU) |
| Namo Narayanam | 17 | [Original](https://youtu.be/4vZEVROZIx8) | [Film](https://youtu.be/WIDyQVQY2X8) |
| Thiruvaiyaaru Thirumurai | 12 | [Original](https://youtu.be/xAgvuRIIl6o) | [Film](https://youtu.be/iTALOLp7MkQ) |
| Vedasar Shiva Stotram | 12 | [Original](https://youtu.be/_6amHDAc8EI) | [Film](https://youtu.be/Csc5uzl184s) |
| Thirupulambal | 12 | [Original](https://youtu.be/BbDNJdLDy-4) | [Film](https://youtu.be/4sJwwtZHUvI) |
| Naal En Seyyum | 12 | [Original](https://youtu.be/pYh67ltckLQ) | [Film](https://youtu.be/5RTBMEIozEg) |
| Inna Seidharai | 12 | [Original](https://youtu.be/Y3xujLwXuBs) | [Film](https://youtu.be/7npbkuQwjEE) |
| Nenjari Vuruthal Part 2 | 12 | [Original](https://youtu.be/7wJJCQrYo04) | [Film](https://youtu.be/R8OyFbqJJEw) |

The `manifest.json` in each song folder records source ID and unique shot order. `render.py` generates the finished files; `qc.py` verifies them. The contact sheets were generated as four independent scenes per sheet, then split into unique shot files.
