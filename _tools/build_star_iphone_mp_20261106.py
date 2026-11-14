import os, sys, subprocess, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R=os.path.expanduser('~/Documents/Claude/Projects/ariagames'); D=f'{R}/content/2026-11-06'; G=f'{D}/gem'; S=f'{D}/sim'; W=f'{D}/work'
os.makedirs(W,exist_ok=True)
FONT=next(f for f in ['/System/Library/Fonts/Supplemental/Impact.ttf','/System/Library/Fonts/Supplemental/Arial Black.ttf','/System/Library/Fonts/Helvetica.ttc'] if os.path.exists(f))
FPS=30; XF=0.6
GRADE="eq=contrast=1.08:saturation=1.20:gamma=0.97,vignette=PI/6"
def sh(c): subprocess.run(c,shell=True,check=True)
def ov(name,lines,y,size,col=(255,255,255),sub=None):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); f=ImageFont.truetype(FONT,size)
    glow=Image.new('RGBA',(1080,1920),(0,0,0,0)); gd=ImageDraw.Draw(glow)
    yy=y
    for l in lines:
        w=d.textlength(l,font=f); x=(1080-w)/2
        gd.text((x,yy),l,font=f,fill=(80,170,255,255),stroke_width=10,stroke_fill=(80,170,255,255))
        yy+=int(size*1.12)
    glow=glow.filter(ImageFilter.GaussianBlur(14)); im.alpha_composite(glow); d=ImageDraw.Draw(im); yy=y
    for l in lines:
        w=d.textlength(l,font=f); x=(1080-w)/2
        d.text((x,yy),l,font=f,fill=col,stroke_width=7,stroke_fill=(10,12,40,255)); yy+=int(size*1.12)
    if sub:
        f2=ImageFont.truetype(FONT,int(size*0.5)); w=d.textlength(sub,font=f2)
        d.text(((1080-w)/2,yy+10),sub,font=f2,fill=(255,215,90,255),stroke_width=5,stroke_fill=(10,12,40,255))
    p=f'{W}/{name}.png'; im.save(p); return p
def fade(i,L): return f"[{i}:v]format=rgba,fade=t=in:st=0.25:d=0.3:alpha=1,fade=t=out:st={max(L-0.55,0.5)}:d=0.3:alpha=1[tx]"
def vclip(out,src,ss,dur,ovp,zoom=0.08):
    L=dur+XF; n=int(L*FPS)
    vf=f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='1.0+{zoom}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS},{GRADE}"
    sh(f'ffmpeg -v error -y -ss {ss} -t {L} -i "{src}" -loop 1 -t {L} -i {ovp} -filter_complex "[0:v]{vf}[b];{fade(1,L)};[b][tx]overlay=0:0[o]" -map "[o]" -r {FPS} -t {L} -pix_fmt yuv420p -an "{out}"')
def card(out,mov,ss,dur,bg,bgss,ovp):
    # landscape iPhone gameplay card centred on blurred Gemini background
    L=dur+XF; cw=1000; ch=460
    fc=(f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=24:4,eq=brightness=0.02:saturation=1.3,{GRADE}[bg];"
        f"[1:v]scale={cw}:{ch}:force_original_aspect_ratio=increase,crop={cw}:{ch}[sc];"
        f"[bg]drawbox=x=(iw-{cw+36})/2:y=700:w={cw+36}:h={ch+36}:color=0x101018@1:t=fill[b0];"
        f"[b0][sc]overlay=(W-{cw})/2:718[b1];{fade(2,L)};[b1][tx]overlay=0:0[o]")
    sh(f'ffmpeg -v error -y -ss {bgss} -t {L} -i "{bg}" -ss {ss} -t {L} -i "{mov}" -loop 1 -t {L} -i {ovp} -filter_complex "{fc}" -map "[o]" -r {FPS} -t {L} -pix_fmt yuv420p -an "{out}"')
