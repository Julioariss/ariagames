#!/usr/bin/env python3
# Builds App Store iPhone poster screenshots (1206x2622) from the site art.
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H = 1206, 2622
FB = '/System/Library/Fonts/Supplemental/Arial Black.ttf'
FR = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
RED = (229, 9, 20)

def grad(img, top=0.52, strength=235):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    px = ov.load()
    for y in range(H):
        t = max(0, (y / H - top) / (1 - top))
        a = int(min(1, t * 1.25) ** 1.4 * strength)
        for x in range(W):
            px[x, y] = (6, 6, 10, a)
    return Image.alpha_composite(img.convert('RGBA'), ov)

def text_block(d, lines, y, size, fill=(255, 255, 255), font=FB, gap=12, shadow=True):
    f = ImageFont.truetype(font, size)
    for ln in lines:
        w = d.textlength(ln, font=f)
        x = (W - w) / 2
        if shadow:
            d.text((x + 4, y + 6), ln, font=f, fill=(0, 0, 0, 160))
        d.text((x, y), ln, font=f, fill=fill)
        y += size + gap
    return y

def hero(art, cx, title, tag, out):
    a = Image.open(art).convert('RGB')
    s = H / a.height
    a = a.resize((int(a.width * s), H), Image.LANCZOS)
    left = int(max(0, min(a.width - W, cx * a.width - W / 2)))
    c = a.crop((left, 0, left + W, H))
    c = grad(c)
    d = ImageDraw.Draw(c)
    d.rectangle((W // 2 - 70, 1960, W // 2 + 70, 1968), fill=RED)
    y = text_block(d, title, 2010, 124, gap=6)
    text_block(d, tag, y + 26, 58, fill=(235, 235, 235), font=FR)
    text_block(d, ['ONLY ON APPLE WATCH'], H - 140, 34, fill=(255, 255, 255), font=FR, shadow=False)
    c.convert('RGB').save(out, quality=92)

def card(art, head, sub, out, cx=0.5):
    a0 = Image.open(art).convert('RGB')
    cw = int(a0.height * 0.8)
    l = int(max(0, min(a0.width - cw, cx * a0.width - cw / 2)))
    a = a0.crop((l, 0, l + cw, a0.height))
    bgsrc = a0
    bg = bgsrc.resize((int(bgsrc.width * H / bgsrc.height), H), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, 0, (bg.width - W) // 2 + W, H)).filter(ImageFilter.GaussianBlur(38))
    bg = Image.blend(bg, Image.new('RGB', (W, H), (8, 8, 12)), 0.62).convert('RGBA')
    pic_w = W - 120
    pic = a.resize((pic_w, int(a.height * pic_w / a.width)), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', pic.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, pic.width, pic.height), 56, fill=255)
    pic.putalpha(m)
    py = 1020
    sh = Image.new('RGBA', (pic.width + 160, pic.height + 160), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((80, 100, 80 + pic.width, 100 + pic.height), 56, fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(34))
    bg.alpha_composite(sh, (60 - 80, py - 80))
    bg.alpha_composite(pic, (60, py))
    d = ImageDraw.Draw(bg)
    d.rectangle((W // 2 - 70, 330, W // 2 + 70, 338), fill=RED)
    y = text_block(d, head, 400, 128, gap=6)
    text_block(d, sub, y + 20, 56, fill=(225, 225, 225), font=FR)
    text_block(d, ['ARIAGAMES · APPLE WATCH'], H - 140, 34, fill=(255, 255, 255), font=FR, shadow=False)
    bg.convert('RGB').save(out, quality=92)

os.makedirs('_asc', exist_ok=True)
hero('art/kart.jpg', 0.74, ['KART', 'WATCH GP'], ['Race on your wrist.'], '_asc/k_a.jpg')
card('art/kart.jpg', ['DRIFT.', 'BOOST. WIN.'], ['A full kart championship', 'for Apple Watch'], '_asc/k_b.jpg', 0.74)
hero('art/staracce.jpg', 0.8, ['STARWING', 'ACE'], ['Dodge. Roll. Lock on.'], '_asc/s_a.jpg')
card('art/staracce.jpg', ['FIVE WORLDS.', 'FIVE BOSSES.'], ['An arcade space shooter', 'built for Apple Watch'], '_asc/s_b.jpg', 0.78)
print('ok')
