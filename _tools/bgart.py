import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
W, H = 1080, 1920

def lerp(a, b, t): return tuple(int(a[k] * (1 - t) + b[k] * t) for k in range(3))

def sky(top, mid, bot, hy=800):
    y = np.linspace(0, 1, H)[:, None]
    top, mid, bot = [np.array(c, float) for c in (top, mid, bot)]
    t1 = np.clip(y / (hy / H), 0, 1)
    a = top * (1 - t1[..., None]) + mid * t1[..., None]
    t2 = np.clip((y - hy / H) / (1 - hy / H), 0, 1)
    b = mid * (1 - t2[..., None]) + bot * t2[..., None]
    arr = np.where(y[..., None] < hy / H, a, b)
    arr = np.broadcast_to(arr, (H, W, 3))
    return Image.fromarray(arr.astype('uint8'), 'RGB').convert('RGBA')

def glow(im, cx, cy, r, col, alpha=200, blur=None):
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col + (alpha,))
    g = g.filter(ImageFilter.GaussianBlur(blur or r * 0.6))
    return Image.alpha_composite(im, g)

def ridge(im, y0, amp, col, seed, step=6, rough=1.0, fade=None):
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.28) for _ in range(5)]
    fr = [0.004, 0.009, 0.02, 0.043, 0.09]
    am = [1, .55, .3, .15, .06]
    pts = []
    for x in range(0, W + step, step):
        v = sum(am[k] * math.sin(x * fr[k] * rough + ph[k]) for k in range(5))
        pts.append((x, y0 - amp * v))
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    d.polygon(pts + [(W, H), (0, H)], fill=col + (255,))
    return Image.alpha_composite(im, l)

def mesas(im, y0, col, seed):
    rnd = random.Random(seed)
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    x = -40
    while x < W:
        w = rnd.randint(140, 320); h = rnd.randint(90, 260); s = rnd.randint(18, 40)
        d.polygon([(x, y0), (x + s, y0 - h), (x + w - s, y0 - h), (x + w, y0)], fill=col + (255,))
        d.rectangle((x, y0 - 6, x + w, H), fill=col + (255,))
        x += w + rnd.randint(-40, 60)
    return Image.alpha_composite(im, l)

