# Guru Kula Desam: next song film batch

Three more films were published as **Public** on September 27, 2026. Each uses the original song audio, the channel emblem at lower left, and a wide opening scene. All 56 shots in this batch use distinct images. Across this batch and the preceding ten-song batch, all 200 shot images have unique SHA-256 hashes.

| Song | Scenes | Source audio | Published film |
|---|---:|---|---|
| Aalaya Naatham | 12 | [Original](https://youtu.be/Wf1Ehxt_A5s) | [Film](https://youtu.be/coUEhVQH0Uk) |
| Nenjari Vuruthal Part 1 | 24 | [Original](https://youtu.be/JDqbpISJjIA) | [Film](https://youtu.be/KFtS403RfbY) |
| Tunjalum Tunjal | 20 | [Original](https://youtu.be/xGb7ZXDRvVU) | [Film](https://youtu.be/0SUn5igNEE0) |

Each render passed an exact decoded-audio comparison against the source and a full media decode. YouTube Studio showed all three as **Public / Published**. Copyright checking was still in progress for Tunjalum Tunjal at the time of publication; no issue was displayed.

The `manifest.json` in each song folder records the source ID and shot order. `render.py` builds the films, and `qc.py` verifies them.
