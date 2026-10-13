import addlang as A, re, os
NL=['ARIAgames — Games gemaakt voor Apple Watch','Zoek Apple Watch-games','Games','Op je pols','Binnenkort in de App Store','Racen · Nieuw',
 '16 originele banen, 5 cups en gekke voertuigen die vliegen en drijven — alles bestuurd met de Digital Crown.',
 'Ontdek de game','Ruimteshooter · Nieuw',
 'Ontwijk, rol en lock vijanden in vijf werelden — en neem het op tegen vijf unieke eindbazen met een volledige orkestscore.',
 'Racen · US$1.99','Ruimteshooter · US$1.99','De catalogus','Alleen op','Racen','Ruimteshooter',
 'Racen · Apple Watch',
 'Een compleet kampioenschap op je pols. Drift voor mini-turbo’s, doe tricks in de lucht en race tegen vrienden in de buurt via lokaal wifi of Bluetooth.',
 'Originele banen','Cups','Coureurs','Karts die veranderen in vliegtuigen en boten','VS-race met maximaal 4 horloges in de buurt',
 'Voor elke baan gecomponeerde muziek','US$1.99 · Binnenkort','Ruimteshooter · Apple Watch',
 'Bestuur de Vanguard van de asteroïdengordel tot het vijandelijke vlaggenschip. Ontwijk vuur, lock vijanden en gooi bommen — met één kroon en één duim.',
 'Missies','Unieke eindbazen','Epische soundtrack','Ontwijkgerichte railgevechten met automatisch richten','Gesproken radiomeldingen van je wingman',
 'Originele orkestsoundtrack','Gemaakt voor de pols','Grote games.','Klein scherm.',
 'Wij porteren geen telefoongames. Elke ARIAgames-titel is vanaf nul ontworpen voor de Digital Crown, haptiek en een scherm van 45 mm.',
 'Digital Crown','Haptiek','Geen advertenties','Geen accounts','Geen tracking','Eén aankoop','Speel op je pols.',
 'Kart Watch GP en Star Ace : Watch Shooter komen binnenkort naar de App Store.','Updates &amp; support',
 '© 2026 ARIAgames · Onafhankelijke games gemaakt in Chili','Privacy','Support','Muziek uit','Muziek aan',
 'Muziek aan- of uitzetten',
 'Games in consolestijl, alleen voor Apple Watch. Kart Watch GP en Star Ace : Watch Shooter — één aankoop, geen advertenties, geen accounts.',
 'Games alleen voor Apple Watch.',
 'Vereist Apple Watch Series 10 of nieuwer (incl. Ultra 3).']
PL=['ARIAgames — Gry stworzone dla Apple Watch','Szukaj gier na Apple Watch','Gry','Na twoim nadgarstku','Wkrótce w App Store','Wyścigi · Nowość',
 '16 oryginalnych tras, 5 pucharów i szalone pojazdy, które latają i pływają — wszystko sterowane Digital Crown.',
 'Poznaj grę','Strzelanka kosmiczna · Nowość',
 'Uchylaj się, turlaj i namierzaj cele w pięciu światach — a potem stań naprzeciw pięciu wyjątkowych bossów przy pełnej orkiestrowej ścieżce dźwiękowej.',
 'Wyścigi · US$1.99','Strzelanka kosmiczna · US$1.99','Katalog','Tylko na','Wyścigi','Strzelanka kosmiczna',
 'Wyścigi · Apple Watch',
 'Pełne mistrzostwa na nadgarstku. Driftuj dla mini-turbo, wykonuj sztuczki w powietrzu i ścigaj się ze znajomymi w pobliżu przez lokalne Wi-Fi lub Bluetooth.',
 'Oryginalne trasy','Puchary','Kierowcy','Gokarty zmieniające się w samoloty i łodzie','Wyścig VS z maks. 4 zegarkami w pobliżu',
 'Muzyka skomponowana do każdej trasy','US$1.99 · Wkrótce','Strzelanka kosmiczna · Apple Watch',
 'Pilotuj Vanguard od pasa asteroid aż do okrętu flagowego wroga. Odbijaj ogień, namierzaj cele i zrzucaj bomby — jedną koroną i jednym kciukiem.',
 'Misje','Wyjątkowi bossowie','Epicka ścieżka dźwiękowa','Walka na szynach oparta na unikach, z automatycznym celowaniem','Głosowe komunikaty radiowe skrzydłowego',
 'Oryginalna orkiestrowa ścieżka dźwiękowa','Stworzone dla nadgarstka','Wielkie gry.','Mały ekran.',
 'Nie portujemy gier z telefonów. Każdy tytuł ARIAgames jest projektowany od zera pod Digital Crown, haptykę i ekran 45 mm.',
 'Digital Crown','Haptyka','Bez reklam','Bez kont','Bez śledzenia','Jednorazowy zakup','Graj na nadgarstku.',
 'Kart Watch GP i Star Ace : Watch Shooter wkrótce w App Store.','Aktualności i wsparcie',
 '© 2026 ARIAgames · Niezależne gry z Chile','Prywatność','Wsparcie','Muzyka wyłączona','Muzyka włączona',
 'Włącz lub wyłącz muzykę',
 'Gry w stylu konsolowym tylko na Apple Watch. Kart Watch GP i Star Ace : Watch Shooter — jednorazowy zakup, bez reklam, bez kont.',
 'Gry tylko na Apple Watch.',
 'Wymaga Apple Watch Series 10 lub nowszego (w tym Ultra 3).']
