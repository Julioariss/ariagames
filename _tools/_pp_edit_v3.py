import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s=open('index.src.html',encoding='utf-8').read()
import re
def rep(a,b,cnt=1):
    global s
    pat=r'\s*'.join(re.escape(x) for x in re.split(r'\s+',a.strip()))
    m=re.search(pat,s)
    assert m,a[:60]
    s=s[:m.start()]+b+s[m.end():]
rep('<a href="#starwingace">Star Ace : Watch Shooter</a><a href="#watch">','<a href="#starwingace">Star Ace : Watch Shooter</a><a href="#petalpop">Petal Pop</a><a href="#watch">')
slide='''  <div class="slide" data-i="2"><img class="bg" src="art/petalpop.jpg" alt="Petal Pop" style="object-position:50% 50%"><div class="shade"></div>
   <div class="info"><span class="tag">@PP_TAG@</span><h2>Petal Pop</h2><p>@PP_DESC@</p><div class="row"><a class="btn red" href="#petalpop">Explore the game</a><span class="price">@PP_SOON@</span></div></div></div>
 </div> <div class="list">'''
rep('</div> <div class="list">',slide)
rep('<i></i></button> </div></div></div><div class="marq">','<i></i></button>\n  <button class="item" data-go="2"><img src="img/petalpop.png" alt=""><span><b>Petal Pop</b><small>@PP_GENRE@ · @PP_SOON@</small></span><i></i></button> </div></div></div><div class="marq">')
rep('<span class="pr">US$1.99</span></div></a> </div></div></section><section id="kart"','<span class="pr">US$1.99</span></div></a>\n  <a class="card rv" href="#petalpop"><img class="art" src="art/petalpop.jpg" alt="" style="object-position:50% 50%"><div class="glass"><img src="img/petalpop.png" alt=""><span><b>Petal Pop</b><small>@PP_GENRE@</small></span><span class="pr">@PP_SOON@</span></div></a> </div></div></section><section id="kart"')
sec='''<section id="petalpop" style="padding-top:20px"><div class="wrap game">
 <div class="shot rv"><img src="art/petalpop.jpg" alt="Petal Pop" style="object-position:50% 50%"></div>
 <div class="copy rv"><span class="mono">@PP_MONO@</span><h3>Petal <em>Pop</em></h3>
  <p>@PP_P@</p>
  <ul class="ticks"><li>@PP_T1@</li><li>@PP_T2@</li><li>@PP_T3@</li></ul>
  <div class="row"><span class="btn red">@PP_SOON@</span></div><p class="req">Requires Apple Watch Series 10 or later (including Ultra 3).</p></div></div></section><section class="watchband" id="watch">'''
rep('<section class="watchband" id="watch">',sec)
rep('<span>Star Ace : Watch Shooter</span><span>One purchase','<span>Star Ace : Watch Shooter</span><span>Petal Pop</span><span>One purchase')
rep('<p>Kart Watch GP and Star Ace : Watch Shooter are coming to the App Store.</p>','<p>@PP_CTA@</p>')
open('index.src.html','w',encoding='utf-8').write(s)
