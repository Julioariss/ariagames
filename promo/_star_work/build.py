from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, os
H='/Users/julioarisserey'
W,Ht=1206,2622
def font(sz,bold=True):
    f=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',sz)
    try:
        for i in range(8):
            f=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',sz,index=i)
            n=' '.join(f.getname()).lower()
            if bold and n.endswith('bold'): return f
            if (not bold) and n.endswith('regular'): return f
    except Exception: pass
    return f
def center(d,y,t,f,fill,stroke=0):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill)
    return w
# ---------- SHOT 1 (hero)
art=Image.open(H+'/Documents/Claude/Projects/ariagames/art/staracce.jpg').convert('RGB')
s=Ht/art.height; art=art.resize((int(art.width*s),Ht),Image.LANCZOS)
cx=int(art.width*0.40); x0=max(0,min(art.width-W,cx-W//2)); hero=art.crop((x0,0,x0+W,Ht))
g=np.zeros((Ht,1,1),dtype=float)
ramp=np.clip((np.arange(Ht)-1350)/(Ht-1350),0,1)**1.3*0.92
ov=Image.fromarray((np.stack([np.zeros(Ht),np.zeros(Ht),np.zeros(Ht)],axis=1)[:,None,:].repeat(W,axis=1)).astype('uint8'))
mask=Image.fromarray((ramp[:,None].repeat(W,axis=1)*255).astype('uint8'))
hero=Image.composite(ov,hero,mask)
d=ImageDraw.Draw(hero)
d.rectangle((W//2-90,2030,W//2+90,2038),fill=(220,40,40))
center(d,2110,'STAR ACE',font(210),(255,255,255))
center(d,2360,'Dodge. Roll. Lock on.',font(64,False),(255,255,255))
center(d,2515,'ONLY ON APPLE WATCH',font(34),(255,255,255))
hero.save('new_1.png')
# ---------- SHOT 5 (boss) cloned from old s2 template
tpl=Image.open('APP_IPHONE_61_4_s2.jpg.png').convert('RGB')
a=np.array(tpl)
col=a[:,5:6,:]                      # vertical gradient strip
y0,y1=120,520
patch=np.repeat(col[y0:y1],W,axis=1); a[y0:y1]=patch
tpl=Image.fromarray(a); d=ImageDraw.Draw(tpl)
center(d,215,'Epic boss fights',font(118),(255,255,255))
center(d,372,'Lock on and take them down',font(50,False),(255,255,255))
scr=Image.open(H+'/Developer/NovaStrike/screenshots/bd_b.png').convert('RGB').resize((803,982),Image.LANCZOS)
m=Image.new('L',(803,982),0); ImageDraw.Draw(m).rounded_rectangle((0,0,802,981),radius=135,fill=255)
tpl.paste(scr,(201,699),m)
tpl.save('new_5.png')
# ---------- reuse: shots 2,3,4
import shutil
shutil.copy('APP_IPHONE_61_1_s_b.jpg.png','new_2.png'); shutil.copy('APP_IPHONE_61_2_s0.jpg.png','new_3.png'); shutil.copy('APP_IPHONE_61_3_s1.jpg.png','new_4.png')
# ---------- watch ultra
shutil.copy(H+'/Developer/NovaStrike/screenshots/bd_b.png','watch_1.png')
shutil.copy('APP_WATCH_ULTRA_1_s1.jpg.png','watch_2.png'); shutil.copy('APP_WATCH_ULTRA_2_s2.jpg.png','watch_3.png')
# preview montage
ims=[Image.open(f'new_{i}.png').convert('RGB') for i in (1,2,3,4,5)]
h=900; ims=[i.resize((int(i.width*h/i.height),h)) for i in ims]
mo=Image.new('RGB',(sum(i.width for i in ims),h)); x=0
for i in ims: mo.paste(i,(x,0)); x+=i.width
mo.save('../_star_new_preview.png'); print(mo.size)
