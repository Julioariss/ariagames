#!/usr/bin/env python3
"""STAR Ace reel 11-nov (rehecho): estilo juego de acción de los 90 (tarjetas WARNING de jefe, texto metálico),
clips Gemini fieles al juego + gameplay real + música Gemini rock/synth. 1080x1920, ~30 s."""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
H = os.path.expanduser
R = H('~/Documents/Claude/Projects/ariagames')
OUT = f'{R}/content/2026-11-11/rehecho_es'; os.makedirs(OUT, exist_ok=True)
W, HH, FPS = 1080, 1920, 30
IMPACT = '/System/Library/Fonts/Supplemental/Impact.ttf'
DL = H('~/Downloads')
COSMO = f'{DL}/gemini_generated_video_5615bb96.mp4'
DEVOUR = f'{DL}/gemini_generated_video_883e85e3.mp4'
SHIP = sys.argv[1] if len(sys.argv) > 1 else None
SIM = f'{R}/content/2026-11-06/sim'
ASSETS = H('~/Developer/NovaStrike/Sources/Assets.xcassets')
MUSIC = f'{DL}/Final_Vector_Locked.mp3'

def asset(n):
    import glob
    return sorted(glob.glob(f'{ASSETS}/{n}.imageset/*.*g'))[0]

def font(s): return ImageFont.truetype(IMPACT, s)

def metal_text(img, text, y, size, top=(255, 255, 255), bot=(90, 200, 255), stroke=(10, 20, 60), glow=(60, 160, 255)):
    """Texto estilo arcade 90s: degradado metálico vertical, borde oscuro grueso y resplandor."""
    f = font(size)
    d = ImageDraw.Draw(img)
    w = d.textlength(text, font=f)
    x = (W - w) / 2
    # glow
    g = Image.new('RGBA', img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.text((x, y), text, font=f, fill=glow + (255,), stroke_width=14, stroke_fill=glow + (255,))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(18)))
    # stroke
    d.text((x, y), text, font=f, fill=stroke + (255,), stroke_width=10, stroke_fill=stroke + (255,))
    # gradient fill through mask
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).text((x, y), text, font=f, fill=255)
    bbox = m.getbbox()
    grad = Image.new('RGBA', img.size, (0, 0, 0, 0)); gp = grad.load()
    if bbox:
        y0, y1 = bbox[1], bbox[3]
        for yy in range(y0, y1):
            t = (yy - y0) / max(1, y1 - y0)
            c = tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)) + (255,)
            for xx in range(bbox[0], bbox[2]): gp[xx, yy] = c
    img.paste(grad, (0, 0), m)

def overlay(name, lines, warn=False):
    """lines: [(text, y, size, palette)] -> PNG transparente 1080x1920."""
    img = Image.new('RGBA', (W, HH), (0, 0, 0, 0))
    if warn:
        d = ImageDraw.Draw(img)
        for yb in (330, 640):
            d.rectangle([0, yb, W, yb + 70], fill=(200, 10, 20, 230))
            for k in range(-2, 14):
                d.polygon([(k * 90, yb), (k * 90 + 45, yb), (k * 90 + 5, yb + 70), (k * 90 - 40, yb + 70)], fill=(255, 210, 0, 255))
    for text, y, size, pal in lines:
        if pal == 'red': metal_text(img, text, y, size, top=(255, 240, 200), bot=(255, 40, 30), stroke=(60, 0, 0), glow=(255, 30, 30))
        elif pal == 'gold': metal_text(img, text, y, size, top=(255, 255, 220), bot=(255, 170, 20), stroke=(60, 25, 0), glow=(255, 150, 0))
        else: metal_text(img, text, y, size)
    p = f'{OUT}/{name}.png'; img.save(p); return p

GRADE = 'eq=contrast=1.08:saturation=1.18,unsharp=5:5:0.6'

