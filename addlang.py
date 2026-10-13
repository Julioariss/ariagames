import re, os, glob
src = open('i18n.py', encoding='utf-8').read()
ns = {}
pre = src.split("import opencc")[0].split("T = {",1)
exec("import re,os\n" + pre[0].split("SRC =",1)[0].split("import re, os",1)[1].replace("os.chdir(os.path.dirname(os.path.abspath(__file__)))","") if False else "")
# extract K and T['es'] by exec of K/T blocks
kblock = src[src.index("K = ["):src.index("T = {")]
exec(kblock, ns)
tblock = src[src.index("T = {"):src.index("REQ=")]
exec(tblock, ns)
K = ns['K']; ES = ns['T']['es']
IT = ['ARIAgames — Giochi creati per Apple Watch','Cerca giochi per Apple Watch','Giochi','Sul tuo polso','In arrivo su App Store','Corse · Novità',
 '16 piste originali, 5 coppe e veicoli pazzeschi che volano e galleggiano — tutto con la Digital Crown.',
 'Scopri il gioco','Sparatutto spaziale · Novità',
 'Schiva, rotola e aggancia i bersagli in cinque mondi — poi affronta cinque boss unici con una colonna sonora orchestrale completa.',
 'Corse · US$1.99','Sparatutto spaziale · US$1.99','Il catalogo','Solo su','Corse','Sparatutto spaziale',
 'Corse · Apple Watch',
 'Un campionato completo sul tuo polso. Derapa per i mini-turbo, fai acrobazie in aria e sfida gli amici vicini via Wi-Fi locale o Bluetooth.',
 'Piste originali','Coppe','Piloti','Kart che si trasformano in aerei e barche','Gara VS fino a 4 orologi vicini',
 'Musica composta per ogni pista','US$1.99 · In arrivo','Sparatutto spaziale · Apple Watch',
 'Pilota la Vanguard dalla fascia di asteroidi fino all’ammiraglia nemica. Devia i colpi, aggancia i bersagli e sgancia bombe — con una corona e un pollice.',
 'Missioni','Boss unici','Colonna sonora epica','Combattimento su binari basato sulla schivata, con mira automatica','Radio parlata del gregario',
 'Colonna sonora orchestrale originale','Creato per il polso','Grandi giochi.','Schermo minuscolo.',
 'Non portiamo i giochi da telefono. Ogni titolo ARIAgames è progettato da zero per la Digital Crown, l’aptica e uno schermo da 45 mm.',
 'Digital Crown','Aptica','Senza pubblicità','Senza account','Senza tracciamento','Un solo acquisto','Gioca sul tuo polso.',
 'Kart Watch GP e Star Ace : Watch Shooter arrivano presto su App Store.','Novità e assistenza',
 '© 2026 ARIAgames · Giochi indipendenti realizzati in Cile','Privacy','Assistenza','Musica disattivata','Musica attivata',
 'Attiva o disattiva la musica',
 'Giochi in stile console creati solo per Apple Watch. Kart Watch GP e Star Ace : Watch Shooter — un solo acquisto, niente pubblicità, niente account.',
 'Giochi creati solo per Apple Watch.',
 'Richiede Apple Watch Series 10 o successivo (incluso Ultra 3).']