def city(im, y0, col, win, seed, hmin=120, hmax=520, lit=0.45):
    rnd = random.Random(seed)
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    x = -10
    while x < W:
        w = rnd.randint(70, 160); h = rnd.randint(hmin, hmax)
        d.rectangle((x, y0 - h, x + w, H), fill=col + (255,))
        if rnd.random() < .3: d.rectangle((x + w // 2 - 3, y0 - h - 60, x + w // 2 + 3, y0 - h), fill=col + (255,))
        for wy in range(y0 - h + 18, y0 - 10, 26):
            for wx in range(x + 12, x + w - 14, 22):
                if rnd.random() < lit: d.rectangle((wx, wy, wx + 10, wy + 14), fill=win[rnd.randrange(len(win))] + (255,))
        x += w + rnd.randint(2, 14)
    return Image.alpha_composite(im, l)

def pines(im, y0, col, seed, n=14, hmin=130, hmax=300):
    rnd = random.Random(seed)
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for _ in range(n):
        x = rnd.randint(-30, W + 30); h = rnd.randint(hmin, hmax); w = h * .42
        for k in range(4):
            yy = y0 - h + k * h * .24; ww = w * (.35 + k * .22)
            d.polygon([(x, yy - h * .22), (x - ww, yy + h * .26), (x + ww, yy + h * .26)], fill=col + (255,))
        d.rectangle((x - 5, y0 - 20, x + 5, y0 + 6), fill=col + (255,))
    d.rectangle((0, y0, W, H), fill=col + (255,))
    return Image.alpha_composite(im, l)

def palms(im, col, seed, n=3):
    rnd = random.Random(seed)
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for side in (0, 1):
        for j in range(n // 2 + side):
            bx = rnd.randint(-20, 140) if side == 0 else rnd.randint(W - 140, W + 20)
            by = 900; top = (bx + (60 if side == 0 else -60) + rnd.randint(-20, 20), rnd.randint(330, 520))
            d.line([(bx, by), ((bx + top[0]) / 2 + (30 if side == 0 else -30), (by + top[1]) / 2), top], fill=col + (255,), width=22, joint='curve')
            for k in range(7):
                a = -math.pi + k * math.pi / 6 + rnd.uniform(-.1, .1)
                ln = rnd.randint(150, 230)
                ex, ey = top[0] + ln * math.cos(a), top[1] + ln * math.sin(a) * .6 + 70
                mx, my = top[0] + ln * .5 * math.cos(a), top[1] + ln * .5 * math.sin(a) * .9 - 30
                d.line([top, (mx, my), (ex, ey)], fill=col + (255,), width=16, joint='curve')
    return Image.alpha_composite(im, l)

def streaks(im, seed, n=40, col=(255, 255, 255), alpha=70, cy=900):
    rnd = random.Random(seed)
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for _ in range(n):
        side = rnd.choice((-1, 1)); x = W // 2 + side * rnd.randint(380, 700)
        y = rnd.randint(300, 1800); ln = rnd.randint(160, 420)
        d.line([(x, y), (x - side * 30, y + ln)], fill=col + (rnd.randint(alpha // 2, alpha),), width=rnd.randint(3, 9))
    return Image.alpha_composite(im, l)

def sparkles(im, seed, n=60, col=(255, 255, 255), ymax=800):
    rnd = random.Random(seed)
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for _ in range(n):
        x, y = rnd.randint(0, W), rnd.randint(0, ymax); r = rnd.randint(2, 6)
        d.ellipse((x - r, y - r, x + r, y + r), fill=col + (rnd.randint(120, 255),))
    return Image.alpha_composite(im, l)

def confetti(im, seed, n=55):
    rnd = random.Random(seed)
    cs = [(255, 220, 70), (255, 90, 90), (90, 220, 255), (255, 255, 255), (150, 255, 130), (255, 140, 230)]
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for _ in range(n):
        x, y = rnd.randint(0, W), rnd.randint(40, 1850)
        if 120 < y < 700 and 150 < x < 930: continue
        s = rnd.randint(10, 22); a = rnd.uniform(0, 6.28)
        d.polygon([(x + s * math.cos(a + k * 1.57), y + s * .55 * math.sin(a + k * 1.57)) for k in range(4)], fill=rnd.choice(cs) + (230,))
    return Image.alpha_composite(im, l)

def checker(im, y, h=34):
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    s = h
    for r in range(2):
        for c in range(W // s + 1):
            if (r + c) % 2 == 0: d.rectangle((c * s, y + r * s, c * s + s, y + r * s + s), fill=(255, 255, 255, 235))
            else: d.rectangle((c * s, y + r * s, c * s + s, y + r * s + s), fill=(20, 20, 30, 235))
    return Image.alpha_composite(im, l)

def vignette(im, strength=170):
    y, x = np.ogrid[:H, :W]
    d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H * .45) / (H * .62)) ** 2)
    a = np.clip((d - .55) * strength / .8, 0, strength).astype('uint8')
    l = np.zeros((H, W, 4), 'uint8'); l[..., 3] = a
    return Image.alpha_composite(im, Image.fromarray(l, 'RGBA'))

def grain_light(im):
    return im

SCENES = {}
def scene(i):
    s = i
    if i == 0:  # canyon sunset
        im = sky((70, 20, 90), (255, 120, 60), (255, 200, 110), 700)
        im = glow(im, 540, 620, 330, (255, 230, 150), 255)
        im = mesas(im, 780, (150, 60, 50), 1); im = mesas(im, 880, (110, 40, 45), 2)
        im = ridge(im, 1000, 60, (70, 25, 40), 3)
        im = streaks(im, 5, col=(255, 230, 190))
    elif i == 1:  # tropical bay
        im = sky((20, 110, 200), (90, 200, 240), (255, 235, 190), 640)
        im = glow(im, 780, 470, 230, (255, 250, 200), 255)
        im = ridge(im, 690, 55, (40, 140, 140), 2)
        l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
        for y in range(690, 1000):
            t = (y - 690) / 310; d.line([(0, y), (W, y)], fill=lerp((50, 190, 220), (10, 90, 160), t) + (255,))
        im = Image.alpha_composite(im, l)
        im = glow(im, 780, 720, 110, (255, 255, 220), 150)
        im = palms(im, (14, 70, 60), 4)
        im = sparkles(im, 7, 40, ymax=250, col=(255, 255, 255))
    elif i in (2, 7):  # neon city
        pal = [((18, 6, 60), (120, 20, 140), (255, 90, 150), (30, 10, 70)), ((5, 20, 60), (10, 110, 140), (60, 230, 200), (10, 30, 70))][i == 7]
        im = sky(pal[0], pal[1], pal[2], 760)
        im = glow(im, 540, 700, 320, pal[2], 200)
        im = city(im, 880, tuple(int(c * .5) for c in pal[1]), [(255, 220, 120), (140, 240, 255), (255, 120, 200)], 11, 140, 460, .3)
        im = city(im, 960, pal[3], [(255, 220, 120), (140, 240, 255), (255, 120, 200), (255, 255, 255)], 12, 100, 380, .5)
        im = streaks(im, 8, col=(160, 240, 255), alpha=90)
        im = sparkles(im, 9, 70, ymax=500)
    elif i in (3, 9):  # snow mountains / aurora
        pal = [((8, 20, 70), (50, 120, 200), (210, 240, 255)), ((60, 80, 160), (240, 160, 160), (255, 235, 210))][i == 9]
        im = sky(*pal, 700)
        if i == 3:
            for k, c in enumerate([(80, 255, 190), (120, 160, 255), (190, 110, 255)]):
                im = glow(im, 250 + k * 280, 250 + k * 40, 210, c, 120, 90)
        else:
            im = glow(im, 540, 640, 300, (255, 240, 190), 255)
        im = ridge(im, 760, 170, (170, 200, 235) if i == 3 else (190, 160, 200), 21, rough=.7)
        im = ridge(im, 860, 130, (225, 240, 255) if i == 3 else (240, 225, 235), 22, rough=.9)
        im = pines(im, 960, (18, 60, 70), 23)
        im = sparkles(im, 24, 90 if i == 3 else 40, ymax=700)
    elif i == 4:  # volcano
        im = sky((25, 5, 25), (160, 25, 30), (255, 140, 40), 720)
        im = glow(im, 540, 720, 360, (255, 190, 70), 230)
        im = ridge(im, 820, 120, (50, 12, 22), 31, rough=.6)
        l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
        d.polygon([(250, 900), (470, 470), (610, 470), (830, 900)], fill=(40, 10, 20, 255))
        d.polygon([(470, 470), (610, 470), (590, 500), (490, 500)], fill=(255, 130, 40, 255))
        im = Image.alpha_composite(im, l)
        im = glow(im, 540, 460, 120, (255, 200, 80), 220)
        im = ridge(im, 980, 50, (25, 6, 16), 32)
        im = sparkles(im, 33, 80, col=(255, 190, 90), ymax=700)
    elif i == 5:  # jungle
        im = sky((10, 80, 70), (80, 190, 110), (240, 240, 150), 700)
        im = glow(im, 540, 560, 300, (255, 255, 190), 230)
        im = ridge(im, 760, 90, (30, 120, 80), 41, rough=.8)
        im = ridge(im, 860, 70, (15, 90, 60), 42, rough=1.2)
        im = pines(im, 960, (8, 55, 40), 43, n=18, hmin=180, hmax=360)
        im = palms(im, (6, 45, 35), 44, 4)
        im = sparkles(im, 45, 50, col=(255, 255, 170), ymax=800)
    elif i == 6:  # underwater
        im = sky((6, 20, 90), (20, 110, 190), (80, 220, 230), 900)
        l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
        for k in range(9):
            x = 80 + k * 125
            d.polygon([(x, 0), (x + 70, 0), (x + 330, 1000), (x - 60, 1000)], fill=(255, 255, 255, 26))
        im = Image.alpha_composite(im, l)
        im = ridge(im, 880, 70, (10, 80, 130), 51)
        im = ridge(im, 960, 50, (8, 50, 110), 52, rough=1.4)
        rnd = random.Random(53); l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
        for k in range(40):
            x, y, r = rnd.randint(0, W), rnd.randint(200, 1800), rnd.randint(6, 26)
            d.ellipse((x - r, y - r, x + r, y + r), outline=(220, 250, 255, 170), width=3)
        im = Image.alpha_composite(im, l)
    else:  # 8 autumn forest
        im = sky((90, 40, 100), (250, 150, 70), (255, 215, 120), 700)
        im = glow(im, 540, 600, 300, (255, 235, 150), 240)
        im = ridge(im, 770, 100, (170, 80, 50), 61, rough=.8)
        im = ridge(im, 870, 80, (140, 60, 40), 62, rough=1.1)
        im = pines(im, 970, (90, 35, 30), 63, n=16, hmin=170, hmax=330)
        im = sparkles(im, 64, 60, col=(255, 200, 90), ymax=800)
    im = streaks(im, 100 + i, 26, alpha=50)
    im = checker(im, 0, 26) if False else im
    im = confetti(im, 200 + i)
    im = vignette(im)
    return im.convert('RGB')
