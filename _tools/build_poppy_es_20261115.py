import os, sys
# Uso: build_poppy_es_20261115.py <clip1.mp4> <clip2.mp4> <musica.mp3>
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_v3_20261024.py')).read()
exec(src[:src.index("import glob")])
O = f'{R}/content/2026-11-15/work'; os.makedirs(O, exist_ok=True)
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
    im.paste(ic, (330, 380), m)
    c('Poppy Pop', 860, 96); c('GRATIS · Compra dentro de la app', 1010, 50, (255,225,120))
    c('iPhone + iPad + Apple Watch', 1100, 56)
    d.rounded_rectangle((190,1230,890,1380), 45, fill=(255,255,255))
    c('ariagames.dev/go', 1275, 60, (10,10,20))
    c('ARIAgames', 1560, 48, (210,210,230))
    p = f'{O}/{name}.png'; im.save(p); return p

segs = [intro('p15_h', ['Une. Explota.', 'Encadena.'])]
cuts = [(A1, 0.3, 3.2, 'Un mundo mágico'), (A1, 4.6, 3.0, 'Flores que brillan'),
        (A2, 0.3, 3.2, 'Aventura de 50 capítulos'), (A2, 4.6, 2.8, '10 mundos por explorar')]
for i, (a, ss, t, cap) in enumerate(cuts):
    segs.append(f'{O}/p15_a{i}.mp4'); clip_seg(segs[-1], a, ss, t, txt(f'p15_t{i}', [cap], 1330, 76))
    if i == 1:
        f, gss, gt = 'n_s12.mov', 3.0, 'Gameplay real'
        segs.append(f'{O}/p15_g0.mp4'); game_seg(segs[-1], f'{EP}/{f}', gss, 2.2, txt('p15_gt0', [gt], 1620, 84))
    if i == 3:
        segs.append(f'{O}/p15_g1.mp4'); game_seg(segs[-1], f'{EP}/n_boss.mov', 10.0, 2.2, txt('p15_gt1', ['Vence a los jefes'], 1620, 84))
e = endcard_es('p15_end')
segs.append(f'{O}/p15_e.mp4'); still_seg(segs[-1], e, 3.2, framed=False)
finish(segs, MUSIC, 0, f'{R}/content/2026-11-15/daily_20261115_poppypop_es.mp4')
