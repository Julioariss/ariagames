import subprocess, os, math, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from textfx import textfx
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = os.path.expanduser('~/Documents/Claude/Projects/ariagames')
S = R + '/content/2026-10-16/sim'
CH = R + '/content/2026-10-16/chars'
V = S + '/v4'
os.makedirs(V, exist_ok=True)
FB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
W, H = 1080, 1920
def font(s): return ImageFont.truetype(FB, s)
def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode:
        print(cmd, '\n', r.stderr[-2000:]); raise SystemExit(1)

keys = ['chispa', 'cosmo', 'tuerca', 'migas', 'brasita', 'bruno', 'remi', 'ada', 'hazel', 'kodiak']
names = ['BLAZE', 'COSMO', 'SPROCKET', 'PIP', 'EMBER', 'BRUNO', 'REMY', 'ADA', 'HAZEL', 'KODIAK']
tags = ['The fox', 'The otter', 'The hedgehog', 'The penguin', 'The dragon', 'The koala', 'The octopus', 'The cat', 'The squirrel', 'The bear']
cols = [((255, 120, 20), (120, 20, 10)), ((40, 170, 255), (10, 40, 120)), ((150, 150, 175), (35, 35, 55)),
        ((255, 215, 60), (20, 30, 90)), ((255, 70, 50), (90, 10, 30)), ((70, 190, 100), (10, 70, 40)),
        ((190, 90, 255), (50, 15, 110)), ((40, 210, 190), (10, 70, 80)), ((255, 160, 40), (110, 50, 10)),
        ((90, 140, 255), (20, 30, 100))]
SEG, T0 = 2.4, 10.0
GW, GH = 700, 853
GX, GY = (W - GW) // 2, 885

def txt(d, t, cx, y, s, fill=(255, 255, 255), stroke=6):
    yel = fill[2] < 200
    top, bot = ((255, 245, 130), (255, 150, 30)) if yel else ((255, 255, 255), (185, 215, 255))
    textfx(d._image, t, cx, y, s, top, bot, ext=max(2, s // 12))

def bg(i):
    import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))) if '__file__' in globals() else None
    import bgart
    p=f'{V}/bg{i}.png'; bgart.scene(i).save(p); return p

