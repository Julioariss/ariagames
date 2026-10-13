#!/usr/bin/env python3
"""Usage: build_reel.py RAW.mp4 ICON.png MUSIC.m4a OUT.mp4 "sub1|sub2|sub3"
Intro (0.8s ARIAgames logo on white) + clip with timed subtitles (original music, Gemini audio muted)
+ end card (real app icon on white + ariagames.dev, 1.5s). Output 1080x1920."""
import subprocess, sys, os, tempfile
from PIL import Image, ImageDraw, ImageFont
raw, icon, music, out, subs = sys.argv[1:6]
subs = subs.split("|")
W, H = 1080, 1920
root = os.path.expanduser("~/Documents/Claude/Projects/ariagames")
tmp = tempfile.mkdtemp()
FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def font(s): return ImageFont.truetype(FB, s)

def center(d, text, y, f, fill):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)

# intro card
logo = Image.open(f"{root}/img/logo.jpg").convert("RGB")
card = Image.new("RGB", (W, H), "white")
lw = 900; lh = int(logo.height * lw / logo.width)
card.paste(logo.resize((lw, lh)), ((W - lw) // 2, (H - lh) // 2))
card.save(f"{tmp}/intro.png")
# end card
card = Image.new("RGB", (W, H), "white")
ic = Image.open(icon).convert("RGB").resize((560, 560))
mask = Image.new("L", (560, 560), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, 559, 559), 125, fill=255)
card.paste(ic, ((W - 560) // 2, 600), mask)
d = ImageDraw.Draw(card)
center(d, "ariagames.dev", 1250, font(80), "black")
center(d, "Apple Watch only  -  $1.99", 1370, font(48), (90, 90, 90))
card.save(f"{tmp}/end.png")
# subtitle overlays (transparent PNG, bottom third)
clip_len = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", raw]).strip())
clip_len = min(clip_len, 10.0)
seg = clip_len / len(subs)
inputs = ["-i", f"{tmp}/intro.png", "-i", raw, "-i", f"{tmp}/end.png", "-i", music]
filt = []
# scale clip to 1080x1920
filt.append(f"[1:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps=30,trim=0:{clip_len},setpts=PTS-STARTPTS[c0]")
last = "c0"
for i, s in enumerate(subs):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    f = font(78)
    w = dd.textlength(s, font=f)
    pad = 36
    dd.rounded_rectangle(((W - w) / 2 - pad, 1380 - pad / 2, (W + w) / 2 + pad, 1380 + 100 + pad / 2), 36, fill=(0, 0, 0, 170))
    dd.text(((W - w) / 2, 1380), s, font=f, fill="white")
    p = f"{tmp}/sub{i}.png"; im.save(p)
    inputs += ["-loop", "1", "-i", p]
    idx = 4 + i
    filt.append(f"[{last}][{idx}:v]overlay=0:0:enable='between(t,{i*seg:.2f},{(i+1)*seg:.2f})'[c{i+1}]")
    last = f"c{i+1}"
filt.append(f"[0:v]scale={W}:{H},setsar=1,fps=30,trim=0:0.8,setpts=PTS-STARTPTS[iv]")
filt.append(f"[2:v]scale={W}:{H},setsar=1,fps=30,trim=0:1.5,setpts=PTS-STARTPTS[ev]")
filt.append(f"[iv][{last}][ev]concat=n=3:v=1:a=0[v]")
total = 0.8 + clip_len + 1.5
filt.append(f"[3:a]atrim=0:{total},afade=t=in:d=0.3,afade=t=out:st={total-0.8}:d=0.8,asetpts=PTS-STARTPTS[a]")
inputs_final = ["ffmpeg", "-y", "-loglevel", "error"]
# loop images for intro/end
inputs_final += ["-loop", "1", "-t", "1", "-i", f"{tmp}/intro.png", "-i", raw, "-loop", "1", "-t", "2", "-i", f"{tmp}/end.png", "-i", music]
for i in range(len(subs)):
    inputs_final += ["-loop", "1", "-t", f"{clip_len}", "-i", f"{tmp}/sub{i}.png"]
cmd = inputs_final + ["-filter_complex", ";".join(filt), "-map", "[v]", "-map", "[a]", "-t", f"{total}",
                      "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
subprocess.check_call(cmd)
print("OK", out, round(total, 1), "s")
