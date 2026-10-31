import os, sys
s = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_launch_20261031.py')).read()
exec(s[:s.index("ART = f'{PP}")])          # helpers: txt, endcard, sh, still_seg, finish, devices_seg, phone_seg, frame_png...
O = f'{R}/content/2026-10-31/work3'; os.makedirs(O, exist_ok=True)
frame_png(f'{O}/f_phone.png', PH_W, PH_H, 62, PH_BZ, PH_BZ, 48, island=True)
frame_png(f'{O}/f_watch.png', WT_W, WT_H, 66, 14, 14, 52)
Image.new('RGBA', (WT_W-80, 150), (30, 30, 38, 255)).save(f'{O}/f_band.png')
DL = os.path.expanduser('~/Downloads')
MUSIC = sys.argv[1] if len(sys.argv) > 1 else f'{DL}/Banners_Over_the_Peak.mp3'
FPS = 30
GRADE = "eq=contrast=1.10:saturation=1.22:gamma=0.96,colorbalance=rs=.04:bs=-.04:rh=.05:bh=-.03,vignette=PI/5,noise=alls=7:allf=t"

def fadetxt(i, dur, d_in=0.18):
    return f"[{i}:v]format=rgba,fade=t=in:st={d_in}:d=0.22:alpha=1,fade=t=out:st={dur-0.2}:d=0.18:alpha=1[tx]"

def vclip(out, src, ss, dur, overlay, zoom=0.12, rev=False):
    """cinematic shot: cover-crop, slow push-in, grade, flash-in, animated text."""
    n = int(dur*FPS)
    vf = (f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          f"zoompan=z='1.0+{zoom}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS},{GRADE},fade=t=in:st=0:d=0.12:color=white")
    fc = f"[0:v]{vf}[b];{fadetxt(1, dur)};[b][tx]overlay=0:0[o]"
    sh(f'ffmpeg -v error -y -ss {ss} -t {dur} -i "{src}" -loop 1 -t {dur} -i {overlay} -filter_complex "{fc}" -map "[o]" -r {FPS} -t {dur} -pix_fmt yuv420p -an "{out}"')

def phone_scene(out, mov, ss, dur, bgsrc, bgss, overlay, tilt=0):
    """blurred cinematic backdrop + floating iPhone with live gameplay."""
    n = int(dur*FPS); pw, ph = PH_W+90, PH_H+190
    bez = PH_BZ+4
    fc = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=22:4,eq=brightness=0.03:saturation=1.3,{GRADE},fade=t=in:st=0:d=0.12:color=white[bg];"
          f"[1:v]scale={pw-2*bez}:{ph-2*bez}:force_original_aspect_ratio=increase,crop={pw-2*bez}:{ph-2*bez}[sc];"
          f"[3:v]scale={pw}:{ph}[fr];"
          f"[bg][sc]overlay=(W-{pw})/2+{bez}:'330+{bez}+22*sin(t*2.2)+70*max(0,1-t/0.45)*max(0,1-t/0.45)'[a];"
          f"[a][fr]overlay=(W-{pw})/2:'330+22*sin(t*2.2)+70*max(0,1-t/0.45)*max(0,1-t/0.45)'[b];{fadetxt(2, dur)};[b][tx]overlay=0:0[o]")
    sh(f'ffmpeg -v error -y -ss {bgss} -t {dur} -i "{bgsrc}" -ss {ss} -t {dur} -i "{mov}" -loop 1 -t {dur} -i {overlay} -loop 1 -t {dur} -i {O}/f_phone.png '
       f'-filter_complex "{fc}" -map "[o]" -r {FPS} -t {dur} -pix_fmt yuv420p -an "{out}"')

def title_card(out, dur, overlay, bg=None):
    fc = f"[0:v]{'' if not bg else ''}null[b];{fadetxt(1, dur, 0.25)};[b][tx]overlay=0:0[o]"
    sh(f'ffmpeg -v error -y -f lavfi -t {dur} -i "color=c=0x07050f:s=1080x1920:r={FPS}" -loop 1 -t {dur} -i {overlay} -filter_complex "{fc}" -map "[o]" -t {dur} -pix_fmt yuv420p -an "{out}"')

G = f'{DL}/gemini_generated_video'
sh(f'ffmpeg -v error -y -ss 4 -i {G}_e66d4925.mp4 -frames:v 1 {O}/bgframe.png'); BG = f'{O}/bgframe.png'
VID = f'{PP}/iOSApp/Video'; PR = f'{PP}/dist/promo'
segs = []
def add(name): p = f'{O}/{name}.mp4'; segs.append(p); return p

title_card(add('t0'), 1.7, txt('T0', ['ARIAGAMES', 'presents'], 880, 84))
vclip(add('s1'), f'{G}_3f9505e7.mp4', 0.5, 2.6, txt('T1', ['Once, a garden', 'bloomed.'], 1450, 92), zoom=0.14)
vclip(add('s2'), f'{VID}/vid_intro.mp4', 0.3, 2.2, txt('T2', ['Then the sun', 'went dark.'], 1450, 92), zoom=0.16)
vclip(add('s3'), f'{G}_e66d4925.mp4', 3.0, 1.9, txt('T3', ['One girl.'], 1500, 110), zoom=0.12)
phone_scene(add('p1'), f'{PR}/r_dlg.mov', 0.5, 2.2, f'{VID}/vid_intro.mp4', 2.0, txt('T4', ['A STORY.'], 200, 120))
vclip(add('s4'), f'{G}_86e07736.mp4', 1.0, 1.7, txt('T5', ['Strange friends.'], 1500, 90), zoom=0.12)
vclip(add('s5'), f'{VID}/vid_boss14.mp4', 0.5, 1.5, txt('T6', ['Fierce rivals.'], 1500, 96), zoom=0.12)
phone_scene(add('p2'), f'{PR}/r_versus.mov', 1.0, 2.4, f'{VID}/vid_boss14.mp4', 2.0, txt('T7', ['DUEL MODE.'], 200, 120))
vclip(add('s6'), f'{VID}/vid_boss9.mp4', 0.8, 1.5, txt('T8', ['Dark bosses.'], 1500, 96), zoom=0.12)
phone_scene(add('p3'), f'{PR}/r_fuzz.mov', 1.0, 2.4, f'{G}_5d541b5f.mp4', 3.0, txt('T9', ['FEVER CHAINS.'], 200, 120))
vclip(add('s7'), f'{G}_5d541b5f.mp4', 3.5, 1.9, txt('T10', ['One final Eclipse.'], 1500, 88), zoom=0.12)
phone_scene(add('p4'), f'{PR}/r_endless.mov', 3.0, 2.2, f'{G}_e66d4925.mp4', 1.0, txt('T11', ['ENDLESS MODE.'], 200, 120))
devices_seg(add('dv'), 3.0, txt('T12', ['iPhone  ·  iPad', '+ Apple Watch'], 200, 96))
title_card(add('t1'), 1.3, txt('T13', ['POPPY POP'], 880, 150))
e = endcard('T_end', 'Poppy Pop', 'poppypop.png', '+ iPhone & iPad', (190, 90, 170))
still_seg(add('e'), e, 3.0, framed=False)
finish(segs, MUSIC, 22, f'{R}/promo/trailer_20261031_poppypop_en.mp4')
