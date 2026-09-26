$ErrorActionPreference='Stop'
Set-Location (Resolve-Path "$PSScriptRoot/../../..").Path
$ffmpegExe='C:\Users\Shishyan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
$label="drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='ANBU - INCOMPLETE REVIEW':fontsize=22:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=24,drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='Independent acts of care - provisional musical timing':fontsize=17:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=54"
$graph="[0:v]trim=start=3.75:end=9.5,setpts=PTS-STARTPTS,fps=24,setsar=1,$label[a];[1:v]trim=start=0.5:end=9,setpts=PTS-STARTPTS,fps=24,setsar=1,$label[b];[a][b]concat=n=2:v=1:a=0[v];[2:a]atrim=start=0:duration=14.25,asetpts=PTS-STARTPTS[s]"
& $ffmpegExe -hide_banner -loglevel warning -y -i production/batch03/anbudaimai/AN01-rainy-courtyard-take01-silent-review.mp4 -i production/batch03/anbudaimai/AN02-seated-veranda-take01-silent-review.mp4 -i source/youtube/lneosghJWgs.m4a -filter_complex $graph -map '[v]' -map '[s]' -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v1.mp4
if($LASTEXITCODE -ne 0){throw 'Opening encode failed'}
