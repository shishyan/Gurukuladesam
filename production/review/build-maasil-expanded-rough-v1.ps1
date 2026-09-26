param([switch]$IncludeV2Selects,[switch]$IncludeV3Selects,[switch]$IncludeV4Selects,[switch]$IncludeV5Selects)
$ErrorActionPreference='Stop'
$ffmpegExe='C:\Users\Shishyan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
Set-Location (Resolve-Path "$PSScriptRoot/../..").Path
$shots=@(
 @('MW01-take01.mp4',0.5,9.5),
 @('MT04-rear-prayer-take01.mp4',0.5,4.5),
 @('MG01-take01.mp4',0.5,9),
 @('MV01-veena-gathering-take01.mp4',1,8),
 @('ML04-evening-take01.mp4',0.5,9),
 @('ML01-lyrics-take01-new-section.mp4',4,9.5),
 @('M07-take01.mp4',1.5,9.5),
 @('MG02-take01-new-section.mp4',0.5,9),
 @('ML02-grove-take01.mp4',0.5,9),
 @('M09B-take02.mp4',0.5,8.5),
 @('M12J-take01.mp4',2,6),
 @('ML07-prayer-grove-take01.mp4',0.5,6.5),
 @('M12R-take01.mp4',0.25,4.20),
 @('MR01-pond-shelter-take01.mp4',0.5,8.5),
 @('M12R-take01.mp4',6.35,9.75),
 @('ML03-dhoopam-take01.mp4',0.5,5.5),
 @('MT04-rear-prayer-take01.mp4',4.5,8.5)
)
$outputFile='production/review/maasil-EXPANDED-ROUGH-INCOMPLETE-v1.mp4'
if($IncludeV2Selects){
 $shots=@($shots[0..14])+(,@('MT05-flower-offering-take01-new-section.mp4',1,7.5))+@($shots[15..16])+(,@('MC02-closing-vista-take01.mp4',0.5,9.5))
 $outputFile='production/review/maasil-EXPANDED-ROUGH-INCOMPLETE-v2.mp4'
}
if($IncludeV3Selects -or $IncludeV4Selects -or $IncludeV5Selects){
 $shots=@(
  @('MW01-take01.mp4',0.5,9.5),
  @('MT04-rear-prayer-take01.mp4',0.5,4.5),
  @('MG01-take01.mp4',0.5,9),
  @('MF01-garland-group-take01.mp4',1,8),
  @('MV01-veena-gathering-take01.mp4',1,8),
  @('MG02-take01-new-section.mp4',0.5,9),
  @('MV02-family-listening-take01.mp4',2,7),
  @('ML02-grove-take01.mp4',0.5,9),
  @('M09B-take02.mp4',0.5,8.5),
  @('M12J-take01.mp4',2,6),
  @('ML07-prayer-grove-take01.mp4',0.5,6.5),
  @('M07-take01.mp4',1.5,9.5),
  @('M12R-take01.mp4',0.25,4.20),
  @('MR01-pond-shelter-take01.mp4',0.5,8.5),
  @('M12R-take01.mp4',6.35,9.75),
  @('MT05-flower-offering-take01-new-section.mp4',1,7.5),
  @('ML03-dhoopam-take01.mp4',0.5,5.5),
  @('MT04-rear-prayer-take01.mp4',4.5,8.5),
  @('MC02-closing-vista-take01.mp4',0.5,9.5),
  @('ML01-lyrics-take01-new-section.mp4',4,9.5),
  @('ML04-evening-take01.mp4',0.5,9)
 )
 $outputFile='production/review/maasil-EXPANDED-ROUGH-INCOMPLETE-v3.mp4'
}
if($IncludeV4Selects -or $IncludeV5Selects){
 $shots=@($shots[0..14])+(,@('MR02-pavilion-rain-take01.mp4',1,8.5))+@($shots[15..20])
 $outputFile='production/review/maasil-EXPANDED-ROUGH-INCOMPLETE-v4.mp4'
}
if($IncludeV5Selects){
 $shots=@($shots[0..17])+(,@('MT06-seated-side-take01.mp4',3,9))+@($shots[18..21])
 $outputFile='production/review/maasil-EXPANDED-ROUGH-INCOMPLETE-v5.mp4'
}
$label="drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='EXPANDED ROUGH CUT - INCOMPLETE':fontsize=21:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=24,drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='Independent montage - provisional musical timing':fontsize=18:fontcolor=white:box=1:boxcolor=black@0.7:x=24:y=55"
 $ffArgs=@('-hide_banner','-loglevel','warning','-y')
$filters=@()
$labels=''
$frames=0
for($i=0;$i -lt $shots.Count;$i++){
 $shot=$shots[$i]
 $ffArgs+=@('-i',"production/candidates/maasil/$($shot[0])")
 $startFrame=[int][math]::Ceiling([double]$shot[1]*24)
 $endFrame=[int][math]::Ceiling([double]$shot[2]*24)
 $frames+=$endFrame-$startFrame
 $filters+="[$($i):v]trim=start_frame=${startFrame}:end_frame=${endFrame},setpts=PTS-STARTPTS,fps=24,setsar=1,$label[v$i]"
 $labels+="[v$i]"
}
$duration=$frames/24.0
$ffArgs+=@('-i','source/youtube/cKyT1Cv7zEA-மாசில் வீணையும்.m4a')
$filters+="${labels}concat=n=$($shots.Count):v=1:a=0[v]"
$filters+="[$($shots.Count):a]atrim=start=0:duration=$duration,asetpts=PTS-STARTPTS[a]"
$ffArgs+=@('-filter_complex',($filters -join ';'),'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',$outputFile)
& $ffmpegExe @ffArgs
if($LASTEXITCODE -ne 0){throw 'Expanded rough cut encode failed'}
Write-Output "Frames=$frames; duration=$duration"
