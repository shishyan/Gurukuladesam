# MO01 / MO02 signage correction feasibility

2026-09-17. Bounded inspection only, not a corrected asset or release approval. Originals unchanged. No footage generated, no substitute opening rendered or published.

## Evidence

Inspected MO01 and MO02 full-resolution5sec frames, MO01 full-resolution0.5sec and3.5sec, and six1fps samples covering source0.5–6.5sec. Supplementary video-extracted evidence: `review/MO01-start.png`, `review/MO01-end.png`, `review/MO01-signage-feasibility.png`. These are FFmpeg extractions, not edited stills.

## Restrained crop: not viable

In MO01 at0.5sec, blue boards flank the central tower at approximately x410–434 and775–795, y340–375 on1280x720 frame. By3.5sec they are approximately389–416 and791–811,y375–408. Full tower reaches roughly y40 and group bodies extend below y560 later. Thus a central horizontal crop narrow enough to exclude both boards is only about340pixels wide across the selected interval. A16:9 crop at that width is approximately191pixels high: it cannot retain both complete tower and congregation. Keeping the full vertical span would instead produce a narrow portrait composition, sacrifice most community/side architecture and require padding or distortion to restore16:9. A crop above the boards loses doorway and congregation; below them loses tower. This defeats the requested broad establishing composition.

MO02 has the same structural problem: boards at both sides of tower/base plus a left foreground plaque. Its signs are embedded between the tower and the community, not isolated at discardable outer edges. A restrained16:9 trim cannot exclude them while retaining complete tower and group context. Cropping away generator watermark is not an acceptable objective or workaround.

## Local treatment: technically possible, not yet a credible clean correction

The physical signboards could remain while their invented writing is replaced by an intentionally plain board surface. That is different from removing the boards entirely, and would relax the original zero-board art direction. A surface replacement requires planar tracking (translation, scale and perspective), matched illumination/texture, antialiased boundary and foreground occlusion handling. In MO01 the left board shifts roughly20pixels horizontally and34pixels vertically over3seconds and grows; a single stationary patch cannot work. Foreground heads approach/overlap board area near the beginning, so an indiscriminate tracked rectangle risks painting over a person. MO02 additionally has the foreground plaque and more surfaces to solve.

FFmpeg can translate/scale masks manually, but ordinary boxblur/delogo removes readable detail by visible smearing, not faithful reconstruction of a sign-free temple wall. Large rectangular coverage sufficient to catch uncertain letter edges risks smearing board frames, masonry and people. A solid patch would flatten lighting and introduce a conspicuous rectangle; it is not a defensible no-signboard correction. No simple local filter is certified by this inspection.

Therefore **no treatment comparison was produced**, rather than create a known-obvious blur and present it as improvement. This is not a claim that professional tracked compositing is impossible. It is a finding that crop/basic-filter correction does not currently satisfy the supplied clean, wide, unsmeared opening criteria. The next defensible local method would be an explicit short planar-compositing proof with occlusion masks and full-resolution temporal review, with authorization to retain blank physical boards; no full render should be replaced until that proof passes. Alternatively a genuinely different board-free viewpoint/reference composition is needed, not repeated wording of the same frontal template.