KO = ['ARIAgames — Apple Watch를 위한 게임','Apple Watch 게임 검색','게임','당신의 손목 위에','App Store 출시 예정','레이싱 · 신작',
 '오리지널 트랙 16개, 컵 5개, 날고 물에 뜨는 별난 탈것 — 모두 디지털 크라운으로 조작합니다.',
 '게임 보기','우주 슈팅 · 신작',
 '다섯 개의 월드에서 피하고, 구르고, 록온하세요 — 그리고 풀 오케스트라 음악과 함께 독특한 보스 5명에 맞서세요.',
 '레이싱 · US$1.99','우주 슈팅 · US$1.99','카탈로그','전용:','레이싱','우주 슈팅',
 '레이싱 · Apple Watch',
 '손목 위의 완전한 챔피언십. 드리프트로 미니 터보, 공중 트릭, 가까운 친구와 로컬 Wi-Fi 또는 블루투스로 대결하세요.',
 '오리지널 트랙','컵','레이서','비행기와 배로 변신하는 카트','근처 시계 최대 4대와 VS 레이스',
 '모든 트랙을 위해 작곡된 음악','US$1.99 · 출시 예정','우주 슈팅 · Apple Watch',
 '소행성대에서 적 기함까지 뱅가드를 조종하세요. 총알을 튕겨내고, 록온하고, 폭탄을 투하 — 크라운 하나와 엄지 하나로.',
 '미션','독특한 보스','웅장한 사운드트랙','회피 중심의 레일 전투, 자동 조준 지원','음성 윙맨 무전',
 '오리지널 오케스트라 사운드트랙','손목을 위해 설계','큰 게임.','작은 화면.',
 '휴대폰 게임을 이식하지 않습니다. ARIAgames의 모든 타이틀은 디지털 크라운, 햅틱, 45mm 화면에 맞춰 처음부터 설계했습니다.',
 '디지털 크라운','햅틱','광고 없음','계정 불필요','추적 없음','한 번 구매','손목 위에서 플레이.',
 'Kart Watch GP와 Star Ace : Watch Shooter가 곧 App Store에 출시됩니다.','소식 및 지원',
 '© 2026 ARIAgames · 칠레에서 만든 인디 게임','개인정보 보호','지원','음악 끄기','음악 켜기',
 '음악 켜기/끄기',
 'Apple Watch 전용 콘솔 스타일 게임. Kart Watch GP와 Star Ace : Watch Shooter — 한 번 구매, 광고 없음, 계정 불필요.',
 'Apple Watch 전용 게임.',
 'Apple Watch Series 10 이상(Ultra 3 포함)이 필요합니다.']
ES = ES + ['Requiere Apple Watch Series 10 o posterior (incluye Ultra 3).']
EXTRA_ES = ['Descargar en el App Store']
EXTRA = {'it':['Scarica da App Store'],'ko':['App Store에서 다운로드']}
NEW = {'it':IT,'ko':KO}
assert len(IT)==len(ES)==len(KO), (len(IT),len(ES),len(KO))
page = open('es/index.html', encoding='utf-8').read()
for lang in NEW:
    h = page
    pairs = list(zip(ES+EXTRA_ES, NEW[lang]+EXTRA[lang]))
    order = sorted(range(len(pairs)), key=lambda i:-len(pairs[i][0]))
    for i in order: h = h.replace(pairs[i][0], f'\x00{i}\x00')
    for i,(a,b) in enumerate(pairs): h = h.replace(f'\x00{i}\x00', b)
    h = h.replace('<html lang="es">', f'<html lang="{lang}">')
    h = h.replace('/es/privacy.html','/privacy.html').replace('/es/support.html','/support.html')
    h = h.replace('href="/es/"', f'href="/{lang}/"')
    os.makedirs(lang, exist_ok=True)
    open(f'{lang}/index.html','w',encoding='utf-8').write(h)
NAMES = [('en','English','/'),('es','Español','/es/'),('pt','Português','/pt/'),('de','Deutsch','/de/'),('fr','Français','/fr/'),('it','Italiano','/it/'),('ja','日本語','/ja/'),('ko','한국어','/ko/'),('zh','简体中文','/zh/'),('zh-hant','繁體中文','/zh-hant/')]
HL = {'zh':'zh-Hans','zh-hant':'zh-Hant'}
BASE='https://ariagames.dev'
for f in ['index.html','index.src.html']+[f'{l}/index.html' for l,_,_ in NAMES if l!='en']:
    h = open(f,encoding='utf-8').read()
    lang = 'en' if f.startswith('index') else f.split('/')[0]
    items = ' · '.join(f'<b>{n}</b>' if l==lang else f'<a href="{p}" data-l="{l}">{n}</a>' for l,n,p in NAMES)
    h = re.sub(r'<nav class="langs"[^>]*>.*?</nav>', f'<nav class="langs" aria-label="Language">{items}</nav>', h, flags=re.S)
    if 'hreflang' in h:
        alts = ''.join(f'<link rel="alternate" hreflang="{HL.get(l,l)}" href="{BASE}{p}">' for l,_,p in NAMES)+f'<link rel="alternate" hreflang="x-default" href="{BASE}/">'
        h = re.sub(r'(<link rel="alternate" hreflang="[^"]*" href="[^"]*">)+', alts, h, count=1)
    h = h.replace('{es:1,pt:1,de:1,fr:1,ja:1,zh:1,"zh-hant":1}','{es:1,pt:1,de:1,fr:1,it:1,ja:1,ko:1,zh:1,"zh-hant":1}')
    open(f,'w',encoding='utf-8').write(h)
print('done')
