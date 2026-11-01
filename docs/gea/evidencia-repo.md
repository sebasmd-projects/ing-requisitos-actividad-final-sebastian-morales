# GEA - Evidencia en el repositorio publico

Repositorio: <https://github.com/sebasmd-projects/gea_module_0> (publico, rama por defecto `master`).

Todos los enlaces apuntan al commit HEAD verificado: `5be1ed914df1a2764b2ae238e9ff252d1ea937c8` (2026-10-26), de modo
que el contenido enlazado no cambia aunque `master` avance. Cada archivo fue comprobado con
`git cat-file -e HEAD:<ruta>` en un clon completo.

## Archivos que existen en HEAD

| Documento | Enlace |
|---|---|
| README | <https://github.com/sebasmd-projects/gea_module_0/blob/5be1ed914df1a2764b2ae238e9ff252d1ea937c8/README.md> |
| Guia de arranque | <https://github.com/sebasmd-projects/gea_module_0/blob/5be1ed914df1a2764b2ae238e9ff252d1ea937c8/docs/GETTING_STARTED.md> |
| Seguridad | <https://github.com/sebasmd-projects/gea_module_0/blob/5be1ed914df1a2764b2ae238e9ff252d1ea937c8/docs/SEGURIDAD.md> |
| Mapa de rutas | <https://github.com/sebasmd-projects/gea_module_0/blob/5be1ed914df1a2764b2ae238e9ff252d1ea937c8/docs/ROUTES_MAP.md> |
| Mapa de funcionalidades | <https://github.com/sebasmd-projects/gea_module_0/blob/5be1ed914df1a2764b2ae238e9ff252d1ea937c8/docs/FEATURES_MAP.md> |
| CLAUDE.md (mapa de arquitectura del codigo) | <https://github.com/sebasmd-projects/gea_module_0/blob/5be1ed914df1a2764b2ae238e9ff252d1ea937c8/CLAUDE.md> |
| Guia de verificacion de certificados (HTML) | <https://github.com/sebasmd-projects/gea_module_0/blob/5be1ed914df1a2764b2ae238e9ff252d1ea937c8/docs/verificar-certificado.html> |

La guia de verificacion tambien existe en formato presentacion: `docs/verificar-certificado.pptx` (presente en HEAD).

Nota: GitHub muestra el HTML como codigo fuente en la vista `blob`; no lo renderiza como pagina.

## Historial de commits

- Commits de `master`: <https://github.com/sebasmd-projects/gea_module_0/commits/master>
- Commits hasta el HEAD citado: <https://github.com/sebasmd-projects/gea_module_0/commits/5be1ed914df1a2764b2ae238e9ff252d1ea937c8>
- Pull requests: <https://github.com/sebasmd-projects/gea_module_0/pulls?q=is%3Apr>

Cifras verificadas con git: 385 commits, 67 merges, primer commit 2025-08-26, sin etiquetas (tags), version
`0.1.0` en `pyproject.toml`. Detalle en `git-facts.txt` y `CHANGELOG-reconstruido.md`.

## Archivos no encontrados en HEAD

- `CHANGELOG.md`: **no existe** (`git cat-file -e` falla). Por eso se publica una reconstruccion en
  `CHANGELOG-reconstruido.md`.

## No verificable desde git

- El estado de las pull requests en GitHub (abiertas/cerradas, revisiones, comentarios) y los numeros de PR que no dejaron
  un commit de merge (por ejemplo #44): git solo muestra los PR que aparecen en mensajes de commit.
- Cualquier despliegue en produccion: git no dice que version corre en un servidor.
