#!/usr/bin/env python3
"""STAR Ace reel 18-nov (EN): gancho ACE MODE. Uso: build_star_en_20261118.py <clipCosmo.mp4> <clipArmada.mp4> <musica.mp3>
Reutiliza helpers (overlay/seg) del builder 20261113."""
import os, sys, subprocess
H = os.path.expanduser
R = H('~/Documents/Claude/Projects/ariagames')
src = open(f'{R}/_tools/build_star_es_20261113.py').read().split('S = []')[0]
exec(src)
A, B, MUS = sys.argv[1], sys.argv[2], sys.argv[3]
OUT = f'{R}/content/2026-11-18/work'; os.makedirs(OUT, exist_ok=True)
SIM = f'{R}/content/2026-11-16/sim'
S = []
S.append(seg('s01', A, 2.8, ss=0.3, ov=overlay('o01', [('ACE MODE', 260, 210, 'gold'), ('UNLOCKED', 1240, 120, 'blue')]), flash=True))
S.append(seg('s02', B, 3.4, ss=0.3, ov=overlay('o02', [('ENEMY ARMADA', 300, 120, 'red'), ('INCOMING', 440, 120, 'gold')])))
S.append(seg('s03', f'{SIM}/st12.mov', 3.0, ss=12.0, kind='land', pre0='transpose=2,', ov=overlay('o03', [('REAL GAMEPLAY', 300, 110, 'blue')])))
S.append(seg('s04', f'{SIM}/devourer.mov', 4.0, ss=11.0, kind='land', pre0='transpose=2,', ov=overlay('o04', [('WARNING', 360, 150, 'red'), ('THE DEVOURER', 1150, 130, 'gold'), ('OF WORLDS', 1290, 110, 'red')], warn=True), shake=True))
S.append(seg('s05', f'{SIM}/st17.mov', 3.0, ss=11.0, kind='land', pre0='transpose=2,', ov=overlay('o05', [('BEAT HIM...', 300, 115, 'blue'), ('UNLOCK ACE MODE', 440, 100, 'gold')])))
S.append(seg('s06', f'{R}/img/staracce.png', 4.6, kind='still', ov=overlay('o06', [('FREE ON', 260, 110, 'blue'), ('IPHONE + APPLE WATCH', 390, 90, 'gold'), ('ARIAGAMES.DEV/GO', 1500, 80, 'blue')]), flash=True))
lst = f'{OUT}/list.txt'
open(lst, 'w').write(''.join(f"file '{p}'\n" for p in S))
v = f'{OUT}/video.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', v], check=True)
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout)
a = f'{OUT}/music.m4a'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', MUS, '-af', 'afade=in:d=0.3,afade=out:st=%.2f:d=1.0' % (dur - 1.0), '-t', str(dur), '-c:a', 'aac', '-b:a', '192k', a], check=True)
final = f'{R}/content/2026-11-18/daily_20261118_staracce_en.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', v, '-i', a, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', final], check=True)
up = f'{DL}/STARAce_0118_upload.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', final, '-c:v', 'libx264', '-preset', 'veryfast', '-b:v', '2000k', '-maxrate', '2400k', '-bufsize', '4000k', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', up], check=True)
print('OK', final, dur, os.path.getsize(up))