def title(out,dur,ovp):
    L=dur+XF
    sh(f'ffmpeg -v error -y -f lavfi -t {L} -i "color=c=0x05060f:s=1080x1920:r={FPS}" -loop 1 -t {L} -i {ovp} -filter_complex "[0:v]null[b];{fade(1,L)};[b][tx]overlay=0:0[o]" -map "[o]" -t {L} -pix_fmt yuv420p "{out}"')
def still(out,img,dur,ovp):
    L=dur+XF; n=int(L*FPS)
    vf=f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='1.0+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS},{GRADE}"
    sh(f'ffmpeg -v error -y -loop 1 -t {L} -i "{img}" -loop 1 -t {L} -i {ovp} -filter_complex "[0:v]{vf}[b];{fade(1,L)};[b][tx]overlay=0:0[o]" -map "[o]" -r {FPS} -t {L} -pix_fmt yuv420p -an "{out}"')
SQ,PH,BO=f'{G}/sa_squad.mp4',f'{G}/sa_phone.mp4',f'{G}/sa_boss.mp4'
ART=glob.glob(os.path.expanduser('~/Downloads/Gemini_Generated_Image_w0s5q1w0s5q1w0s5.jpeg'))[0]
sim={k:(f'{S}/{k}.mov' if os.path.exists(f'{S}/{k}.mov') and os.path.getsize(f'{S}/{k}.mov')>200000 else None) for k in ['s1','boss','vs','menu']}
plan=[]
def add(n,d): plan.append((f'{W}/{n}.mp4',d)); return plan[-1][0]
title(add('t0',1.8),1.8,ov('T0',['ARIAGAMES','presents'],800,84))
vclip(add('a1',3.0),SQ,0.2,3.0,ov('T1',['FOUR PILOTS.','ONE SQUADRON.'],300,96),0.06)
vclip(add('a2',3.2),PH,0.0,3.2,ov('T2',['STAR ACE','COMES TO IPHONE'],300,96),0.05)
if sim['s1']: card(add('c1',3.0),sim['s1'],4.0,3.0,PH,5.0,ov('T3',['FLY ON YOUR PHONE.'],270,84))
vclip(add('a3',3.0),SQ,3.8,3.0,ov('T4',['TEAM UP.','2 TO 4 PLAYERS.'],300,96),0.06)
if sim['vs']: card(add('c2',3.0),sim['vs'],3.0,3.0,SQ,6.0,ov('T5',['ONLINE OR SAME WI-FI.'],270,84))
vclip(add('b1',3.2),BO,0.2,3.2,ov('T6',['GIANT BOSSES.','FIVE ELEMENTS.'],300,96),0.06)
if sim['boss']: card(add('c3',3.0),sim['boss'],5.0,3.0,BO,3.0,ov('T7',['BATTLE THEM ALL.'],270,84))
vclip(add('b2',3.4),BO,4.6,3.4,ov('T8',['BLAST THE','DEVOURER OF WORLDS.'],300,92),0.05)
still(add('e',3.6),ART,3.6,ov('T9',['STAR ACE'],120,150,sub='iPhone + Apple Watch'))
files=[p for p,_ in plan]; durs=[d for _,d in plan]
inp=' '.join(f'-i "{f}"' for f in files)
fc='';prev='[0:v]';t=0.0
for k in range(1,len(files)):
    t+=durs[k-1]; fc+=f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={t:.3f}[x{k}];"; prev=f'[x{k}]'
fc+=f"{prev}fade=t=out:st={t+durs[-1]-0.6:.3f}:d=0.6[v]"
tot=t+durs[-1]+XF
OUT=f'{D}/trailer_staracE_iphone_mp_en_silent.mp4'
sh(f'ffmpeg -v error -y {inp} -filter_complex "{fc}" -map "[v]" -r {FPS} -pix_fmt yuv420p -c:v libx264 -preset veryfast -crf 19 "{OUT}"')
print('OK',OUT,round(t+durs[-1],1),'s sim:',[k for k,v in sim.items() if v])
