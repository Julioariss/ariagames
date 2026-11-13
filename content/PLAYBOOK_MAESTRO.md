# PLAYBOOK MAESTRO ARIAgames v2 (13-nov-2026)
Reemplaza al v1 (archivado en PLAYBOOK_v1_archivado.md; NO leerlo ni seguir PROMPT_*.md antiguos). Si algo aquí contradice otro archivo, manda este, salvo las cifras de las apps: esas salen de content/APPS_STATUS.md.

## 0. OBJETIVO
Descargas y compras de Poppy Pop, STAR Ace y Kart Watch GP con gasto US$0.
Diagnóstico al 13-nov: ~8 descargas/día en total; IG 63 seguidores (533 seguidos), TikTok ~32; casi todas las ventas históricas son de CHILE.
Metas a 30 días: IG 300 seguidores, TikTok 300, 1 reel con >2.000 vistas por semana, 15 descargas/día.
Número que manda cada semana: vistas de NO seguidores por reel y visitas al perfil. Lo que suba eso se repite; lo que no, se cambia.

## 1. REGLAS DURAS (nunca se rompen)
1. US$0. Nunca pedir ni escribir credenciales ni resolver captchas: si una red pide login, anotarlo, avisar a Julio y seguir con la otra.
2. No borrar publicaciones ni cuentas. No enviar códigos, regalos ni DMs en frío sin OK de Julio.
3. Nunca nombrar juegos, personajes ni marcas de terceros en videos, captions, comentarios o prompts de Gemini.
4. Solo personajes y diseños OFICIALES (FICHAS_PERSONAJES.md, arte en ~/Developer/<juego> y art/). Nunca inventar personajes, logos ni cifras.
5. Sin spam: comentarios distintos y específicos al post, en el idioma de la cuenta, sin links en posts ajenos.
6. Chrome solo en la sesión "Julio Aris Serey". Una pestaña a la vez.
7. Nunca publicar un video que no pase el CONTROL DE CALIDAD (sección 4.6). Es preferible no publicar ese día y avisar.

## 2. JORNADA DIARIA (una corrida, ~60-90 min)
Orden fijo. Si un paso falla, aplicar la sección 8 y seguir con el siguiente; nunca abandonar la jornada entera por un paso.
1. PREPARAR (5 min): `git pull` (si falla, seguir igual). Leer este archivo, APPS_STATUS.md, las últimas 6 líneas de cm_log.md y content/targets.md.
2. PENDIENTES DE AYER (5 min): comentario de desarrollador con link en el video de TikTok de ayer si ya salió de revisión (tiktokstudio/comment/<id>, máx. 150 caracteres); responder comentarios y DMs de quien nos escribió.
3. CONTENIDO (40-50 min): producir y publicar el reel del día (sección 4).
4. INTERACCIÓN (15-20 min): sección 5.
5. MÉTRICAS (5 min): agregar 1 fila a content/metrics.csv (sección 6).
6. CIERRE: 1 línea en cm_log.md con el formato de la sección 9; commit + push (si el push falla, dejar el commit local); resumen a Julio (máx. 5 líneas) y enviarle el archivo del video publicado.
Corrida de reintento (12:00): si cm_log ya tiene "MARKETING DIARIO OK" de hoy, hacer solo SEGUNDA RONDA (máx. 15 min): comentario dev en TikTok si ya es público, responder comentarios/DMs, y 3 comentarios más en cuentas de targets.md. Si no lo tiene, jornada completa.

## 3. HECHOS DE LAS APPS
Fuente: content/APPS_STATUS.md (actualizado 13-nov). Antes de escribir una cifra en pantalla o en un caption, comprobar que está ahí. Las tres son gratis con compra única dentro de la app. Link único: ariagames.dev/go.

## 4. CONTENIDO: 1 reel al día (IG + TikTok, el mismo archivo)
### 4.1 Calendario
Rotación Poppy Pop → STAR Ace → Kart Watch GP (ver en cm_log cuál fue ayer). Nunca el mismo juego dos días seguidos.
Idioma del texto en pantalla y del caption: lunes a viernes en inglés; sábado y domingo en ESPAÑOL para Chile (con ubicación "Santiago, Chile" en IG), porque casi todos los compradores han sido chilenos.
Cada reel muestra una ESCENA o capítulo distinto del juego (otro mundo, otro jefe, otro piloto, otro modo). Revisar clips_used.md y no repetir escena ni gancho de los últimos 10 reels. Kart: rotar piloto (siguiente: Hazel).

