import os,re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SOON={'index.html':'Coming soon','es/index.html':'Próximamente','pt/index.html':'Em breve','de/index.html':'Demnächst','fr/index.html':'Bientôt','ja/index.html':'近日公開','zh/index.html':'即将推出','zh-hant/index.html':'即將推出'}
for p,so in SOON.items():
    t=open(p,encoding='utf-8').read()
    n0=t.count(so)
    # kart section button text in this language (full "US$1.99 · soon" string)
    m=re.search(r'<span class="btn red">(US\$1\.99[^<]*)</span>',t); full=m.group(1)
    a=t.index('data-i="2"'); 
    t=t.replace('<span class="price">%s</span>'%so,'<span class="price">US$1.99</span>')
    t=re.sub(r'(data-go="2".*?<small>[^<]*? · )%s'%re.escape(so),r'\1US$1.99',t,count=1,flags=re.S)
    t=t.replace('<span class="pr">%s</span>'%so,'<span class="pr">US$1.99</span>')
    t=t.replace('<span class="btn red">%s</span>'%so,'<span class="btn red">%s</span>'%full)
    open(p,'w',encoding='utf-8').write(t)
    print(p,n0,t.count(so))
