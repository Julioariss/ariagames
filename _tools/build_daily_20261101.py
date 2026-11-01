import os, sys
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_v3_20261024.py')).read()
exec(src[:src.index("import glob")])
O = f'{R}/content/2026-11-01/work'; os.makedirs(O, exist_ok=True)
G = f"{R}/content/2026-11-01/gem"; SIM = f"{R}/content/2026-10-25/sim"; KC = f"{R}/content/2026-10-16/sim/clips"
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
which = sys.argv[1]
if which == 'star':
    build('s1101', ['Dodge 3 planet rings', 'in 8 seconds'], f'{G}/staracce_gem_rings.mp4',
      [(0.5, 2.2, 'Into the rings'), (3.2, 2.2, 'Bank hard'), (5.8, 2.2, 'Cosmo never slows')],
      [(f'{SIM}/en6.mov', 3.0, 'Real gameplay', 2.0), (f'{SIM}/en3.mov', 8.0, 'Lock on. Fire.', 2.0), (f'{SIM}/en9.mov', 9.0, 'Roll through', 2.0)],
      ('STAR Ace', 'staracce.png', 'Series 10+', (40, 50, 140)), f'{DL}/Assault_on_the_Veyra_Core.mp3', f'{R}/promo/daily_20261101_staracce_en.mp4')
elif which == 'kart':
    build('k1101', ['3 turns above', 'the clouds.', "Don't fall."], f'{G}/kartwatchgp_ada_clouds.mp4',
      [(0.5, 2.2, 'Ada takes the lead'), (3.0, 2.2, 'Drift the cloud bend'), (5.6, 2.2, 'Hold the line')],
      [(f'{KC}/c1.mp4', 4.0, 'Real gameplay', 2.0), (f'{KC}/c7.mp4', 6.0, 'Boost out', 2.0), (f'{KC}/c3.mp4', 8.0, 'Win the cup', 2.0)],
      ('Kart Watch GP', 'kart.png', 'Series 10+', (200, 50, 40)), f'{DL}/Full_Throttle_Rush.mp3', f'{R}/promo/daily_20261101_kartwatchgp_en.mp4')
else:
    build('p1101', ['1 flower starts', 'a chain of 12'], f'{G}/lila_flow_sunflowers.mp4',
      [(0.0, 2.4, 'Lila walks the sunflowers'), (2.8, 2.4, 'Flowers wake up'), (5.4, 2.4, 'Pop. Chain. Repeat.')],
      [(f'{EPIC}/n_story_en.mov', 3.2, 'Real gameplay', 2.0), (f'{EPIC}/n_boss_en.mov', 3.5, 'Beat 29 chapters', 2.0)],
      ('Poppy Pop', 'poppypop.png', 'Series 7+', (190, 90, 170)), f'{DL}/Sunlit_Petals.mp3', f'{R}/promo/daily_20261101_poppypop_en.mp4')
