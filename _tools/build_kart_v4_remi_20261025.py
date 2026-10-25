import os, sys, subprocess, wave
import numpy as np
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_daily_gem_20261024.py')).read()
exec(src[:src.index("which = sys.argv[1]")])   # reuse helpers: txt, endcard, sh, clip_seg, intro, R, O, W, H
EP = os.path.expanduser('~/Developer/../Documents/Claude/Projects/ariagames/content/2026-10-16/sim/clips')
ANIME = sys.argv[1] if len(sys.argv) > 1 else f'{R}/content/2026-10-25/gem/kartwatchgp_remi.mp4'

def game_seg(out, mov, ss, dur, overlay):
    fc = ("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:6,eq=brightness=-0.2[bg];"
          "[b]scale=980:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-80[c];[c][1:v]overlay=0:0[o]")
    sh(f'ffmpeg -v error -y -ss {ss} -t {dur} -i "{mov}" -i {overlay} -filter_complex "{fc}" -map "[o]" -r 30 -pix_fmt yuv420p -an "{out}"')

def end_anim(out, img, dur):
    sh(f'ffmpeg -v error -y -loop 1 -t {dur} -i "{img}" -vf "zoompan=z=\'1+0.04*sin(on/6)\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d=1:s=1080x1920:fps=30" -pix_fmt yuv420p -an "{out}"')


import glob
MUSIC = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser('~/Downloads/Cornering_the_Sky.mp3')
segs = [intro('kt3_h', ['POV: your wrist','is a racetrack'])]
T = ['Meet Remi','Race 8 drivers','Drift every corner']
for i, (ss, t) in enumerate([(0.2, 2.2), (3.1, 2.2), (6.3, 2.2)]):
    segs.append(f'{O}/kt3_a{i}.mp4'); clip_seg(segs[-1], ANIME, ss, t, txt(f'kt3_t{i}', [T[i]], 1330, 76))
G = [('c0.mp4', 6.0, 'Real gameplay'), ('c5.mp4', 9.0, 'Grab power-ups'), ('c9.mp4', 11.0, 'Win the cup')]
for i, (f, ss, t) in enumerate(G):
    segs.append(f'{O}/kt3_g{i}.mp4'); game_seg(segs[-1], f'{EP}/{f}', ss, 2.0, txt(f'kt3_gt{i}', [t], 1620, 84))
e = endcard('kt3_end', 'Kart Watch GP', 'kart.png', 'Series 10+', (200, 50, 40))
segs.append(f'{O}/kt3_e.mp4'); still_seg(segs[-1], e, 3.0, framed=False)
finish(segs, MUSIC, 0, f'{R}/promo/daily_20261025_kartwatchgp_en.mp4')
