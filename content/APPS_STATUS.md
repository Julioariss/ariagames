# ESTADO REAL DE LAS APPS (fuente de verdad para videos, captions, comentarios y posters)
Verificado en la App Store el 2026-11-01. Las apps cambian seguido: ANTES DE PUBLICAR cualquier cosa, el agente debe repetir la CHEQUEO DE ESTADO de abajo y actualizar este archivo si algo cambió. Si un texto de un prompt contradice este archivo, MANDA ESTE ARCHIVO.

## Poppy Pop (id 6821664713) — v1.3.0 (1/11/2026)
- Plataformas: iPhone, iPad y Apple Watch (watch app: watchOS 11+, hasta hace poco "Series 7+"; iOS 16+). Nombre en la tienda: "Poppy Pop: Puzzle".
- Modo historia: **50 capítulos/etapas en 10 mundos**, jefes y villano final (Emperador Eclipse). NUNCA decir "29 capítulos" (dato viejo).
- Modo Infinito: gratis, se desbloquea al terminar la historia.
- NUEVO 1.3.0: modos online **Versus y Worldwide** (duelos 2-4 jugadores, Top 100 mundial con banderas, desafios contra jefes, offline-first), hub Tierra, filas de ataque, opciones de privacidad/borrar datos online.
- Gratis: Mundo 1 (9 etapas) + Infinito. Compra unica "Full game" desbloquea el resto. Sin anuncios, sin cuenta. Progreso sincronizado por iCloud. Complicación en la esfera del Watch.
- Etiqueta de precio: "Free · In-App Purchases".

## Kart Watch GP (id 6821168181) — v1.1.1 publicada; v1.1.2 (modo Online) ENVIADA A REVISIÓN (no anunciar Online hasta que salga)
- Apple Watch Series 10+ (compañera iPhone). **18 pistas en 6 copas**, **10 corredores** originales (no 8), Grand Prix con medallas, Time Trials, drift/mini-turbo, items.
- Gratis: Kart Cup. Resto con compra unica "Full Game". Sin anuncios, sin cuenta.

## STAR Ace: Watch Shooter (id 6821445432) — v1.1.3
- Apple Watch Series 10+ (companera iPhone). 5 mundos/misiones y 5 jefes, lock-on multiple, Digital Crown. Piloto: Cosmo (nutria) en la nave Aurora Manta.
- La ficha dice "no in-app purchases / one purchase" pero la tienda muestra IAP: NO afirmar nada de pagos mas alla de "Free · In-App Purchases".

## CHEQUEO DE ESTADO (obligatorio antes de publicar y al inicio de cada tramo)
1. Abrir en Chrome apps.apple.com/us/app/id6821664713, id6821168181 e id6821445432 y leer: version, "What's New", descripcion, dispositivos.
2. Leer en el Project (claude/…): poppypop_ios_*, kartwatchgp_online_*, poppypop_versus_*; y `git log --since="3 days ago"`.
3. Comparar con este archivo; si cambió algo (version, numero de etapas/pistas, modos, plataformas), ACTUALIZAR este archivo y usar los datos nuevos en captions, textos en pantalla y comentarios.
4. Prohibido repetir cifras o funciones que no estén aquí. Si no estás seguro de una cifra, no la pongas.

## REGLA DE VEHÍCULOS (orden de Julio, 1/11/2026)
En TODOS los videos con autos/buggies/karts (Kart Watch GP, y cualquier otro): los vehiculos SIEMPRE avanzan hacia adelante (morro hacia la direccion de movimiento, ruedas girando hacia delante). Nunca en reversa, de lado derrapando sin avanzar, ni retrocediendo. En el prompt del clip incluir literal: "the buggy always drives forward, nose pointing in the direction of travel, wheels spinning forward, never reversing or moving backwards; chase camera behind the buggy or front camera as it approaches". Revisar 4 fotogramas y el movimiento (el fondo/pista debe correr hacia atras respecto al vehiculo); si parece que retrocede, descartar y rehacer (max 3 intentos).
