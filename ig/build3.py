from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
W,H=1080,1350
FP='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; FM='/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
def F(s,m=False): return ImageFont.truetype(FM if m else FP,s)
M=ImageDraw.Draw(Image.new('RGB',(9,9)))
def fit(t,s,mx,m=False):
    while M.textlength(t,font=F(s,m))>mx: s-=2
    return F(s,m)
S='ig/src/'
def op(p): return Image.open(p).convert('RGB')
def cover(im,w,h,cx=.5,cy=.5):
    r=max(w/im.width,h/im.height); im=im.resize((int(im.width*r)+1,int(im.height*r)+1),Image.LANCZOS)
    x=int(min(max(cx*im.width-w/2,0),im.width-w)); y=int(min(max(cy*im.height-h/2,0),im.height-h)); return im.crop((x,y,x+w,y+h))
def shade(im,h0=.5,a=225,top=0):
    g=Image.new('RGBA',im.size); d=ImageDraw.Draw(g)
    for y in range(im.height):
        t=max(0,(y/im.height-h0)/(1-h0)); u=max(0,(top-y/im.height)/top) if top else 0
        d.line([(0,y),(im.width,y)],fill=(0,0,0,int(a*max(t,u*.8))))
    return Image.alpha_composite(im.convert('RGBA'),g).convert('RGB')
def T(d,xy,s,f,fill='white',a='la',st=0,sc='black'): d.text(xy,s,font=f,fill=fill,anchor=a,stroke_width=st,stroke_fill=sc)
def rr(im,r):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,im.width-1,im.height-1),r,fill=255); return m
def bezel(path,w,rot=0,crop=None):
    im=op(path)
    if crop: im=im.crop(crop)
    h=int(w*im.height/im.width); im=im.resize((w,h),Image.LANCZOS); pad=int(w*.045)
    out=Image.new('RGBA',(w+2*pad,h+2*pad),(0,0,0,0)); d=ImageDraw.Draw(out)
    d.rounded_rectangle((0,0,out.width-1,out.height-1),int(w*.24),fill=(18,18,20,255),outline=(70,70,76,255),width=3)
    out.paste(im,(pad,pad),rr(im,int(w*.19)))
    if rot: out=out.rotate(rot,expand=True,resample=Image.BICUBIC)
    return out
def shadow_paste(base,card,xy,blur=30,off=18,a=150):
    sh=Image.new('RGBA',card.size,(0,0,0,0)); sh.putalpha(card.split()[3].point(lambda v:int(v*a/255)))
    layer=Image.new('RGBA',base.size,(0,0,0,0)); layer.paste(sh,(xy[0],xy[1]+off),sh); layer=layer.filter(ImageFilter.GaussianBlur(blur))
    b=Image.alpha_composite(base.convert('RGBA'),layer); b.alpha_composite(card,xy); return b.convert('RGB')
def grad_bg(c1,c2,vert=True):
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H; d.line([(0,y),(W,y)],fill=tuple(int(c1[i]*(1-t)+c2[i]*t) for i in range(3)))
    return im
def blurbg(path,tint=(0,0,0),k=.45):
    im=cover(op(path),W,H).filter(ImageFilter.GaussianBlur(45)); ov=Image.new('RGB',(W,H),tint); return Image.blend(im,ov,k)