### 4.2 Estructura obligatoria (15-30 s, 1080x1920, 30 fps)
1. 0-2 s GANCHO: clip de Gemini con el personaje oficial + texto grande (una pregunta o un reto). Sin logo ni intro lenta al principio.
2. 2-20 s CUERPO: alternar clips de Gemini (mínimo 2 clips NUEVOS generados hoy; STAR Ace y Kart igual) con gameplay REAL en video (máx. 3 segmentos de 2-4 s; nunca capturas fijas). Un texto corto por segmento.
3. Últimos 3-4 s CIERRE: beneficio + "FREE ON IPHONE + APPLE WATCH" (Kart: "FREE ON APPLE WATCH") + "ARIAGAMES.DEV/GO".
Textos dentro de la zona segura (y entre 245 y 1250 de 1920), tipografía gruesa con borde; máx. 5 palabras por línea.

### 4.3 Estilo por juego (fiel a los personajes oficiales)
- STAR Ace: acción anime de los 90. Tarjetas "WARNING" con franjas rojas y amarillas, texto metálico, cortes rápidos con destello blanco, temblor en los jefes. Plantilla aprobada: _tools/build_star_x_20261111.py (referencia: content/2026-11-11/daily_20261111_staracce_v2_en.mp4).
- Poppy Pop: aventura mágica anime kawaii, no demasiado rosa; Lila oficial (mismo traje, pelo y estatura siempre), jefes oficiales. Transiciones suaves, orden de la historia.
- Kart Watch GP: 3D de calidad de película animada; el piloto del día y su vehículo oficiales; los vehículos SIEMPRE avanzan hacia adelante (frase literal de APPS_STATUS.md en el prompt). Transiciones suaves.
Si no existe plantilla para Poppy o Kart, copiar la estructura de build_star_x_20261111.py cambiando paleta, tipografía y transiciones al estilo del juego, y guardar la nueva plantilla en _tools/.

### 4.4 Clips de Gemini (gemini.google.com, sesión de Julio)
"Crear vídeo" → subir 1 imagen oficial como referencia → elegir Vertical (9:16) → prompt en inglés que empiece con "Animate this exact character/scene…", describa la acción y termine con "keep the exact design and colors, no text, no extra characters".
Descargar y revisar 3 fotogramas de cada clip: si el personaje cambió (colores, ropa, especie) o aparece texto o un personaje ajeno, descartar y regenerar.
Cuota: unos 3 clips por día. Si se agota: usar clips generados antes que NUNCA se hayan publicado (anotados en clips_used.md); si no hay, no publicar hoy, avisar a Julio y dejar el reel montado para mañana.

### 4.5 Música
Siempre generada en Gemini ("Crear música"), instrumental, una pista NUEVA por video, descargada como "Solo audio MP3". Nunca usar solo la música del juego ni repetir pista.
- STAR Ace: rock rápido ~170 BPM, guitarras distorsionadas, doble bombo, melodía de sintetizador cuadrado, heroico.
- Poppy Pop: orquestal de aventura mágica, alegre, con campanas y cuerdas, ~130 BPM.
- Kart Watch GP: funk-rock de carreras, bajo marcado y metales, ~150 BPM.
Golpe fuerte en el primer segundo y final con remate (cortar la pista para que el remate caiga en el cierre).

### 4.6 CONTROL DE CALIDAD (obligatorio antes de publicar)
Generar una hoja de contactos (1 fotograma cada 2 s) y mirarla. Publicar solo si TODAS son verdad:
[ ] 1080x1920, 15-30 s, con audio, sin franjas negras ni video horizontal incrustado.
[ ] Gancho con texto visible en el primer segundo.
[ ] Al menos 2 clips de Gemini nuevos y gameplay real en video.
[ ] Personajes idénticos a los oficiales; ningún personaje, logo o marca ajenos.
[ ] Ningún texto de interfaz o diálogo del juego tapado o cortado por nuestros textos; nada fuera de la zona segura.
[ ] Cifras y plataformas iguales a APPS_STATUS.md.
[ ] Música nueva de Gemini del estilo del juego.
[ ] Cierre con ariagames.dev/go.
Si falla una, corregir y repetir el control. Tras 2 intentos fallidos: no publicar, enviar el video a Julio con el motivo.
Formato nuevo (plantilla que Julio no ha visto): enviar a Julio y esperar su OK antes de publicar.

