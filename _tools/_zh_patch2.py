import os,re
os.chdir(os.path.expanduser('~/Documents/Claude/Projects/ariagames'))
# legal
s=open('i18n_legal.py',encoding='utf-8').read()
if "'zh':" not in s:
    ZL=['隐私 — ARIAgames','支持 — ARIAgames','游戏','隐私','支持','首页',
'隐私政策','你的数据只留在你的手表上','适用于 Kart Watch GP 和 Star Ace : Watch Shooter。最后更新：2026 年 10 月。',
'我们收集什么','什么都不收集。游戏没有账号、广告、分析和追踪。我们不收集、存储或分享任何个人信息。',
'留在你设备上的内容','进度、设置和最高分都保存在你的 Apple Watch 本地，永远不会离开它。',
'本地多人游戏','对战竞速通过本地网络让手表彼此直接连接。不使用游戏服务器，不会向我们发送任何内容，除比赛过程中的游戏数据外不交换任何个人信息，这些数据在比赛结束后即被丢弃。',
'第三方','游戏不包含用于广告或分析的第三方 SDK。购买完全由 Apple 通过 App Store 处理。',
'儿童','游戏不会收集任何人的数据，包括儿童。','联系方式','问题请联系：',
'需要帮助吗？','操作方式',
'转动数码表冠即可操控或浏览菜单。滑动或点按进行操作；在支持的游戏中，按住屏幕中央 3 秒可打开暂停菜单。',
'安装','在 iPhone 上打开“Watch”App，在“可用的 App”中找到游戏并点按“安装”。游戏直接在手表上运行。',
'购买与退款','购买和退款由 Apple 管理，请前往','仍然无法解决？','请发邮件至',
'并注明游戏名称、手表型号、watchOS 版本以及发生的情况。',
'ARIAgames · 来自智利的独立游戏']
    code="import opencc\n_cc=opencc.OpenCC('s2twp')\nT['zh']="+repr(ZL)+"\nT['zh-hant']=[_cc.convert(x).replace('數碼','數位') for x in T['zh']]\n"
    s=s.replace("for l, v in T.items(): assert",code+"for l, v in T.items(): assert",1)
    open('i18n_legal.py','w',encoding='utf-8').write(s)
# digital crown wording for zh-hant in main i18n
m=open('i18n.py',encoding='utf-8').read()
m=m.replace("T['zh-hant']=[_cc.convert(x) for x in T['zh']]","T['zh-hant']=[_cc.convert(x).replace('數碼','數位') for x in T['zh']]")
open('i18n.py','w',encoding='utf-8').write(m)
# post scripts
def add(path,anchor,newtxt):
    t=open(path,encoding='utf-8').read()
    if "'zh/index.html'" in t or "'zh':dict" in t: return
    assert anchor in t,(path,anchor)
    open(path,'w',encoding='utf-8').write(t.replace(anchor,newtxt+anchor,1))
add('_tools/_pp_aid.py',"}\nfor p,v in A.items()","'zh/index.html':'由 Julio Aris 设计与开发。艺术作品使用 AI 工具创作，由作者指导。',\n'zh-hant/index.html':'由 Julio Aris 設計與開發。藝術作品使用 AI 工具創作，由作者指導。'")
add('_tools/_pp_price.py',"}\nfor p,so in","'zh/index.html':'即将推出','zh-hant/index.html':'即將推出'")
Z=dict(TAG='益智 · 新作',DESC='在绘本水彩的世界里，把可爱的花朵连成一线——为数码表冠和你的拇指打造的大号弹跳方块。',SOON='即将推出',GENRE='益智',MONO='益智 · Apple Watch',P='让花朵绽放，连出闪亮的连锁，跟着小芽穿过手绘花园——一款专为 Apple Watch 从零打造的治愈系益智游戏。',T1='故事模式与无尽模式',T2='为小屏幕设计的大号易点按方块',T3='绘本水彩画风与原创洗脑配乐',CTA='Kart Watch GP、Star Ace : Watch Shooter 和 Petal Pop 即将登陆 App Store。')
t=open('_tools/_pp_post.py',encoding='utf-8').read()
if "'zh':dict" not in t:
    t=t.replace("\n}\nfor lg,d in L.items():","\n'zh':dict(%s),\n}\nL['zh-hant']={k:__import__('opencc').OpenCC('s2twp').convert(v).replace('數碼','數位') for k,v in L['zh'].items()}\nfor lg,d in L.items():"%",".join("%s=%r"%(k,v) for k,v in Z.items()),1)
    t=t.replace("p='index.html' if lg=='en' else lg+'/index.html'","p='index.html' if lg=='en' else lg+'/index.html'")
    open('_tools/_pp_post.py','w',encoding='utf-8').write(t)
print('ok')