def head(im,l1,l2,acc,y=70,sz=112):
    d=ImageDraw.Draw(im); T(d,(W//2,y),l1,fit(l1,sz,980),acc,'ma',4); 
    if l2: T(d,(W//2,y+sz+8),l2,fit(l2,46,980,True),'white','ma',2)
def foot(im,t):
    d=ImageDraw.Draw(im); T(d,(W//2,H-70),t,fit(t,36,980,True),'white','ma',2)
def cta(real,title,lines,out):
    c=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(c)
    I=op(real).resize((440,440),Image.LANCZOS); c.paste(I,((W-440)//2,210),rr(I,100))
    T(d,(W//2,700),title,fit(title,100,960),'#111','ma')
    for k,l in enumerate(lines): T(d,(W//2,840+k*70),l,F(50),'#333','ma')
    T(d,(W//2,1090),'ONLY ON APPLE WATCH  ·  $1.99',F(46),'#d4202a','ma'); T(d,(W//2,1170),'ariagames.dev',F(64),'black','ma')
    T(d,(W//2,1255),'Save & share with a watch-owner friend',F(34,True),'#777','ma'); c.save(out,quality=93)
Y='#ffcf1f'; C='#3fd0ff'
# ---------- KART ----------
k=[]
h=shade(cover(op('art/kart.jpg'),W,H,.64,.5),.45,230,.18); d=ImageDraw.Draw(h)
T(d,(60,70),'KART WATCH GP',F(46),Y,'la',2); T(d,(W-60,70),'SWIPE >>',F(40),'white','ra',2)
T(d,(60,H-390),'A FULL KART',F(130),'white','la',5); T(d,(60,H-260),'CHAMPIONSHIP',F(118),Y,'la',5); T(d,(60,H-120),'ON YOUR WRIST.',F(76),'white','la',3); k.append(h)
# 2 five worlds fan
b=grad_bg((255,140,40),(120,40,170)); head(b,'5 CUPS.','5 WORLDS. 15 ORIGINAL TRACKS',Y,60,150)
pos=[(-12,40,420,-8),(-6,250,430,-4),(0,470,440,0)]
shots=['kwgp_s1','kwgp_s3','kwgp_s4','kwgp_s2','kwgp_s5']
cards=[bezel(S+s+'.png',320,r) for s,r in zip(shots,[-12,-6,0,6,12])]
xs=[0,165,330,495,660]; ys=[560,520,480,520,560]
for c,x,y in zip(cards,xs,ys): b=shadow_paste(b,c,(x,y),22,14)
foot(b,'Real gameplay · every cup a new look'); k.append(b)
# 3 racers
b=grad_bg((24,70,70),(10,30,40)); head(b,'MEET THE RACERS','10 original characters · each with their own kart',Y,50,92)
for i,n in enumerate(['ada','kodiak','remi']):
    im=op(S+n+'_sheet.jpg'); c=cover(im,960,285); b.paste(c,(60,310+i*(285+18)),rr(c,34))
b=b.convert('RGB'); foot(b,'Pick your driver. Own the track.'); k.append(b)
# 4 night city big
b=blurbg(S+'kwgp_s4.png',(60,0,90),.35); b=shade(b,.9,0,0)
head(b,'DRIFT. BOOST. WIN.','Race 8 drivers on a 1.9-inch screen',Y,60,104)
c=bezel(S+'kwgp_s4.png',620); b=shadow_paste(b,c,((W-c.width)//2,330),30,22,170); foot(b,'Digital Crown steers. Tap to boost.'); k.append(b)
# 5 menu + GO
b=grad_bg((10,60,110),(10,20,50)); head(b,'SOLO OR VS','Race friends nearby · no internet needed',Y,60,120)
c1=bezel(S+'k0.jpg',420,-5); c2=bezel(S+'k1.jpg',420,5)
b=shadow_paste(b,c1,(70,400),26,16); b=shadow_paste(b,c2,(580,470),26,16); foot(b,'Wild items · Local VS races'); k.append(b)
cta('ig/icons/kart_real.png','KART WATCH GP',['5 cups · 15 original tracks','Wild items · Local VS races'],'ig/v3/_c1.jpg'); k.append(Image.open('ig/v3/_c1.jpg'))
for i,im in enumerate(k,1): im.convert('RGB').save(f'ig/v3/kart_{i}.jpg',quality=93)
# ---------- STAR ----------
s=[]
h=shade(cover(op('art/staracce.jpg'),W,H,.62,.5),.45,230,.18); d=ImageDraw.Draw(h)
T(d,(60,70),'Star Ace : Watch Shooter',F(46),C,'la',2); T(d,(W-60,70),'SWIPE >>',F(40),'white','ra',2)
T(d,(60,H-390),'DODGE.',F(150),'white','la',5); T(d,(60,H-235),'BARREL-ROLL.',F(112),C,'la',5); T(d,(60,H-105),'LOCK ON.',F(90),'white','la',3); s.append(h)
b=blurbg(S+'s1.jpg',(0,60,70),.3); head(b,'5 WORLDS','An arcade space shooter built for Apple Watch',C,60,150)
c=bezel(S+'s1.jpg',600); b=shadow_paste(b,c,((W-c.width)//2,360),30,22,170); foot(b,'Drag to fly · Hold to lock on'); s.append(b)
b=blurbg(S+'s2.jpg',(30,0,60),.3); head(b,'5 BOSSES','Asteroid belts, giant planets, one ace',C,60,150)
c=bezel(S+'s2.jpg',600); b=shadow_paste(b,c,((W-c.width)//2,360),30,22,170); foot(b,'Every world ends in a boss fight'); s.append(b)
b=cover(op('art/staracce.jpg'),W,H,.30,.5); b=shade(b,.5,230,.2); d=ImageDraw.Draw(b)
T(d,(60,70),'NO ADS. NO ACCOUNTS.',F(54),'white','la',3); T(d,(60,H-300),'THE ACE',F(140),C,'la',5); T(d,(60,H-150),'FITS ON YOUR WRIST.',F(70),'white','la',3); s.append(b)
b=grad_bg((20,90,110),(8,24,50)); head(b,'REAL GAMEPLAY','Captured on Apple Watch',C,60,100)
c1=bezel(S+'s0.jpg',420,-5); c2=bezel(S+'s1.jpg',420,5)
b=shadow_paste(b,c1,(70,400),26,16); b=shadow_paste(b,c2,(580,470),26,16); foot(b,'Series 10 or later · incl. Ultra 3'); s.append(b)
cta('ig/icons/star_real.png','Star Ace : Watch Shooter',['5 worlds · 5 unique bosses','Rail-shooter on your wrist'],'ig/v3/_c2.jpg'); s.append(Image.open('ig/v3/_c2.jpg'))
for i,im in enumerate(s,1): im.convert('RGB').save(f'ig/v3/star_{i}.jpg',quality=93)
for key,n in [('kart',6),('star',6)]:
    sh=Image.new('RGB',(n*260,325))
    for i in range(n): sh.paste(Image.open(f'ig/v3/{key}_{i+1}.jpg').resize((260,325)),(i*260,0))
    sh.save(f'ig/v3/prev_{key}.jpg')
