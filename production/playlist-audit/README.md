# Guru Kula Desam playlist audit — 2026-09-26

The [catalog](catalog-2026-09-26.json) is a video-ID snapshot of the public
`@guru-kula-desam` YouTube channel after repairing missing playlist entries.
It records all 324 videos in [Discography](https://www.youtube.com/playlist?list=PLAjtBRKl_IlI)
and the dedicated playlists containing each video. YouTube is the live source
of truth; this file is an audit record, not a playlist importer.

## Coverage

- Inspected all 147 albums on the channel's Releases tab: 285 track entries,
  representing 282 distinct video IDs.
- Inspected all 38 videos on the channel's Videos tab.
- Compared those IDs with all 324 entries in Discography and every dedicated
  playlist. Every release track and upload appears in Discography and at least
  one dedicated playlist. Every Discography entry appears in a dedicated
  playlist, and every dedicated-playlist entry appears in Discography.
- The eight dedicated playlists contain 333 memberships: 9 videos belong to
  more than one dedicated collection. Thirukkural and non-deity songs use their
  respective Thirukkural and Other Songs collections.
- Ten existing playlist entries were absent from the channel's current Releases
  and Videos tabs. They are included because they are in Discography and a
  dedicated playlist; this audit did not assume they are channel uploads or
  remove them. Their catalog records have `release: null` and
  `channelUpload: false`.

Playlist names and IDs are in the catalog's `playlist_ids` object. Each song's
`playlists` array lists its dedicated collections; Discography is implicit for
all catalog entries. `release` names one album where the video was found, and
`channelUpload` indicates its presence on the Videos tab. Three release track
IDs occur on more than one album; the catalog stores each video only once.

## Repairs made during this audit

- Added both versions of கண நாதா ஓம் to Discography and Lord Vinayagar Songs.
- Added newly published cinematic videos missing from Discography and their
  relevant collections, including Shiva, Murugar, Vishnu, Krishna, Amman,
  Vinayagar, and Other Songs.
- Added missing Thirukkural release versions across the September 2026
  releases, including அரண், ஊக்கமுடைமை, வெருவந்த செய்யாமை,
  ஆள்வினையுடைமை, கண்ணோட்டம், தெரிந்து தெளிதல், செங்கோன்மை,
  கொடுங்கோன்மை, சுற்றந்தழால், பொச்சாவாமை, தெரிந்து வினையாடல்,
  and தெரிந்து செயல்வகை.
- Added missing Murugar collection entries for ஸ்கந்த மந்திரம்,
  கௌமாரம் ஸ்துதி, and முருகர் வார வழிபாடு.
- Added both அருட்பெருஞ்சோதி அகவல் சாரம் tracks to Discography and Other
  Songs, and repaired two tracks from திருவருட்பா - இரண்டாம் திருமுறை (II)
  plus the திருவருட்பா - நமச்சிவாய track.

Run `python production/playlist-audit/verify_catalog.py` from the repository
root to validate the snapshot's IDs, counts, and playlist invariants. This
checks the committed snapshot; a later live YouTube change requires a new
browser audit and a refreshed catalog.
