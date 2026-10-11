# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# Localizes privacy.html and support.html -> /<lang>/privacy.html, /<lang>/support.html
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
K = ['Privacy — ARIAgames','Support — ARIAgames','Games','Privacy','Support','Home',
 'Privacy policy','Your data stays on your watch','Applies to Kart Watch GP and Star Ace : Watch Shooter. Last updated: October 2026.',
 'What we collect','Nothing. The games have no accounts, no ads, no analytics and no tracking. We do not collect, store or share personal information.',
 'What stays on your device','Progress, settings and high scores are saved locally on your Apple Watch and never leave it.',
 'Local multiplayer','Versus races connect watches directly to each other over your local network. No game servers are involved, nothing is sent to us, and no personal information is exchanged beyond in-race gameplay data, which is discarded when the race ends.',
 'Third parties','The games do not include third-party SDKs for advertising or analytics. Purchases are handled entirely by Apple through the App Store.',
 'Children','The games collect no data from anyone, including children.','Contact','Questions:',
 'Need a hand?','Controls',
 'Turn the Digital Crown to steer or move through menus. Swipe or tap to act, and hold the screen centre for 3 seconds to open the pause menu in games that support it.',
 'Installing','Open the Watch app on your iPhone, find the game under Available Apps and tap Install. Games run on the watch itself.',
 'Purchases and refunds','Purchases and refunds are managed by Apple at','Still stuck','Write to',
 'with the game name, your watch model and watchOS version, and what happened.',
 'ARIAgames · Independent games made in Chile']
