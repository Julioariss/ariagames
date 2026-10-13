#!/bin/zsh
# usage: slideshow.sh OUT.mp4 img1 img2 ... (2 s each, 720x1280, silent)
out=$1; shift
args=(); filt=""; n=0
for f in "$@"; do args+=(-i "$f"); filt+="[$n:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=24,zoompan=z='min(zoom+0.0008,1.12)':d=48:s=720x1280:fps=24[v$n];"; n=$((n+1)); done
for i in $(seq 0 $((n-1))); do filt+="[v$i]"; done
filt+="concat=n=$n:v=1:a=0[v]"
ffmpeg -y -loglevel error $args -filter_complex "$filt" -map "[v]" -c:v libx264 -pix_fmt yuv420p "$out"
