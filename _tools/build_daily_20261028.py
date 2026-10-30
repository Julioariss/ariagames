import os, sys
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_v3_20261024.py')).read()
exec(src[:src.index("import glob")])
O = f'{R}/content/2026-10-28/work'; os.makedirs(O, exist_ok=True)
G25 = f"{R}/content/2026-10-25/gem"; SIM = f"{R}/content/2026-10-25/sim"
DL = os.path.expanduser('~/Downloads')
exec(open(f'{R}/_tools/build_daily_20261026.py').read().split("def build")[1].split("if which")[0].join(["def build",""]) if False else "")
def build(tag, hook, anime, anime_cuts, game, endargs, music, out):
    segs = [intro(f'{tag}_h', hook)]
    for i, (ss, t, cap) in enumerate(anime_cuts):
        segs.append(f'{O}/{tag}_a{i}.mp4'); clip_seg(segs[-1], anime, ss, t, txt(f'{tag}_t{i}', [cap], 1330, 76))
    for i, (f, ss, t, d) in enumerate(game):
        segs.append(f'{O}/{tag}_g{i}.mp4'); game_seg(segs[-1], f, ss, d, txt(f'{tag}_gt{i}', [t], 1620, 80))
    e = endcard(f'{tag}_end', *endargs)
    segs.append(f'{O}/{tag}_e.mp4'); still_seg(segs[-1], e, 3.0, framed=False)
    finish(segs, music, 0, out)
build('s28', ['You have 10 seconds', 'to dodge 3 missiles'], f'{G25}/staracce_gem1.mp4',
      [(1.0, 2.2, 'Missiles incoming'), (3.8, 2.2, 'Roll. Dodge.'), (6.6, 2.2, 'Lock on')],
      [(f'{SIM}/boss3.mov', 4.0, 'Real gameplay', 2.0), (f'{SIM}/boss6.mov', 5.0, 'Find the weak spot', 2.0), (f'{SIM}/en6.mov', 3.0, 'Break the boss', 2.0)],
      ('STAR Ace', 'staracce.png', 'Series 10+', (40, 50, 140)), f'{DL}/Assault_on_the_Veyra_Core.mp3', f'{R}/promo/daily_20261028_staracce_en.mp4')
