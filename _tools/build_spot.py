import subprocess, os
from PIL import Image, ImageDraw, ImageFont
R = os.path.expanduser('~/Documents/Claude/Projects/ariagames')
O = R + '/content/2026-10-16/spot'
os.makedirs(O, exist_ok=True)
FB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
W, H = 1080, 1920

def font(s): return ImageFont.truetype(FB, s)

def overlay(name, lines, y, size=84, color=(255,255,255), sub=None, subsize=44):
    im = Image.new('RGBA', (W, H), (0,0,0,0))
    d = ImageDraw.Draw(im)
    yy = y
    for ln in lines:
        f = font(size)
        w = d.textlength(ln, font=f)
        x = (W - w) / 2
        d.text((x+4, yy+5), ln, font=f, fill=(0,0,0,200))
        d.text((x, yy), ln, font=f, fill=color + (255,), stroke_width=3, stroke_fill=(0,0,0,255))
        yy += int(size * 1.15)
    if sub:
        f = font(subsize)
        w = d.textlength(sub, font=f)
        d.text(((W-w)/2+3, yy+13), sub, font=f, fill=(0,0,0,200))
        d.text(((W-w)/2, yy+10), sub, font=f, fill=(255,230,120,255), stroke_width=2, stroke_fill=(0,0,0,255))
    p = f'{O}/{name}.png'
    im.save(p)
    return p

def endcard():
    im = Image.new('RGB', (W, H), (12, 14, 28))
    px = im.load()
    for y in range(H):
        t = y / H
        for x in range(0, W):
            px[x, y] = (int(20 + 60*t), int(16 + 20*t), int(48 + 70*t))
    d = ImageDraw.Draw(im)
    def c(txt, y, s, col=(255,255,255)):
        f = font(s); w = d.textlength(txt, font=f)
        d.text(((W-w)/2, y), txt, font=f, fill=col)
    c('3 GAMES.', 170, 120)
    c('1 WRIST.', 300, 120, (255, 214, 90))
    for i, n in enumerate(['petalpop', 'kart', 'staracce']):
        ic = Image.open(f'{R}/img/{n}.png').convert('RGBA').resize((280, 280))
        m = Image.new('L', (280, 280), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, 279, 279), 62, fill=255)
        im.paste(ic, (70 + i*330, 520), m)
    c('Poppy Pop  ·  Kart Watch GP  ·  Star Ace', 850, 44)
    c('Apple Watch only', 1000, 74)
    c('US$1.99 each  ·  No ads', 1100, 62, (255, 214, 90))
    d.rounded_rectangle((190, 1260, 890, 1400), 40, fill=(255, 255, 255))
    f = font(52); t = 'Get them on the App Store'; w = d.textlength(t, font=f)
    d.text(((W-w)/2, 1305), t, font=f, fill=(10, 10, 20))
    c('ariagames.dev', 1500, 64)
    c('@ariagames.app', 1600, 46, (200, 200, 220))
    im.save(f'{O}/end.png')

def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode:
        print(cmd, '\n', r.stderr[-1500:]); raise SystemExit(1)

def seg(name, src, ss, dur, ov, landscape=True):
    if landscape:
        vf = "[0:v]scale=-2:1920,crop=1080:1920:(iw-1080)/2:0,setsar=1,fps=30[b]"
    else:
        vf = "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[b]"
    sh(f'ffmpeg -y -v error -ss {ss} -t {dur} -i "{src}" -i "{ov}" -filter_complex '
       f'"{vf};[b][1:v]overlay=0:0,format=yuv420p[v]" -map "[v]" -an -r 30 -c:v libx264 -crf 18 -preset medium {O}/{name}.mp4')

hook = overlay('hook', ['YOUR WRIST', 'IS A GAME', 'CONSOLE NOW'], 1250, 100)
star = overlay('star', ['STAR ACE'], 1420, 110, sub='Space dogfights on your Apple Watch')
kart = overlay('kart', ['KART WATCH GP'], 1420, 100, sub='Race on your wrist')
pop = overlay('pop', ['POPPY POP'], 1620, 90, sub='Match. Pop. Beat the bosses.')
endcard()
seg('s0', f'{R}/promo/star_raw.mp4', 5.0, 2.0, hook)
seg('s1', f'{R}/promo/star_raw.mp4', 0.3, 5.0, star)
seg('s2', f'{R}/promo/kart_raw.mp4', 0.3, 5.5, kart)
seg('s3', f'{R}/tiktok/01_poppypop.mp4', 11.4, 9.0, pop, landscape=False)
sh(f'ffmpeg -y -v error -loop 1 -t 3.5 -i {O}/end.png -vf "fps=30,format=yuv420p" -c:v libx264 -crf 18 {O}/s4.mp4')
open(O + '/list.txt', 'w').write(''.join(f"file '{O}/s{i}.mp4'\n" for i in range(5)))
sh(f'ffmpeg -y -v error -f concat -safe 0 -i {O}/list.txt -c copy {O}/silent.mp4')
total = 2 + 5 + 5.5 + 9 + 3.5
sh(f'ffmpeg -y -v error -i {O}/silent.mp4 -ss 8 -t {total} -i {R}/music/starwing-menu.m4a '
   f'-filter_complex "[1:a]afade=t=in:d=0.5,afade=t=out:st={total-1.5}:d=1.5,volume=0.9[a]" '
   f'-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest {R}/promo/spot_3games_en.mp4')
print('OK', total)
