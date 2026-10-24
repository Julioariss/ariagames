import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont
R = os.path.expanduser('~/Documents/Claude/Projects/ariagames')
D = '20261024'
O = f'{R}/content/2026-10-24/work'
os.makedirs(O, exist_ok=True)
FB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
W, H = 1080, 1920
def font(s): return ImageFont.truetype(FB, s)
def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); sys.exit(1)

def txt(name, lines, y, size=96, col=(255,255,255)):
    im = Image.new('RGBA', (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    for ln in lines:
        f = font(size); w = d.textlength(ln, font=f)
        d.text(((W-w)/2, y), ln, font=f, fill=col+(255,), stroke_width=7, stroke_fill=(0,0,0,255))
        y += int(size*1.2)
    p = f'{O}/{name}.png'; im.save(p); return p

def endcard(name, game, icon, series, col):
    im = Image.new('RGB', (W, H)); px = im.load()
    for y in range(H):
        t = y/H
        for x in range(W): px[x,y] = (int(col[0]*(1-t)+10*t), int(col[1]*(1-t)+12*t), int(col[2]*(1-t)+30*t))
    d = ImageDraw.Draw(im)
    def c(t, y, s, fc=(255,255,255)):
        f = font(s); w = d.textlength(t, font=f); d.text(((W-w)/2, y), t, font=f, fill=fc)
    ic = Image.open(f'{R}/img/{icon}').convert('RGBA').resize((420,420))
    m = Image.new('L', (420,420), 0); ImageDraw.Draw(m).rounded_rectangle((0,0,419,419), 95, fill=255)
    im.paste(ic, (330, 380), m)
    c(game, 860, 96); c('Free · In-App Purchases', 1010, 56, (255,225,120))
    c(f'Apple Watch {series}', 1100, 56)
    d.rounded_rectangle((190,1230,890,1380), 45, fill=(255,255,255))
    c('ariagames.dev/go', 1275, 60, (10,10,20))
    c('ARIAgames', 1560, 48, (210,210,230))
    p = f'{O}/{name}.png'; im.save(p); return p

def still_seg(out, img, dur, overlay=None, framed=True):
    ov = f'-i {overlay}' if overlay else ''
    if framed:
        fc = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.15[bg];"
              f"[0:v]scale=900:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-60[b]")
    else:
        fc = f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[b]"
    if overlay: fc += ";[b][1:v]overlay=0:0[o]"; last='[o]'
    else: last='[b]'
    sh(f'ffmpeg -v error -y -loop 1 -t {dur} -i "{img}" {ov} -filter_complex "{fc}" -map "{last}" -r 30 -pix_fmt yuv420p -an "{out}"')

def clip_seg(out, src, ss, dur, overlay=None):
    ov = f'-i {overlay}' if overlay else ''
    fc = "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[b]"
    last='[b]'
    if overlay: fc += ";[b][1:v]overlay=0:0[o]"; last='[o]'
    sh(f'ffmpeg -v error -y -ss {ss} -t {dur} -i "{src}" {ov} -filter_complex "{fc}" -map "{last}" -r 30 -pix_fmt yuv420p -an "{out}"')

def finish(segs, music, mss, out):
    lst = f'{O}/l.txt'; open(lst,'w').write(''.join(f"file '{s}'\n" for s in segs))
    sh(f'ffmpeg -v error -y -f concat -safe 0 -i {lst} -c copy {O}/cat.mp4')
    dur = float(subprocess.check_output(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {O}/cat.mp4', shell=True))
    sh(f'ffmpeg -v error -y -i {O}/cat.mp4 -ss {mss} -i "{music}" -filter_complex "[0:v]fade=t=in:d=0.3,fade=t=out:st={dur-0.5}:d=0.5[v];[1:a]atrim=0:{dur},afade=t=in:d=0.5,afade=t=out:st={dur-1.2}:d=1.2,volume=0.9[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 25 -preset medium -c:a aac -b:a 128k -t {dur} "{out}"')
    print(out, dur, os.path.getsize(out)/1e6, 'MB')

def intro(name, hook):
    p = txt(name, hook, 1200, 92, (255,230,120))
    out = f'{O}/{name}_i.mp4'
    sh(f'ffmpeg -v error -y -t 2.4 -i {R}/promo/intro_ariagames.mp4 -i {p} -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[b];[b][1:v]overlay=0:0" -r 30 -pix_fmt yuv420p -an {out}')
    return out

which = sys.argv[1]
if which == 'star':
    s = [intro('star_h', ['Your Apple Watch','can do THIS?'])]
    for i,(ss,t) in enumerate([(0.3,2.4),(3.2,2.4),(6.0,2.2)]):
        s.append(f'{O}/star_a{i}.mp4'); clip_seg(s[-1], f'{R}/promo/cosmo_epic5.mp4', ss, t,
            txt(f'star_t{i}', [['Meet Cosmo.','Star Ace pilot.','Dodge. Roll. Lock on.'][i]], 1330, 84))
    for i,f in enumerate(['watch_1','watch_2','watch_3']):
        s.append(f'{O}/star_g{i}.mp4'); still_seg(s[-1], f'{R}/promo/_star_work/{f}.png', 2.0,
            txt(f'star_gt{i}', [['Real gameplay','Drag to fly','Hold to lock on'][i]], 1560, 80))
    e = endcard('star_end', 'STAR Ace', 'staracce.png', 'Series 10+', (40,50,140))
    s.append(f'{O}/star_e.mp4'); still_seg(s[-1], e, 3.0, framed=False)
    finish(s, f'{R}/music/novastrike-bgm3.m4a', 0, f'{R}/promo/daily_{D}_staracce_en.mp4')
else:
    P = os.path.expanduser('~/Developer/PetalPop/shots')
    s = [intro('pp_h', ['Match. Pop. Chain.','in 10 seconds'])]
    ic = f'{R}/img/petalpop.png'
    s.append(f'{O}/pp_a.mp4'); still_seg(s[-1], ic, 3.0, txt('pp_t0', ['Meet Daisy','& the Poppy Pop garden'], 1500, 70), framed=True)
    for i,(f,t) in enumerate([('p2.jpg',"Match 3 flowers"),('g1.png','Chain combos'),('g2.png','Beat the bosses')]):
        s.append(f'{O}/pp_g{i}.mp4'); still_seg(s[-1], f'{R}/shots/{f}' if f.startswith('p') else f'{P}/{f}', 2.4, txt(f'pp_gt{i}', [t], 1560, 84))
    e = endcard('pp_end', 'Poppy Pop', 'petalpop.png', 'Series 7+', (190,90,170))
    s.append(f'{O}/pp_e.mp4'); still_seg(s[-1], e, 3.0, framed=False)
    finish(s, f'{R}/music/petalpop-menu.m4a', 0, f'{R}/promo/daily_{D}_poppypop_en.mp4')
