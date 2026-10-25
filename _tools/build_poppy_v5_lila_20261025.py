import os, sys
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_v3_20261024.py')).read()
exec(src[:src.index("import glob")])
O = f'{R}/content/2026-10-25/work'; os.makedirs(O, exist_ok=True)
G25 = f'{R}/content/2026-10-25/gem'
MUSIC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Downloads/ppmusic/Floating_Garden.mp3')
def lila_seg(out, img, dur, overlay):
    fc = ("[0:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
          f"zoompan=z='1+0.0016*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30[b];[b][1:v]overlay=0:0[o]")
    sh(f'ffmpeg -v error -y -loop 1 -t {dur} -i "{img}" -i {overlay} -filter_complex "{fc}" -map "[o]" -r 30 -pix_fmt yuv420p -an "{out}"')
segs = [intro('pp5_h', ['Save the garden.', 'Beat the Emperor.'])]
for i, (img, d, cap) in enumerate([(f'{G25}/lila_vs_emperador.jpg', 2.8, 'Meet Lila. She will not give up'), (f'{G25}/lila_jardin.jpg', 2.4, 'Match flowers. Chain combos')]):
    segs.append(f'{O}/pp5_l{i}.mp4'); lila_seg(segs[-1], img, d, txt(f'pp5_t{i}', [cap], 1500, 70))
G = [('n_story_en.mov', 3.2, 'Chapter 1 · Sprout', 2.0), ('n_dlg_en.mov', 2.4, 'Chapter 29 · Emperor Eclipse', 2.0), ('n_boss_en.mov', 3.5, 'Chain combos to win', 2.2)]
for i, (f, ss, t, d) in enumerate(G):
    segs.append(f'{O}/pp5_g{i}.mp4'); game_seg(segs[-1], f'{EP}/{f}', ss, d, txt(f'pp5_gt{i}', [t], 1620, 76))
e = endcard('pp5_end', 'Poppy Pop', 'poppypop.png', 'Series 7+', (190, 90, 170))
segs.append(f'{O}/pp5_e.mp4'); still_seg(segs[-1], e, 3.0, framed=False)
finish(segs, MUSIC, 0, f'{R}/promo/daily_20261025_poppypop_en.mp4')
