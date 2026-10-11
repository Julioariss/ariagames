#!/usr/bin/env python3
# Generates /es /pt /de /fr /ja from index.src.html (English source). Run: python3 i18n.py
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists('index.src.html'):
    open('index.src.html', 'w', encoding='utf-8').write(open('index.html', encoding='utf-8').read())
SRC = open('index.src.html', encoding='utf-8').read()

K = ['ARIAgames — Games built for Apple Watch',
 'Search Apple Watch games', 'Games', 'On your wrist', 'Coming to App Store', 'Racing · New',
 '16 original tracks, 5 cups and wild vehicles that fly and float — all steered with the Digital Crown.',
 'Explore the game', 'Space shooter · New',
 'Dodge, roll and lock on across five worlds — then face five unique bosses with a full orchestral score.',
 'Racing · US$1.99', 'Space shooter · US$1.99', 'The catalog', 'Only on', 'Racing', 'Space shooter',
 'Racing · Apple Watch',
 'A complete championship on your wrist. Drift for mini-turbos, pull mid-air tricks, and race friends nearby over local Wi-Fi or Bluetooth.',
 'Original tracks', 'Cups', 'Racers', 'Karts that turn into planes and boats', 'VS Race with up to 4 nearby watches',
 'Music composed for every track', 'US$1.99 · Coming soon', 'Space shooter · Apple Watch',
 'Pilot the Vanguard from the asteroid belt to the enemy flagship. Deflect fire, lock on, and drop bombs — all with a Crown and a thumb.',
 'Missions', 'Unique bosses', 'Epic score', 'Dodge-focused rail combat with auto-target', 'Spoken wingman radio calls',
 'Original orchestral soundtrack', 'Built for the wrist', 'Big games.', 'Tiny screen.',
 "We don't port phone games. Every ARIAgames title is designed from scratch for the Digital Crown, haptics and a 45 mm screen.",
 'Digital Crown', 'Haptics', 'No ads', 'No accounts', 'No tracking', 'One purchase', 'Play on your wrist.',
 'Kart Watch GP and Star Ace : Watch Shooter are coming to the App Store.', 'Get updates &amp; support',
 '© 2026 ARIAgames · Independent games made in Chile', 'Privacy', 'Support', 'Music off', 'Music on',
 'Toggle music',
 'Console-style games made only for Apple Watch. Kart Watch GP and Star Ace : Watch Shooter — one purchase, no ads, no accounts.',
 'Games built only for Apple Watch.']

