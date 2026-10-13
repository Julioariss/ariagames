from PIL import Image, ImageDraw, ImageFont
FP='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
M=ImageDraw.Draw(Image.new('RGB',(9,9)))
def fit(t,s,mx):
    while M.textlength(t,font=ImageFont.truetype(FP,s))>mx: s-=2
    return ImageFont.truetype(FP,s)
def cover(art,cx,title,acc,sub,out):
    W,H=1080,1920; im=Image.open(art).convert('RGB'); r=H/im.height; im=im.resize((int(im.width*r),H),Image.LANCZOS)
    x=int(min(max(cx*im.width-W/2,0),im.width-W)); im=im.crop((x,0,x+W,H)).convert('RGBA')
    g=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(g)
    for y in range(H):
        t=max(0,(y/H-.55)/.45); d.line([(0,y),(W,y)],fill=(0,0,0,int(235*t)))
    im=Image.alpha_composite(im,g).convert('RGB'); d=ImageDraw.Draw(im)
    for dx,dy in [(-3,0),(3,0),(0,3),(0,-3)]: d.text((W//2+dx,1330+dy),title,font=fit(title,130,960),fill='black',anchor='ma')
    d.text((W//2,1330),title,font=fit(title,130,960),fill=acc,anchor='ma')
    d.text((W//2,1500),sub,font=fit(sub,52,960),fill='white',anchor='ma')
    d.text((W//2,1610),'ONLY ON APPLE WATCH · $1.99',font=fit('x',44,960),fill='#ff4b55',anchor='ma')
    im.save(out,quality=93)
cover('art/kart.jpg',.62,'KART WATCH GP','#ffcf1f','Full kart racing on your wrist','ig/v2/cover_kart.jpg')
cover('art/staracce.jpg',.60,'Star Ace : Watch Shooter','#3fd0ff','Dodge. Barrel-roll. Lock on.','ig/v2/cover_star.jpg')
