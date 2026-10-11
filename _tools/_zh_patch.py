import re,os
os.chdir(os.path.expanduser('~/Documents/Claude/Projects/ariagames'))
s=open('i18n.py',encoding='utf-8').read()
if "'zh':" in s: raise SystemExit('already patched')
ZH=['ARIAgames — 专为 Apple Watch 打造的游戏','搜索 Apple Watch 游戏','游戏','就在你的手腕上','即将登陆 App Store','竞速 · 新作',
'16 条原创赛道、5 个杯赛，还有能飞能浮的疯狂载具——全部用数码表冠操控。',
'探索游戏','太空射击 · 新作',
'在五个世界中闪避、翻滚、锁定目标——然后挑战五位独特的 Boss，伴随完整的管弦乐配乐。',
'竞速 · US$1.99','太空射击 · US$1.99','游戏目录','仅限','竞速','太空射击',
'竞速 · Apple Watch',
'手腕上的完整锦标赛。漂移获得小氮气，空中特技，还能通过本地 Wi-Fi 或蓝牙与附近的朋友一起竞速。',
'原创赛道','杯赛','车手','能变成飞机和船的卡丁车','最多 4 块附近手表的对战竞速',
'为每条赛道量身创作的音乐','US$1.99 · 即将推出','太空射击 · Apple Watch',
'驾驶先锋号，从小行星带一路杀向敌方旗舰。弹开炮火、锁定目标、投下炸弹——只需一个表冠和一根拇指。',
'任务','独特 Boss','史诗配乐','以闪避为核心的轨道战斗，支持自动瞄准','语音僚机无线电通话',
'原创管弦乐配乐','为手腕而生','大游戏。','小屏幕。',
'我们从不移植手机游戏。ARIAgames 的每一款作品都为数码表冠、触感反馈和 45 毫米屏幕从零设计。',
'数码表冠','触感反馈','无广告','无需账号','无追踪','一次购买','在手腕上玩。',
'Kart Watch GP 和 Star Ace : Watch Shooter 即将登陆 App Store。','获取更新与支持',
'© 2026 ARIAgames · 来自智利的独立游戏','隐私','支持','音乐关闭','音乐开启',
'切换音乐',
'专为 Apple Watch 打造的主机风格游戏。Kart Watch GP 和 Star Ace : Watch Shooter——一次购买，无广告，无需账号。',
'只为 Apple Watch 而生的游戏。','需要 Apple Watch Series 10 或更新机型（含 Ultra 3）。']
assert len(ZH)==55,len(ZH)
code="import opencc\n_cc=opencc.OpenCC('s2twp')\nT['zh']="+repr(ZH)+"\nT['zh-hant']=[_cc.convert(x) for x in T['zh']]\n"
s=s.replace("for l, v in T.items():\n    assert",code+"for l, v in T.items():\n    assert",1)
s=s.replace("'ja':'日本語'}","'ja':'日本語','zh':'简体中文','zh-hant':'繁體中文'}")
s=s.replace('if({es:1,pt:1,de:1,fr:1,ja:1}[l]&&!location.hash)location.replace("/"+l+"/")','var n=(navigator.language||"").toLowerCase();if(l=="zh"&&/tw|hk|mo|hant/.test(n))l="zh-hant";if({es:1,pt:1,de:1,fr:1,ja:1,zh:1,"zh-hant":1}[l]&&!location.hash)location.replace("/"+l+"/")')
s=s.replace("<link rel=\"alternate\" hreflang=\"{l}\"","<link rel=\"alternate\" hreflang=\"{HL.get(l,l)}\"")
s=s.replace("BASE = 'https://ariagames.dev'","BASE = 'https://ariagames.dev'\nHL = {'zh':'zh-Hans','zh-hant':'zh-Hant'}")
open('i18n.py','w',encoding='utf-8').write(s)
print('patched')
