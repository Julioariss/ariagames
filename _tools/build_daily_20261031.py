import os, sys
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_v3_20261024.py')).read()
exec(src[:src.index("import glob")])
O = f'{R}/content/2026-10-31/work'; os.makedirs(O, exist_ok=True)
G31 = f"{R}/content/2026-10-31/gem"; SIM = f"{R}/content/2026-10-25/sim"
DL = os.path.expanduser('~/Downloads')
def build(tag, hook, anime, anime_cuts, game, endargs, music, out):
    segs = [intro(f'{tag}_h', hook)]
    for i, (ss, t, cap) in enumerate(anime_cuts):
        segs.append(f'{O}/{tag}_a{i}.mp4'); clip_seg(segs[-1], anime, ss, t, txt(f'{tag}_t{i}', [cap], 1330, 76))
    for i, (f, ss, t, d) in enumerate(game):
        segs.append(f'{O}/{tag}_g{i}.mp4'); game_seg(segs[-1], f, ss, d, txt(f'{tag}_gt{i}', [t], 1620, 80))
    e = endcard(f'{tag}_end', *endargs)
    segs.append(f'{O}/{tag}_e.mp4'); still_seg(segs[-1], e, 3.0, framed=False)
    finish(segs, music, 0, out)
build('s31', ['Can your wrist fly', 'through asteroids?'], f'{G31}/staracce_gem_slalom.mp4',
      [(0.8, 2.2, 'Rocks everywhere'), (3.6, 2.2, 'Roll between them'), (6.6, 2.2, 'Never slow down')],
      [(f'{SIM}/en3.mov', 4.0, 'Real gameplay', 2.0), (f'{SIM}/en9.mov', 4.0, 'Dodge. Roll.', 2.0), (f'{SIM}/en6.mov', 6.0, 'Break the boss', 2.0)],
      ('STAR Ace', 'staracce.png', 'Series 10+', (40, 50, 140)), f'{DL}/Breach_of_the_Titan.mp3', f'{R}/promo/daily_20261031_staracce_en.mp4')
