"""Validate the committed Guru Kula Desam playlist snapshot."""

from collections import Counter
from pathlib import Path
import json
import re
import sys


CATALOG = Path(__file__).with_name("catalog-2026-09-26.json")
VIDEO_ID = re.compile(r"[A-Za-z0-9_-]{11}\Z")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    songs = data["songs"]
    playlist_ids = data["playlist_ids"]
    assert playlist_ids["Discography"] == "PLAjtBRKl_IlI"
    dedicated = set(playlist_ids) - {"Discography"}
    ids = [song["id"] for song in songs]
    assert len(ids) == len(set(ids)) == 324, "Catalog IDs must be unique"
    assert all(VIDEO_ID.fullmatch(video_id) for video_id in ids)
    assert all(song["title"] for song in songs)
    assert all(song["playlists"] for song in songs)
    assert all(set(song["playlists"]) <= dedicated for song in songs)
    assert sum(song["release"] is not None for song in songs) == data[
        "distinct_release_tracks"
    ] == 282
    assert sum(song["channelUpload"] for song in songs) == data[
        "channel_uploads_checked"
    ] == 38
    assert data["release_albums_checked"] == 147
    assert data["release_track_entries"] == 285

    counts = Counter(name for song in songs for name in song["playlists"])
    assert sum(counts.values()) == 333
    print(f"Verified {len(songs)} unique videos and {sum(counts.values())} dedicated memberships")
    for name in sorted(counts):
        print(f"  {name}: {counts[name]}")


if __name__ == "__main__":
    main()
