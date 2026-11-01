# GEA - Registro de cambios RECONSTRUIDO desde el historial de git

> **Aviso importante.** Este documento esta **reconstruido a partir del historial de git** del repositorio publico
> `sebasmd-projects/gea_module_0`. **GEA no tiene un archivo CHANGELOG todavia** (`CHANGELOG.md` no existe en HEAD).
> Cada entrada cita el SHA corto del commit, la fecha (AAAA-MM-DD) y el numero de PR cuando el historial lo indica.
> Es una sintesis de grupos de cambios con significado; **no** lista cada commit menor.

## Datos de referencia (verificados con git)

- Rama por defecto: `master`. HEAD: `5be1ed914df1a2764b2ae238e9ff252d1ea937c8` (5be1ed9), fecha 2026-10-26.
- Total de commits alcanzables desde HEAD: 385 (67 son merges). Primer commit: `08db029`, 2025-08-26, "First Commit".
- Version declarada en `pyproject.toml` en HEAD: **0.1.0**.
- **No existe ninguna etiqueta (tag)** en el repositorio. Por eso **no se asignan versiones semanticas** a las entradas:
  se agrupan por mes.
- Las fechas son la fecha de autor del commit; para los PR, la fecha es la del commit de merge, que puede ser anterior
  a la de algunos commits de la rama fusionada (la rama siguio recibiendo commits despues de abrirse el PR).
- Los numeros de PR provienen de los mensajes de merge (`Merge pull request #N`) o del sufijo `(#N)` del titulo.
  El historial muestra PR #1 a #62 con huecos (por ejemplo #44 no aparece como merge; #34 aparece solo como sufijo del
  commit `7e2208c`).
- Detalle de atribucion: en el historial hay commits con autor "Claude" (107), "Sebastian Morales" (202) y
  "Sebastian Morales PC-escritorio" (76). Esto es lo que dice el campo autor de git; no se interpreta mas alla.

---

## 2026-10 (octubre de 2026)

Seguridad de dependencias y ajustes de interfaz.

- **Dependencias con avisos abiertos corregidas** (la rama `security/deps-2026-10` termina en `965f2a5`; los cuatro commits estan en `master`):
  - `2981da6` (2026-10-26) sube dependencias con avisos abiertos (pillow 13, pypdf, urllib3, pyjwt, certifi...).
  - `965f2a5` (2026-10-26) quita `safety` del grupo `dev` para poder subir `filelock` a 4.2.4.
  - `6ef8b28` (2026-10-26) fija `uv >= 0.13.4` para que `pip-audit` no lo marque en el servidor (PYSEC-2026-4321).
  - `5be1ed9` (2026-10-26) fija `wheel >= 0.46.2` (CVE-2026-24049), tambien marcado por `pip-audit`.
- **PR #62** (merge `c1f68ae`, 2026-10-19, rama `claude/elegant-mayer-1u6lf1`):
  - `ab70932` (2026-10-14) movil: el panel deja de ensancharse de lado.
  - `fc71a19` (2026-10-14) barra lateral: los iconos se cargan una sola vez, en el `head`.
  - `d41decb` (2026-10-16) agrega `DEVELOPMENT_CONVENTIONS.md`: como se desarrolla en este repositorio.
- `f58e794` (2026-10-19) verificacion/AEGIS: tras el OTP se vuelve al documento pedido, no al buscador.
- `4e9e396` (2026-10-19) merge de `origin/master` en la rama larga `claude/claude-md-context-architecture-map-jlazo4`
  (integra tambien `0ed3e5e` y `7511a14`, ver septiembre).

## 2026-09 (septiembre de 2026)

Mes con mayor actividad (111 commits por fecha de autor): acceso, certificados, historial de codigos, seguridad, pruebas y
documentacion. La mayor parte llega por una sucesion de PR de la rama `claude/claude-md-context-architecture-map-jlazo4`.

**Generador de codigos y certificacion documental (finales de mes)**
- `c0bcd5b` (2026-09-24) `/generate/code/`: segmentos opcionales, vista previa en vivo y logo de QR cambiable.
- `d02bb40`, `7a75ace`, `7ed8f73`, `5b910e8` (2026-09-27) mismo modulo: nada preseleccionado, la vista previa no depende de
  certificar, y arreglos del comportamiento `sticky` bajo la barra fija (tambien en `layout_form.html`).
- `6aca741` (2026-09-21) generador de codigos: vista previa real y certificacion oculta hasta pedirla.
- `0ed3e5e` (2026-09-30) "C1": certificacion documental para emisores externos (Propensiones).
- `7511a14` (2026-09-30) `SERVER_KEY`: un solo nombre para la clave servidor a servidor.
- `718198d` (2026-09-29) configuracion de graphify para el grafo del repositorio.
- `29b33f8` y `6aed3a4` (2026-09-22) `env.example` documenta la lista real de `COMMON_ATTACK_TERMS`; la trampa anti-escaneo
  cubre el escaneo de credenciales de herramientas de IA.

