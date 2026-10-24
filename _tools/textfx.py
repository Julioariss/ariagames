from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np
IMP='/System/Library/Fonts/Supplemental/Impact.ttf'
def gradfill(w,h,top,bot):
    t=np.linspace(0,1,h)[:,None,None]
    a=np.array(top,float)*(1-t)+np.array(bot,float)*t
    a=np.broadcast_to(a,(h,w,3)).astype('uint8')
    return Image.fromarray(a,'RGB')
def textfx(img, t, cx, y, size, top=(255,255,255), bot=(185,215,255), skew=0.10, ext=9, ol=None, dark=(25,10,70), spacing=3):
    size=int(size*1.18)
    f=ImageFont.truetype(IMP,size)
    tmp=ImageDraw.Draw(Image.new('L',(10,10)))
    tw=int(tmp.textlength(t,font=f))+spacing*len(t); th=int(size*1.3)
    pad=int(size*.35)+ext+10
    cw,ch=tw+2*pad,th+2*pad
    m=Image.new('L',(cw,ch),0); d=ImageDraw.Draw(m)
    x=pad
    for c in t:
        d.text((x,pad),c,font=f,fill=255); x+=d.textlength(c,font=f)+spacing
    m=m.transform((cw,ch),Image.AFFINE,(1,skew,-skew*ch/2,0,1,0),resample=Image.BICUBIC)
    r=max(3,size//13)
    big=m.filter(ImageFilter.MaxFilter(2*r+1))
    ring=m.filter(ImageFilter.MaxFilter(max(3,2*(r//2)+1)))
    layer=Image.new('RGBA',(cw,ch),(0,0,0,0))
    # shadow
    sh=big.filter(ImageFilter.GaussianBlur(8))
    sl=Image.new('RGBA',(cw,ch),(0,0,0,0)); sl.paste((0,0,0,150),(10,ext+14),sh)
    layer=Image.alpha_composite(layer,sl)
    # extrusion
    for k in range(ext,0,-1):
        e=Image.new('RGBA',(cw,ch),(0,0,0,0)); e.paste(dark+(255,),(0,k),big)
        layer=Image.alpha_composite(layer,e)
    o=Image.new('RGBA',(cw,ch),(0,0,0,0)); o.paste(dark+(255,),(0,0),big); layer=Image.alpha_composite(layer,o)
    w_=Image.new('RGBA',(cw,ch),(0,0,0,0)); w_.paste((255,255,255,255),(0,0),ring); layer=Image.alpha_composite(layer,w_)
    g=gradfill(cw,ch,top,bot).convert('RGBA'); g.putalpha(m)
    layer=Image.alpha_composite(layer,g)
    img.alpha_composite(layer,(int(cx-cw/2),int(y-pad)))
