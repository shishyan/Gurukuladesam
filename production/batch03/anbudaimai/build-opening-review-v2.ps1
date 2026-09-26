param([switch]$IncludeV3Selects,[switch]$IncludeV4Selects,[switch]$IncludeV5Selects,[switch]$IncludeV6Selects,[switch]$IncludeV7Selects,[switch]$IncludeV8Selects,[switch]$IncludeV9Selects,[switch]$IncludeV10Selects,[switch]$IncludeV11Selects,[switch]$IncludeV12Selects,[switch]$IncludeV13Batch,[switch]$IncludeV14Batch,[switch]$IncludeV15Batch,[switch]$FullReview)
if($FullReview){$IncludeV15Batch=$true}
if($IncludeV15Batch){$IncludeV14Batch=$true}
if($IncludeV14Batch){$IncludeV13Batch=$true}
if($IncludeV13Batch){$IncludeV12Selects=$true}
if($IncludeV12Selects){$IncludeV11Selects=$true}
if($IncludeV11Selects){$IncludeV10Selects=$true}
if($IncludeV10Selects){$IncludeV9Selects=$true}
if($IncludeV9Selects){$IncludeV8Selects=$true}
if($IncludeV8Selects){$IncludeV7Selects=$true}
$ErrorActionPreference='Stop'
Set-Location (Resolve-Path "$PSScriptRoot/../../..").Path
$ffmpegExe='C:\Users\Shishyan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
$shots=@(
 @('AN01-rainy-courtyard-take01-silent-review.mp4',3.75,9.5),
 @('AN02-seated-veranda-take01-silent-review.mp4',0.5,9),
 @('AN03-shared-produce-take01-silent-review.mp4',0.75,8.75),
 @('AN04-window-listening-take01-silent-review.mp4',0.75,8.25),
 @('AN05-garden-gathering-take01-silent-review.mp4',1,8.5)
)
$outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v2.mp4'
if($IncludeV3Selects -or $IncludeV4Selects -or $IncludeV5Selects -or $IncludeV6Selects -or $IncludeV7Selects){
 $shots=@($shots[0..2])+(,@('AN07-cloth-folding-take01-silent-review.mp4',0.75,8.5))+@($shots[3..4])+(,@('AN06-umbrella-take01-silent-review.mp4',0.75,8.25))
 $outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v3.mp4'
}
if($IncludeV4Selects -or $IncludeV5Selects -or $IncludeV6Selects -or $IncludeV7Selects){
 $shots+=(,@('AN09-invitation-conditioned-take01-silent-review.mp4',0.5,8.5))
 $shots+=(,@('AN10-reaction-conditioned-take01-silent-review.mp4',0.5,8))
 $outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v4.mp4'
}
if($IncludeV5Selects -or $IncludeV6Selects -or $IncludeV7Selects){
 $shots+=(,@('AN11-rain-contact-take01-silent-review.mp4',1,5.5))
 $outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v5.mp4'
}
if($IncludeV6Selects -or $IncludeV7Selects){
 $shots+=(,@('AN12-cups-conditioned-take01-silent-review.mp4',3.5,8.5))
 $outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v6.mp4'
}
if($IncludeV7Selects){
 $shots+=(,@('AN13-acknowledgement-conditioned-take01-silent-review.mp4',0.5,7.5))
 $outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v7.mp4'
}
if($IncludeV8Selects){
 $shots+=(,@('AN14-tray-conditioned-take01-silent-review.mp4',0.5,7.5))
 $outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v8.mp4'
}
if($IncludeV9Selects){
 $shots+=(,@('AN16-leaf-rain-contact-take01-silent-review.mp4',1,5.5))
 $outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v9.mp4'
}
if($IncludeV10Selects){
 $shots+=(,@('AN17-community-table-conditioned-take01-silent-review.mp4',0.5,9))
 $outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v10.mp4'
}
if($IncludeV11Selects){
 $shots+=(,@('AN18-community-reaction-conditioned-take01-silent-review.mp4',0.5,7.5))
 $outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v11.mp4'
}
if($IncludeV12Selects){
 $shots+=(,@('AN19-making-room-conditioned-take01-silent-review.mp4',1.5,7))
 $outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v12.mp4'
}
if($IncludeV13Batch){
 $shots+=(,@('AN20-shared-bench-conditioned-take01-silent-review.mp4',0.5,7.5))
 $shots+=(,@('AN21-shared-attention-conditioned-take01-silent-review.mp4',0.25,3.75))
 $shots+=(,@('AN22-community-together-conditioned-take01-silent-review.mp4',0.5,8.5))
 $outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v13.mp4'
}
if($IncludeV14Batch){
 $shots+=(,@('AN24-courtyard-flow-take01-silent-review.mp4',1,7))
 $outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v14.mp4'
}
if($IncludeV15Batch){
 $shots+=(,@('AN25-practical-care-conditioned-take01-silent-review.mp4',0.5,7.5))
 $shots+=(,@('AN26-care-response-conditioned-take01-silent-review.mp4',0.5,8))
 $shots+=(,@('AN27-basket-task-conditioned-take01-silent-review.mp4',1,7.5))
 $shots+=(,@('AN28-task-complete-conditioned-take01-silent-review.mp4',3,7.5))
 $shots+=(,@('AN29-garden-view-take01-silent-review.mp4',1,6.5))
 $outputFile='production/batch03/anbudaimai/ANBU-moving-opening-INCOMPLETE-v15.mp4'
}
$label="drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='ANBU - INCOMPLETE REVIEW':fontsize=22:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=24,drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='Independent acts of care - provisional musical timing':fontsize=17:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=54"
if($FullReview){
 $shots+=(,@('AN30-closing-family-conditioned-take01-silent-review.mp4',0.25,8.75))
 $shots+=(,@('AN31-towel-care-conditioned-take01-silent-review.mp4',0,7))
 $shots+=(,@('AN32-reciprocal-care-conditioned-take01-silent-review.mp4',0.25,9.25))
 $shots+=(,@('AN33-shared-garden-conditioned-take01-silent-review.mp4',0.25,9.25))
 $shots+=(,@('AN34-family-ending-conditioned-take01-silent-review.mp4',0.25,(229.0/24)))
 $outputFile='production/batch03/anbudaimai/ANBU-FULL-LENGTH-REVIEW-v1.mp4'
 $label="drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='ANBU - FULL-LENGTH REVIEW':fontsize=22:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=24,drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='Human audiovisual approval pending - provisional musical timing':fontsize=17:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=54"
}
$ffArgs=@('-hide_banner','-loglevel','warning','-y');$filters=@();$labels='';$duration=0
for($i=0;$i -lt $shots.Count;$i++){
 $shot=$shots[$i];$duration+=$shot[2]-$shot[1]
 $ffArgs+=@('-i',"production/batch03/anbudaimai/$($shot[0])")
 $cropFilter=''
 if($shot[0] -like 'AN07-*'){$cropFilter='crop=1152:648:128:72,scale=1280:720:flags=lanczos,'}
 if($FullReview){
  $startFrame=[int][math]::Round($shot[1]*24)
  $endFrame=[int][math]::Round($shot[2]*24)
  $filters+="[$($i):v]fps=24,trim=start_frame=${startFrame}:end_frame=${endFrame},setpts=PTS-STARTPTS,fps=24,${cropFilter}setsar=1,$label[v$i]"
 }else{
  $filters+="[$($i):v]trim=start=$($shot[1]):end=$($shot[2]),setpts=PTS-STARTPTS,fps=24,${cropFilter}setsar=1,$label[v$i]"
 }
 $labels+="[v$i]"
}
$ffArgs+=@('-i','source/youtube/lneosghJWgs.m4a')
if($IncludeV8Selects){
 $lastIndex=12
 $priorLabels=''
 for($j=0;$j -lt $lastIndex;$j++){$priorLabels+="[v$j]"}
 $filters+="${priorLabels}concat=n=${lastIndex}:v=1:a=0,settb=AVTB[prior]"
 $filters+="[v${lastIndex}]settb=AVTB[next]"
 if($IncludeV9Selects){
  $filters+='[prior][next]xfade=transition=fade:duration=0.5:offset=84,format=yuv420p[withDissolve]'
  $tailLabels='[withDissolve]'
  for($j=13;$j -lt $shots.Count;$j++){$tailLabels+="[v$j]"}
  $filters+="${tailLabels}concat=n=$($shots.Count-12):v=1:a=0[v]"
 }else{
  $filters+='[prior][next]xfade=transition=fade:duration=0.5:offset=84,format=yuv420p[v]'
 }
 $duration-=0.5
}else{
 $filters+="${labels}concat=n=$($shots.Count):v=1:a=0[v]"
}
if($FullReview){
 $ffArgs+=@('-filter_complex',($filters -join ';'),'-map','[v]','-map',"$($shots.Count):a:0",'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',$outputFile)
}else{
 $filters+="[$($shots.Count):a]atrim=start=0:duration=$duration,asetpts=PTS-STARTPTS[a]"
 $ffArgs+=@('-filter_complex',($filters -join ';'),'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',$outputFile)
}
& $ffmpegExe @ffArgs
if($LASTEXITCODE -ne 0){throw 'Anbu v2 encode failed'}
Write-Output "Duration=$duration"
