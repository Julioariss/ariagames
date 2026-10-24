import os, sys, subprocess, wave
import numpy as np
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_daily_gem_20261024.py')).read()
exec(src[:src.index("which = sys.argv[1]")])   # reuse helpers: txt, endcard, sh, clip_seg, intro, R, O, W, H
EP = f'{R}/content/2026-10-16/sim/clips'
ANIME = sys.argv[1] if len(sys.argv) > 1 else f'{R}/content/2026-10-24/gem/kart_gem1.mp4'

def game_seg(out, mov, ss, dur, overlay):
    fc = ("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:6,eq=brightness=-0.2[bg];"
          "[b]scale=980:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-80[c];[c][1:v]overlay=0:0[o]")
    sh(f'ffmpeg -v error -y -ss {ss} -t {dur} -i "{mov}" -i {overlay} -filter_complex "{fc}" -map "[o]" -r 30 -pix_fmt yuv420p -an "{out}"')

def end_anim(out, img, dur):
    sh(f'ffmpeg -v error -y -loop 1 -t {dur} -i "{img}" -vf "zoompan=z=\'1+0.04*sin(on/6)\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d=1:s=1080x1920:fps=30" -pix_fmt yuv420p -an "{out}"')

segs = [intro('kt2_h', ['POV: your wrist','is a racetrack'])]
for i, (f, ss, t) in enumerate([('c0.mp4', 2.0, 'Meet Blaze'), ('c0.mp4', 11.0, 'Race 8 drivers')]):
    segs.append(f'{O}/kt2_a{i}.mp4')
    game_seg(segs[-1], f'{EP}/{f}', ss, 2.4, txt(f'kt2_t{i}', [t], 1620, 84))
G = [('c0.mp4', 6.0, 'Drift every corner'), ('c5.mp4', 9.0, 'Grab power-ups'), ('c9.mp4', 11.0, 'Win the cup')]
for i, (f, ss, t) in enumerate(G):
    segs.append(f'{O}/kt2_g{i}.mp4')
    game_seg(segs[-1], f'{EP}/{f}', ss, 2.0, txt(f'kt2_gt{i}', [t], 1620, 84))
e = endcard('kt2_end', 'Kart Watch GP', 'kart.png', 'Series 10+', (200, 40, 40))
segs.append(f'{O}/kt2_e.mp4'); end_anim(segs[-1], e, 2.5)
lst = f'{O}/l2.txt'; open(lst, 'w').write(''.join(f"file '{s}'\n" for s in segs))
sh(f'ffmpeg -v error -y -f concat -safe 0 -i {lst} -c copy {O}/cat2.mp4')
dur = float(subprocess.check_output(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {O}/cat2.mp4', shell=True))

# original synthesized music: bright pentatonic marimba arpeggio + bass + hats, with pop SFX at gameplay cuts
SR = 44100; n = int(SR*dur); t = np.arange(n)/SR; out = np.zeros(n)
bpm = 150; beat = 60/bpm; scale = [220.0, 246.9, 277.2, 329.6, 370.0, 440.0, 493.9, 554.4, 659.3]
chords = [[0,2,4],[3,5,7],[4,6,8],[2,4,6]]
def bell(f, t0, d, a=0.22):
    m = (t >= t0) & (t < t0+d); tt = t[m]-t0
    out[m] += a*(np.sin(2*np.pi*f*tt)+0.35*np.sin(2*np.pi*f*2.01*tt)+0.12*np.sin(2*np.pi*f*3.99*tt))*np.exp(-tt*7)
step = beat/2; k = 0; ts = 0.0
while ts < dur:
    ch = chords[(k//16) % 4]; note = scale[ch[[0,1,2,1][k % 4]] % 9]*(2 if k % 8 >= 4 else 1)
    bell(note, ts, 0.5); ts += step; k += 1
for b in range(int(dur/beat)+1):
    tb = b*beat; r = chords[(int(tb/(beat*4))) % 4][0]; f = scale[r]/4
    m = (t >= tb) & (t < tb+beat*0.9); tt = t[m]-tb
    out[m] += 0.28*np.sin(2*np.pi*f*tt)*np.exp(-tt*3.5)
    h = (t >= tb+beat/2) & (t < tb+beat/2+0.05); out[h] += 0.05*np.random.randn(h.sum())*np.exp(-(t[h]-tb-beat/2)*80)
    kk = (t >= tb) & (t < tb+0.12); out[kk] += 0.35*np.sin(2*np.pi*(90*np.exp(-(t[kk]-tb)*25)+40)*(t[kk]-tb))*np.exp(-(t[kk]-tb)*20)
cuts = [2.4+4.8 + 2.0*i for i in range(3)]
for c in cuts:
    m = (t >= c) & (t < c+0.25); tt = t[m]-c
    out[m] += 0.45*np.sin(2*np.pi*(900*np.exp(-tt*14)+300)*tt)*np.exp(-tt*16)
out *= 1.0/np.max(np.abs(out)); out *= 1.0
fade = np.minimum(1, np.minimum(t/0.3, (dur-t)/0.6)); out *= fade
wav = f'{O}/kt2_music.wav'
w = wave.open(wav, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
fin = f'{R}/promo/daily_20261024_kartwatchgp_en.mp4'
sh(f'ffmpeg -v error -y -i {O}/cat2.mp4 -i {wav} -filter_complex "[0:v]fade=t=in:d=0.3,fade=t=out:st={dur-0.5}:d=0.5[v]" -map "[v]" -map 1:a -c:v libx264 -preset veryfast -crf 24 -c:a aac -b:a 160k -shortest -movflags +faststart {fin}')
print(fin, dur, os.path.getsize(fin)/1e6, 'MB')
