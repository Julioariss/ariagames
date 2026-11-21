import os, sys
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_daily_gem_20261024.py')).read()
exec(src[:src.index("which = sys.argv[1]")])
O = f'{R}/content/2026-11-21/work/b'; os.makedirs(O, exist_ok=True)
A = f'{R}/content/2026-11-21/gem/pip_a.mp4'
GP = f'{R}/content/2026-11-21/work/pip_gameplay.mp4'
MUSIC = os.path.expanduser('~/Downloads/Checkered_Flag_Pursuit.mp3')
def game_seg(out, mov, ss, dur, overlay):
    fc = ("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:6,eq=brightness=-0.2[bg];"
          "[b]scale=860:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-80[c];[c][1:v]overlay=0:0[o]")
    sh(f'ffmpeg -v error -y -ss {ss} -t {dur} -i "{mov}" -i {overlay} -filter_complex "{fc}" -map "[o]" -r 30 -pix_fmt yuv420p -an "{out}"')
segs = [intro('kp_h', ['Pip al volante.','Sin frenos.'])]
T = ['Pip toma la pista','Acelera en la curva','Mantén la línea']
for i,(ss,t) in enumerate([(0.4,2.6),(3.6,2.6),(6.8,2.6)]):
    segs.append(f'{O}/kp_a{i}.mp4'); clip_seg(segs[-1], A, ss, t, txt(f'kp_t{i}', [T[i]], 1330, 76))
G = [(6.0,'Juego real'),(10.0,'Derrapa y carga'),(16.0,'Gana la copa')]
for i,(ss,t) in enumerate(G):
    segs.append(f'{O}/kp_g{i}.mp4'); game_seg(segs[-1], GP, ss, 2.2, txt(f'kp_gt{i}', [t], 1620, 84))
e = endcard('kp_end','Kart Watch GP','kart.png','Series 10+',(200,50,40))
segs.append(f'{O}/kp_e.mp4'); still_seg(segs[-1], e, 3.0, framed=False)
finish(segs, MUSIC, 0, f'{R}/content/2026-11-21/daily_20261121_kartwatchgp_es.mp4')