TR=['ARIAgames — Apple Watch için tasarlanmış oyunlar','Apple Watch oyunları ara','Oyunlar','Bileğinde','Yakında App Store’da','Yarış · Yeni',
 '16 orijinal pist, 5 kupa ve uçan, yüzen çılgın araçlar — hepsi Digital Crown ile yönetiliyor.',
 'Oyunu keşfet','Uzay nişancı · Yeni',
 'Beş dünyada kaç, yuvarlan ve hedefe kilitlen — sonra tam orkestra müziği eşliğinde beş benzersiz patronla yüzleş.',
 'Yarış · US$1.99','Uzay nişancı · US$1.99','Katalog','Yalnızca','Yarış','Uzay nişancı',
 'Yarış · Apple Watch',
 'Bileğinde eksiksiz bir şampiyona. Mini turbo için drift yap, havada numaralar çek ve yakındaki arkadaşlarınla yerel Wi-Fi veya Bluetooth üzerinden yarış.',
 'Orijinal pistler','Kupalar','Yarışçılar','Uçağa ve tekneye dönüşen kartlar','Yakındaki 4 saate kadar VS yarışı',
 'Her pist için bestelenmiş müzik','US$1.99 · Yakında','Uzay nişancı · Apple Watch',
 'Vanguard’ı asteroit kuşağından düşman amiral gemisine kadar uçur. Ateşi savur, hedefe kilitlen ve bomba at — bir taç ve bir başparmakla.',
 'Görevler','Benzersiz patronlar','Epik müzik','Kaçınmaya odaklı ray savaşı, otomatik hedefleme','Sesli kanat adamı telsiz çağrıları',
 'Orijinal orkestra müziği','Bilek için tasarlandı','Büyük oyunlar.','Küçük ekran.',
 'Telefon oyunlarını taşımıyoruz. Her ARIAgames oyunu Digital Crown, dokunsal geri bildirim ve 45 mm ekran için sıfırdan tasarlanır.',
 'Digital Crown','Dokunsal geri bildirim','Reklam yok','Hesap yok','İzleme yok','Tek seferlik satın alma','Bileğinde oyna.',
 'Kart Watch GP ve Star Ace : Watch Shooter yakında App Store’da.','Haberler ve destek',
 '© 2026 ARIAgames · Şili’den bağımsız oyunlar','Gizlilik','Destek','Müzik kapalı','Müzik açık',
 'Müziği aç/kapat',
 'Yalnızca Apple Watch için konsol tarzı oyunlar. Kart Watch GP ve Star Ace : Watch Shooter — tek seferlik satın alma, reklam yok, hesap yok.',
 'Yalnızca Apple Watch için oyunlar.',
 'Apple Watch Series 10 veya üzeri gerektirir (Ultra 3 dahil).']
