# Despliegue del sitio en sebasmoralesd.com/ing-requisitos/

Versión desplegada: v1.0.0 (commit de contenido certificado, hash 3c4ebaa9).

## Dónde vive
- Contenido: `/var/www/ing-requisitos/releases/<sha>/ing-requisitos/`, con el enlace `/var/www/ing-requisitos/current` apuntando a la versión activa.
- Configuración de nginx: `/etc/nginx/snippets/ing-requisitos.conf` (copia en `deploy/nginx-ing-requisitos.conf`), incluido una sola vez en `/etc/nginx/cv/site.conf`, justo antes de `include /etc/nginx/cv/locations.conf;`.
- Copia de seguridad previa al cambio: `/root/backups/ing-requisitos-20261101-232404/etc-nginx`.

## Verificación tras el despliegue
- `/ing-requisitos` responde 301 a `/ing-requisitos/`.
- `/ing-requisitos/` responde 200 con HTML y cabeceras HSTS, CSP, X-Frame-Options, nosniff y Referrer-Policy.
- `/ing-requisitos/.git/config` responde 404; `POST /ing-requisitos/` responde 403.
- `/` del dominio principal sigue igual (307 a `/es/`).

## Revertir
1. Quitar la línea `include /etc/nginx/snippets/ing-requisitos.conf;` de `/etc/nginx/cv/site.conf`, o restaurar ese archivo desde la copia de seguridad.
2. `nginx -t` y `systemctl reload nginx`.

## Riesgo conocido
`render.sh` de cv-src regenera `/etc/nginx/cv/site.conf`. Si se vuelve a renderizar, la línea de include se pierde y el sitio deja de servirse. Hay que añadir la línea a la plantilla de cv-src antes de la próxima renderización.
