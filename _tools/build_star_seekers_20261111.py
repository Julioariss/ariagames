import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R=os.path.expanduser('~/Documents/Claude/Projects/ariagames'); D=f'{R}/content/2026-11-11'; os.makedirs(D,exist_ok=True)
SRC=os.path.expanduser('~/Developer/NovaStrike/dist/shots/seek_rec.mp4')
MUS=os.path.expanduser('~/Developer/NovaStrike/Sources/Music/bgm4.m4a')
FONT='/System/Library/Fonts/Supplemental/Impact.ttf'
def ov(name,lines,y,size,sub=None):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); f=ImageFont.truetype(FONT,size)
    glow=Image.new('RGBA',(1080,1920),(0,0,0,0)); gd=ImageDraw.Draw(glow); yy=y
    for l in lines:
        w=gd.textlength(l,font=f); gd.text(((1080-w)/2,yy),l,font=f,fill=(255,70,200,255),stroke_width=10,stroke_fill=(255,70,200,255)); yy+=int(size*1.12)
    glow=glow.filter(ImageFilter.GaussianBlur(14)); im.alpha_composite(glow); d=ImageDraw.Draw(im); yy=y
    for l in lines:
        w=d.textlength(l,font=f); d.text(((1080-w)/2,yy),l,font=f,fill=(255,255,255,255),stroke_width=7,stroke_fill=(10,12,40,255)); yy+=int(size*1.12)
    if sub:
        f2=ImageFont.truetype(FONT,int(size*0.5)); w=d.textlength(sub,font=f2)
        d.text(((1080-w)/2,yy+10),sub,font=f2,fill=(255,215,90,255),stroke_width=5,stroke_fill=(10,12,40,255))
    p=f'{D}/{name}.png'; im.save(p); return p
a=ov('t1',['THE FINAL BOSS','JUST GOT HARDER'],330,100,'can your wrist survive it?')
b=ov('t2',['NOVA SEEKERS','3 homing missiles'],330,100)
c=ov('t3',['STAR Ace'],520,130,'Apple Watch · ariagames.dev/go')
T=15
fc=("[0:v]transpose=2,crop=678:1206,scale=1080:1920,eq=contrast=1.08:saturation=1.15[b];"
    "[1:v]format=rgba,fade=t=in:st=0.2:d=0.3:alpha=1,fade=t=out:st=3.3:d=0.3:alpha=1[x1];"
    "[2:v]format=rgba,fade=t=in:st=5:d=0.3:alpha=1,fade=t=out:st=9.5:d=0.3:alpha=1[x2];"
    "[3:v]format=rgba,fade=t=in:st=11.5:d=0.4:alpha=1[x3];"
    "[b][x1]overlay=0:0:eof_action=pass[o1];[o1][x2]overlay=0:0:eof_action=pass[o2];[o2][x3]overlay=0:0:eof_action=pass[o]")
out=f'{D}/daily_20261111_staracce_en.mp4'
cmd=(f'ffmpeg -v error -y -ss 20 -t {T} -i "{SRC}" -loop 1 -t {T} -i {a} -loop 1 -t {T} -i {b} -loop 1 -t {T} -i {c} -ss 5 -t {T} -i "{MUS}" '
     f'-filter_complex "{fc}" -map "[o]" -map 4:a -af "afade=t=in:d=0.5,afade=t=out:st=13.5:d=1.5" -r 30 -t {T} -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k "{out}"')
subprocess.run(cmd,shell=True,check=True); print(out)