ID=['ARIAgames — Game yang dibuat untuk Apple Watch','Cari game Apple Watch','Game','Di pergelangan tanganmu','Segera hadir di App Store','Balap · Baru',
 '16 lintasan orisinal, 5 piala, dan kendaraan gila yang bisa terbang dan mengapung — semua dikendalikan dengan Digital Crown.',
 'Jelajahi game','Penembak luar angkasa · Baru',
 'Menghindar, berguling, dan kunci target di lima dunia — lalu hadapi lima bos unik dengan musik orkestra penuh.',
 'Balap · US$1.99','Penembak luar angkasa · US$1.99','Katalog','Hanya di','Balap','Penembak luar angkasa',
 'Balap · Apple Watch',
 'Kejuaraan lengkap di pergelangan tanganmu. Drift untuk mini-turbo, aksi di udara, dan balapan dengan teman terdekat lewat Wi-Fi lokal atau Bluetooth.',
 'Lintasan orisinal','Piala','Pembalap','Kart yang berubah jadi pesawat dan perahu','Balapan VS hingga 4 jam tangan terdekat',
 'Musik yang dikomposisi untuk setiap lintasan','US$1.99 · Segera hadir','Penembak luar angkasa · Apple Watch',
 'Kemudikan Vanguard dari sabuk asteroid hingga kapal induk musuh. Tangkis tembakan, kunci target, dan jatuhkan bom — dengan satu crown dan satu jempol.',
 'Misi','Bos unik','Musik epik','Pertempuran rel berfokus menghindar dengan bidik otomatis','Radio suara dari rekan terbang',
 'Musik orkestra orisinal','Dibuat untuk pergelangan tangan','Game besar.','Layar mungil.',
 'Kami tidak memporting game ponsel. Setiap judul ARIAgames dirancang dari nol untuk Digital Crown, haptik, dan layar 45 mm.',
 'Digital Crown','Haptik','Tanpa iklan','Tanpa akun','Tanpa pelacakan','Sekali beli','Main di pergelangan tanganmu.',
 'Kart Watch GP dan Star Ace : Watch Shooter segera hadir di App Store.','Kabar &amp; dukungan',
 '© 2026 ARIAgames · Game indie buatan Chili','Privasi','Dukungan','Musik mati','Musik hidup',
 'Nyalakan atau matikan musik',
 'Game bergaya konsol khusus Apple Watch. Kart Watch GP dan Star Ace : Watch Shooter — sekali beli, tanpa iklan, tanpa akun.',
 'Game khusus untuk Apple Watch.',
 'Memerlukan Apple Watch Series 10 atau lebih baru (termasuk Ultra 3).']
TH=['ARIAgames — เกมที่สร้างมาเพื่อ Apple Watch','ค้นหาเกม Apple Watch','เกม','บนข้อมือของคุณ','เร็วๆ นี้บน App Store','แข่งรถ · ใหม่',
 'สนามต้นฉบับ 16 สนาม 5 ถ้วย และยานพาหนะสุดแปลกที่บินและลอยน้ำได้ — ควบคุมทั้งหมดด้วย Digital Crown',
 'สำรวจเกม','ยิงอวกาศ · ใหม่',
 'หลบ กลิ้ง และล็อกเป้าใน 5 โลก — แล้วเผชิญหน้าบอสสุดพิเศษ 5 ตัวพร้อมดนตรีออร์เคสตราเต็มรูปแบบ',
 'แข่งรถ · US$1.99','ยิงอวกาศ · US$1.99','แคตตาล็อก','เฉพาะบน','แข่งรถ','ยิงอวกาศ',
 'แข่งรถ · Apple Watch',
 'แชมเปี้ยนชิพเต็มรูปแบบบนข้อมือ ดริฟต์เพื่อมินิเทอร์โบ ทำท่าทางกลางอากาศ และแข่งกับเพื่อนใกล้ตัวผ่าน Wi-Fi ในพื้นที่หรือบลูทูธ',
 'สนามต้นฉบับ','ถ้วย','นักแข่ง','คาร์ตที่แปลงเป็นเครื่องบินและเรือ','แข่ง VS กับนาฬิกาใกล้เคียงสูงสุด 4 เรือน',
 'ดนตรีที่แต่งขึ้นสำหรับทุกสนาม','US$1.99 · เร็วๆ นี้','ยิงอวกาศ · Apple Watch',
 'ขับ Vanguard จากแถบดาวเคราะห์น้อยไปจนถึงเรือธงของศัตรู สะท้อนกระสุน ล็อกเป้า และทิ้งระเบิด — ด้วยเพียงครั่งหนึ่งอันกับนิ้วโป้งเดียว',
 'ภารกิจ','บอสสุดพิเศษ','ดนตรีสุดอลังการ','การต่อสู้บนราง เน้นการหลบ พร้อมเล็งอัตโนมัติ','วิทยุเสียงจากเพื่อนร่วมบิน',
 'ดนตรีออร์เคสตราต้นฉบับ','ออกแบบมาเพื่อข้อมือ','เกมใหญ่','หน้าจอจิ๋ว',
 'เราไม่พอร์ตเกมมือถือ ทุกเกมของ ARIAgames ออกแบบใหม่ทั้งหมดสำหรับ Digital Crown การตอบสนองแบบสัมผัส และหน้าจอ 45 มม.',
 'Digital Crown','การสั่นตอบสนอง','ไม่มีโฆษณา','ไม่ต้องมีบัญชี','ไม่ติดตาม','ซื้อครั้งเดียว','เล่นบนข้อมือของคุณ',
 'Kart Watch GP และ Star Ace : Watch Shooter กำลังจะมาบน App Store','ข่าวสารและการสนับสนุน',
 '© 2026 ARIAgames · เกมอินดี้จากชิลี','ความเป็นส่วนตัว','การสนับสนุน','ปิดเพลง','เปิดเพลง',
 'เปิดหรือปิดเพลง',
 'เกมสไตล์คอนโซลสำหรับ Apple Watch เท่านั้น Kart Watch GP และ Star Ace : Watch Shooter — ซื้อครั้งเดียว ไม่มีโฆษณา ไม่ต้องมีบัญชี',
 'เกมสำหรับ Apple Watch เท่านั้น',
 'ต้องใช้ Apple Watch Series 10 ขึ้นไป (รวม Ultra 3)']