T = {
'es': ['ARIAgames — Juegos hechos para Apple Watch','Buscar juegos de Apple Watch','Juegos','En tu muñeca','Próximamente en la App Store','Carreras · Nuevo',
 '16 pistas originales, 5 copas y vehículos locos que vuelan y flotan — todo con la corona digital.',
 'Explorar el juego','Disparos espaciales · Nuevo',
 'Esquiva, rueda y fija el objetivo en cinco mundos — y enfréntate a cinco jefes únicos con una banda sonora orquestal completa.',
 'Carreras · US$1.99','Disparos espaciales · US$1.99','El catálogo','Solo en','Carreras','Disparos espaciales',
 'Carreras · Apple Watch',
 'Un campeonato completo en tu muñeca. Derrapa para mini-turbos, haz acrobacias en el aire y corre con amigos cercanos por Wi-Fi local o Bluetooth.',
 'Pistas originales','Copas','Pilotos','Karts que se transforman en aviones y botes','Carrera VS con hasta 4 relojes cercanos',
 'Música compuesta para cada pista','US$1.99 · Próximamente','Disparos espaciales · Apple Watch',
 'Pilota la Vanguard desde el cinturón de asteroides hasta la nave insignia enemiga. Desvía disparos, fija el objetivo y lanza bombas — con una corona y un pulgar.',
 'Misiones','Jefes únicos','Banda sonora épica','Combate sobre rieles centrado en esquivar, con autoapuntado','Radio del copiloto con voz',
 'Banda sonora orquestal original','Hecho para la muñeca','Grandes juegos.','Pantalla diminuta.',
 'No portamos juegos de teléfono. Cada título de ARIAgames está diseñado desde cero para la corona digital, la háptica y una pantalla de 45 mm.',
 'Corona digital','Háptica','Sin anuncios','Sin cuentas','Sin rastreo','Una sola compra','Juega en tu muñeca.',
 'Kart Watch GP y Star Ace : Watch Shooter llegan pronto a la App Store.','Novedades y soporte',
 '© 2026 ARIAgames · Juegos independientes hechos en Chile','Privacidad','Soporte','Música apagada','Música encendida',
 'Activar o desactivar música',
 'Juegos estilo consola hechos solo para Apple Watch. Kart Watch GP y Star Ace : Watch Shooter — una compra, sin anuncios, sin cuentas.',
 'Juegos hechos solo para Apple Watch.'],
'pt': ['ARIAgames — Jogos feitos para Apple Watch','Buscar jogos de Apple Watch','Jogos','No seu pulso','Em breve na App Store','Corrida · Novo',
 '16 pistas originais, 5 copas e veículos malucos que voam e flutuam — tudo com a coroa digital.',
 'Conhecer o jogo','Tiro espacial · Novo',
 'Desvie, role e trave o alvo em cinco mundos — e enfrente cinco chefes únicos com trilha sonora orquestral completa.',
 'Corrida · US$1.99','Tiro espacial · US$1.99','O catálogo','Somente no','Corrida','Tiro espacial',
 'Corrida · Apple Watch',
 'Um campeonato completo no seu pulso. Derrape para mini-turbos, faça manobras no ar e corra com amigos por perto via Wi-Fi local ou Bluetooth.',
 'Pistas originais','Copas','Pilotos','Karts que viram aviões e barcos','Corrida VS com até 4 relógios por perto',
 'Música composta para cada pista','US$1.99 · Em breve','Tiro espacial · Apple Watch',
 'Pilote a Vanguard do cinturão de asteroides até a nave-capitânia inimiga. Desvie dos tiros, trave o alvo e lance bombas — com uma coroa e um polegar.',
 'Missões','Chefes únicos','Trilha épica','Combate sobre trilhos focado em esquiva, com mira automática','Rádio do ala com voz',
 'Trilha sonora orquestral original','Feito para o pulso','Jogos grandes.','Tela minúscula.',
 'Não portamos jogos de celular. Cada título da ARIAgames é criado do zero para a coroa digital, a resposta háptica e uma tela de 45 mm.',
 'Coroa digital','Resposta háptica','Sem anúncios','Sem contas','Sem rastreamento','Compra única','Jogue no seu pulso.',
 'Kart Watch GP e Star Ace : Watch Shooter chegam em breve à App Store.','Novidades e suporte',
 '© 2026 ARIAgames · Jogos independentes feitos no Chile','Privacidade','Suporte','Música desligada','Música ligada',
 'Ligar ou desligar a música',
 'Jogos estilo console feitos só para Apple Watch. Kart Watch GP e Star Ace : Watch Shooter — compra única, sem anúncios, sem contas.',
 'Jogos feitos só para Apple Watch.'],
'de': ['ARIAgames — Spiele für die Apple Watch','Apple-Watch-Spiele suchen','Spiele','Am Handgelenk','Bald im App Store','Rennen · Neu',
 '16 originale Strecken, 5 Cups und wilde Fahrzeuge, die fliegen und schwimmen — alles per Digital Crown gesteuert.',
 'Spiel entdecken','Weltraum-Shooter · Neu',
 'Weiche aus, rolle dich und erfasse Ziele in fünf Welten — und stelle dich fünf einzigartigen Bossen mit vollem Orchester-Soundtrack.',
 'Rennen · US$1.99','Weltraum-Shooter · US$1.99','Der Katalog','Nur auf der','Rennen','Weltraum-Shooter',
 'Rennen · Apple Watch',
 'Eine komplette Meisterschaft am Handgelenk. Drifte für Mini-Turbos, zeige Tricks in der Luft und fahre gegen Freunde in der Nähe per lokalem WLAN oder Bluetooth.',
 'Originale Strecken','Cups','Fahrer','Karts, die zu Flugzeugen und Booten werden','VS-Rennen mit bis zu 4 Uhren in der Nähe',
 'Für jede Strecke komponierte Musik','US$1.99 · Demnächst','Weltraum-Shooter · Apple Watch',
 'Steuere die Vanguard vom Asteroidengürtel bis zum feindlichen Flaggschiff. Lenke Feuer ab, erfasse Ziele und wirf Bomben — mit einer Krone und einem Daumen.',
 'Missionen','Einzigartige Bosse','Epischer Soundtrack','Ausweich-fokussierter Schienenkampf mit Zielautomatik','Gesprochene Funksprüche des Flügelmanns',
 'Originaler Orchester-Soundtrack','Gemacht fürs Handgelenk','Große Spiele.','Winziger Bildschirm.',
 'Wir portieren keine Handyspiele. Jeder ARIAgames-Titel ist von Grund auf für die Digital Crown, Haptik und ein 45-mm-Display entwickelt.',
 'Digital Crown','Haptik','Keine Werbung','Keine Konten','Kein Tracking','Einmal kaufen','Spiele am Handgelenk.',
 'Kart Watch GP und Star Ace : Watch Shooter erscheinen bald im App Store.','Updates &amp; Support',
 '© 2026 ARIAgames · Unabhängige Spiele aus Chile','Datenschutz','Support','Musik aus','Musik an',
 'Musik ein- oder ausschalten',
 'Spiele im Konsolenstil, nur für die Apple Watch. Kart Watch GP und Star Ace : Watch Shooter — einmal kaufen, keine Werbung, keine Konten.',
 'Spiele nur für die Apple Watch.'],
'fr': ['ARIAgames — Des jeux conçus pour l’Apple Watch','Rechercher des jeux Apple Watch','Jeux','À votre poignet','Bientôt sur l’App Store','Course · Nouveau',
 '16 circuits originaux, 5 coupes et des véhicules fous qui volent et flottent — le tout piloté avec la Digital Crown.',
 'Découvrir le jeu','Tir spatial · Nouveau',
 'Esquivez, roulez et verrouillez vos cibles dans cinq mondes — puis affrontez cinq boss uniques avec une bande-son orchestrale complète.',
 'Course · US$1.99','Tir spatial · US$1.99','Le catalogue','Uniquement sur','Course','Tir spatial',
 'Course · Apple Watch',
 'Un championnat complet à votre poignet. Dérapez pour des mini-turbos, réalisez des figures dans les airs et affrontez des amis à proximité en Wi-Fi local ou Bluetooth.',
 'Circuits originaux','Coupes','Pilotes','Des karts qui se transforment en avions et en bateaux','Course VS jusqu’à 4 montres à proximité',
 'Musique composée pour chaque circuit','US$1.99 · Bientôt','Tir spatial · Apple Watch',
 'Pilotez le Vanguard de la ceinture d’astéroïdes jusqu’au vaisseau amiral ennemi. Déviez les tirs, verrouillez vos cibles et larguez des bombes — avec une couronne et un pouce.',
 'Missions','Boss uniques','Bande-son épique','Combat sur rails axé sur l’esquive, avec visée automatique','Appels radio parlés de votre ailier',
 'Bande-son orchestrale originale','Pensé pour le poignet','De grands jeux.','Un tout petit écran.',
 'Nous ne portons pas de jeux de téléphone. Chaque titre ARIAgames est conçu de zéro pour la Digital Crown, le retour haptique et un écran de 45 mm.',
 'Digital Crown','Retour haptique','Sans publicité','Sans compte','Sans suivi','Un seul achat','Jouez à votre poignet.',
 'Kart Watch GP et Star Ace : Watch Shooter arrivent bientôt sur l’App Store.','Actualités &amp; assistance',
 '© 2026 ARIAgames · Jeux indépendants créés au Chili','Confidentialité','Assistance','Musique coupée','Musique activée',
 'Activer ou couper la musique',
 'Des jeux de style console conçus uniquement pour l’Apple Watch. Kart Watch GP et Star Ace : Watch Shooter — un seul achat, sans publicité, sans compte.',
 'Des jeux conçus uniquement pour l’Apple Watch.'],
'ja': ['ARIAgames — Apple Watch専用ゲーム','Apple Watchゲームを検索','ゲーム','あなたの手首で','App Storeに近日登場','レース · 新作',
 'オリジナル16コース、5つのカップ、空を飛び水に浮かぶ変わった乗り物 — すべてデジタルクラウンで操作。',
 'ゲームを見る','シューティング · 新作',
 '5つのワールドで避けて、ローリングして、ロックオン — さらに、フルオーケストラの音楽とともに5体の個性的なボスに挑め。',
 'レース · US$1.99','シューティング · US$1.99','カタログ','専用:','レース','シューティング',
 'レース · Apple Watch',
 '手首で楽しむ本格チャンピオンシップ。ドリフトでミニターボ、空中トリック、近くの友だちとローカルWi-FiやBluetoothで対戦。',
 'オリジナルコース','カップ','レーサー','飛行機や船に変身するカート','近くの最大4台のウォッチでVS対戦',
 '全コースに作曲されたBGM','US$1.99 · 近日公開','シューティング · Apple Watch',
 '小惑星帯から敵の旗艦まで、ヴァンガードを操縦。弾を弾き、ロックオンし、爆弾を投下 — クラウン1つと親指1本で。',
 'ミッション','個性的なボス','壮大なサウンドトラック','回避重視のレールバトル（オートターゲット対応）','ボイス付きの僚機無線',
 'オリジナル・オーケストラ音楽','手首のために設計','大きなゲーム。','小さな画面。',
 'スマホゲームの移植はしません。ARIAgamesの全作品は、デジタルクラウン、触覚、45mmの画面のためにゼロから設計しています。',
 'デジタルクラウン','触覚フィードバック','広告なし','アカウント不要','トラッキングなし','買い切り','手首でプレイ。',
 'Kart Watch GPとStar Ace : Watch Shooterは、まもなくApp Storeに登場します。','最新情報とサポート',
 '© 2026 ARIAgames · チリ発のインディーゲーム','プライバシー','サポート','音楽オフ','音楽オン',
 '音楽のオン/オフ',
 'Apple Watch専用のコンソール風ゲーム。Kart Watch GPとStar Ace : Watch Shooter — 買い切り、広告なし、アカウント不要。',
 'Apple Watch専用のゲーム。'],
}
REQ='Requires Apple Watch Series 10 or later (including Ultra 3).'
K.append(REQ)
T['es'].append('Requiere Apple Watch Series 10 o posterior (incluye Ultra 3).')
T['pt'].append('Requer Apple Watch Series 10 ou posterior (inclui Ultra 3).')
T['de'].append('Erfordert Apple Watch Series 10 oder neuer (inkl. Ultra 3).')
T['fr'].append('Nécessite une Apple Watch Series 10 ou ultérieure (Ultra 3 incluse).')
T['ja'].append('Apple Watch Series 10以降（Ultra 3を含む）が必要です。')
for l, v in T.items():
    assert len(v) == len(K), (l, len(v), len(K))
