from PIL import Image, ImageDraw, ImageFont, ImageFilter
import glob
W,H=1080,1350
def font(sz,bold=True):
    for p in ['/usr/share/fonts/truetype/google-fonts/Poppins-Black.ttf','/usr/share/fonts/truetype/google-fonts/Poppins-ExtraBold.ttf','/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf']:
        try: return ImageFont.truetype(p,sz)
        except: pass
    return ImageFont.load_default()
def cover(im,w,h):
    r=max(w/im.width,h/im.height); im=im.resize((int(im.width*r)+1,int(im.height*r)+1),Image.LANCZOS)
    x=(im.width-w)//2; y=(im.height-h)//2; return im.crop((x,y,x+w,y+h))
def grad(c,h0=0.55):
    g=Image.new('RGBA',c.size); d=ImageDraw.Draw(g)
    for y in range(c.height):
        t=max(0,(y/c.height-h0)/(1-h0)); d.line([(0,y),(c.width,y)],fill=(0,0,0,int(215*t)))
    return Image.alpha_composite(c.convert('RGBA'),g)
def txt(d,xy,s,sz,fill='white',anchor='la',stroke=0):
    d.text(xy,s,font=font(sz),fill=fill,anchor=anchor,stroke_width=stroke,stroke_fill='black')
def game(key,art,icon,title,accent,posters,tag,lines):
    pano=cover(Image.open(art).convert('RGB'),W*3,H)
    pano=grad(pano,0.5); d=ImageDraw.Draw(pano)
    sz=150
    while ImageDraw.Draw(Image.new('RGB',(9,9))).textlength(title,font=font(sz))>940: sz-=4
    txt(d,(60,H-330),title,sz,accent,stroke=4)
    tz=56
    while ImageDraw.Draw(Image.new('RGB',(9,9))).textlength(tag,font=font(tz))>940: tz-=2
    txt(d,(66,H-170),tag,tz,'white',stroke=2)
    txt(d,(W*3-60,H-120),'SWIPE >>  ariagames.dev',46,'white','ra',stroke=2)
    out=[]
    for i in range(3): out.append(pano.crop((i*W,0,(i+1)*W,H)).convert('RGB'))
    for p in posters:  # poster slides: blurred bg + phone-ratio poster
        bg=cover(Image.open(p).convert('RGB'),W,H).filter(ImageFilter.GaussianBlur(40))
        po=Image.open(p).convert('RGB'); r=(H-120)/po.height; po=po.resize((int(po.width*r),H-120))
        bg.paste(po,((W-po.width)//2,60)); out.append(bg)
    # CTA
    c=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(c)
    ic=Image.open(icon).convert('RGB').resize((420,420)); m=Image.new('L',(420,420),0); ImageDraw.Draw(m).rounded_rectangle((0,0,419,419),95,fill=255)
    c.paste(ic,((W-420)//2,230),m)
    txt(d,(W//2,740),title,100,accent,'ma',stroke=0)
    for k,l in enumerate(lines): txt(d,(W//2,880+k*70),l,52,'#222222','ma')
    txt(d,(W//2,1160),'ONLY ON APPLE WATCH · $1.99',46,'#d4202a','ma')
    txt(d,(W//2,1240),'ariagames.dev',60,'black','ma')
    out.append(c)
    for i,im in enumerate(out,1): im.save(f'ig/{key}_{i}.jpg',quality=93)
game('kart','art/kart.jpg','img/kart.png','KART WATCH GP','#ffcf1f',['_asc/k_a.jpg','_asc/k_b.jpg'],'A full kart championship on your wrist',['5 cups · 15 original tracks','Wild items · Local VS races'])
game('star','art/staracce.jpg','img/staracce.png','Star Ace : Watch Shooter','#3fd0ff',['_asc/s_a.jpg','_asc/s_b.jpg'],'Dodge. Barrel-roll. Lock on.',['5 worlds · 5 unique bosses','Rail-shooter on your wrist'])
# highlight covers 1080x1920 (safe circle)
for key,icon,bgc in [('kart','img/kart.png','#ffcf1f'),('star','img/staracce.png','#3fd0ff'),('aria',None,'#f6f4f0')]:
    c=Image.new('RGB',(1080,1920),bgc); d=ImageDraw.Draw(c)
    if icon:
        ic=Image.open(icon).convert('RGB').resize((560,560)); m=Image.new('L',(560,560),0); ImageDraw.Draw(m).rounded_rectangle((0,0,559,559),125,fill=255); c.paste(ic,(260,680),m)
    else:
        txt(d,(540,820),'ARIA',260,'#d4202a','ma'); txt(d,(540,1070),'games',200,'black','ma')
    c.save(f'ig/hl_{key}.jpg',quality=93)