NEW={'nl':(NL,'Downloaden in de App Store'),'pl':(PL,'Pobierz z App Store'),'tr':(TR,"App Store'dan indir"),'id':(ID,'Unduh di App Store'),'th':(TH,'ดาวน์โหลดบน App Store')}
page=A.page; ES=A.ES; EX=A.EXTRA_ES
for lang,(T,btn) in NEW.items():
    assert len(T)==len(ES),(lang,len(T),len(ES))
    pairs=list(zip(ES+EX,T+[btn]))
    h=page
    for i in sorted(range(len(pairs)),key=lambda i:-len(pairs[i][0])): h=h.replace(pairs[i][0],f'\x00{i}\x00')
    for i,(a,b) in enumerate(pairs): h=h.replace(f'\x00{i}\x00',b)
    h=h.replace('<html lang="es">',f'<html lang="{lang}">').replace('/es/privacy.html','/privacy.html').replace('/es/support.html','/support.html').replace('href="/es/"',f'href="/{lang}/"').replace('rel="canonical" href="https://ariagames.dev/es/"',f'rel="canonical" href="https://ariagames.dev/{lang}/"')
    os.makedirs(lang,exist_ok=True); open(f'{lang}/index.html','w',encoding='utf-8').write(h)
NAMES=[('en','English','/'),('es','Español','/es/'),('pt','Português','/pt/'),('de','Deutsch','/de/'),('fr','Français','/fr/'),('it','Italiano','/it/'),('nl','Nederlands','/nl/'),('pl','Polski','/pl/'),('tr','Türkçe','/tr/'),('ja','日本語','/ja/'),('ko','한국어','/ko/'),('th','ไทย','/th/'),('id','Indonesia','/id/'),('zh','简体中文','/zh/'),('zh-hant','繁體中文','/zh-hant/')]
HL={'zh':'zh-Hans','zh-hant':'zh-Hant'}
for f in ['index.html','index.src.html']+[f'{l}/index.html' for l,_,_ in NAMES if l!='en']:
    h=open(f,encoding='utf-8').read(); lang='en' if f.startswith('index') else f.split('/')[0]
    items=' · '.join(f'<b>{n}</b>' if l==lang else f'<a href="{p}" data-l="{l}">{n}</a>' for l,n,p in NAMES)
    h=re.sub(r'<nav class="langs"[^>]*>.*?</nav>',f'<nav class="langs" aria-label="Language">{items}</nav>',h,flags=re.S)
    alts=''.join(f'<link rel="alternate" hreflang="{HL.get(l,l)}" href="https://ariagames.dev{p}">' for l,_,p in NAMES)+'<link rel="alternate" hreflang="x-default" href="https://ariagames.dev/">'
    h=re.sub(r'(<link rel="alternate" hreflang="[^"]*" href="[^"]*">)+',alts,h,count=1)
    h=h.replace('it:1,ja:1,ko:1,zh:1','it:1,nl:1,pl:1,tr:1,ja:1,ko:1,th:1,id:1,zh:1')
    open(f,'w',encoding='utf-8').write(h)
print('ok')
