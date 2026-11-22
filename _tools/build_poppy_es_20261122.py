import os, sys
# Uso: build_poppy_es_20261122.py <clip1.mp4> <clip2.mp4> <musica.mp3>
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_v3_20261024.py')).read()
exec(src[:src.index("import glob")])
O = f'{R}/content/2026-11-22/work'; os.makedirs(O, exist_ok=True)
A1, A2, MUSIC = sys.argv[1], sys.argv[2], sys.argv[3]

def endcard_es(name, col=(190, 90, 170)):
    im = Image.new('RGB', (W, H)); px = im.load()
    for y in range(H):
        t = y/H
        for x in range(W): px[x,y] = (int(col[0]*(1-t)+10*t), int(col[1]*(1-t)+12*t), int(col[2]*(1-t)+30*t))
    d = ImageDraw.Draw(im)
    def c(t, y, s, fc=(255,255,255)):
        f = font(s); w = d.textlength(t, font=f); d.text(((W-w)/2, y), t, font=f, fill=fc)
    ic = Image.open(f'{R}/img/poppypop.png').convert('RGBA').resize((420,420))
    m = Image.new('L', (420,420), 0); ImageDraw.Draw(m).rounded_rectangle((0,0,419,419), 95, fill=255)
    im.paste(ic, (330, 300), m)
    c('Poppy Pop', 760, 96); c('GRATIS · Compra dentro de la app', 900, 50, (255,225,120))
    c('iPhone + iPad + Apple Watch', 985, 56)
    d.rounded_rectangle((190,1100,890,1240), 45, fill=(255,255,255))
    c('ariagames.dev/go', 1140, 60, (10,10,20))
    c('ARIAgames', 1420, 48, (210,210,230))
    p = f'{O}/{name}.png'; im.save(p); return p

hk = txt('p22_hook', ['¿Salvas el', 'jardín mágico?'], 1200, 92, (255,230,120))
segs = [f'{O}/p22_hook.mp4']; clip_seg(segs[0], A1, 0.0, 2.4, hk)
cuts = [(A1, 2.6, 3.0, 'Un bosque mágico'), (A2, 0.2, 3.0, 'Flores que explotan'),
        (A1, 5.4, 2.4, 'Une. Encadena.'), (A2, 3.6, 3.0, '10 mundos por explorar')]
def game_seg(out, mov, ss, dur, overlay):
    fc = ("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:6,eq=brightness=-0.2[bg];"
          "[b]scale=820:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:330[c];[c][1:v]overlay=0:0[o]")
    sh(f'ffmpeg -v error -y -ss {ss} -t {dur} -i "{mov}" -i {overlay} -filter_complex "{fc}" -map "[o]" -r 30 -pix_fmt yuv420p -an "{out}"')
GP = f'{R}/content/2026-11-22/work/pp_game.mov'
for i, (a, ss, t, cap) in enumerate(cuts):
    segs.append(f'{O}/p22_a{i}.mp4'); clip_seg(segs[-1], a, ss, t, txt(f'p22_t{i}', [cap], 1120, 76))
    if i == 0:
        segs.append(f'{O}/p22_g0.mp4'); game_seg(segs[-1], GP, 8.0, 2.6, txt('p22_gt0', ['Gameplay real'], 245, 84))
    if i == 2:
        segs.append(f'{O}/p22_g1.mp4'); game_seg(segs[-1], GP, 12.4, 2.6, txt('p22_gt1', ['Vence a los jefes'], 245, 84))
e = endcard_es('p22_end')
segs.append(f'{O}/p22_e.mp4'); still_seg(segs[-1], e, 3.2, framed=False)
finish(segs, MUSIC, 0, f'{R}/content/2026-11-22/daily_20261122_poppypop_es.mp4')
