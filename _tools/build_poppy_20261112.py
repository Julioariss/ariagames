import os, sys
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_v3_20261024.py')).read()
exec(src[:src.index("import glob")])
O = f'{R}/content/2026-11-12/work'; os.makedirs(O, exist_ok=True)
G = f"{R}/content/2026-11-03/gem"
EPIC = os.path.expanduser('~/Developer/PetalPop/dist/epic')
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
build('p1112', ['Play Poppy Pop', 'with friends', 'online'],  f'{G}/lila_friends_garden.mp4',
  [(0.0, 3.0, 'Friends in the garden'), (3.2, 3.2, 'Challenge anyone'), (6.6, 3.0, 'Versus. Worldwide.')],
  [(f'{EPIC}/n_story_en.mov', 6.0, 'Real gameplay', 2.0), (f'{EPIC}/n_boss_en.mov', 7.0, 'Beat 50 chapters', 2.0)],
  ('Poppy Pop', 'poppypop.png', 'iPhone, iPad, Watch', (190, 90, 170)), f'{DL}/Bouncing_Petals.mp3', f'{R}/promo/daily_20261112_poppypop_en.mp4')
