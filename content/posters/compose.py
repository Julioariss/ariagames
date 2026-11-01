import sys
from PIL import Image, ImageDraw, ImageFont
# usage: compose.py art.png "TITLE" "tagline" "GAME LINE" out.jpg [accent hex]
W, H = 1080, 1350
IMP = '/System/Library/Fonts/Supplemental/Impact.ttf'
BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def F(p, s): return ImageFont.truetype(p, s)
def fit(d, t, p, s, mx):
    while d.textlength(t, font=F(p, s)) > mx and s > 20: s -= 2
    return F(p, s)
def cover(im, w, h, cy=.5):
    r = max(w/im.width, h/im.height); im = im.resize((int(im.width*r)+1, int(im.height*r)+1), Image.LANCZOS)
    x = (im.width-w)//2; y = int((im.height-h)*cy); return im.crop((x, y, x+w, y+h))
art, title, tag, game, out = sys.argv[1:6]
acc = sys.argv[6] if len(sys.argv) > 6 else '#FFD21F'
im = cover(Image.open(art).convert('RGB'), W, H, .35).convert('RGBA')
g = Image.new('RGBA', (W, H)); gd = ImageDraw.Draw(g)
for y in range(H):
    t = max(0, (y/H-.55)/.45); gd.line([(0, y), (W, y)], fill=(0, 0, 0, int(235*t**1.2)))
im = Image.alpha_composite(im, g); d = ImageDraw.Draw(im)
def C(t, y, f, fill, st=0):
    d.text(((W-d.textlength(t, font=f))/2, y), t, font=f, fill=fill, stroke_width=st, stroke_fill='black')
ft = fit(d, title.upper(), IMP, 190, 900); C(title.upper(), 930, ft, acc, 6)
fg = fit(d, tag.upper(), BOLD, 46, 900); C(tag.upper(), 1150, fg, 'white', 3)
fs = fit(d, game, BOLD, 34, 900); C(game, 1240, fs, '#dddddd', 2)
fu = F(BOLD, 34); C('ariagames.dev/go', 1290, fu, acc, 2)
im.convert('RGB').save(out, quality=94)
