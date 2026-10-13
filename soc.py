import re
files=["index.html","index.src.html"]+[f"{l}/index.html" for l in "es pt de fr ja zh zh-hant".split()]
SOC='<span class="soc"><a href="https://www.instagram.com/ariagames.app" target="_blank" rel="noopener" aria-label="Instagram">Instagram</a><a href="https://www.tiktok.com/@ariagames.app" target="_blank" rel="noopener" aria-label="TikTok">TikTok</a><a href="https://www.xiaohongshu.com/search_result?keyword=95991233062" target="_blank" rel="noopener" aria-label="Xiaohongshu">小红书</a></span>'
for f in files:
    s=open(f,encoding="utf-8").read()
    if 'class="soc"' in s: print(f,"skip"); continue
    n=re.sub(r'(<span><a href="[^"]*privacy\.html">)',SOC+r'\1',s,count=1)
    print(f,"ok" if n!=s else "NOMATCH"); open(f,"w",encoding="utf-8").write(n)
c=open("style.css",encoding="utf-8").read()
if ".soc" not in c:
    open("style.css","a",encoding="utf-8").write("\nfooter .soc a{margin-left:0;margin-right:20px}footer .soc a:before{content:'';}\n")
