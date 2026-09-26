# Expanded meaning-led rough cut v1

Output: `production/review/maasil-EXPANDED-ROUGH-INCOMPLETE-v1.mp4`.

Built anew from original selected candidates, not by appending another clip to prior reviews. Mountain→maintained shared shrine establishes devotional context; community and veena lead into moon/pond/bee imagery, then summer/breeze contemplation, rain/refuge, incense and a return to the shrine. Outdoor groups are independent contemplation, not falsely described as all praying toward Shiva. The shrine return is a **different nonoverlapping portion** of MT04, not repeated footage. Interpretation is meaning-led, not verified against sung phrase positions or beats.

## Exact source ranges and order

All source files under `production/candidates/maasil/`. End-exclusive times; frame selection uses ceil(start×24) through ceil(end×24)-1, so only frames beginning before requested out are included. No speed changes, loops or padding.

| Source | Requested range | Frames | Timeline seconds |
|---|---|---:|---|
| MW01-take01.mp4 |0.50–9.50|216|0–9 |
| MT04-rear-prayer-take01.mp4 |0.50–4.50|96|9–13 |
| MG01-take01.mp4 |0.50–9.00|204|13–21.5 |
| MV01-veena-gathering-take01.mp4 |1.00–8.00|168|21.5–28.5 |
| ML04-evening-take01.mp4 |0.50–9.00|204|28.5–37 |
| ML01-lyrics-take01-new-section.mp4 |4.00–9.50|132|37–42.5 |
| M07-take01.mp4 |1.50–9.50|192|42.5–50.5 |
| MG02-take01-new-section.mp4 |0.50–9.00|204|50.5–59 |
| ML02-grove-take01.mp4 |0.50–9.00|204|59–67.5 |
| M09B-take02.mp4 |0.50–8.50|192|67.5–75.5 |
| M12J-take01.mp4 |2.00–6.00|96|75.5–79.5 |
| ML07-prayer-grove-take01.mp4 |0.50–6.50|144|79.5–85.5 |
| M12R-take01.mp4 |0.25–4.20|95|85.5–89.458333 |
| MR01-pond-shelter-take01.mp4 |0.50–8.50|192|89.458333–97.458333 |
| M12R-take01.mp4 |6.35–9.75|81|97.458333–100.833333 |
| ML03-dhoopam-take01.mp4 |0.50–5.50|120|100.833333–105.833333 |
| MT04-rear-prayer-take01.mp4 |4.50–8.50|96|105.833333–109.833333 |

Total2636frames /24 = **109.833333sec** distinct selected review footage. Source272.462948sec leaves **162.629615sec** uncovered by this rough cut. Nominal-source accounting: prior106.85sec pool minus MO01 6sec and ML05 8sec plus recovered10sec and MV01 7sec =109.85sec; frame quantization explains the0.016667sec difference. This is not release-approved duration. Review versions are never added together as coverage.

## Evidence and restrictions

Read MAASIL-FULL-SONG-COVERAGE.md, MAASIL-RECOVERABLE-QC.md, MAASIL-MV01-QC.md and prior shot decisions. M12J4sec and ML07 6sec are recovered selects, not whole10sec outputs. Both support early-summer/refuge only, not the film's governing generic-grove story. Explicit shared shrine focus brackets the montage; additional genuine shrine coverage is still needed in full film.

MO01/MO02 signage exteriors, ML05 archaeological-looking approach, MT01/MT02 weathered-shrine setting, MT03, lone-pilgrim shots, failed veenas, ribbon incense, patterned rain and held/unselected footage omitted. Original files and all previous reviews preserved. No added graphics conceal defects; persistent small review labels identify incompleteness/provisional timing. Watermarks retained.

Only original channel Maasil soundtrack source0–109.833333sec directly mapped, with technical AAC re-encoding. No generated sound, musical rearrangement or claimed instrumental synchronization. Veena imagery illustrates the concept; it is not documentation of the recorded performance.

Same geography, time-of-day progression and cast identity are not established. Ordinary unclassified ritual fixtures are recorded, not automatically treated as malformed. MT04 gold object/tube light remain visible; fine motion and musical cadence need perceptual review. MR01 wet open veranda is not a dry-interior claim. Rain insert cuts do not establish continuous droplet trajectories. The current ending is an excerpt endpoint, not the completed song's resolution. No publication.

Build script: `production/review/build-maasil-expanded-rough-v1.ps1`.

Verification: encode and full audio/video decode exit0 without errors; decoder completed2636frames. Container reports1:49.83,1280x72024fps H.264 yuv420p,AAC44.1kHz stereo. This verifies media integrity, not full-speed perceived quality or release readiness.
