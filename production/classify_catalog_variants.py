"""Composition-level audit: one film per song; alternate recordings are not new songs."""
import json
from pathlib import Path
root=Path(__file__).resolve().parent
audit=json.loads((root/'REMAINING-CATALOG-AUDIT.json').read_text(encoding='utf-8'))
groups={
 'Sivapuranam':['u41L3XgIgGc','6cE4xUOmSzU','aq0j2OMVNoU','wXD_lSlfiSQ','Y0tOS_2Azxs'],
 'Thennadudaiya Sivaney Potri':['vZyHNMkm8xU','j1tzixa2raU','QFCD-U3sT4M','XwlGJp3gqCc'],
 'Thiruppadai Aatchi':['tW9-r0H5rx8','S9WQ-O0tZJI'],
 'Thiruvenba':['xc1iNs05Bkw','o5PVED0ZcfU'],
 'Thirumanthiram':['gwTtvj-h77g'],
 'Thirumullaivayil':['uMK4LISQFE4'],
 'Kuzhaitha Pathu':['jsFIjA8ZOkw'],
 'Thiruvaiyaaru Thirumurai':['2vQYuvePk9U','J7sfVqWuxyU'],
 'Thiruvothur Pathigam':['YycgNlQl6Go','zFb2PGEPrr4','oOGRP4cqGP8','pWSY0_0UQwc','qjxmrb4fmjA','8b2B047SSTo','34D_HpbRxfo'],
 'Pidiyathan Uruvumai':['nutm-A24QcM'],
 'Potri Thiruagaval':['XlCvnE6y9d0'],
 'Maasil Veenaiyum':['nSQKZ2htJ-o'],
 'Thiruneetru Pathigam':['P-gtNBy8sRE'],
 'Thillai Vazh Anthanar':['l-JJXW1QKdg'],
 'Thiruppavai 2':['Lzkbhp_ehA8','phlMcxN_Cfw'],
 'Thiruppavai 1':['fkgEbW9HdtI'],
 'Raghupati Raghava':['Q5G2h9GuGQs','_DHXM8tymn8'],
 'Hare Krishna Hare Rama':['HPP3IG7DWRc'],
 'Kandhar Shashti Thuthi':['PVcmqZuROSU'],
 'Thiruppugazh 712':['YxP_uh3dM18'],
 'Muthai Tharu':['3oJ2OPG-WCs'],
 'Siva Subramaniyar Thiruvirutham':['-unILRjNLHQ'],
 'Abirami Anthathi Thuthi':['w0lNqTk3QCU'],
 'Dhanam Tharum Abirami':['Q2xax9mIhZw'],
 'Paalum Thelithenum':['AW4cljBWy2w'],
 'Anbudaimai':['lneosghJWgs'],
}
lookup={sid:group for group,ids in groups.items() for sid in ids}
rows=[]
for song in audit['remaining']:
    sid= song['id']; title=song['title'];low=title.lower()
    if sid=='5gO0xpY_Y3E':status='excluded: third-party Hans Zimmer recording'; evidence='User scope: own audio songs'
    elif any(x in low for x in ['cinematic','music video','story version','story film','full song film']):status='existing film entry';evidence=title
    elif 'திருக்குறள் | Thirukkural — Master Collection' in song['playlists']:
        status='alternate recording of covered Thirukkural chapter';evidence='playlist-audit/thirukkural-production-completion-2026-09-28.json'
    elif sid in lookup:
        status='same composition as existing or reserved film';evidence=lookup[sid]
    else:status='needs audit';evidence='No composition mapping'
    rows.append({**song,'status':status,'evidence':evidence})
out={'policy':'One film per composition; remixes and alternate performances excluded to avoid duplicate songs. Composition equivalence is not a claim of exact audio equality.','songs':rows,'unresolved':[s for s in rows if s['status']=='needs audit']}
(root/'CATALOG-VARIANTS-AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Unresolved',len(out['unresolved']))
for row in out['unresolved']:print(row['id'],row['title'])
