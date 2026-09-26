"""Numerical energy evidence only; does not infer lyrics, beats or emotion."""
import subprocess
import numpy as np

ffmpeg = r'C:\Users\Shishyan\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
source = 'source/youtube/cKyT1Cv7zEA-மாசில் வீணையும்.m4a'
raw = subprocess.check_output([ffmpeg, '-v', 'error', '-i', source, '-vn', '-ac', '1', '-ar', '22050', '-f', 'f32le', '-'])
samples = np.frombuffer(raw, dtype=np.float32)
sr = 22050
def db(x):
    return float(20*np.log10(max(np.sqrt(np.mean(x*x)), 1e-10)))
print('MONO DECODE SECONDS', len(samples)/sr)
print('TEN SECOND RMS dBFS (mono; not LUFS)')
for start in range(0, int(len(samples)/sr), 10):
    segment = samples[start*sr:min((start+10)*sr,len(samples))]
    print(f'{start:6.2f} - {min(start+10,len(samples)/sr):6.2f} : {db(segment):6.2f}')
# Two-second smoothed RMS troughs: candidates to listen around, not phrase labels.
hop = sr//4
energy = np.array([db(samples[i:i+2*sr]) for i in range(0,len(samples)-2*sr,hop)])
troughs=[]
for i in range(12,len(energy)-12):
    if energy[i] == np.min(energy[i-12:i+13]):
        contrast = (float(np.max(energy[i-12:i]))+float(np.max(energy[i+1:i+13])))/2-energy[i]
        if contrast >= 2:
            troughs.append((round(i*hop/sr+1,2),round(float(energy[i]),2),round(float(contrast),2)))
print('LOCAL TWO-SECOND ENERGY TROUGHS (center sec, dBFS, neighbor contrast dB)',troughs)
