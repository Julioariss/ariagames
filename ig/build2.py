from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=1080,1350
FP='/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf'
def F(s,w='Black'): return ImageFont.truetype(FP%('Medium' if w=='Medium' else 'Bold'),s)
M=ImageDraw.Draw(Image.new('RGB',(9,9)))
def fit(t,s,mx,w='Black'):
    while M.textlength(t,font=F(s,w))>mx: s-=2
    return F(s,w)
def cover(im,w,h,cx=.5,cy=.5):
    r=max(w/im.width,h/im.height); im=im.resize((int(im.width*r)+1,int(im.height*r)+1),Image.LANCZOS)
    x=int(min(max(cx*im.width-w/2,0),im.width-w)); y=int(min(max(cy*im.height-h/2,0),im.height-h)); return im.crop((x,y,x+w,y+h))
def shade(im,h0=.5,a=225):
    g=Image.new('RGBA',im.size); d=ImageDraw.Draw(g)
    for y in range(im.height):
        t=max(0,(y/im.height-h0)/(1-h0)); d.line([(0,y),(im.width,y)],fill=(0,0,0,int(a*t)))
    return Image.alpha_composite(im.convert('RGBA'),g).convert('RGB')
def T(d,xy,s,f,fill='white',anchor='la',st=0): d.text(xy,s,font=f,fill=fill,anchor=anchor,stroke_width=st,stroke_fill='black')
def dots(im,n,i):
    d=ImageDraw.Draw(im)
    for k in range(n): d.ellipse((W//2-n*14+k*28,H-40,W//2-n*14+k*28+12,H-28),fill='white' if k==i else (255,255,255,90) if False else '#888888')
def poster(p):
    bg=cover(Image.open(p).convert('RGB'),W,H).filter(ImageFilter.GaussianBlur(40))
    po=Image.open(p).convert('RGB'); r=(H-120)/po.height; po=po.resize((int(po.width*r),H-120)); bg.paste(po,((W-po.width)//2,60)); return bg
def game(key,art,real,icon_site,title,acc,cx,tag,feat,lines,posters):
    s=[]
    # 1 hero on subject
    h=shade(cover(Image.open(art).convert('RGB'),W,H,cx,.5),.52); d=ImageDraw.Draw(h)
    T(d,(60,H-330),title,fit(title,150,960),acc,st=4); T(d,(64,H-165),tag,fit(tag,56,950,'Bold'),'white',st=2)
    T(d,(W-60,60),'SWIPE  >>',F(40,'Bold'),'white','ra',2); s.append(h)
    # 2 real icon art full-bleed with feature
    ic=Image.open(real).convert('RGB').resize((W,W),Image.LANCZOS); c=Image.new('RGB',(W,H),'black'); c.paste(ic,(0,0)); c=shade(c,.62,235); d=ImageDraw.Draw(c)
    T(d,(W//2,W+40),feat[0],fit(feat[0],86,980),acc,'ma',3); T(d,(W//2,W+150),feat[1],fit(feat[1],50,980,'Bold'),'white','ma',2); s.append(c)
    for p in posters: s.append(poster(p))
    # CTA
    c=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(c)
    I=Image.open(real).convert('RGB').resize((440,440),Image.LANCZOS); m=Image.new('L',(440,440),0); ImageDraw.Draw(m).rounded_rectangle((0,0,439,439),100,fill=255); c.paste(I,((W-440)//2,210),m)
    T(d,(W//2,700),title,fit(title,100,960),'#111111','ma')
    for k,l in enumerate(lines): T(d,(W//2,840+k*70),l,F(50,'SemiBold'),'#333333','ma')
    T(d,(W//2,1090),'ONLY ON APPLE WATCH  ·  $1.99',F(46,'ExtraBold'),'#d4202a','ma'); T(d,(W//2,1170),'ariagames.dev',F(64,'ExtraBold'),'black','ma'); T(d,(W//2,1255),'Save & share with a watch-owner friend',F(34,'Medium'),'#777777','ma'); s.append(c)
    for i,im in enumerate(s,1): im.save(f'ig/v2/{key}_{i}.jpg',quality=93)
    return len(s)
game('kart','art/kart.jpg','ig/icons/kart_real.png',None,'KART WATCH GP','#ffcf1f',.64,'A full kart championship on your wrist',('5 CUPS · 15 TRACKS','Wild items · Drift · Local VS races'),['5 cups · 15 original tracks','Wild items · Local VS races'],['_asc/k_a.jpg','_asc/k_b.jpg'])
game('star','art/staracce.jpg','ig/icons/star_real.png',None,'Star Ace : Watch Shooter','#3fd0ff',.62,'Dodge. Barrel-roll. Lock on.',('5 WORLDS · 5 BOSSES','Rail-shooter built for Apple Watch'),['5 worlds · 5 unique bosses','Rail-shooter on your wrist'],['_asc/s_a.jpg','_asc/s_b.jpg'])
from PIL import Image as I2
for k in ['kart','star']:
    s=I2.new('RGB',(5*300,375))
    for i in range(5): s.paste(I2.open(f'ig/v2/{k}_{i+1}.jpg').resize((300,375)),(i*300,0))
    s.save(f'ig/v2/prev_{k}.jpg')