NAMES = {'en':'English','es':'Español','pt':'Português','de':'Deutsch','fr':'Français','ja':'日本語'}
BASE = 'https://ariagames.dev'
MET = (K[-3], K[-2])

def build(lang):
    h = SRC
    tr = dict(zip(K, T[lang]))
    h = h.replace('<html lang="en">', f'<html lang="{lang}">')
    h = h.replace(K[0], tr[K[0]])
    for k in MET:
        h = h.replace(f'content="{k}"', f'content="{tr[k]}"')
    h = h.replace('aria-label="Toggle music"', f'aria-label="{tr["Toggle music"]}"')
    for k in sorted(K, key=len, reverse=True):
        if k in MET or k in ('Toggle music', 'Music on', 'Music off') or k == K[0]: continue
        h = re.sub(r'>(\s*)' + re.escape(k) + r'(\s*)<', lambda m: '>' + m.group(1) + tr[k] + m.group(2) + '<', h)
    for k in ('Music on', 'Music off'):
        h = h.replace("'" + k + "'", "'" + tr[k].replace("'", "\\'") + "'")
        h = re.sub(r'>' + k + '<', '>' + tr[k] + '<', h)
    h = re.sub(r'(href|src)="(style\.css[^"]*|intro\.html|art/|img/|shots/|music/|support\.html|privacy\.html)',
               lambda m: f'{m.group(1)}="/{m.group(2)}', h)
    h = h.replace('href="./"', f'href="/{lang}/"')
    h = h.replace('href="/privacy.html', f'href="/{lang}/privacy.html').replace('href="/support.html', f'href="/{lang}/support.html')
    return h

