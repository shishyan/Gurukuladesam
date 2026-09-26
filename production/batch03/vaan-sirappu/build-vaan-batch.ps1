param([string]$ManifestPath="$PSScriptRoot/batch-next.json")
$ErrorActionPreference='Stop'
$projectRoot=(Resolve-Path "$PSScriptRoot/../../..").Path
$manifest=Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
if(-not $manifest.batchReady){throw 'Batch not released for assembly; collect director-selected actual assets first.'}
if(@($manifest.shots).Count -eq 0){throw 'No selected moving footage; refusing placeholder render.'}
if($manifest.outputName -notmatch '^VAAN-[A-Za-z0-9-]+\.mp4$'){throw 'Use a distinct VAAN-*.mp4 review filename.'}
$outputFile=Join-Path $PSScriptRoot $manifest.outputName
if(Test-Path -LiteralPath $outputFile){throw 'Output already exists; preserve prior version and choose a fresh filename.'}
$ffmpegExe='C:\Users\Shishyan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
$argsFF=@('-hide_banner','-loglevel','warning','-n')
$filters=@();$concatLabels='';$frameCount=0;$seen=@{}
$label="drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='VAAN SIRAPPU - REVIEW':fontsize=22:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=24,drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='Human audiovisual approval pending - provisional musical timing':fontsize=17:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=54"
for($i=0;$i -lt $manifest.shots.Count;$i++){
 $shot=$manifest.shots[$i]
 if($shot.file -notmatch '^VS[A-Za-z0-9-]+\.mp4$'){throw 'Only local Vaan source filenames are allowed.'}
 if($seen.ContainsKey($shot.file)){throw 'Repeated source file requires explicit unique-range review; default workflow refuses it.'}
 $seen[$shot.file]=$true
 if(-not $shot.directorSelected -or [string]::IsNullOrWhiteSpace($shot.role)){throw 'Each shot requires actual director selection and a stated narrative role.'}
 $inFrame=[int]$shot.inFrame;$outFrame=[int]$shot.outFrame
 if($inFrame -lt 0 -or $outFrame -le $inFrame){throw 'Invalid24fps source interval.'}
 $sourcePath=Join-Path $PSScriptRoot $shot.file
 if(-not(Test-Path -LiteralPath $sourcePath -PathType Leaf)){throw "Missing actual moving source: $sourcePath"}
 $frameCount+=$outFrame-$inFrame
 $argsFF+=@('-i',$sourcePath)
 $filters+="[$($i):v]fps=24,trim=start_frame=${inFrame}:end_frame=${outFrame},setpts=PTS-STARTPTS,fps=24,scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,$label[v$i]"
 $concatLabels+="[v$i]"
}
$duration=$frameCount/24.0
if($manifest.fullLength -and $frameCount -ne 7501){throw 'Full-length review requires exactly7501 genuine selected frames, not padded footage.'}
if(-not $manifest.fullLength -and $frameCount -ge 7501){throw 'Full coverage reached; review exact final handles/audio before marking fullLength.'}
$audioIndex=$manifest.shots.Count
$argsFF+=@('-i',(Join-Path $projectRoot 'source/youtube/tX4JtRSOuxE.m4a'))
$filters+="${concatLabels}concat=n=$audioIndex`:v=1:a=0[v]"
if($manifest.fullLength){
 $audioMap="$($audioIndex):a:0";$audioCodec=@('-c:a','copy')
}else{
 $filters+="[$($audioIndex):a]atrim=start=0:duration=$duration,asetpts=PTS-STARTPTS[a]"
 $audioMap='[a]';$audioCodec=@('-c:a','aac','-b:a','192k')
}
$argsFF+=@('-filter_complex',($filters -join ';'),'-map','[v]','-map',$audioMap,'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p')+$audioCodec+@('-movflags','+faststart',$outputFile)
& $ffmpegExe @argsFF
if($LASTEXITCODE -ne 0){throw 'Vaan encode failed; no completion claim.'}
Write-Output "ExpectedFrames=$frameCount ExpectedPictureSeconds=$duration Output=$outputFile"
Write-Output 'Encode only: independent decode/frame/cut/rain/audio checks still required before reporting verified review.'
