import os, sys
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_v3_20261024.py')).read()
exec(src[:src.index("import glob")])
O = f'{R}/content/2026-10-25/work'; os.makedirs(O, exist_ok=True)
G25 = f'{R}/content/2026-10-25/gem'
MUSIC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Downloads/ppmusic/Crystal_Throne_Gambit.mp3')
segs = []
segs.append(f'{O}/pp6_a.mp4'); clip_seg(segs[-1], f'{G25}/lila_flow1.mp4', 0.0, 4.0, txt('pp6_t0', ['Meet Lila.', 'The garden needs her.'], 1500, 76))
segs.append(f'{O}/pp6_b.mp4'); clip_seg(segs[-1], f'{G25}/lila_flow1.mp4', 4.0, 4.0, txt('pp6_t1', ['Weed King blocks the way'], 1560, 70))
segs.append(f'{O}/pp6_c.mp4'); clip_seg(segs[-1], f'{G25}/lila_flow2.mp4', 0.0, 3.6, txt('pp6_t2', ['Queen Orchid. Next boss.'], 1560, 70))
segs.append(f'{O}/pp6_d.mp4'); clip_seg(segs[-1], f'{G25}/lila_flow2.mp4', 3.8, 4.2, txt('pp6_t3', ['Then Emperor Eclipse...'], 1560, 70))
segs.append(f'{O}/pp6_g.mp4'); game_seg(segs[-1], f'{EP}/n_boss_en.mov', 3.5, 2.4, txt('pp6_gt', ['Match flowers. Chain combos.'], 1620, 70))
e = endcard('pp6_end', 'Poppy Pop', 'poppypop.png', 'Series 7+', (190, 90, 170))
segs.append(f'{O}/pp6_e.mp4'); still_seg(segs[-1], e, 3.0, framed=False)
finish(segs, MUSIC, 0, f'{R}/promo/daily_20261025_poppypop_en.mp4')
