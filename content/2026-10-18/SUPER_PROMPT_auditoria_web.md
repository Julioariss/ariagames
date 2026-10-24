# Super prompt — Auditoría y arreglo total de ariagames.dev

Rol: equipo senior (Front-end/QA + CRO + i18n + SEO + Accesibilidad). Auditar TODAS las páginas (15 idiomas, /go, /poppypop, /staracce, /starwingace, privacy, intro) y arreglar todo, US$0.

Reglas duras
1. NO correr i18n.py / addlang*.py (index.src.html está desactualizado y rompe la home). Editar */index.html directo con scripts a los 15 archivos.
2. Etiqueta de precio única: "In-App Purchases" (nunca US$1.99, pago único, Gratis/Free, Coming soon).
3. Los 3 juegos con badge oficial App Store enlazando a https://apps.apple.com/app/id6821664713 (Poppy Pop, Watch Series 7+), id6821168181 (Kart Watch GP, Series 10+), id6821445432 (STAR Ace, Series 10+).
4. Sin gastar dinero, sin credenciales, no subir content/outreach/promo_codes_influencers.csv.
5. git push solo desde Mac (Desktop_Commander), esperar deploy 1–3 min y verificar en vivo con ?v=N.

Áreas: A visual/responsive (1440/1024/768/390), B contenido y enlaces, C conversión (badge sin scroll), D SEO (hreflang, og, JSON-LD, sitemap), E rendimiento (imágenes, lazy, CLS), F accesibilidad, G consola/red sin errores, H legal coherente con freemium.

Método: baseline + hallazgos P0/P1/P2 (content/2026-10-18/audit_web.md) → arreglar por lotes → push → verificar en vivo (home, es, ja, de, /go, móvil) → revisión final como usuario nuevo.
