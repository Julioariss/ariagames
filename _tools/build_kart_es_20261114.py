#!/usr/bin/env python3
"""Kart Watch GP reel 14-nov (ES, Chile): piloto Hazel, clips Gemini + gameplay real del reloj + musica Gemini.
Estilo: 3D tipo pelicula animada, transiciones suaves (xfade). 1080x1920, ~22 s.
Uso: build_kart_es_20261114.py <hazel1.mp4> <hazel2.mp4> <musica.mp3>"""
import os, subprocess, sys
sys.argv += [''] * 4
from PIL import Image, ImageDraw, ImageFont, ImageFilter
H = os.path.expanduser
R = H('~/Documents/Claude/Projects/ariagames')
OUT = f'{R}/content/2026-11-14/kart_es'; os.makedirs(OUT, exist_ok=True)
W, HH, FPS = 1080, 1920, 30
IMPACT = '/System/Library/Fonts/Supplemental/Impact.ttf'
DL = H('~/Downloads')
HZ1, HZ2, MUSIC = sys.argv[1], sys.argv[2], sys.argv[3]
GAME = f'{DL}/kart_watch_gp_reel.mp4'  # gameplay real del reloj (t=10.5-16.5 s)

def font(s): return ImageFont.truetype(IMPACT, s)

def text(img, t, y, size, top, bot, stroke, glow):
    f = font(size); d = ImageDraw.Draw(img)
    w = d.textlength(t, font=f); x = (W - w) / 2
    g = Image.new('RGBA', img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.text((x, y), t, font=f, fill=glow + (255,), stroke_width=14, stroke_fill=glow + (255,))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(16)))
    d.text((x, y), t, font=f, fill=stroke + (255,), stroke_width=9, stroke_fill=stroke + (255,))
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).text((x, y), t, font=f, fill=255)
    bb = m.getbbox(); grad = Image.new('RGBA', img.size, (0, 0, 0, 0)); gp = grad.load()
    if bb:
        for yy in range(bb[1], bb[3]):
            k = (yy - bb[1]) / max(1, bb[3] - bb[1])
            c = tuple(int(top[i] * (1 - k) + bot[i] * k) for i in range(3)) + (255,)
            for xx in range(bb[0], bb[2]): gp[xx, yy] = c
    img.paste(grad, (0, 0), m)

PAL = {
    'gold': ((255, 255, 220), (255, 170, 20), (70, 30, 0), (255, 150, 0)),
    'lime': ((250, 255, 220), (150, 220, 40), (20, 50, 0), (120, 220, 40)),
    'white': ((255, 255, 255), (200, 225, 255), (15, 25, 60), (90, 160, 255)),
}

def overlay(name, lines):
    img = Image.new('RGBA', (W, HH), (0, 0, 0, 0))
    for t, y, size, pal in lines: text(img, t, y, size, *PAL[pal])
    p = f'{OUT}/{name}.png'; img.save(p); return p

GRADE = 'eq=contrast=1.06:saturation=1.15,unsharp=5:5:0.5'

def clip(name, src, dur, ss, ov, mode='vert'):
    out = f'{OUT}/{name}.mp4'
    if mode == 'vert':
        base = f'[0:v]scale={W}:{HH}:force_original_aspect_ratio=increase,crop={W}:{HH},fps={FPS},{GRADE}[b]'
    else:  # gameplay del reloj sobre fondo difuminado
        base = (f'[0:v]crop=980:1120:50:280,split[a][c];[a]scale={W}:{HH}:force_original_aspect_ratio=increase,crop={W}:{HH},boxblur=30:6,eq=brightness=-0.12[bg];'
                f'[c]scale=1000:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2+30,fps={FPS},{GRADE}[b]')
    fc = f'{base};[1:v]format=rgba,fade=in:st=0.15:d=0.25:alpha=1[o];[b][o]overlay=0:0:shortest=1,format=yuv420p[v]'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(ss), '-t', str(dur), '-i', src, '-loop', '1', '-i', ov,
           '-filter_complex', fc, '-map', '[v]', '-t', str(dur), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', out]
    subprocess.run(cmd, check=True); return out

SEG = [  # (nombre, fuente, duracion, ss, overlay lines, modo)
    ('k1', HZ1, 3.2, 0.3, [('HAZEL NO FRENA', 300, 135, 'gold'), ('¿LA ALCANZAS?', 1250, 105, 'white')], 'vert'),
    ('k2', GAME, 3.1, 10.4, [('CARRERAS EN', 170, 105, 'white'), ('TU MUÑECA', 290, 125, 'gold')], 'game'),
    ('k3', HZ1, 3.2, 5.0, [('10 PILOTOS', 300, 135, 'lime'), ('¡ELIGE EL TUYO!', 1250, 100, 'white')], 'vert'),
    ('k4', HZ2, 3.0, 0.3, [('18 PISTAS', 300, 135, 'gold'), ('EN 6 COPAS', 1250, 105, 'white')], 'vert'),
    ('k5', HZ2, 2.8, 3.2, [('¡A TODO GAS!', 300, 140, 'lime')], 'vert'),
    ('k7', HZ2, 4.2, 5.8, [('GRATIS EN', 250, 110, 'white'), ('APPLE WATCH', 380, 135, 'gold'), ('ARIAGAMES.DEV/GO', 1560, 78, 'white')], 'vert'),
]
files, durs = [], []
for n, src, d, ss, lines, mode in SEG:
    f=clip(n, src, d, ss, overlay('o_' + n, lines), 'vert' if mode == 'vert' else 'game'); files.append(f); durs.append(float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout))

# crossfades suaves de 0.25 s
FD = 0.25
inp = []
for f in files: inp += ['-i', f]
chain, last, acc = '', '[0:v]', durs[0]
for i in range(1, len(files)):
    off = acc - FD
    chain += f'{last}[{i}:v]xfade=transition=fade:duration={FD}:offset={off:.3f}[x{i}];'
    last = f'[x{i}]'; acc += durs[i] - FD
chain = chain.rstrip(';')
v = f'{OUT}/video.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inp + ['-filter_complex', chain, '-map', last, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', v], check=True)
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout)
a = f'{OUT}/music.m4a'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', MUSIC, '-af', f'afade=in:d=0.1,afade=out:st={dur-1.0:.2f}:d=1.0', '-t', f'{dur:.2f}', '-c:a', 'aac', '-b:a', '192k', a], check=True)
final = f'{R}/content/2026-11-14/daily_20261114_kartwatchgp_hazel_es.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', v, '-i', a, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'veryfast', '-b:v', '2200k', '-maxrate', '2600k', '-bufsize', '4400k', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', final], check=True)
print('OK', final, dur, os.path.getsize(final))
