import os, sys
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_v3_20261024.py')).read()
exec(src[:src.index("import glob")])   # helpers: txt, endcard, sh, clip_seg, still_seg, finish, intro, game_seg, R, O, EP
O = f'{R}/content/2026-10-26/work'; os.makedirs(O, exist_ok=True)
G25 = f"{R}/content/2026-10-25/gem"
SIM = f"{R}/content/2026-10-25/sim"
DL = os.path.expanduser('~/Downloads')
which = sys.argv[1]

def build(tag, hook, anime, anime_cuts, game, endargs, music, out):
    segs = [intro(f'{tag}_h', hook)]
    for i, (ss, t, cap) in enumerate(anime_cuts):
        segs.append(f'{O}/{tag}_a{i}.mp4'); clip_seg(segs[-1], anime, ss, t, txt(f'{tag}_t{i}', [cap], 1330, 76))
    for i, (f, ss, t, d) in enumerate(game):
        segs.append(f'{O}/{tag}_g{i}.mp4'); game_seg(segs[-1], f, ss, d, txt(f'{tag}_gt{i}', [t], 1620, 80))
    e = endcard(f'{tag}_end', *endargs)
    segs.append(f'{O}/{tag}_e.mp4'); still_seg(segs[-1], e, 3.0, framed=False)
    finish(segs, music, 0, out)

if which == 'star':
    build('s26', ['Can a watch', 'beat a leviathan?'], f'{G25}/staracce_galaxia.mp4',
          [(0.3, 2.2, 'Into the nebula'), (3.0, 2.2, 'The leviathan wakes'), (5.8, 2.2, 'Lock on'), ],
          [(f'{SIM}/en9.mov', 3.0, 'Real gameplay', 2.0), (f'{SIM}/en3.mov', 8.5, 'Dodge the barrage', 2.0), (f'{SIM}/en6.mov', 9.0, 'Break the boss', 2.0)],
          ('STAR Ace', 'staracce.png', 'Series 10+', (40, 50, 140)), f'{DL}/Gravity_Breach.mp3', f'{R}/promo/daily_20261026_staracce_en.mp4')
elif which == 'kart':
    K = f'{R}/content/2026-10-16/sim/clips'
    build('k25', ["You'll lose this race", 'in 3 turns'], f'{G25}/kartwatchgp_gem1.mp4',
          [(0.2, 2.2, 'Hairpin ahead'), (3.2, 2.2, 'Drift. Boost.'), (6.3, 2.2, '3 rivals on your tail')],
          [(f'{K}/c1.mp4', 6.0, 'Real gameplay', 2.0), (f'{K}/c7.mp4', 7.5, 'Grab power-ups', 2.0), (f'{K}/c3.mp4', 9.0, 'Win the cup', 2.0)],
          ('Kart Watch GP', 'kart.png', 'Series 10+', (200, 50, 40)), f'{DL}/Summit_of_Cinders.mp3', f'{R}/promo/daily_20261025_kartwatchgp_en.mp4')
else:
    build('p25', ['The Emperor stole', 'every garden'], f'{R}/content/2026-10-24/gem/poppypop_gem4.mp4',
          [(5.0, 2.2, 'Flowers answer her spell'), (6.8, 2.2, 'Chain the blooms'), (7.8, 2.2, 'Take the gardens back')],
          [(f'{EP}/n_story_en.mov', 6.2, 'Match and chain', 2.0), (f'{EP}/n_map_en.mov', 3.0, 'Reach Chapter 29', 2.0), (f'{EP}/n_boss_en.mov', 6.5, 'Face the Emperor', 2.0)],
          ('Poppy Pop', 'poppypop.png', 'Series 7+', (190, 90, 170)), f'{DL}/ppmusic/Sea_King_s_Ballroom.mp3', f'{R}/promo/daily_20261025_poppypop_en.mp4')

