$ErrorActionPreference='Stop'
$ffmpegExe='C:\Users\Shishyan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
Set-Location (Resolve-Path "$PSScriptRoot/../..").Path
$duration=45
$label="drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='NEW DIRECTION - INCOMPLETE REVIEW':fontsize=22:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=24,drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='Provisional timing - not rhythm verified':fontsize=18:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=55"
$filter="[0:v]trim=start=0:end=31.5,setpts=PTS-STARTPTS,fps=24,setsar=1[v0];[1:v]trim=start=0.5:end=9,setpts=PTS-STARTPTS,fps=24,setsar=1,$label[v1];[2:v]trim=start=0.5:end=5.5,setpts=PTS-STARTPTS,fps=24,setsar=1,$label[v2];[v0][v1][v2]concat=n=3:v=1:a=0[v];[3:a]atrim=start=0:duration=${duration},asetpts=PTS-STARTPTS[a]"
& $ffmpegExe -hide_banner -loglevel warning -y -i production/review/maasil-NEW-DIRECTION-INCOMPLETE-v3.mp4 -i production/review/ML02-grove-take01-silent-review.mp4 -i production/review/ML03-dhoopam-take01-silent-review.mp4 -i 'source/youtube/cKyT1Cv7zEA-மாசில் வீணையும்.m4a' -filter_complex $filter -map '[v]' -map '[a]' -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart production/review/maasil-NEW-DIRECTION-INCOMPLETE-v4.mp4
if ($LASTEXITCODE -ne 0) {throw 'New-direction v4 review encode failed'}
