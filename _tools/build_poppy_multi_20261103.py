import os, sys, subprocess
s = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_launch_20261031.py')).read()
exec(s[:s.index("ART = f'{PP}")])
O = f'{R}/content/2026-10-31/work4'; O=f'{R}/content/2026-11-03/multi'; os.makedirs(O, exist_ok=True)
frame_png(f'{O}/f_phone.png', PH_W, PH_H, 62, PH_BZ, PH_BZ, 48, island=True)
frame_png(f'{O}/f_watch.png', WT_W, WT_H, 66, 14, 14, 52)
Image.new('RGBA', (WT_W-80, 150), (30, 30, 38, 255)).save(f'{O}/f_band.png')
DL = os.path.expanduser('~/Downloads'); PR = f'{PP}/dist/promo'; VID = f'{PP}/iOSApp/Video'
MUSIC = f'{PP}/iOSApp/Music/bgm_fever.m4a'
FPS = 30; XF = 0.6
GRADE = "eq=contrast=1.08:saturation=1.20:gamma=0.97,colorbalance=rs=.03:bs=-.03:rh=.04:bh=-.02,vignette=PI/6,noise=alls=5:allf=t"


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
          f"[bg][sc]overlay=(W-{pw})/2+{bez}:'420+{bez}+22*sin(t*2.2)+60*max(0,1-t/0.5)*max(0,1-t/0.5)'[a];"
          f"[a][fr]overlay=(W-{pw})/2:'420+22*sin(t*2.2)+60*max(0,1-t/0.5)*max(0,1-t/0.5)'[b];{fadetxt(2, L)};[b][tx]overlay=0:0[o]")
    sh(f'ffmpeg -v error -y -ss {bgss} -t {L} -i "{bgsrc}" -ss {ss} -t {L} -i "{mov}" -loop 1 -t {L} -i {overlay} -loop 1 -t {L} -i {O}/f_phone.png '
       f'-filter_complex "{fc}" -map "[o]" -r {FPS} -t {L} -pix_fmt yuv420p -an "{out}"')

def title_card(out, dur, overlay):
    L = dur + XF
    fc = f"[0:v]null[b];{fadetxt(1, L, 0.3)};[b][tx]overlay=0:0[o]"
    sh(f'ffmpeg -v error -y -f lavfi -t {L} -i "color=c=0x07050f:s=1080x1920:r={FPS}" -loop 1 -t {L} -i {overlay} -filter_complex "{fc}" -map "[o]" -t {L} -pix_fmt yuv420p -an "{out}"')


V=f'{VID}'
B14=f'{V}/vid_boss14.mp4'; B24=f'{V}/vid_boss24.mp4'; B50=f'{V}/vid_boss50.mp4'
RM=f'{PR}/r_multi.mov'; RV=f'{PR}/r_versus.mov'
INTRO=f'{R}/promo/intro_ariagames.mp4'
plan=[]
def add(name,d): plan.append((f'{O}/{name}.mp4',d)); return plan[-1][0]
sh(f'ffmpeg -v error -y -i "{INTRO}" -vf "scale=1080:1920,fps={FPS},format=yuv420p" -an -t 5 "{add("i0",5.0-XF)}"')
vclip(add('a0',3.4),f'{R}/content/2026-11-03/gem/lila_friends_garden.mp4',0.8,3.4,txt('T1',['Poppy Pop','goes multiplayer.'],330,92),0.06)
phone_scene(add('p1',3.0),RM,1.0,3.0,B14,3.5,txt('T2',['LIVE DUELS.'],245,84))
vclip(add('a1',3.0),B24,0.4,3.0,txt('T3',['Chain combos.','Send garbage.'],330,92),0.06)
phone_scene(add('p2',3.0),RM,5.0,3.0,B24,3.5,txt('T4',['BEAT YOUR','RIVALS.'],245,84))
vclip(add('a2',3.0),B50,5.0,3.0,txt('T5',['Who is your','co-op partner?'],330,92),0.05)
phone_scene(add('p3',3.0),RV,2.0,3.0,B50,2.0,txt('T6',['PLAY WORLDWIDE.'],245,84))
vclip(add('dv',3.4),f'{R}/content/2026-11-02/versus/gem/c2.mp4',11.0,3.4,txt('T7',['iPhone  ·  iPad','+ Apple Watch'],245,96),0.04)
title_card(add('t1',1.4),1.4,txt('T8',['POPPY POP'],880,150))
e=endcard('T_end','Poppy Pop','poppypop.png','+ iPhone & iPad',(190,90,170))
still_seg(add('e',3.0),e,3.0+XF,framed=False)
files=[p for p,_ in plan]; durs=[d for _,d in plan]
inp=' '.join(f'-i "{f}"' for f in files)
fc='';prev='[0:v]';t=0.0
for k in range(1,len(files)):
    t+=durs[k-1]
    fc+=f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={t:.3f}[x{k}];";prev=f'[x{k}]'
total=sum(durs)+XF
OUT=f'{R}/content/2026-11-03/poppypop_multiplayer_v4.mp4'
sh(f'ffmpeg -v error -y {inp} -stream_loop -1 -i "{MUSIC}" -filter_complex "{fc.rstrip(";")}" -map "{prev}" -map {len(files)}:a -af "afade=t=in:st=0:d=0.8,afade=t=out:st={total-1.6:.2f}:d=1.6,volume=1.1" -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p -r {FPS} -c:a aac -b:a 192k -t {total:.2f} -movflags +faststart "{OUT}"')
print(OUT,round(total,1))
