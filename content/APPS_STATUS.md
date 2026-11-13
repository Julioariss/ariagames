# ESTADO REAL DE LAS APPS (fuente de verdad para videos, captions, comentarios y posters)
Verificado en la App Store el 2026-11-13. Las apps cambian seguido: ANTES DE PUBLICAR cualquier cosa, el agente debe repetir la CHEQUEO DE ESTADO de abajo y actualizar este archivo si algo cambió. Si un texto de un prompt contradice este archivo, MANDA ESTE ARCHIVO.

## Poppy Pop: Puzzle (id 6821664713) — v1.3.7 (nov-2026)
- Plataformas: iPhone, iPad y Apple Watch (iOS 16+, watchOS 11+).
- Historia: **50 capítulos en 10 mundos**, jefes y villano final (Emperador Eclipse). Online: Versus y Worldwide (2-4 jugadores).
- Gratis: Mundo 1 (9 capítulos). Compra única "Juego completo" desbloquea los otros 9 mundos. Sin anuncios ni suscripción.
- Texto de cierre: "FREE ON IPHONE + IPAD + APPLE WATCH".

## STAR Ace: Space Shooter (id 6821445432) — v1.2.3 (nov-2026)
- Plataformas: **iPhone y Apple Watch (Series 8 o posterior)**. iOS 17+.
- **20 sectores** en 2 galaxias, 5 jefes elementales y el Devorador de Mundos; lock-on hasta 6 blancos; Versus y Co-op para 2-4 pilotos (online o misma Wi-Fi). Piloto: Cosmo (nutria azul).
- Gratis: primeros 2 sectores y el primer jefe. Compra única desbloquea el resto.
- Texto de cierre: "FREE ON IPHONE + APPLE WATCH".

## Kart Watch GP (id 6821168181) — v1.1.4 (nov-2026)
- Plataforma: **Apple Watch Series 10 o posterior** (la app de iPhone es compañera). La versión 3D fue descartada: se promociona esta.
- **18 pistas en 6 copas**, **10 pilotos** oficiales, Grand Prix con medallas, contrarreloj, modo Online (publicado).
- Gratis: Copa Kart. Compra única desbloquea las otras 5 copas.
- Texto de cierre: "FREE ON APPLE WATCH".

Para las tres: decir solo "Free · In-App Purchases" / "gratis con compra única opcional"; nunca prometer precio.

## CHEQUEO DE ESTADO (obligatorio antes de publicar y al inicio de cada tramo)
1. Abrir en Chrome apps.apple.com/us/app/id6821664713, id6821168181 e id6821445432 y leer: version, "What's New", descripcion, dispositivos.
2. Leer en el Project (claude/…): poppypop_ios_*, kartwatchgp_online_*, poppypop_versus_*; y `git log --since="3 days ago"`.
3. Comparar con este archivo; si cambió algo (version, numero de etapas/pistas, modos, plataformas), ACTUALIZAR este archivo y usar los datos nuevos en captions, textos en pantalla y comentarios.
4. Prohibido repetir cifras o funciones que no estén aquí. Si no estás seguro de una cifra, no la pongas.

## REGLA DE VEHÍCULOS (orden de Julio, 1/11/2026)
En TODOS los videos con autos/buggies/karts (Kart Watch GP, y cualquier otro): los vehiculos SIEMPRE avanzan hacia adelante (morro hacia la direccion de movimiento, ruedas girando hacia delante). Nunca en reversa, de lado derrapando sin avanzar, ni retrocediendo. En el prompt del clip incluir literal: "the buggy always drives forward, nose pointing in the direction of travel, wheels spinning forward, never reversing or moving backwards; chase camera behind the buggy or front camera as it approaches". Revisar 4 fotogramas y el movimiento (el fondo/pista debe correr hacia atras respecto al vehiculo); si parece que retrocede, descartar y rehacer (max 3 intentos).
