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

CS=os.path.expanduser('~/Developer/NovaStrike/Sources'); AX=CS+'/Assets.xcassets'
def land(out,src,ss,dur,ovp,pre=''):
    L=dur+XF; n=int(L*FPS)
    vf=(f"{pre}crop=ih*9/16:ih,scale=2160:3840:flags=lanczos,zoompan=z='1.0+0.07*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS},unsharp=5:5:0.9,{GRADE}")
    sh(f'ffmpeg -v error -y -ss {ss} -t {L} -i "{src}" -loop 1 -t {L} -i {ovp} -filter_complex "[0:v]{vf}[b];{fade(1,L)};[b][tx]overlay=0:0[o]" -map "[o]" -r {FPS} -t {L} -pix_fmt yuv420p -an "{out}"')
def vfull(out,src,ss,dur,ovp):
    land(out,src,ss,dur,ovp)
# versus composite from the game's own art
bg=Image.open(f'{AX}/vsbg.imageset/vsbg.png').convert('RGB').resize((1080,1920)) if False else Image.open(f'{AX}/vsbg.imageset/vsbg.png').convert('RGB')
bw,bh=bg.size; sc=max(1080/bw,1920/bh); bg=bg.resize((int(bw*sc),int(bh*sc))); bg=bg.crop(((bg.width-1080)//2,(bg.height-1920)//2,(bg.width-1080)//2+1080,(bg.height-1920)//2+1920)).filter(ImageFilter.GaussianBlur(3))
pl=Image.new('RGB',(1080,1920)); pl.paste(bg)
for i in range(4):
    p=Image.open(f'{AX}/vspilot{i+1}.imageset/vspilot{i+1}.png').convert('RGB').resize((500,500))
    pl.paste(p,(30+(i%2)*520,560+(i//2)*520))
pl.save(f'{W}/vs_comp.png')
CT,CSTART,H0,H2,B4=[f'{CS}/{n}.mp4' for n in ['cine_team','cine_start','cine_h0','cine_h2','cine_b4']]
gp=f'{S}/s1.mov'
plan=[]
def add(n,d): plan.append((f'{W}/{n}.mp4',d)); return plan[-1][0]
title(add('t0',1.6),1.6,ov('T0',['ARIAGAMES','presents'],800,84))
land(add('a1',3.2),CSTART,0.4,3.2,ov('T1',['STAR ACE','COMES TO IPHONE'],230,100))
land(add('c1',3.0),gp,9.0,3.0,ov('T3',['FLY ON YOUR PHONE.'],230,96),pre='crop=2868:952:0:184,')
land(add('a2',3.0),H2,0.6,3.0,ov('T4',['FIVE ELEMENTAL','BOSSES.'],230,96))
land(add('a3',3.0),H0,0.6,3.0,ov('T5',['EVERY WORLD','HAS A GUARDIAN.'],230,96))
still(add('v1',3.4),f'{W}/vs_comp.png',3.4,ov('T6',['NEW: MULTIPLAYER.','2 TO 4 PILOTS.'],200,92,sub='ONLINE  ·  SAME WI-FI'))
land(add('a4',3.4),CT,0.2,3.4,ov('T7',['TEAM UP.','FIGHT TOGETHER.'],230,96))
land(add('a5',3.2),B4,0.8,3.2,ov('T8',['THE DEVOURER','OF WORLDS.'],230,96))
land(add('a6',3.4),CT,15.0,3.4,ov('T9',['SAVE THE STARS.'],250,96))
still(add('e',3.8),f'{R}/img/staracce.png',3.8,ov('T10',['STAR ACE'],140,150,sub='COMING SOON TO IPHONE'))
files=[p for p,_ in plan]; durs=[d for _,d in plan]
inp=' '.join(f'-i "{f}"' for f in files)
fc='';prev='[0:v]';t=0.0
for k in range(1,len(files)):
    t+=durs[k-1]; fc+=f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={t:.3f}[x{k}];"; prev=f'[x{k}]'
fc+=f"{prev}fade=t=out:st={t+durs[-1]-0.6:.3f}:d=0.6[v]"
OUT=f'{D}/trailer_staracE_canon_v2_silent.mp4'
sh(f'ffmpeg -v error -y {inp} -filter_complex "{fc}" -map "[v]" -r {FPS} -pix_fmt yuv420p -c:v libx264 -preset veryfast -crf 19 "{OUT}"')
tot=round(t+durs[-1],1)
M=os.path.expanduser('~/Downloads/Launch_at_the_Horizon.mp3')
FIN=f'{D}/trailer_staracE_iphone_multiplayer_v2_en.mp4'
sh(f'ffmpeg -v error -y -i "{OUT}" -i "{M}" -filter_complex "[1:a]atrim=0:{tot},afade=t=in:d=0.5,afade=t=out:st={tot-1.5}:d=1.5,volume=0.9[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t {tot} "{FIN}"')
print('OK',FIN,tot)