def path(l): return '/' if l == 'en' else f'/{l}/'
def alternates(lang):
    o = [f'<link rel="canonical" href="{BASE}{path(lang)}">']
    o += [f'<link rel="alternate" hreflang="{l}" href="{BASE}{path(l)}">' for l in NAMES]
    o.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}/">')
    return ''.join(o)
def switcher(lang):
    items = ' · '.join(f'<b>{n}</b>' if l == lang else f'<a href="{path(l)}" data-l="{l}">{n}</a>' for l, n in NAMES.items())
    return f'<nav class="langs" aria-label="Language">{items}</nav>'
SAVE = '<script>document.querySelectorAll(".langs a").forEach(function(a){a.addEventListener("click",function(){try{localStorage.setItem("ariaLang",a.dataset.l)}catch(e){}})})</script>'
AUTO = '<script>(function(){try{if(localStorage.getItem("ariaLang"))return;var l=(navigator.language||"en").slice(0,2).toLowerCase();if({es:1,pt:1,de:1,fr:1,ja:1}[l]&&!location.hash)location.replace("/"+l+"/")}catch(e){}})()</script>'

def finish(h, lang, auto=False):
    h = h.replace('</head>', (AUTO if auto else '') + alternates(lang) + '</head>', 1)
    h = h.replace('<button id="snd"', switcher(lang) + '<button id="snd"', 1)
    return h.replace('</body>', SAVE + '</body>', 1)

for lang in T:
    os.makedirs(lang, exist_ok=True)
    open(f'{lang}/index.html', 'w', encoding='utf-8').write(finish(build(lang), lang))
open('index.html', 'w', encoding='utf-8').write(finish(SRC, 'en', auto=True))
print('ok', list(T))
