import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
A={'index.html':'Designed and developed by Julio Aris. Art created with AI tools, directed by the author.',
'es/index.html':'Diseñado y desarrollado por Julio Aris. Arte creado con herramientas de IA, dirigido por el autor.',
'pt/index.html':'Projetado e desenvolvido por Julio Aris. Arte criada com ferramentas de IA, dirigida pelo autor.',
'de/index.html':'Entworfen und entwickelt von Julio Aris. Kunst mit KI-Werkzeugen erstellt, vom Autor gesteuert.',
'fr/index.html':'Conçu et développé par Julio Aris. Illustrations créées avec des outils d’IA, dirigées par l’auteur.',
'ja/index.html':'デザイン・開発：Julio Aris。アートはAIツールで作成し、作者が監修しています。','zh/index.html':'由 Julio Aris 设计与开发。艺术作品使用 AI 工具创作，由作者指导。',
'zh-hant/index.html':'由 Julio Aris 設計與開發。藝術作品使用 AI 工具創作，由作者指導。'}
for p,v in A.items():
    t=open(p,encoding='utf-8').read(); assert 'AIDISC' in t,p
    open(p,'w',encoding='utf-8').write(t.replace('AIDISC',v))
print('aid ok')
