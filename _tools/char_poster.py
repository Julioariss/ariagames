import sys, os
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1350
FB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def F(s): return ImageFont.truetype(FB, s)
def fit(d, t, s, mx):
    while d.textlength(t, font=F(s)) > mx and s > 20: s -= 2
    return F(s)
def poster(src, out, title, sub, line, acc, cx=.5, cy=.38):
    im = Image.open(src).convert('RGB')
    r = max(W/im.width, H/im.height); im = im.resize((int(im.width*r)+1, int(im.height*r)+1), Image.LANCZOS)
    x = int(min(max(cx*im.width-W/2, 0), im.width-W)); y = int(min(max(cy*im.height-H/2, 0), im.height-H))
    im = im.crop((x, y, x+W, y+H)).convert('RGBA')
    g = Image.new('RGBA', im.size); gd = ImageDraw.Draw(g)
    for yy in range(H):
        t = max(0, (yy/H-.58)/.42); gd.line([(0, yy), (W, yy)], fill=(0, 0, 0, int(215*t)))
    im = Image.alpha_composite(im, g); d = ImageDraw.Draw(im)
    def C(t, yy, f, fill, st):
        w = d.textlength(t, font=f); d.text(((W-w)/2, yy), t, font=f, fill=fill, stroke_width=st, stroke_fill='black')
    C(title, 975, fit(d, title, 150, 940), 'white', 6)
    C(sub, 1130, fit(d, sub, 54, 940), acc, 3)
    C(line, 1200, fit(d, line, 44, 940), 'white', 3)
    C('Free on Apple Watch  ·  ariagames.dev/go', 1272, fit(d, 'Free on Apple Watch  ·  ariagames.dev/go', 34, 900), (230, 230, 230), 2)
    im.convert('RGB').save(out, quality=93)
if __name__ == '__main__':
    a = sys.argv
    poster(a[1], a[2], a[3], a[4], a[5], tuple(int(v) for v in a[6].split(",")), .5, float(a[7]) if len(a)>7 else .38)