def seg(name, src, dur, ss=0, ov=None, kind='vert', flash=False, shake=False, pre0=''):
    """kind: vert (ya 9:16), land (16:9 recortado al centro), still (imagen con zoom)."""
    out = f'{OUT}/{name}.mp4'
    if kind == 'still':
        n = int(dur * FPS)
        vf = f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='1+0.18*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{HH}:fps={FPS}"
        inp = ['-i', src]
    else:
        pre = (pre0 + 'crop=ih*9/16:ih,') if kind == 'land' else ''
        vf = f'{pre}scale={W}:{HH}:force_original_aspect_ratio=increase,crop={W}:{HH},fps={FPS}'
        inp = ['-ss', str(ss), '-t', str(dur), '-i', src]
    vf += ',' + GRADE
    if shake: vf += f",crop=iw-40:ih-40:20+12*sin(t*47):20+12*cos(t*39),scale={W}:{HH}"
    if flash: vf += ",fade=in:st=0:d=0.25:color=white"
    cmd = ['ffmpeg', '-y', '-loglevel', 'error'] + inp
    if ov:
        cmd += ['-loop', '1', '-i', ov, '-filter_complex', f'[0:v]{vf}[b];[1:v]format=rgba,fade=in:st=0:d=0.18:alpha=1[o];[b][o]overlay=0:0:shortest=1,format=yuv420p[v]', '-map', '[v]']
    else:
        cmd += ['-vf', vf + ',format=yuv420p']
    cmd += ['-t', str(dur), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', out]
    subprocess.run(cmd, check=True); return out

S = []
S.append(seg('s01', COSMO, 2.6, ss=0.4, ov=overlay('o01', [('STAR ACE', 260, 210, 'blue'), ('¿LISTO?', 1240, 120, 'gold')]), flash=True))
S.append(seg('s02', f'{SIM}/s1.mov', 3.0, ss=9.0, kind='land', pre0='crop=2868:952:0:184,', ov=overlay('o02', [('VUELA. APUNTA.', 300, 120, 'blue'), ('¡FUEGO!', 440, 150, 'gold')])))
if SHIP and os.path.exists(SHIP):
    S.append(seg('s03', SHIP, 3.6, ss=1.0, ov=overlay('o03', [('HASTA 6 OBJETIVOS', 300, 110, 'blue')])))
else:
    S.append(seg('s03', COSMO, 3.6, ss=5.5, ov=overlay('o03', [('HYPERSPACE!', 300, 120, 'blue')])))
S.append(seg('s04', asset('cine_b2a'), 2.6, kind='still', ov=overlay('o04', [('ALERTA', 360, 150, 'red'), ('ZONA DE MAGMA', 1180, 140, 'gold'), ('JEFE EN CAMINO', 1330, 80, 'red')], warn=True), flash=True, shake=True))
S.append(seg('s05', f'{SIM}/boss2.mov', 3.2, ss=11.0, kind='land', ov=overlay('o05', [('5 JEFES', 280, 120, 'blue'), ('ELEMENTALES', 410, 140, 'gold')])))
S.append(seg('s06', asset('cine_b3a'), 2.2, kind='still', ov=overlay('o06', [('ALERTA', 360, 150, 'red'), ('NEBULOSA HELADA', 1180, 130, 'gold'), ('JEFE EN CAMINO', 1330, 80, 'red')], warn=True), flash=True, shake=True))
S.append(seg('s07', DEVOUR, 4.2, ss=0.8, ov=overlay('o07', [('ALERTA', 360, 150, 'red'), ('EL DEVORADOR', 1150, 130, 'gold'), ('DE MUNDOS', 1290, 110, 'red')], warn=True), shake=True))
S.append(seg('s08', asset('vsbg'), 3.4, kind='still', ov=overlay('o08', [('VERSUS Y CO-OP', 300, 115, 'blue'), ('2-4 PILOTOS', 440, 130, 'gold'), ('EN LÍNEA', 1250, 100, 'blue')]), flash=True))
S.append(seg('s09', f'{R}/img/staracce.png', 5.2, kind='still', ov=overlay('o09', [('GRATIS EN', 260, 110, 'blue'), ('IPHONE + APPLE WATCH', 390, 90, 'gold'), ('ARIAGAMES.DEV/GO', 1500, 80, 'blue')]), flash=True))

# concat with quick white-flash hard cuts (no xfade: punchy 90s cuts)
lst = f'{OUT}/list.txt'
open(lst, 'w').write(''.join(f"file '{p}'\n" for p in S))
v = f'{OUT}/video.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', v], check=True)
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout)
# music: intro (0-26.5) + big ending (57.5-62.3) crossfaded
a = f'{OUT}/music.m4a'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', MUSIC, '-filter_complex',
                '[0:a]atrim=0:26.6,asetpts=PTS-STARTPTS[a1];[0:a]atrim=57.4:62.3,asetpts=PTS-STARTPTS[a2];[a1][a2]acrossfade=d=0.9:c1=tri:c2=tri,afade=out:st=%.2f:d=0.8[m]' % (dur - 0.8),
                '-map', '[m]', '-t', str(dur), '-c:a', 'aac', '-b:a', '192k', a], check=True)
final = f'{R}/content/2026-11-13/daily_20261113_staracce_es.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', v, '-i', a, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', final], check=True)
up = f'{DL}/STARAce_reel_v2_upload.mp4'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', final, '-c:v', 'libx264', '-preset', 'veryfast', '-b:v', '2000k', '-maxrate', '2400k', '-bufsize', '4000k', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', up], check=True)
print('OK', final, dur, os.path.getsize(up))
