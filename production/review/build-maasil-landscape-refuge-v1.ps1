$ErrorActionPreference='Stop'
$ffmpegExe='C:\Users\Shishyan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
Set-Location (Resolve-Path "$PSScriptRoot/../..").Path
$shots=@(
 @{file='MW01-take01-silent-review.mp4';start=0.5;end=9.5},
 @{file='MT04-rear-prayer-take01-silent-review.mp4';start=0.5;end=8.5},
 @{file='MV01-veena-gathering-take01-silent-review.mp4';start=1;end=8},
 @{file='ML03-dhoopam-take01-silent-review.mp4';start=0.5;end=5.5},
 @{file='MR01-pond-shelter-take01-silent-review.mp4';start=0.5;end=8.5}
)
$label="drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='LANDSCAPE AND REFUGE - INCOMPLETE REVIEW':fontsize=21:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=24,drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='Independent montage - provisional musical timing':fontsize=18:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=55"
$ffArgs=@('-hide_banner','-loglevel','warning','-y')
$filters=@()
for($i=0;$i -lt $shots.Count;$i++){
 $shot=$shots[$i]
 $ffArgs+=@('-i',"production/review/$($shot.file)")
 $filters+="[$($i):v]trim=start=$($shot.start):end=$($shot.end),setpts=PTS-STARTPTS,fps=24,setsar=1,$label[v$i]"
}
$ffArgs+=@('-i','source/youtube/cKyT1Cv7zEA-மாசில் வீணையும்.m4a')
$filters+='[v0][v1][v2][v3][v4]concat=n=5:v=1:a=0[v]'
$filters+='[5:a]atrim=start=0:duration=37,asetpts=PTS-STARTPTS[a]'
$ffArgs+=@('-filter_complex',($filters -join ';'),'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','production/review/maasil-LANDSCAPE-REFUGE-INCOMPLETE-v1.mp4')
& $ffmpegExe @ffArgs
if($LASTEXITCODE -ne 0){throw 'Landscape refuge review encode failed'}
