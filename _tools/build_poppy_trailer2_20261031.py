import os, sys, subprocess
s = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_launch_20261031.py')).read()
exec(s[:s.index("ART = f'{PP}")])
O = f'{R}/content/2026-10-31/work4'; os.makedirs(O, exist_ok=True)
frame_png(f'{O}/f_phone.png', PH_W, PH_H, 62, PH_BZ, PH_BZ, 48, island=True)
frame_png(f'{O}/f_watch.png', WT_W, WT_H, 66, 14, 14, 52)
Image.new('RGBA', (WT_W-80, 150), (30, 30, 38, 255)).save(f'{O}/f_band.png')
DL = os.path.expanduser('~/Downloads'); PR = f'{PP}/dist/promo'; VID = f'{PP}/iOSApp/Video'
MUSIC = os.path.expanduser('~/Downloads/Banners_Over_the_Peak.mp3')
FPS = 30; XF = 0.35
GRADE = "eq=contrast=1.08:saturation=1.20:gamma=0.97,colorbalance=rs=.03:bs=-.03:rh=.04:bh=-.02,vignette=PI/6,noise=alls=5:allf=t"
CL = dict(a=sys.argv[1], b=sys.argv[2]) if len(sys.argv) > 2 else dict(a=f'{DL}/gemini_generated_video_155de80a.mp4', b=None)

def fadetxt(i, dur, d_in=0.25):
    return f"[{i}:v]format=rgba,fade=t=in:st={d_in}:d=0.3:alpha=1,fade=t=out:st={max(dur-0.55,0.5)}:d=0.3:alpha=1[tx]"

def vclip(out, src, ss, dur, overlay, zoom=0.10):
    L = dur + XF; n = int(L*FPS)
    vf = (f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          f"zoompan=z='1.0+{zoom}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS},{GRADE}")
    fc = f"[0:v]{vf}[b];{fadetxt(1, L)};[b][tx]overlay=0:0[o]"
    sh(f'ffmpeg -v error -y -ss {ss} -t {L} -i "{src}" -loop 1 -t {L} -i {overlay} -filter_complex "{fc}" -map "[o]" -r {FPS} -t {L} -pix_fmt yuv420p -an "{out}"')

def phone_scene(out, mov, ss, dur, bgsrc, bgss, overlay):
    L = dur + XF; pw, ph = PH_W+90, PH_H+190; bez = PH_BZ+4
    fc = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=22:4,eq=brightness=0.03:saturation=1.3,{GRADE}[bg];"
          f"[1:v]scale={pw-2*bez}:{ph-2*bez}:force_original_aspect_ratio=increase,crop={pw-2*bez}:{ph-2*bez}[sc];[3:v]scale={pw}:{ph}[fr];"
          f"[bg][sc]overlay=(W-{pw})/2+{bez}:'330+{bez}+22*sin(t*2.2)+60*max(0,1-t/0.5)*max(0,1-t/0.5)'[a];"
          f"[a][fr]overlay=(W-{pw})/2:'330+22*sin(t*2.2)+60*max(0,1-t/0.5)*max(0,1-t/0.5)'[b];{fadetxt(2, L)};[b][tx]overlay=0:0[o]")
    sh(f'ffmpeg -v error -y -ss {bgss} -t {L} -i "{bgsrc}" -ss {ss} -t {L} -i "{mov}" -loop 1 -t {L} -i {overlay} -loop 1 -t {L} -i {O}/f_phone.png '
       f'-filter_complex "{fc}" -map "[o]" -r {FPS} -t {L} -pix_fmt yuv420p -an "{out}"')

def title_card(out, dur, overlay):
    L = dur + XF
    fc = f"[0:v]null[b];{fadetxt(1, L, 0.3)};[b][tx]overlay=0:0[o]"
    sh(f'ffmpeg -v error -y -f lavfi -t {L} -i "color=c=0x07050f:s=1080x1920:r={FPS}" -loop 1 -t {L} -i {overlay} -filter_complex "{fc}" -map "[o]" -t {L} -pix_fmt yuv420p -an "{out}"')

A = CL['a']; B = CL['b']
sh(f'ffmpeg -v error -y -ss 4 -i "{A}" -frames:v 1 {O}/bgframe.png')
plan = []
def add(name, d): plan.append((f'{O}/{name}.mp4', d)); return plan[-1][0]
title_card(add('t0', 1.6), 1.6, txt('T0', ['ARIAGAMES', 'presents'], 880, 84))
vclip(add('a1', 2.3), A, 0.4, 2.3, txt('T1', ['One tiny girl.'], 1500, 100))
vclip(add('a2', 2.2), f'{VID}/vid_intro.mp4', 0.3, 2.2, txt('T2', ['A world gone dark.'], 1500, 92))
phone_scene(add('p1', 2.2), f'{PR}/r_dlg.mov', 0.5, 2.2, f'{VID}/vid_intro.mp4', 2.0, txt('T3', ['A STORY.'], 200, 120))
vclip(add('a3', 2.3), A, 2.6, 2.3, txt('T4', ['Giant guardians.'], 1500, 96))
if B: vclip(add('b1', 2.4), B, 1.5, 2.4, txt('T5', ['Epic bosses.'], 1500, 100))
phone_scene(add('p2', 2.3), f'{PR}/r_versus.mov', 1.0, 2.3, A, 3.0, txt('T6', ['DUEL THE WORLD.'], 200, 110))
if B: vclip(add('b2', 2.2), B, 5.0, 2.2, txt('T7', ['Fierce rivals.'], 1500, 96))
phone_scene(add('p3', 2.4), f'{PR}/r_fuzz.mov', 1.0, 2.4, B or A, 3.0, txt('T8', ['FEVER CHAINS.'], 200, 120))
vclip(add('a4', 2.4), A, 6.2, 2.4, txt('T9', ['She never backs down.'], 1500, 84))
phone_scene(add('p4', 2.2), f'{PR}/r_endless.mov', 3.0, 2.2, A, 1.0, txt('T10', ['ENDLESS MODE.'], 200, 120))
devices_seg(add('dv', 3.0), 3.0 + XF, txt('T11', ['iPhone  ·  iPad', '+ Apple Watch'], 200, 96))
title_card(add('t1', 1.4), 1.4, txt('T12', ['POPPY POP'], 880, 150))
e = endcard('T_end', 'Poppy Pop', 'poppypop.png', '+ iPhone & iPad', (190, 90, 170))
still_seg(add('e', 3.0), e, 3.0 + XF, framed=False)

files = [p for p, _ in plan]; durs = [d for _, d in plan]
inp = ' '.join(f'-i "{f}"' for f in files)
fc = ''; prev = '[0:v]'; t = 0.0
for k in range(1, len(files)):
    t += durs[k-1]
    fc += f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={t:.3f}[x{k}];"; prev = f'[x{k}]'
total = sum(durs) + XF
OUT = f'{R}/promo/trailer2_20261031_poppypop_en.mp4'
sh(f'ffmpeg -v error -y {inp} -ss 22 -i "{MUSIC}" -filter_complex "{fc.rstrip(";")}" -map "{prev}" -map {len(files)}:a '
   f'-af "afade=t=in:st=0:d=0.8,afade=t=out:st={total-1.6:.2f}:d=1.6,volume=1.15" -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p -r {FPS} -c:a aac -b:a 192k -t {total:.2f} -movflags +faststart "{OUT}"')
print(OUT, round(total, 1))