**Notificaciones - PR #61** (merge `a3214a3`, 2026-09-20, rama `feat/notificaciones`)
- "Fase 0": medir si cPanel aguanta tiempo real contra el Redis del VPS (`4001fde`, `0d24502`, 2026-09-15) y documentar el
  "relay" (`9db450f`). El PR tambien trae varios merges de `master` en la rama.

**Titular de certificado y verificacion (PR #59, #60 y commits directos)**
- PR #59 (merge `4134399`, 2026-09-14): `9882483` historico de codigos tambien para el titular de un certificado.
- PR #60 (merge `42dbf03`, 2026-09-15): `44316ec` el titular ya tiene por donde llegar a sus certificados.
- `310992e`, `ca6c8a1`, `9b2bc5d`, `ede3509` (2026-09-15): un certificado puede tener varios titulares; los enlaces de
  ver/verificar abren en pestana nueva; el codigo del registro de comprador pasa de cache a sesion; resumen AEGIS enlazado
  desde el historico agrupado.

**Historial de codigos, documentos legales, anclaje (PR #53 a #58)**
- PR #53 `c8f3bcd` (2026-09-13) / `08ecbe4`: historial de codigos en arbol.
- PR #54 `c09a962` / `5cea8f9` (2026-09-14): modo lista sin repetir ninguno.
- PR #55 `440de97` / `efafaa7`, `9efd10b` (2026-09-14): documentos legales editables, aprobables y con constancia de quien
  acepto; una variable faltante ya no tumba la pagina del historial.
- PR #56 `789442d` (2026-09-13) / `dda2713`, `893f1df` (2026-09-14): ruta de `call_command` de CRONJOBS escrita una vez;
  aprobar desde donde se redacta.
- PR #57 `af95c09` (2026-09-14) / `d006685`: entregar un resumen en USB solo si esta en verde.
- PR #58 `4e4389b` (2026-09-14) / `67a1aec`: poder comprobar un anclaje sin depender de GEA (la prueba y la fecha).

**Acceso, base de datos y dependencias (PR #43 a #52)**
- PR #43 `eb83b0c` (2026-09-13): `check_security` con bandit (codigo) y safety (dependencias, `dc14b80`); arreglo de seis avisos
  de SonarCloud (`c38365c`); `pip-audit` en el servidor y `safety` solo en local (`8eef902`).
- PR #45 `2c324ab` (2026-09-13, rama `fix-deps`): `da73568` arregla lo que rompio la actualizacion de dependencias.
- PR #46 `b3cd0ef` (2026-09-13): `b500b22` README profesional, guia de arranque y plantilla de `.env`.
- PR #47 `50e65d7` (2026-09-13): `53ecdf0` sube a **Django 5.2 LTS** y revisa dependencias; `82cdebf` el error de `.env`
  indica por nombre lo que falta.
- PR #48 a #50 (`08c0d5a`, `fb3d57e`, `08be3bf`, 2026-09-13): serie de arreglos de acceso (`a5f867c`, `37594e0`, `9707a5a`,
  `f1f21c0`): no llamar a `login()` sin usuario y diagnostico de la causa (un `pk` que no viaja de vuelta).
- PR #51 `01e1382` / `3c4bc94`: MariaDB, los UUID se siguen guardando como se guardaron.
- PR #52 (`da57fdb`) / `5ecf2d3` (2026-09-13): traduccion de los `.po` (647 cadenas sin traducir y 58 "fuzzy" equivocadas).
- Commits directos del 2026-09-13 de Sebastian Morales: zona horaria America/Bogota (`6d15999`), mensajes en espanol
  (`aa8cd3f`), eliminacion de carpetas de API (`a96b382`), `TEST_PUBLIC_PATHS` (`4262694`), debug toolbar en modo dev
  (`8d932ae`), documentacion para ejecutar pruebas y para generar requirements (`1d00ffb`, `119d173`).
- `5ef2935` (2026-09-15) fix: volver al login desde "olvide mi contrasena".

**Pruebas, respaldos y capa inicial (PR #40 a #42)**
- PR #40 `3d52b14` (2026-09-08) / `3a1402f`: tres senales en la capa inicial y una tabla de bloqueos legible.
- PR #41 `261d448` (2026-09-08) / `2ffd402`: el respaldo ya no deshace el cifrado; nada externo se ejecuta sin comprobarlo.
- PR #42 `862cb40` (2026-09-09) / `1d5627a`, `7e0ab66`: la suite corre en Windows con informe de cobertura y pagina de
  resumen de pruebas en la consola (se corrigen hallazgos de SonarCloud en `d8dc791`, `381206b`).

**Acceso por correo (PR #37 a #39, 2026-09-02)**
- PR #37 `3814eed` / `727b2d8`: entrar con un codigo enviado al correo.
- PR #38 `5f4acb7` / `4bb8db7`: se rehace el flujo de acceso y se unifica el contador.
- PR #39 `a9fd559` / `7faa934`: la comprobacion del broker no podia dar verde nunca.

**Guia de verificacion (2026-09-01)**
- `7e2208c` (#34) guia de verificacion para titulares y auditores; `8190ebd` (#35) en espanol e ingles; `33325b0` (#36) tambien
  en `.pptx`. Estas guias existen hoy como `docs/verificar-certificado.html` y `docs/verificar-certificado.pptx`.
- `b048771` (#33) documentos legales accesibles desde toda la plataforma y adjuntos de PQRS fuera del servidor web;
  `2b39f23` (#32) los limites de intentos ya no se apagan solos si Redis se cae.

## 2026-08 (agosto de 2026)

Inicio de la serie de PR (#1 a #31) en los ultimos tres dias del mes; 84 commits por fecha de autor.

- **2026-08-29 - PR #1 y #2**: `292c07f` mapa de arquitectura del codebase en `CLAUDE.md` (merge `3d40c40`, PR #1).
  PR #2 (`eec38dc`): traduccion de la consola de operaciones (`343c53b`), bloqueo de login que frena al atacante y no a la
  oficina (`aba87f7`), panel de administracion protegido por la sesion (`0bae51d`), documento sobre el encaje normativo de
  la certificacion y por que no se adopta W3C VC (`a9a58cb`), recuperacion de contrasena sin filtrar informacion
  (`913d344`), sellado y envio a cadena de bloques como dos actos separados (`0b6457e`).
- **Cache compartida en Redis (PR #3 a #12, 2026-08-29/30)**: `ae29783` `CACHES` sale de `REDIS_URL` con runbook para un VPS
  (PR #3); runbook concretado (#4, #6; `1553860`, `a0097ec`); produccion instala con `pip`, no `uv`, con chequeo de deriva
  (#7, `f2af071`); correccion de la ACL de Redis cuyo usuario `default` abria el servicio sin contrasena (#8, `a68c0db`);
  comprobador y diagnostico por capas de la cache (#9, #10); hash de la ACL y bucle de reinicio (#11); los dos tiempos de la
  cache (#12, `ed086a1`).
- **Anclaje en cadena de bloques (PR #5, #13)**: diagnosticar por que falla el envio (`476eb15`) y poder comprobarlo
  (`a535a13`).
- **AEGIS (PR #15, #16, 2026-08-30/31)**: `83f2c26` emitir el documento de la caja sin esperar a la cadena de bloques;
  `526c27b` "un AEGIS es un resumen, no una caja" y el log se escribe donde se mira.
- **Workers y cron (PR #14, #18 a #21, 2026-08-30/31)**: medir si cabe un worker (`efb8587`), estado de las tareas cron
  (`9a916e3`), explicacion del worker en el VPS (`5a5db38`) y la prueba larga de supervivencia (`9191e5d`).
- **Formulario y vista previa (PR #17, #22 a #24, 2026-08-31)**: arreglo del envio cancelado por el guardia contra doble clic
  (`e535e6d`), vista previa con datos reales (`72b6f46`), simbolos con fondo transparente (`9fb2ac3`), posiciones en dos filas
  y breadcrumb (`0cb6558`).
- **Trampa anti-escaneo y consola (PR #25, #26, 2026-08-31)**: `6505c7c`, `cf28833` (consola con git, mas comandos, buscador
  y filtros) y `df89100` (rotacion del log y health check).
- **Pruebas y cobertura (PR #27, #28)**: pruebas de `users`, ordenes y `assets_location`; se quita `betterforms`, que no
  usaba nadie; la traduccion automatica ya no puede tumbar el proyecto.
- **PR #29 a #31 (2026-08-31, mergeados; commits hasta 2026-09-01)**: `9f01cbc` arreglo de `feather is not defined`;
  `03edfb5` PQRS con plazos legales y cuatro documentos legales; `d182695` auditoria de seguridad con cinco arreglos.
- **Desarrollo de Sebastian Morales (2026-08-23 a 2026-08-29)**: validacion de documentos con QR y codigo de barras
  (`0b80513`), disposicion de los codigos (`91e7027`), traducciones (`8c9be8c`), resumen y caja AEGIS (`77aa59e`, `9e96158`),
  script de comprobacion de certificaciones (`c112e77`), nueva app `ops` (`5bda375`), documentacion para IA (`c8bf2c9`).

## 2026-03 y 2026-02 (marzo y febrero de 2026)

Pocos commits (2 en marzo, 10 en febrero).
- 2026-02-02: modo de espera activo (`46dda47`, `935f423`) y ocultar visuales (`5cdf30e`).
- 2026-02-04: reactivacion de la plataforma tras el cierre administrativo (`67a1cdb`, ver nota al final).
- 2026-02-27 y 2026-03-05: nuevo video y posters de GEA (`599a24d`), cambio del video hero (`42827b0`), retiro de documentos
  visuales de certificados AEGIS (`1f49d02`).
- 2026-02-10: JotForm, se quita el tiempo de interes (`be2d7c8`).

## 2026-01 (enero de 2026)

46 commits.
- **Certificacion y verificacion** (2026-01-08 a 2026-01-13): primer paso de certificados y verificacion (`e9a075d`),
  certificacion de documentos y escarapelas AEGIS e IPCON (`15f7164`), landing de certificaciones (`82f52c1`),
  listado de certificados en admin (`d468442`), verificacion de usuario con nombres (`f88ae87`).
- **Cuenta y seguridad** (2026-01-22 a 2026-01-29): verificacion por correo de IPCON (`9e854c4`), cambio y recuperacion de
  contrasena (`796503b`, `d81f759`), hash del correo en recuperacion (`614c193`), nuevo formulario de registro sin codigo
  diario para compra (`c1edfe4`), codigo diario solo para usuarios generales (`87b2934`).
- **Orion Scheduler y video** (2026-01-25 a 2026-01-27): `f2a9ed1` Orion Scheduler, `22e9037` `video_masonry`, filtro por
  categoria (`5a8df2b`), seguimiento de vistas de usuario (`cbbbdee`).
- 2026-01-21: entorno de proyecto con `uv` (`77115ac`).

## 2025-12 (diciembre de 2025)

20 commits: formulario de credito de activos (`8757d07`), manejo de decimales en numeros (`2978fa0` y siguientes, 2025-12-26),
nuevas marcas y encabezados para ordenes de compra y venta (`fa34e03`, `370fdcc`), mensaje "hasta enero" (`1f71ca6`),
renombre `ipcoin` a `ipcon` (`ebfbf7f`), cambio "Client" a "Suppliers" (`83bfa86`, 2025-12-13), eliminacion del
servicio AM PRO (`fe576fb`) y arreglo de un 500 en el asistente (`5f8f8a5`).

## 2025-11 (noviembre de 2025)

12 commits: certificacion en PDF (`7278a87`), permisos personalizados para rentabilidad y mejor admin de grupos (`4b5f205`,
`250a3e2`), nuevo portafolio y video de IPCON (`b856f29`, `60b4d09`), rebranding "global alliance" a "propensiones"
(`437be03`, `2492502`), videos de rendimiento y pruebas de arranque en frio (`04a6ab3`, `594fbb3`, `d650e31`).

## 2025-10 (octubre de 2025)

19 commits: inventario (formato de numeros, exportacion por columna, ubicaciones de activos con `unique_together`, suplantacion
de usuario, nuevas vistas: `5663a04`, `2421a8e`, `0ba724b`, `a42c97b`), imagen solicitada en orden de compra (`46c1c13`),
nuevos videos y logo (`9ba87a4`, `14e177e`, `52222c7`).

## 2025-09 (septiembre de 2025)

62 commits: compradores y ordenes de compra (listado y creacion separados `e35b85b`, asistente de aprobacion `3fc931f`, envio de
correo `ce1ace0`), codigo diario de GEA (`cc1e4a3`), bloqueo de actividad sospechosa y cron jobs (`05c5f34`, `6629b9a`),
campos de referidos (`1d93411`), nueva estructura estatica (`aac28ca`), retiro de Django REST Framework (`0647c7c`),
ajustes de zona horaria y SSL de base de datos (`f839710`, `6170c7e`), permisos de administracion (`2e23eb6`).

## 2025-08 (agosto de 2025)

9 commits: `08db029` (2025-08-26) "First Commit"; `6e8586d` `GEA_REGISTER_UNIQUE_CODE` con cron job; `70d63cd` PDF de orden de
compra; ajustes de requirements para Windows y `reportlab` (`f1a79a4`, `9978dad`); cambios del panel de comprador.

---

### Notas de verificacion

- Todos los SHA, fechas y numeros de PR de este documento provienen de `git log` sobre `origin/master` en un clon completo.
- El commit `67a1cdb` (2026-02-04) tiene un mensaje en el historial con un comentario personal y poco profesional; aqui solo se
  resume su efecto (reactivacion de la plataforma). Conviene no citarlo textualmente en el sitio.
- La descripcion funcional de cada grupo se basa unicamente en los mensajes de commit y en los titulos de merge; el contenido
  exacto de cada cambio no se ha auditado archivo por archivo: **no verificable desde git** mas alla del mensaje.
- Los commits de merge de `master` hacia ramas (por ejemplo "Merge branch 'master' into feat/notificaciones") no se listan.
