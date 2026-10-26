import os, sys
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_v3_20261024.py')).read()
exec(src[:src.index("import glob")])
O = f'{R}/content/2026-10-26/work'; os.makedirs(O, exist_ok=True)
G25 = f'{R}/content/2026-10-25/gem'
MUSIC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Downloads/ppmusic/Frost_Petal_Logic.mp3')
segs = []
segs.append(f'{O}/pp7_a.mp4'); clip_seg(segs[-1], f'{G25}/lila_flow2.mp4', 3.8, 3.6, txt('pp7_t0', ['One girl. One watch.', 'One dark Emperor.'], 1500, 76))
segs.append(f'{O}/pp7_b.mp4'); clip_seg(segs[-1], f'{G25}/lila_flow1.mp4', 4.0, 3.6, txt('pp7_t1', ['Weed King blocks her way'], 1560, 70))
segs.append(f'{O}/pp7_c.mp4'); clip_seg(segs[-1], f'{G25}/lila_flow1.mp4', 0.0, 3.4, txt('pp7_t2', ['Lila never gives up'], 1560, 70))
segs.append(f'{O}/pp7_g.mp4'); game_seg(segs[-1], f'{EP}/n_boss_en.mov', 3.5, 3.0, txt('pp7_gt', ['Chain flowers. Beat 29 chapters.'], 1620, 70))
e = endcard('pp7_end', 'Poppy Pop', 'poppypop.png', 'Series 7+', (190, 90, 170))
segs.append(f'{O}/pp7_e.mp4'); still_seg(segs[-1], e, 3.0, framed=False)
finish(segs, MUSIC, 0, f'{R}/promo/daily_20261026_poppypop_en.mp4')