def frame(i):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((GX - 12, GY - 12, GX + GW + 12, GY + GH + 12), 70, outline=(255, 255, 255, 255), width=12)
    txt(d, 'KART WATCH GP', W // 2, 55, 62, (255, 235, 150))
    txt(d, names[i], W // 2, 1735, 100, (255, 255, 255), 8)
    f = font(36); tt = tags[i] + ' · Apple Watch'; w = d.textlength(tt, font=f)
    d.text((W / 2 - w / 2, 1862), tt, font=f, fill=(255, 235, 150, 255), stroke_width=5, stroke_fill=(25, 10, 70, 255))
    p = f'{V}/fr{i}.png'; im.save(p); return p

def mask():
    m = Image.new('L', (GW, GH), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, GW - 1, GH - 1), 58, fill=255)
    p = f'{V}/mask.png'; m.save(p); return p

def charimg(i):
    im = Image.open(f'{CH}/{keys[i]}_front.png').convert('RGBA')
    im = im.resize((1040, int(380 * 1040 / 530)), Image.LANCZOS)
    # white outline sticker effect
    a = im.split()[3].filter(ImageFilter.MaxFilter(9))
    out = Image.new('RGBA', im.size, (255, 255, 255, 0)); out.putalpha(a)
    wh = Image.new('RGBA', im.size, (255, 255, 255, 255)); wh.putalpha(a)
    sh_ = Image.new('RGBA', im.size, (0, 0, 0, 120)); sh_.putalpha(a.filter(ImageFilter.GaussianBlur(14)))
    base = Image.new('RGBA', (im.width + 40, im.height + 40), (0, 0, 0, 0))
    base.alpha_composite(sh_, (20, 34)); base.alpha_composite(wh, (20, 20)); base.alpha_composite(im, (20, 20))
    p = f'{V}/ch{i}.png'; base.save(p); return p, base.size

def intro():
    import bgart
    im = bgart.scene(2).convert('RGBA')
    for i, k in enumerate(keys):
        c = Image.open(f'{CH}/{k}_front.png').convert('RGBA').resize((460, 330), Image.LANCZOS)
        a_ = c.split()[3].filter(ImageFilter.MaxFilter(9))
        wh = Image.new('RGBA', c.size, (255, 255, 255, 255)); wh.putalpha(a_)
        shd = Image.new('RGBA', c.size, (0, 0, 0, 130)); shd.putalpha(a_.filter(ImageFilter.GaussianBlur(10)))
        x = 40 + (i % 2) * 540 + (0 if i % 4 < 2 else 0); y = 400 + (i // 2) * 270
        im.alpha_composite(shd, (x + 6, y + 14)); im.alpha_composite(wh, (x, y)); im.alpha_composite(c, (x, y))
    d = ImageDraw.Draw(im)
    textfx(im, '10 RACERS.', W // 2, 45, 135, (255, 255, 255), (185, 215, 255), ext=12)
    textfx(im, 'ONE WRIST.', W // 2, 205, 135, (255, 245, 130), (255, 150, 30), ext=12)
    p = f'{V}/intro.png'; im.convert('RGB').save(p); return p

def endcard():
    import bgart
    im = bgart.scene(2).convert('RGBA')
    for i, k in enumerate(keys):
        c = Image.open(f'{CH}/{k}_front.png').convert('RGBA').resize((212, 152), Image.LANCZOS)
        im.alpha_composite(c, (24 + (i % 5) * 206, 1560 + (i // 5) * 150))
    d = ImageDraw.Draw(im)
    ic = Image.open(f'{R}/img/kart.png').convert('RGBA').resize((300, 300))
    m = Image.new('L', (300, 300), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 299, 299), 68, fill=255)
    im.paste(ic, ((W - 300) // 2, 120), m)
    textfx(im, 'KART WATCH GP', W // 2, 450, 120, (255, 245, 130), (255, 150, 30), ext=12)
    textfx(im, '10 RACERS. 16 TRACKS.', W // 2, 650, 62, (255, 255, 255), (185, 215, 255), ext=6)
    textfx(im, 'APPLE WATCH ONLY', W // 2, 780, 80, (255, 255, 255), (185, 215, 255), ext=8)
    textfx(im, 'US$1.99 · NO ADS', W // 2, 900, 72, (255, 245, 130), (255, 150, 30), ext=8)
    d.rounded_rectangle((170, 1060, 910, 1210), 45, fill=(255, 255, 255), outline=(25, 10, 70), width=8)
    f = font(54); t = 'Get it on the App Store'; w = d.textlength(t, font=f)
    d.text(((W - w) / 2, 1105), t, font=f, fill=(10, 10, 20))
    textfx(im, 'ariagames.dev', W // 2, 1290, 70, (255, 255, 255), (185, 215, 255), ext=7)
    textfx(im, '@ariagames.app', W // 2, 1410, 52, (255, 255, 255), (185, 215, 255), ext=5)
    p = f'{V}/end.png'; im.convert('RGB').save(p); return p

mk = mask()
segs = []
# intro 2.4 s
ip = intro()
sh(f'ffmpeg -y -v error -loop 1 -t 2.4 -i {ip} -vf "fps=30,zoompan=z=\'1+0.0006*on\':d=1:s=1080x1920:fps=30,format=yuv420p" -c:v libx264 -crf 18 {V}/segintro.mp4')
segs.append(f'{V}/segintro.mp4')
for i in range(10):
    b = bg(i); fr = frame(i); cp, (cw, chh) = charimg(i)
    ytop = 120
    if i % 2 == 0:
        xexpr = f"if(lt(t,0.3),-w+(t/0.3)*((W-w)/2+w),(W-w)/2)"
    else:
        xexpr = f"if(lt(t,0.3),W-(t/0.3)*(W-(W-w)/2),(W-w)/2)"
    yexpr = f"{ytop}+if(lt(t,0.3),0,4*sin((t-0.3)*9))"
    sh(f'ffmpeg -y -v error -loop 1 -t {SEG} -i {b} -ss {T0} -t {SEG} -i {S}/clips/c{i}.mp4 -loop 1 -t {SEG} -i {fr} -loop 1 -t {SEG} -i {cp} -loop 1 -t {SEG} -i {mk} -filter_complex '
       f'"[1:v]scale={GW}:{GH}:flags=lanczos,format=yuva420p[g];[4:v]format=gray[m];[g][m]alphamerge[gm];'
       f'[0:v][gm]overlay={GX}:{GY}[a];[a][2:v]overlay=0:0[b2];[b2][3:v]overlay=x=\'{xexpr}\':y=\'{yexpr}\',fps=30,format=yuv420p[v]" '
       f'-map "[v]" -an -t {SEG} -c:v libx264 -crf 18 {V}/seg{i}.mp4')
    segs.append(f'{V}/seg{i}.mp4')
ep = endcard()
sh(f'ffmpeg -y -v error -loop 1 -t 3.5 -i {ep} -vf "fps=30,format=yuv420p" -c:v libx264 -crf 18 {V}/segend.mp4')
segs.append(f'{V}/segend.mp4')
open(V + '/list.txt', 'w').write(''.join(f"file '{p}'\n" for p in segs))
sh(f'ffmpeg -y -v error -f concat -safe 0 -i {V}/list.txt -c copy {V}/silent.mp4')
total = 2.4 + SEG * 10 + 3.5
A = os.path.expanduser('~/Developer/ZipZapKarts/Sources/Assets.xcassets')
sh(f'ffmpeg -y -v error -i {V}/silent.mp4 -ss 15 -t {total} -i {A}/snd_track_6.dataset/track_6.m4a '
   f'-filter_complex "[1:a]afade=t=in:d=0.4,afade=t=out:st={total-1.5}:d=1.5[a]" '
   f'-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest {R}/promo/spot_kart_10racers_v4.mp4')
print('OK', total)
