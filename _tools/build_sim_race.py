import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont
R = os.path.expanduser('~/Documents/Claude/Projects/ariagames')
S = R + '/content/2026-10-16/sim'
C = S + '/clips'
FB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
W, H = 1080, 1920
def font(s): return ImageFont.truetype(FB, s)
def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode:
        print(cmd, '\n', r.stderr[-1500:]); raise SystemExit(1)

names = ['Blaze', 'Cosmo', 'Sprocket', 'Pip', 'Ember', 'Bruno', 'Remy', 'Ada', 'Hazel', 'Kodiak']
species = ['the fox', 'the otter', 'the hedgehog', 'the penguin', 'the dragon', 'the koala', 'the octopus', 'the cat', 'the squirrel', 'the bear']
SEG, T0 = 2.4, 10.0

def txt(d, t, y, s, fill=(255, 255, 255)):
    f = font(s); w = d.textlength(t, font=f); x = (W - w) / 2
    d.text((x+4, y+5), t, font=f, fill=(0, 0, 0, 220))
    d.text((x, y), t, font=f, fill=fill, stroke_width=4, stroke_fill=(0, 0, 0, 255))

def overlay(i):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if i == 0:
        txt(d, '10 RACERS.', 90, 104); txt(d, 'ONE WRIST.', 215, 104, (255, 214, 90))
    else:
        txt(d, 'KART WATCH GP', 120, 84)
    txt(d, names[i].upper(), 1640, 120, (255, 214, 90))
    txt(d, 'Race as ' + species[i], 1790, 48)
    p = f'{S}/ov{i}.png'; im.save(p); return p

def end_png():
    im = Image.new('RGB', (W, H)); px = im.load()
    for y in range(H):
        t = y / H
        for x in range(W): px[x, y] = (int(120 + 130*t), int(20 + 130*t), int(20 + 40*t))
    d = ImageDraw.Draw(im)
    def c(t, y, s, col=(255, 255, 255)):
        f = font(s); w = d.textlength(t, font=f); d.text(((W-w)/2, y), t, font=f, fill=col)
    ic = Image.open(f'{R}/img/kart.png').convert('RGBA').resize((360, 360))
    m = Image.new('L', (360, 360), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 359, 359), 80, fill=255)
    im.paste(ic, ((W-360)//2, 260), m)
    c('Kart Watch GP', 680, 104); c('10 racers. 16 tracks.', 820, 52, (255, 235, 150))
    c('Apple Watch only', 960, 76); c('US$1.99  ·  No ads', 1070, 64, (255, 235, 150))
    d.rounded_rectangle((190, 1230, 890, 1370), 40, fill=(255, 255, 255))
    f = font(52); t = 'Get it on the App Store'; w = d.textlength(t, font=f)
    d.text(((W-w)/2, 1275), t, font=f, fill=(10, 10, 20))
    c('ariagames.dev', 1470, 64); c('@ariagames.app', 1570, 46, (240, 220, 220))
    im.save(f'{S}/end.png')

segs = []
for i in range(10):
    ov = overlay(i)
    sh(f'ffmpeg -y -v error -ss {T0} -t {SEG} -i {C}/c{i}.mp4 -i {ov} -filter_complex '
       f'"[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.15[bg];'
       f'[b]scale=1000:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-40[m];[m][1:v]overlay=0:0,fps=30,format=yuv420p[v]" '
       f'-map "[v]" -an -c:v libx264 -crf 18 {S}/seg{i}.mp4')
    segs.append(f'{S}/seg{i}.mp4')
end_png()
sh(f'ffmpeg -y -v error -loop 1 -t 3.5 -i {S}/end.png -vf "fps=30,format=yuv420p" -c:v libx264 -crf 18 {S}/segend.mp4')
open(S + '/list.txt', 'w').write(''.join(f"file '{p}'\n" for p in segs + [f'{S}/segend.mp4']))
sh(f'ffmpeg -y -v error -f concat -safe 0 -i {S}/list.txt -c copy {S}/race_silent.mp4')
total = SEG * 10 + 3.5
sh(f'ffmpeg -y -v error -i {S}/race_silent.mp4 -ss 6 -t {total} -i {R}/music/kart-menu.m4a '
   f'-filter_complex "[1:a]afade=t=in:d=0.4,afade=t=out:st={total-1.5}:d=1.5[a]" '
   f'-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest {R}/promo/spot_kart_10racers_en.mp4')
print('OK', total)
