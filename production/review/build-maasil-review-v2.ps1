$ErrorActionPreference = 'Stop'
$ffmpegExe = 'C:\Users\Shishyan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
$projectDir = (Resolve-Path "$PSScriptRoot/../..").Path
Set-Location $projectDir
# Review only: these ranges are not release approval. Never repeat footage.
$shots = @(
    @{file='M01-take01.mp4';start=1;end=8;label='M01 - pilgrim'},
    @{file='M01C-take01.mp4';start=2;end=6;label='M01C - footsteps'},
    @{file='M01B-take01-new-section.mp4';start=2;end=9;label='M01B - reaction'},
    @{file='M09B-take02.mp4';start=0.5;end=8.5;label='M09B - breeze'},
    @{file='M07-take01.mp4';start=1.5;end=9.5;label='M07 - lotus'},
    @{file='M12R-take01.mp4';start=0.25;end=4.20;label='M12R - rain leaves'},
    @{file='M12R-take01.mp4';start=6.35;end=9.75;label='M12R - puddle'}
)
$ffArgs = @('-hide_banner','-loglevel','warning','-y')
foreach ($shot in $shots) { $ffArgs += @('-i',"production/candidates/maasil/$($shot.file)") }
$ffArgs += @('-i','source/youtube/cKyT1Cv7zEA-மாசில் வீணையும்.m4a')
$filters = @()
$duration = 0.0
for ($i=0; $i -lt $shots.Count; $i++) {
    $shot = $shots[$i]
    $duration += $shot.end-$shot.start
    $filters += "[$($i):v]trim=start=$($shot.start):end=$($shot.end),setpts=PTS-STARTPTS,fps=24,scale=1280:720,setsar=1,drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='INCOMPLETE REVIEW - NOT FOR PUBLICATION':fontsize=20:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=24,drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='$($shot.label)':fontsize=18:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=54[v$i]"
}
$videoLabels = ((0..($shots.Count-1) | ForEach-Object { "[v$_]" }) -join '')
$filters += "${videoLabels}concat=n=$($shots.Count):v=1:a=0[vout]"
$filters += "[$($shots.Count):a]atrim=start=10:duration=$duration,asetpts=PTS-STARTPTS[aout]"
$ffArgs += @('-filter_complex',($filters -join ';'),'-map','[vout]','-map','[aout]','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','production/review/maasil-INCOMPLETE-sequence-v2.mp4')
& $ffmpegExe @ffArgs
if ($LASTEXITCODE -ne 0) { throw "Review encode failed: $LASTEXITCODE" }
Write-Output "Rendered unique-footage review. Requested duration: $duration seconds."