T = {
'es': ['Privacidad — ARIAgames','Soporte — ARIAgames','Juegos','Privacidad','Soporte','Inicio',
 'Política de privacidad','Tus datos se quedan en tu reloj','Se aplica a Kart Watch GP y Star Ace : Watch Shooter. Última actualización: octubre de 2026.',
 'Qué recopilamos','Nada. Los juegos no tienen cuentas, anuncios, analíticas ni rastreo. No recopilamos, almacenamos ni compartimos información personal.',
 'Qué queda en tu dispositivo','El progreso, los ajustes y las mejores puntuaciones se guardan localmente en tu Apple Watch y nunca salen de él.',
 'Multijugador local','Las carreras VS conectan los relojes directamente entre sí por tu red local. No hay servidores de juego, no se nos envía nada y no se intercambia información personal más allá de los datos de la carrera, que se descartan al terminar.',
 'Terceros','Los juegos no incluyen SDK de terceros de publicidad ni analítica. Apple gestiona las compras por completo a través de la App Store.',
 'Niños','Los juegos no recopilan datos de nadie, incluidos los niños.','Contacto','Consultas:',
 '¿Necesitas ayuda?','Controles',
 'Gira la corona digital para dirigir o moverte por los menús. Desliza o toca para actuar y mantén el centro de la pantalla 3 segundos para abrir el menú de pausa en los juegos que lo admiten.',
 'Instalación','Abre la app Watch en tu iPhone, busca el juego en Apps disponibles y toca Instalar. Los juegos funcionan en el propio reloj.',
 'Compras y reembolsos','Apple gestiona las compras y los reembolsos en','¿Sigues atascado?','Escribe a',
 'con el nombre del juego, el modelo de tu reloj, la versión de watchOS y lo que ocurrió.',
 'ARIAgames · Juegos independientes hechos en Chile'],
'pt': ['Privacidade — ARIAgames','Suporte — ARIAgames','Jogos','Privacidade','Suporte','Início',
 'Política de privacidade','Seus dados ficam no seu relógio','Aplica-se a Kart Watch GP e Star Ace : Watch Shooter. Última atualização: outubro de 2026.',
 'O que coletamos','Nada. Os jogos não têm contas, anúncios, análises nem rastreamento. Não coletamos, armazenamos nem compartilhamos informações pessoais.',
 'O que fica no seu dispositivo','Progresso, ajustes e recordes são salvos localmente no seu Apple Watch e nunca saem dele.',
 'Multijogador local','As corridas VS conectam os relógios diretamente entre si pela sua rede local. Não há servidores de jogo, nada é enviado a nós e nenhuma informação pessoal é trocada além dos dados da corrida, descartados ao final.',
 'Terceiros','Os jogos não incluem SDKs de terceiros de publicidade ou análise. As compras são tratadas inteiramente pela Apple na App Store.',
 'Crianças','Os jogos não coletam dados de ninguém, inclusive de crianças.','Contato','Dúvidas:',
 'Precisa de ajuda?','Controles',
 'Gire a coroa digital para direcionar ou navegar pelos menus. Deslize ou toque para agir e mantenha o centro da tela por 3 segundos para abrir o menu de pausa nos jogos compatíveis.',
 'Instalação','Abra o app Watch no iPhone, encontre o jogo em Apps disponíveis e toque em Instalar. Os jogos rodam no próprio relógio.',
 'Compras e reembolsos','Compras e reembolsos são gerenciados pela Apple em','Ainda com problemas?','Escreva para',
 'com o nome do jogo, o modelo do relógio, a versão do watchOS e o que aconteceu.',
 'ARIAgames · Jogos independentes feitos no Chile'],
'de': ['Datenschutz — ARIAgames','Support — ARIAgames','Spiele','Datenschutz','Support','Start',
 'Datenschutzerklärung','Deine Daten bleiben auf deiner Uhr','Gilt für Kart Watch GP und Star Ace : Watch Shooter. Zuletzt aktualisiert: Oktober 2026.',
 'Was wir erfassen','Nichts. Die Spiele haben keine Konten, keine Werbung, keine Analysen und kein Tracking. Wir erfassen, speichern oder teilen keine personenbezogenen Daten.',
 'Was auf deinem Gerät bleibt','Fortschritt, Einstellungen und Highscores werden lokal auf deiner Apple Watch gespeichert und verlassen sie nie.',
 'Lokaler Mehrspieler','VS-Rennen verbinden die Uhren direkt über dein lokales Netzwerk. Es gibt keine Spielserver, nichts wird an uns gesendet, und außer den Rennspieldaten, die nach dem Rennen verworfen werden, werden keine personenbezogenen Daten ausgetauscht.',
 'Drittanbieter','Die Spiele enthalten keine Drittanbieter-SDKs für Werbung oder Analyse. Käufe werden vollständig von Apple über den App Store abgewickelt.',
 'Kinder','Die Spiele erfassen von niemandem Daten, auch nicht von Kindern.','Kontakt','Fragen:',
 'Brauchst du Hilfe?','Steuerung',
 'Drehe die Digital Crown zum Lenken oder Navigieren in Menüs. Wische oder tippe zum Handeln und halte die Bildschirmmitte 3 Sekunden gedrückt, um in unterstützten Spielen das Pausenmenü zu öffnen.',
 'Installation','Öffne die Watch-App auf dem iPhone, suche das Spiel unter „Verfügbare Apps“ und tippe auf „Installieren“. Die Spiele laufen auf der Uhr selbst.',
 'Käufe und Rückerstattungen','Käufe und Rückerstattungen verwaltet Apple unter','Weiterhin Probleme?','Schreibe an',
 'mit dem Namen des Spiels, deinem Uhrenmodell, der watchOS-Version und was passiert ist.',
 'ARIAgames · Unabhängige Spiele aus Chile'],
'fr': ['Confidentialité — ARIAgames','Assistance — ARIAgames','Jeux','Confidentialité','Assistance','Accueil',
 'Politique de confidentialité','Vos données restent sur votre montre','S’applique à Kart Watch GP et Star Ace : Watch Shooter. Dernière mise à jour : octobre 2026.',
 'Ce que nous collectons','Rien. Les jeux n’ont ni compte, ni publicité, ni analyse, ni suivi. Nous ne collectons, ne stockons ni ne partageons aucune information personnelle.',
 'Ce qui reste sur votre appareil','La progression, les réglages et les meilleurs scores sont enregistrés localement sur votre Apple Watch et ne la quittent jamais.',
 'Multijoueur local','Les courses VS relient directement les montres entre elles via votre réseau local. Aucun serveur de jeu n’intervient, rien ne nous est envoyé et aucune information personnelle n’est échangée en dehors des données de course, supprimées à la fin de la course.',
 'Tiers','Les jeux n’incluent aucun SDK tiers de publicité ou d’analyse. Les achats sont entièrement gérés par Apple via l’App Store.',
 'Enfants','Les jeux ne collectent aucune donnée, y compris celles des enfants.','Contact','Questions :',
 'Besoin d’aide ?','Commandes',
 'Tournez la Digital Crown pour diriger ou naviguer dans les menus. Balayez ou touchez pour agir, et maintenez le centre de l’écran 3 secondes pour ouvrir le menu pause dans les jeux compatibles.',
 'Installation','Ouvrez l’app Watch sur votre iPhone, trouvez le jeu dans Apps disponibles et touchez Installer. Les jeux fonctionnent sur la montre elle-même.',
 'Achats et remboursements','Les achats et remboursements sont gérés par Apple sur','Toujours bloqué ?','Écrivez à',
 'avec le nom du jeu, le modèle de votre montre, la version de watchOS et ce qui s’est passé.',
 'ARIAgames · Jeux indépendants créés au Chili'],
'ja': ['プライバシー — ARIAgames','サポート — ARIAgames','ゲーム','プライバシー','サポート','ホーム',
 'プライバシーポリシー','データはあなたのウォッチの中だけに','Kart Watch GPおよびStar Ace : Watch Shooterに適用されます。最終更新：2026年10月。',
 '収集する情報','何も収集しません。ゲームにはアカウント、広告、分析、トラッキングがありません。個人情報の収集・保存・共有は一切行いません。',
 'デバイスに残るもの','進行状況、設定、ハイスコアはApple Watch内にローカル保存され、外部に出ることはありません。',
 'ローカルマルチプレイ','VSレースでは、ウォッチ同士がローカルネットワーク経由で直接接続されます。ゲームサーバーは使用せず、当社には何も送信されません。レース中のプレイデータ以外の個人情報は交換されず、そのデータもレース終了時に破棄されます。',
 '第三者','ゲームには、広告や分析のための第三者SDKは含まれていません。購入はすべてApple（App Store）が処理します。',
 'お子様','ゲームは、お子様を含め誰からもデータを収集しません。','お問い合わせ','ご質問：',
 'お困りですか？','操作方法',
 'デジタルクラウンを回して操作・メニュー移動ができます。スワイプまたはタップで操作し、対応ゲームでは画面中央を3秒間長押しするとポーズメニューが開きます。',
 'インストール','iPhoneのWatchアプリを開き、「利用可能なApp」からゲームを見つけて「インストール」をタップしてください。ゲームはウォッチ単体で動作します。',
 '購入と返金','購入と返金はAppleが次のページで管理しています：','解決しない場合','次のアドレスまでご連絡ください：',
 'ゲーム名、ウォッチのモデル、watchOSのバージョン、発生した状況を添えてください。',
 'ARIAgames · チリ発のインディーゲーム'],
}
import opencc
_cc=opencc.OpenCC('s2twp')
T['zh']=['隐私 — ARIAgames', '支持 — ARIAgames', '游戏', '隐私', '支持', '首页', '隐私政策', '你的数据只留在你的手表上', '适用于 Kart Watch GP 和 Star Ace : Watch Shooter。最后更新：2026 年 10 月。', '我们收集什么', '什么都不收集。游戏没有账号、广告、分析和追踪。我们不收集、存储或分享任何个人信息。', '留在你设备上的内容', '进度、设置和最高分都保存在你的 Apple Watch 本地，永远不会离开它。', '本地多人游戏', '对战竞速通过本地网络让手表彼此直接连接。不使用游戏服务器，不会向我们发送任何内容，除比赛过程中的游戏数据外不交换任何个人信息，这些数据在比赛结束后即被丢弃。', '第三方', '游戏不包含用于广告或分析的第三方 SDK。购买完全由 Apple 通过 App Store 处理。', '儿童', '游戏不会收集任何人的数据，包括儿童。', '联系方式', '问题请联系：', '需要帮助吗？', '操作方式', '转动数码表冠即可操控或浏览菜单。滑动或点按进行操作；在支持的游戏中，按住屏幕中央 3 秒可打开暂停菜单。', '安装', '在 iPhone 上打开“Watch”App，在“可用的 App”中找到游戏并点按“安装”。游戏直接在手表上运行。', '购买与退款', '购买和退款由 Apple 管理，请前往', '仍然无法解决？', '请发邮件至', '并注明游戏名称、手表型号、watchOS 版本以及发生的情况。', 'ARIAgames · 来自智利的独立游戏']
T['zh-hant']=[_cc.convert(x).replace('數碼','數位') for x in T['zh']]
for l, v in T.items(): assert len(v) == len(K), (l, len(v), len(K))
for lang, vals in T.items():
    tr = dict(zip(K, vals))
    for f in ('privacy.html', 'support.html'):
        h = open(f, encoding='utf-8').read()
        h = h.replace('<html lang="en">', f'<html lang="{lang}">')
        for k in sorted(K, key=len, reverse=True):
            h = re.sub(r'>(\s*)' + re.escape(k) + r'(\s*)<', lambda m: '>' + m.group(1) + tr[k] + m.group(2) + '<', h)
        h = h.replace('href="style.css', 'href="/style.css').replace('href="./"', f'href="/{lang}/"')
        h = h.replace('href="privacy.html"', f'href="/{lang}/privacy.html"').replace('href="support.html"', f'href="/{lang}/support.html"')
        os.makedirs(lang, exist_ok=True)
        open(f'{lang}/{f}', 'w', encoding='utf-8').write(h)
print('legal ok')
