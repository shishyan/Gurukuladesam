# Thirukkural local production queue

Claimed recordings: jBA9wlyNjAE (Amaichu), IiZoud1sP2o (Aran), FrZmyvY3sEc (Avai Anjaamai).

These films are being produced while YouTube's daily upload quota blocks new uploads.
They must not be listed as published until Studio confirms publication and a public URL is verified.

Each film uses twelve distinct illustrated scenes, continuous image movement, the original
AAC audio stream, and the existing channel emblem at bottom-left. No generated clip audio is used.

The channel inventory contains 180 public videos at this audit. Matching existing films,
local manifests, and source IDs were checked before selection. Recheck the live channel
before publishing because other production agents may have released more films.

## Reproduce

Run `python prepare.py` after `generated-assets.json` has local storyboard sheet paths.
Run `python render.py <song>/manifest.json` for each song, then `python qc.py`.
`ready.json` records the finished local films awaiting publication.

## Publishing order

First publish the two pending films in `../batch-sept-28-10/ready.json`, then this batch.
Import the finished full-song MP4 into Google Vids and preserve its project URL.
Upload via the Guru Kula Desam YouTube Studio account, not the different account used by
the Vids direct YouTube export. Scheduling publication still requires uploading the file;
it does not bypass the channel's daily upload quota.
