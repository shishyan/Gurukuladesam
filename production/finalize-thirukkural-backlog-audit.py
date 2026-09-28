"""Summarize the completed local plan without claiming YouTube publication."""
import json
from collections import Counter
from pathlib import Path

P = Path(__file__).resolve().parent
queue = json.loads((P/'publication-queue.json').read_text(encoding='utf-8'))
audio = json.loads((P/'backlog-audio-uniqueness.json').read_text(encoding='utf-8'))
coverage = json.loads((P/'playlist-audit/thirukkural-backlog-audit.json').read_text(encoding='utf-8'))
catalog = json.loads((P/'playlist-audit/catalog-2026-09-26.json').read_text(encoding='utf-8'))
live = json.loads((P/'thirukkural-playlist-live-2026-09-28.json').read_text(encoding='utf-8-sig'))
limit = json.loads((P/'upload-limit-status.json').read_text(encoding='utf-8'))
produced = []
for ready in sorted(P.glob('thirukkural-backlog-*/ready.json')):
    for song in json.loads(ready.read_text(encoding='utf-8'))['songs']:
        qc = song['qc']
        assert qc['originalAacBitstreamMatched'] and qc['fullDecodePassed'] and qc['allScenesHaveMovement']
        assert qc['scenes'] == qc['uniqueImages'] == 12
        assert (ready.parent/song['file']).is_file()
        produced.append(song)
assert len(produced) == 45
assert len({s['sourceId'] for s in produced}) == 45
assert audio['tracksChecked'] == queue['pendingCount']
assert audio['decodedPcmHashesUnique'] and not audio['duplicateCandidates']
assert not any(c['status']=='needs production' for c in coverage['chapters'])
old_ids = {s['id'] for s in catalog['songs'] if any('Master Collection' in p for p in s['playlists'])}
new = [{'id':s['id'],'title':s['title']} for s in live['entries'] if s['id'] not in old_ids]
assert all(any(w in s['title'].lower() for w in ['film','cinematic','video']) for s in new)
report = {
    'checkedAtUtc':limit['checkedAtUtc'],
    'playlist':'Thirukkural Master Collection',
    'playlistUrl':'https://www.youtube.com/playlist?list=PLW7qBZp_Q8Ro',
    'livePlaylistEntriesChecked':len(live['entries']),
    'catalogSourceEntries':len(old_ids),
    'newLiveEntriesAllExistingFilms':new,
    'chapterStatusCounts':dict(Counter(c['status'] for c in coverage['chapters'])),
    'chaptersWithoutKnownPublicOrLocalProduction':0,
    'localBacklogBatchesRendered':15,
    'rendersCompleted':45,
    'uniqueNewBacklogFilmsInUploadQueue':sum('thirukkural-backlog-' in s['file'] for s in queue['songs']),
    'earlierReadyFilmsInUploadQueue':2,
    'readyToUploadCount':queue['pendingCount'],
    'parallelAlternateRendersSuppressed':len(queue['excludedAlternateRenders']),
    'otherAgentOwners':queue['excludedAlternateRenders'],
    'noDuplicateAudioCandidates':True,
    'productionPlanFinished':True,
    'publicationFinished':False,
    'blocker':limit,
    'scopeNote':'One film per uncovered devotional Thirukkural chapter. Alternate recordings of filmed chapters are deferred; the Hans Zimmer Space Sounds entry is outside the devotional scope. Other-agent productions retain ownership of six source songs.'
}
(P/'playlist-audit/thirukkural-production-completion-2026-09-28.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Rendered:',len(produced),'unique new queued:',report['uniqueNewBacklogFilmsInUploadQueue'],
      'ready to upload:',report['readyToUploadCount'],'cross-agent alternates excluded:',report['parallelAlternateRendersSuppressed'])
