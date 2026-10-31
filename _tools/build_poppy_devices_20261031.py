import os, sys
from PIL import Image, ImageDraw
src = open(os.path.expanduser('~/Documents/Claude/Projects/ariagames/_tools/build_poppy_v3_20261024.py')).read()
exec(src[:src.index("import glob")])   # helpers: txt, endcard, sh, clip_seg, still_seg, finish, R, W, H
O = f'{R}/content/2026-10-31/work'; os.makedirs(O, exist_ok=True)
PP = os.path.expanduser('~/Developer/PetalPop')
VID = f'{PP}/iOSApp/Video'; PR = f'{PP}/dist/promo'
MUSIC = os.path.expanduser('~/Downloads/ppmusic/Floating_Garden.mp3')
BG = f'{PP}/iOSApp/ArtHD/bgHD20.jpg'

def frame_png(path, w, h, rad, bez, hole_inset, hole_rad, island=False, bands=False):
    S = 3
    im = Image.new('RGBA', (w*S, h*S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w*S-1, h*S-1], rad*S, fill=(18, 18, 24, 255), outline=(120, 120, 140, 255), width=3*S)
    hole = Image.new('L', im.size, 0); hd = ImageDraw.Draw(hole)
    hd.rounded_rectangle([bez*S, hole_inset*S, (w-bez)*S, (h-hole_inset)*S], hole_rad*S, fill=255)
    a = im.split()[3]; a = Image.composite(Image.new('L', im.size, 0), a, hole); im.putalpha(a)
    if island:
        ImageDraw.Draw(im).rounded_rectangle([(w/2-52)*S, (hole_inset+10)*S, (w/2+52)*S, (hole_inset+40)*S], 15*S, fill=(0, 0, 0, 255))
    im.resize((w, h), Image.LANCZOS).save(path)

PH_W, PH_H, PH_BZ = 560, 1180, 14
frame_png(f'{O}/f_phone.png', PH_W, PH_H, 62, PH_BZ, PH_BZ, 48, island=True)
WT_W, WT_H = 340, 410
frame_png(f'{O}/f_watch.png', WT_W, WT_H, 66, 14, 14, 52)
# watch bands drawn as part of a separate overlay
b = Image.new('RGBA', (WT_W-80, 150), (30, 30, 38, 255)); b.save(f'{O}/f_band.png')

def devices_seg(out, dur, overlay):
    # inputs: 0 bg, 1 phone mov, 2 watch mov, 3 phone frame, 4 watch frame, 5 band, 6 overlay
    px, py = 70, 360; wx, wy = 690, 930
    fc = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=18:3,eq=brightness=-0.12:saturation=1.15,"
          f"zoompan=z='1.06-0.03*on/{int(dur*30)}':d=1:s=1080x1920:fps=30[bg];"
          f"[1:v]scale={PH_W-2*PH_BZ}:{PH_H-2*PH_BZ}:force_original_aspect_ratio=increase,crop={PH_W-2*PH_BZ}:{PH_H-2*PH_BZ}[ph];"
          f"[2:v]scale={WT_W-28}:{WT_H-28}:force_original_aspect_ratio=increase,crop={WT_W-28}:{WT_H-28}[wt];"
          f"[bg][ph]overlay={px+PH_BZ}:'{py+PH_BZ}+60*max(0,1-t/0.7)*max(0,1-t/0.7)'[a];"
          f"[a][3:v]overlay={px}:'{py}+60*max(0,1-t/0.7)*max(0,1-t/0.7)'[b];"
          f"[b][5:v]overlay={wx+40}:'{wy-130}+80*max(0,1-(t-0.4)/0.7)*max(0,1-(t-0.4)/0.7)'[c0];"
          f"[c0][5:v]overlay={wx+40}:'{wy+WT_H-20}+80*max(0,1-(t-0.4)/0.7)*max(0,1-(t-0.4)/0.7)'[c1];"
          f"[c1][wt]overlay={wx+14}:'{wy+14}+80*max(0,1-(t-0.4)/0.7)*max(0,1-(t-0.4)/0.7)'[d];"
          f"[d][4:v]overlay={wx}:'{wy}+80*max(0,1-(t-0.4)/0.7)*max(0,1-(t-0.4)/0.7)'[e];[e][6:v]overlay=0:0[o]")
    sh(f'ffmpeg -v error -y -loop 1 -t {dur} -i "{BG}" -t {dur} -i "{PR}/ios_stage9.mov" -stream_loop -1 -t {dur} -ss 3 -i "{EP}/n_boss_en.mov" '
       f'-loop 1 -t {dur} -i {O}/f_phone.png -loop 1 -t {dur} -i {O}/f_watch.png -loop 1 -t {dur} -i {O}/f_band.png -loop 1 -t {dur} -i {overlay} '
       f'-filter_complex "{fc}" -map "[o]" -r 30 -t {dur} -pix_fmt yuv420p -an "{out}"')

EP = os.path.expanduser('~/Developer/PetalPop/dist/epic')

def phone_seg(out, mov, ss, dur, overlay):
    fc = ("[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:6,eq=brightness=-0.2[bg];"
          "[b]scale=-2:1500:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:140[c];[c][1:v]overlay=0:0[o]")
    sh(f'ffmpeg -v error -y -ss {ss} -t {dur} -i "{mov}" -i {overlay} -filter_complex "{fc}" -map "[o]" -r 30 -pix_fmt yuv420p -an "{out}"')

mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
ov_dev = txt('pd_dev', ['Poppy Pop', 'on Apple Watch', '+ iPhone & iPad'], 110, 74)
if mode == 'check':
    devices_seg(f'{O}/pd_dev_chk.mp4', 6, ov_dev)
    sh(f'ffmpeg -v error -y -ss 2 -i {O}/pd_dev_chk.mp4 -frames:v 1 {O}/pd_dev_chk.jpg')
    sys.exit()
segs = []
segs.append(f'{O}/pd_a.mp4'); clip_seg(segs[-1], f'{VID}/vid_intro.mp4', 0.0, 4.0, txt('pd_t0', ['A garden. A girl.', 'A story on your wrist.'], 1500, 74))
segs.append(f'{O}/pd_b.mp4'); clip_seg(segs[-1], f'{VID}/vid_boss9.mp4', 0.0, 3.2, txt('pd_t1', ['Beat the Weed King'], 1560, 72))
segs.append(f'{O}/pd_c.mp4'); clip_seg(segs[-1], f'{VID}/vid_boss14.mp4', 0.0, 3.2, txt('pd_t2', ['Duel every boss'], 1560, 72))
segs.append(f'{O}/pd_d.mp4'); devices_seg(segs[-1], 6.0, ov_dev)
segs.append(f'{O}/pd_g.mp4'); phone_seg(segs[-1], f'{PR}/ios_stage24.mov', 1.0, 3.4, txt('pd_gt', ['Chain flowers. Win duels.'], 1690, 70))
e = endcard('pd_end', 'Poppy Pop', 'poppypop.png', 'Apple Watch · iPhone · iPad', (190, 90, 170))
segs.append(f'{O}/pd_e.mp4'); still_seg(segs[-1], e, 3.0, framed=False)
finish(segs, MUSIC, 0, f'{R}/promo/daily_20261031_poppypop_devices_en.mp4')