### 4.7 Publicación
- Archivo < 10 MB para subir desde la sesión: comprimir a ~2 Mbps, copiar a ~/Downloads y prepararlo con device_stage_files.
- Instagram: Crear → Publicación → subir → en "Recortar" elegir 9:16 → portada con el personaje (no negra ni blanca) → caption → etiqueta de IA ON → Facebook OFF → Compartir. Después, comentario propio: "Dev here 👋 <juego> is free to try: https://apps.apple.com/app/id<ID>".
- TikTok Studio: subir → descripción → Mostrar más → "Contenido generado por IA" ON → Publicar. El comentario dev va al día siguiente (queda en revisión).
- Caption: 1 frase con el gancho + 1 frase con qué es el juego (palabras que la gente busca: "space shooter", "match-3 puzzle", "kart racing", "Apple Watch game", "iPhone game") + "link in bio: ariagames.dev/go" + 3-5 hashtags específicos. Sin bloques de 30 hashtags.
- Verificar que el reel aparece en el perfil. Anotar la escena y los clips usados en clips_used.md.

## 5. INTERACCIÓN (lo que más ha fallado: 1-3 comentarios al día)
Las búsquedas por hashtag devuelven posts viejos. NO usarlas como fuente principal. Fuente principal: content/targets.md (lista de cuentas).
Cada día, por red (IG y TikTok):
1. Abrir el perfil de 8-10 cuentas de targets.md (rotar: empezar por las que llevan más días sin visita) y comentar su post más reciente SI tiene menos de 72 h. Meta: 6 comentarios por red. Mínimo aceptable: 4.
2. Comentario: 1-2 frases sobre ALGO CONCRETO del post, en su idioma. Mencionar que somos desarrolladores o nuestro juego solo si viene al caso y como máximo 1 de cada 3 comentarios. Sin links.
3. Responder a quien respondió a nuestros comentarios anteriores (eso es lo que trae visitas al perfil).
4. Mantener la lista: si una cuenta lleva 14 días sin publicar, marcarla "inactiva"; agregar 2 cuentas nuevas por día sacadas de "Sugerencias para ti" de las cuentas que mejor funcionan, de quienes comentan en ellas y de la pestaña Reels/Para ti. Criterio: 1.000-200.000 seguidores, publica al menos 2 veces por semana, tema Apple Watch / juegos de iPhone / indie dev / gaming chileno.
Seguir cuentas: IG sigue a 533 y lo siguen 63, mala proporción. NO seguir a nadie nuevo salvo creadores que nos respondieron (máx. 3 por día). No dejar de seguir en masa.

## 6. MÉTRICAS Y REVISIÓN SEMANAL
Cada día, una fila en content/metrics.csv: fecha, seguidores_ig, seguidores_tiktok, juego, idioma, gancho, vistas_ig_24h_del_reel_de_ayer, vistas_tiktok_24h, likes, comentarios, comentarios_hechos_ig, comentarios_hechos_tiktok.
Lunes (dentro de la misma jornada): leer la semana en metrics.csv y escribir 5 líneas en claude/growth_log.md (Projects): mejor y peor reel y por qué (gancho, juego, idioma), qué cuentas de targets.md nos respondieron, y 2 cambios concretos para la semana. Aplicarlos: repetir el tipo de gancho ganador con otra escena; abandonar el perdedor.

## 7. COMUNIDAD Y CREADORES
Responder todos los comentarios en nuestros posts y los DMs de quien nos escribió (plantillas en content/dm_templates.md), el mismo día. Si un creador muestra interés o pide un código, avisar a Julio y esperar. Los DMs personales de la cuenta (familia y amigos de Julio) no se tocan.
Oportunidad abierta: FestiGame (Chile, 10-13 dic). Comentar sus posts en español; el DM pidiendo espacio lo aprueba Julio.

## 8. SI ALGO FALLA
- Sin Mac o sin Chrome: no marcar la jornada; avisar a Julio en 1 línea.
- Una red pide login: saltarla, hacer la otra, avisar.
- Gemini sin cuota o no carga: sección 4.4 (clips no publicados; si no hay, no publicar).
- La subida falla 2 veces: guardar el archivo en ~/Downloads, avisar a Julio con la ruta; seguir con interacción y métricas.
- Un botón no responde tras 2-3 intentos: no insistir en bucle; anotar y pasar al siguiente paso.
- Jornada incompleta: registrar "MARKETING DIARIO PARCIAL" con lo que faltó (el reintento de las 12:00 la completa).

## 9. REGISTRO
cm_log.md, una línea: `AAAA-MM-DD MARKETING DIARIO OK|PARCIAL: reel <juego> "<gancho>" (<idioma>, <n> clips Gemini, música "<pista>", archivo) IG <id> / TikTok <estado>; QA ok; comentarios IG <n> TikTok <n>; respuestas <n>; seguidores IG <n> TikTok <n>; pendientes: <...>`
