import subprocess, os
from PIL import Image, ImageDraw, ImageFont
R = os.path.expanduser('~/Documents/Claude/Projects/ariagames')
G = R + '/content/2026-10-16/gem'
FB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
W, H = 1080, 1920
def font(s): return ImageFont.truetype(FB, s)

def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode:
        print(cmd, '\n', r.stderr[-1500:]); raise SystemExit(1)

def hook_png(path, lines, y=210, size=96):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for ln in lines:
        f = font(size); w = d.textlength(ln, font=f); x = (W - w) / 2
        d.text((x+4, y+5), ln, font=f, fill=(0, 0, 0, 220))
        d.text((x, y), ln, font=f, fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))
        y += int(size * 1.15)
    im.save(path)

def end_png(path, title, icon, tag, c1, c2):
    im = Image.new('RGB', (W, H))
    px = im.load()
    for y in range(H):
        t = y / H
        col = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        for x in range(W): px[x, y] = col
    d = ImageDraw.Draw(im)
    def c(txt, y, s, col=(255, 255, 255)):
        f = font(s); w = d.textlength(txt, font=f)
        d.text(((W - w) / 2, y), txt, font=f, fill=col)
    ic = Image.open(f'{R}/img/{icon}.png').convert('RGBA').resize((360, 360))
    m = Image.new('L', (360, 360), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, 359, 359), 80, fill=255)
    im.paste(ic, ((W - 360) // 2, 260), m)
    c(title, 680, 110)
    c(tag, 820, 50, (255, 226, 140))
    c('Apple Watch only', 960, 76)
    c('US$1.99  ·  No ads', 1070, 64, (255, 226, 140))
    d.rounded_rectangle((190, 1230, 890, 1370), 40, fill=(255, 255, 255))
    f = font(52); t = 'Get it on the App Store'; w = d.textlength(t, font=f)
    d.text(((W - w) / 2, 1275), t, font=f, fill=(10, 10, 20))
    c('ariagames.dev', 1470, 64)
    c('@ariagames.app', 1570, 46, (210, 210, 230))
    im.save(path)

def build(name, src, hook_lines, title, icon, tag, c1, c2, music, mstart, out):
    hp, ep = f'{G}/{name}_hook.png', f'{G}/{name}_end.png'
    hook_png(hp, hook_lines); end_png(ep, title, icon, tag, c1, c2)
    sh(f'ffmpeg -y -v error -i {src} -i {hp} -filter_complex '
       f'"[0:v]scale=1080:1920:flags=lanczos,setsar=1,fps=30[b];'
       f'[b][1:v]overlay=0:0:enable=\'between(t,0.3,3.5)\',format=yuv420p[v]" '
       f'-map "[v]" -an -c:v libx264 -crf 17 -preset medium {G}/{name}_a.mp4')
    sh(f'ffmpeg -y -v error -loop 1 -t 3.5 -i {ep} -vf "fps=30,format=yuv420p" -c:v libx264 -crf 17 {G}/{name}_b.mp4')
    open(f'{G}/{name}_list.txt', 'w').write(f"file '{G}/{name}_a.mp4'\nfile '{G}/{name}_b.mp4'\n")
    sh(f'ffmpeg -y -v error -f concat -safe 0 -i {G}/{name}_list.txt -c copy {G}/{name}_silent.mp4')
    total = 13.5
    sh(f'ffmpeg -y -v error -i {G}/{name}_silent.mp4 -ss {mstart} -t {total} -i {R}/music/{music} '
       f'-filter_complex "[1:a]afade=t=in:d=0.4,afade=t=out:st={total-1.5}:d=1.5[a]" '
       f'-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest {R}/promo/{out}')

build('staracce', f'{G}/staracce_gem.mp4', ['YOUR WRIST.', 'YOUR STARFIGHTER.'],
      'Star Ace', 'staracce', 'Space dogfights on Apple Watch', (8, 14, 40), (20, 60, 110),
      'starwing-menu.m4a', 8, 'spot_staracce_en.mp4')
build('poppy', f'{G}/poppy_gem.mp4', ['A GARDEN', 'ON YOUR WRIST'],
      'Poppy Pop', 'petalpop', 'Match. Pop. Beat the bosses.', (70, 40, 120), (230, 140, 190),
      'petalpop-menu.m4a', 5, 'spot_poppypop_en.mp4')
print('OK')
