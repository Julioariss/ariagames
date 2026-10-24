import os, sys
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_v3_20261024.py')).read()
# reuse helpers/definitions of v3 (everything before the segment assembly)
exec(src[:src.index("import glob")])
MUSIC = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser('~/Downloads/ppmusic/Crystal_Throne_Gambit.mp3')
segs = [intro('pp4_h', ['Save the garden.', 'Beat the Emperor.'])]
# 1) epic anime clip: hero vs Emperor
for i, (ss, t, cap) in enumerate([(0.2, 2.3, 'The Emperor wants the flowers'), (3.2, 2.0, 'One florist says NO')]):
    segs.append(f'{O}/pp4_a{i}.mp4'); clip_seg(segs[-1], ANIME, ss, t, txt(f'pp4_t{i}', [cap], 1330, 70))
# 2) game story arc: stage 1 -> chapter 29 -> boss
G = [('n_story_en.mov', 3.2, 'Chapter 1 · Sprout', 2.0),
     ('n_dlg_en.mov', 2.4, 'Chapter 29 · Emperor Eclipse', 2.0),
     ('n_boss_en.mov', 3.5, 'Chain combos to win', 2.2)]
for i, (f, ss, t, d) in enumerate(G):
    segs.append(f'{O}/pp4_g{i}.mp4'); game_seg(segs[-1], f'{EP}/{f}', ss, d, txt(f'pp4_gt{i}', [t], 1620, 76))
e = endcard('pp4_end', 'Poppy Pop', 'poppypop.png', 'Series 7+', (190, 90, 170))
segs.append(f'{O}/pp4_e.mp4'); still_seg(segs[-1], e, 3.0, framed=False)
finish(segs, MUSIC, 0, f'{R}/promo/daily_20261024_poppypop_en.mp4')
