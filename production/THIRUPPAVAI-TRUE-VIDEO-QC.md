# Thiruppavai 1 — True-Video Production and QC Standard

Updated 2026-09-12. This document is the release gate for every newly generated
Thiruppavai clip. `THIRUPPAVAI-TRUE-VIDEO-MANIFEST.template.json` is the required
shot-level record.

## Non-negotiable source rule

Only native, temporally generated video clips that pass this document may enter
the edit. A moving camera over a still image is not true video.

**Hard exclusion:** all old ImageGen motion proofs, all videos made from stills by
`production/render_motion_test.py` or equivalent pan/zoom/parallax processing,
all files under `renders/tests` matching motion-proof work, all rejected assets,
and every deleted or superseded release/master are excluded from the production
manifest and final assembly even if a copy remains on disk. They may be viewed
only as negative examples. A deleted release cannot be restored to eligibility;
it must be regenerated as native video and reviewed as a new asset.

The approved still PNGs may guide composition and continuity, but may not be
animated, interpolated, or presented as final true-video shots.

## Audit baseline

The three existing reference contact sheets in `production/audit` establish the
desired photographic vocabulary: devotional realism, measured wide/medium/detail
coverage, wet stone and reflected practical light, restrained incense foreground,
warm sanctum interiors, and cool rainy exteriors. Contact sheets are spatial
references only; they do not prove camera or subject motion.

The local pilot `production/approved/thiruppavai1/S12-gemini-gopuram.mp4` decodes
cleanly and is 10.01 seconds, 1280x720, 24 fps, H.264 with AAC audio. It is the
only local true-video candidate presently recognized. Its generator audio must
be discarded in the music edit. It remains conditional until its temporal,
anatomy, watermark, and transition-handle fields are completed in the manifest.

## Locked story continuity

- Andal is a young adult Tamil woman in a maroon silk sari with emerald border,
  jasmine-wrapped long braid, white-and-red Vaishnava namam, and simple antique
  temple gold.
- A full group is Andal plus exactly eight recurring companions: nine women total.
  Their faces and sari colours remain distinct and unchanged.
- The pilgrimage travels screen-left to screen-right until the sanctum.
- Outdoors: fine Margazhi rain, blue mist, wet stone, small puddle ripples, and
  physically coherent amber reflections.
- Indoors: no rain. Only residual droplets may be visible outside an open doorway.
- When required, the same small brass dhoopam holder is anchored bottom centre,
  occupying 4–6% of frame width, with two or three translucent pale-grey wisps.
- One physically possible camera move per shot: locked tripod, slider, dolly, or
  crane. No handheld shake, orbit drift, digital zoom, reframing pulse, or speed ramp.
- 16:9 cinematic live action, natural anatomy, no modern objects, text, logo, or
  watermark, and no lip-sync close-ups.

## Intake and provenance

Before review, copy the manifest template entry and record the final prompt,
generator and model/version, generator job ID or project URL, original download
path, SHA-256, generation date, and intended story beat. Never overwrite an
earlier download. A revised generation receives a new take suffix and manifest
entry. The download path must point to the untouched native generator file.

## Pass 1 — Technical gate

Reject the clip if any mandatory item fails:

- Native 16:9 video, minimum 1280x720, target 1920x1080 or higher, progressive.
- Target 24 fps; other constant frame rates require an explicit conform note.
- Duration recorded to two decimals; no unexplained truncation or duplicated tail.
- Full decode succeeds without corrupt frames, timestamp errors, black frames, or
  baked generator fade.
- Watermark, logo, captions, UI, or unintended text are absent.
- Generator audio is recorded but is never used in the final song assembly.
- At least 1.0 second of clean motion at both head and tail. Prefer 1.5 seconds.

## Pass 2 — Real-time motion gate

Watch once at normal speed with sound muted and once looped. True temporal motion
must be visible in subjects or environment—not merely in camera translation.

- Camera motion is smooth, constant, mechanically plausible, and matches the
  prompt. Reject jitter, warping, pulsing, horizon roll, sudden acceleration,
  fake depth layers, or a Ken Burns/still-image appearance.
- People breathe, shift weight, walk, gesture, and interact naturally. Fabric,
  jasmine, flame, bells, foliage, water, flowers, and ritual objects move only as
  their materials and forces permit. Reject frozen crowds masked by camera motion.
- No person, limb, garment, flower, vessel, architecture, or deity morphs,
  duplicates, vanishes, teleports, or changes scale/identity during the shot.

## Pass 3 — Frame-step and continuity gate

Inspect the clean head, quarter, middle, three-quarter, and clean tail, plus every
suspicious motion segment frame-by-frame.

### Headcount and identity

For a full-group shot, count exactly nine women in multiple frames. For partial or
detail shots, record required, visible, and intentionally occluded people. Reject
unexplained count changes, face swaps, costume drift, or a background person
appearing/disappearing. Occlusion is acceptable only when spatially continuous.

### Anatomy and interaction

Inspect every visible face, eye, hand, finger, foot, limb, gait, jewellery contact,
object grip, and cloth boundary. Reject fused or extra anatomy, sliding feet,
impossible joints, melted jewellery, intersecting bodies, or unstable facial identity.

### Rain physicality

When rain is required, it must have coherent world-space direction, velocity,
depth, occlusion, and scale. Wet surfaces need plausible accumulation, ripples,
edge drips, splashes or reflections appropriate to the framing. Reject screen-space
rain overlays, rain passing through roofs/people, conflicting directions, frozen
streaks, or indoor rainfall. If rain is not story-appropriate, mark it not required.

### Dhoopam physicality

When required, the brass holder remains anchored to a credible surface at bottom
centre without sliding, resizing, redesigning, or intersecting the frame. Smoke
rises from the holder, curls and diffuses continuously, responds gently to air,
and occludes/gets occluded in correct depth order. Reject frozen smoke, smoke
detached from the vessel, smoke behind a foreground rain layer when geometry says
otherwise, or a holder that teleports or morphs. Indoors/outdoors placement must
remain physically credible; mark not required for shots whose composition cannot
support it rather than forcing a floating overlay.

### Transition handles

The first and final clean seconds must preserve stable exposure, camera velocity,
identity, headcount, and object geometry. Reject generator fades, prompt-start
poses, last-frame freezes, subject cutoffs, abrupt stops, or morphs inside either
handle. Record usable handle lengths separately from total duration.

## Decision rule

Approval requires every hard gate to pass and all manifest fields to be complete.
Use `conditional` only while a factual check is outstanding; conditional clips
cannot enter the release timeline. Any single hard failure means `rejected`.
Revisions are new takes, never silent replacements.

Standard rejection codes: `NOT_TRUE_VIDEO`, `DECODE`, `FORMAT`, `HEADCOUNT`,
`IDENTITY_DRIFT`, `CAMERA_JITTER`, `MOTION_PHYSICS`, `RAIN_PHYSICS`,
`DHOOPAM_PHYSICS`, `ANATOMY`, `MORPH`, `WATERMARK_TEXT`, `MODERN_ELEMENT`,
`EXPOSURE_PULSE`, `HANDLE_HEAD`, `HANDLE_TAIL`, `INDOOR_RAIN`, and `DUPLICATE_BEAT`.

## Assembly preflight

Before export, build the timeline only from manifest entries marked `approved`.
Recompute hashes against each native download, confirm no excluded path or hash is
present, strip generator audio, and review every transition at full speed and
frame-by-frame. The release checklist must name the manifest version used.
