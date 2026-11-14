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

## REGLA DE DIRECCIÓN DE MOVIMIENTO (vehículos, aviones, naves) — orden de Julio 14-nov, OBLIGATORIA
Problema: la IA confunde si el vehículo avanza hacia adelante o hacia atrás y el video se ve extraño. Se previene en el PROMPT y se verifica en el QA.
PROMPT (incluir TODO, en inglés, en cada clip con algo que se mueve):
"The [kart/plane/ship] moves FORWARD only: its nose/front points exactly in the direction of travel and the driver/pilot looks straight ahead in that direction, never looking back. Wheels/propellers/engines spin forward. Exhaust flames, dust, sparks and contrails trail BEHIND it, on the opposite side of the direction of travel. The track/ground/clouds/background stream past in the opposite direction. Camera: [chase camera directly behind, OR front camera as it approaches, OR steady side tracking shot where the nose leads the frame]. Never reversing, never drifting sideways without advancing, no spinning, no backwards motion."
EVITAR en el prompt: "drift", "spin", "turn around", "camera orbit", "she looks at the camera/back" (el personaje no mira a cámara mientras conduce si la cámara está delante: debe mirar hacia adelante), planos laterales ambiguos.
Encuadre preferido: cámara DETRÁS (chase) con el vehículo alejándose, o delantera con el vehículo acercándose y el piloto mirando al frente; escribir 1 solo encuadre por clip.
QA DE MOVIMIENTO (además del 4.6): ver 4 fotogramas consecutivos (cada 0.3 s) y comprobar: (1) el morro apunta a la dirección de avance, (2) el piloto mira al frente, (3) llamas, polvo y chispas quedan ATRÁS, (4) el fondo corre en sentido contrario. Si UNA falla: descartar y regenerar (máx. 3 intentos); si aún falla, no usar ese clip.
Nota: la regla aplica a autos, karts, aviones, naves y cualquier cosa con dirección.

REGLA DE MATERIAL NUEVO: ver PLAYBOOK_MAESTRO.md (clips, gameplay y música nuevos en cada video; nunca reciclar).
