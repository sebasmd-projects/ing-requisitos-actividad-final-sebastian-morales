#!/usr/bin/env python3
"""Construye el sitio estatico GEA (Grupo 7) a partir de GEA_contenido_Google_Sites.md.

Solo libreria estandar (Python 3.11). Uso:  python tools/build.py
Salida: site/  (8 paginas + print.html + assets/site.css + img/ + hash.json)
Falla con codigo != 0 si falta una imagen, una seccion obligatoria, el menu no
tiene 8 paginas, el HTML esta desbalanceado o algun conteo de la rubrica no cuadra.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import struct
import sys
import unicodedata
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_MD = ROOT / "GEA_contenido_Google_Sites.md"
SITE = ROOT / "site"
CSS_SRC = ROOT / "tools" / "site.css"

# (archivo, nombre del menu): el orden y los nombres son fijos.
MENU = [
    ("index.html", "Inicio"),
    ("calidad.html", "Calidad"),
    ("pruebas.html", "Pruebas"),
    ("configuracion.html", "Configuración"),
    ("despliegue.html", "Despliegue"),
    ("soporte.html", "Soporte"),
    ("documentacion.html", "Documentación"),
    ("referencias.html", "Referencias"),
]

PENDING_TEXT = "Pendiente de certificación GEA"


def _read_cert_status() -> str:
    """CERT_STATUS: lee site/cert/certificado.json si existe; si no, el texto pendiente."""
    cert = SITE / "cert" / "certificado.json"
    if not cert.is_file():
        return PENDING_TEXT
    try:
        data = json.loads(cert.read_text(encoding="utf-8"))
        for key in ("status", "estado", "certification_status"):
            if isinstance(data, dict) and data.get(key):
                return str(data[key])
        return "Certificado GEA"
    except (OSError, ValueError):
        print("AVISO: site/cert/certificado.json ilegible; se usa el estado pendiente", file=sys.stderr)
        return PENDING_TEXT


CERT_STATUS = _read_cert_status()

GEA_HOST_PREFIX = "https://geausa.propensionesabogados.com/"
CERT_PDF = "cert/GEA_actividad_final.pdf"
CERT_PUBLIC_PDF = "cert/GEA_actividad_final-copia-publica.pdf"


def _read_cert_data() -> dict | None:
    """Datos de site/cert/certificado.json, o None si no existe o es ilegible.
    Solo se usa para mostrar el bloque; NUNCA entra en el hash de contenido."""
    cert = SITE / "cert" / "certificado.json"
    if not cert.is_file():
        return None
    try:
        data = json.loads(cert.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _safe_link(label: str, url: object, field: str) -> str:
    """Enlace solo si la URL empieza por el host GEA; si no, texto escapado y WARNING."""
    text = str(url)
    if text.startswith(GEA_HOST_PREFIX):
        return f'<a href="{escape(text, quote=True)}">{escape(label)}</a>'
    print(f"WARNING: certificado.json: {field} no empieza por {GEA_HOST_PREFIX}; "
          f"se muestra como texto, sin enlace", file=sys.stderr)
    return f"{escape(label)}: {escape(text)}"


def cert_block_html(heading_tag: str = "h2") -> str:
    """Bloque 'Certificado en GEA (producción)'; vacio si no hay certificado.json.
    Nunca muestra idempotency_key ni valores tipo clave."""
    data = _read_cert_data()
    if data is None:
        return ""
    h = heading_tag
    parts = [
        '<aside class="hash-box cert-box" aria-label="Certificado en GEA (producción)">',
        f"<{h}>Certificado en GEA (producción)</{h}>",
        f'<p>Estado: <span class="cert-status">{escape(CERT_STATUS)}</span></p>',
    ]
    if data.get("reference"):
        parts.append(f"<p>Referencia: {escape(str(data['reference']))}</p>")
    if data.get("code"):
        parts.append(f"<p>Código: <code>{escape(str(data['code']))}</code></p>")
    if data.get("verification_url"):
        parts.append("<p>" + _safe_link("Verificar el certificado en GEA",
                                        data["verification_url"], "verification_url") + "</p>")
    parts.append(f'<p><a href="{CERT_PDF}">Descargar el PDF certificado</a></p>')
    parts.append(f'<p><a href="{CERT_PUBLIC_PDF}">Copia pública certificada</a> (PDF)</p>')
    if data.get("public_copy_url"):
        parts.append("<p>" + _safe_link("Verificar la copia pública en GEA",
                                        data["public_copy_url"], "public_copy_url") + "</p>")
    if data.get("source_hash"):
        parts.append(f"<p>Hash del documento (source_hash): <code>{escape(str(data['source_hash']))}</code></p>")
    if data.get("public_copy_hash"):
        parts.append(f"<p>Hash de la copia pública (public_copy_hash): "
                     f"<code>{escape(str(data['public_copy_hash']))}</code></p>")
    parts.append("</aside>")
    return "\n".join(parts)

ERRORS: list[str] = []


def fail(msg: str) -> None:
    ERRORS.append(msg)


# --------------------------------------------------------------------------- inline

def _restore(text: str, stash: list[str]) -> str:
    while "\x00" in text:
        text = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)
    return text


def inline(text: str) -> str:
    stash: list[str] = []

    def put(h: str) -> str:
        stash.append(h)
        return f"\x00{len(stash) - 1}\x00"

    text = re.sub(r"`([^`]+)`", lambda m: put(f"<code>{escape(m.group(1), quote=False)}</code>"), text)
    text = escape(text, quote=False)

    def fmt(s: str) -> str:
        s = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<![\w*])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![\w*])", r"<em>\1</em>", s)
        return s

    def link(m: re.Match) -> str:
        return put(f'<a href="{m.group(2)}">{fmt(m.group(1))}</a>')

    text = re.sub(r"\[([^\]\[]+)\]\((https?://[^)\s\"]+)\)", link, text)

    def bare(m: re.Match) -> str:
        url = m.group(0)
        tail = ""
        while url and url[-1] in ".,;:)":
            tail = url[-1] + tail
            url = url[:-1]
        return put(f'<a href="{url}">{url}</a>') + tail

    text = re.sub(r"https?://[^\s<>\"\x00]+", bare, text)
    text = fmt(text)
    return _restore(text, stash)


def plain(html: str) -> str:
    import html as h
    return h.unescape(re.sub(r"<[^>]+>", "", html)).strip()


def slugify(t: str) -> str:
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "sec"


# --------------------------------------------------------------------------- bloques

IMG_RE = re.compile(r"^\[Imagen:\s*([^\]]+?)\s*\](?:\s*—\s*(.*?))?\s*$")
LIST_RE = re.compile(r"^\s{0,3}([*-]|\d+\.)\s+(.*)$")
HEAD_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
HR_RE = re.compile(r"^\s{0,3}(-{3,}|\*{3,}|_{3,})\s*$")
SEP_RE = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$")


def png_size(path: Path):
    try:
        with path.open("rb") as f:
            head = f.read(24)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", head[16:24])
    except OSError:
        pass
    return None


def split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells, cur, in_code, i = [], [], False, 0
    while i < len(s):
        c = s[i]
        if c == "`":
            in_code = not in_code
            cur.append(c)
        elif c == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur.append("|")
            i += 1
        elif c == "|" and not in_code:
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(c)
        i += 1
    cells.append("".join(cur).strip())
    return cells


class Ctx:
    def __init__(self, first_level: int, link_imgs: bool):
        self.first_level = first_level  # nivel HTML que corresponde a "###"
        self.link_imgs = link_imgs
        self.ids: dict[str, int] = {}
        self.imgs: list[str] = []

    def uid(self, text: str) -> str:
        base = slugify(text)
        n = self.ids.get(base, 0) + 1
        self.ids[base] = n
        return base if n == 1 else f"{base}-{n}"


def figure(file: str, caption: str | None, ctx: Ctx) -> str:
    ctx.imgs.append(file)
    if "/" in file or "\\" in file or file.startswith("."):
        fail(f"referencia de imagen no relativa/plana: {file!r}")
    elif not (ROOT / file).is_file():
        fail(f"imagen referenciada no existe en la raiz: {file}")
    cap_html = inline(caption) if caption else ""
    alt = plain(cap_html) if caption else Path(file).stem.replace("-", " ")
    size = png_size(ROOT / file)
    wh = f' width="{size[0]}" height="{size[1]}"' if size else ""
    src = f"img/{escape(file)}"
    img = f'<img src="{src}" alt="{escape(alt)}"{wh} loading="lazy">'
    if ctx.link_imgs:
        img = f'<a href="{src}">{img}</a>'
    figcap = f"<figcaption>{cap_html}</figcaption>" if caption else ""
    return f"<figure>{img}{figcap}</figure>"


def render_table(rows: list[list[str]]) -> str:
    header, body = rows[0], rows[1:]
    ncol = len(header)
    out = ['<div class="table-wrap"><table>', "<thead><tr>"]
    out += [f'<th scope="col">{inline(h)}</th>' for h in header]
    out.append("</tr></thead><tbody>")
    for r in body:
        r = (r + [""] * ncol)[:ncol]
        out.append("<tr>")
        for c in r:
            out.append(f"<td>{inline(c)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def is_block_start(line: str, nxt: str | None) -> bool:
    if HEAD_RE.match(line) or HR_RE.match(line) or IMG_RE.match(line.strip()):
        return True
    if LIST_RE.match(line):
        return True
    if line.lstrip().startswith("|") and nxt is not None and SEP_RE.match(nxt) and "-" in nxt:
        return True
    return False


def render_blocks(lines: list[str], ctx: Ctx) -> str:
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if HR_RE.match(line):
            out.append("<hr>")
            i += 1
            continue
        m = HEAD_RE.match(line)
        if m:
            level = min(6, max(1, len(m.group(1)) - 3 + ctx.first_level))
            html = inline(m.group(2))
            out.append(f'<h{level} id="{ctx.uid(plain(html))}">{html}</h{level}>')
            i += 1
            continue
        m = IMG_RE.match(line.strip())
        if m:
            out.append(figure(m.group(1), m.group(2), ctx))
            i += 1
            continue
        nxt = lines[i + 1] if i + 1 < n else None
        if line.lstrip().startswith("|") and nxt is not None and SEP_RE.match(nxt) and "-" in nxt:
            rows = [split_row(line)]
            i += 2
            while i < n and lines[i].lstrip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            out.append(render_table(rows))
            continue
        m = LIST_RE.match(line)
        if m:
            ordered = m.group(1)[0].isdigit()
            start = int(m.group(1)[:-1]) if ordered else 1
            items: list[str] = []
            while i < n:
                lm = LIST_RE.match(lines[i])
                if lm and lm.group(1)[0].isdigit() == ordered:
                    items.append(lm.group(2).strip())
                    i += 1
                elif lines[i].strip() and lines[i][:1].isspace() and items and not lm:
                    items[-1] += " " + lines[i].strip()
                    i += 1
                elif not lines[i].strip():
                    j = i
                    while j < n and not lines[j].strip():
                        j += 1
                    jm = LIST_RE.match(lines[j]) if j < n else None
                    if jm and jm.group(1)[0].isdigit() == ordered:
                        i = j
                    else:
                        break
                else:
                    break
            tag = "ol" if ordered else "ul"
            attr = f' start="{start}"' if ordered and start != 1 else ""
            lis = []
            for it in items:
                im = IMG_RE.match(it)
                lis.append(f"<li>{figure(im.group(1), im.group(2), ctx) if im else inline(it)}</li>")
            out.append(f"<{tag}{attr}>" + "".join(lis) + f"</{tag}>")
            continue
        para = [line.strip()]
        i += 1
        while i < n and lines[i].strip():
            nx = lines[i + 1] if i + 1 < n else None
            if is_block_start(lines[i], nx):
                break
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


# --------------------------------------------------------------------------- fuente

def load_source():
    raw = SRC_MD.read_bytes().replace(b"\r\n", b"\n")
    text = raw.decode("utf-8")
    lines = text.split("\n")
    sections: dict[int, tuple[str, list[str]]] = {}
    preamble: list[str] = []
    cur = None
    for ln in lines:
        m = re.match(r"^##\s+(\d+)\.\s+(.+?)\s*$", ln)
        if m:
            cur = int(m.group(1))
            sections[cur] = (m.group(2), [])
            continue
        if re.match(r"^##\s", ln):  # Anexo u otra seccion: no va en el sitio
            cur = None
            continue
        if cur is None:
            if not sections:
                preamble.append(ln)
        else:
            sections[cur][1].append(ln)
    for num, (_, body) in sections.items():
        while body and (not body[-1].strip() or HR_RE.match(body[-1])):
            body.pop()
    return raw, text, preamble, sections


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# --------------------------------------------------------------------------- plantillas

def nav_html(current: str | None) -> str:
    items = []
    for fn, name in MENU:
        if fn == current:
            items.append(f'<li><a class="current" href="{fn}" aria-current="page">{escape(name)}</a></li>')
        else:
            items.append(f'<li><a href="{fn}">{escape(name)}</a></li>')
    return (
        '<nav class="site-nav" aria-label="Menú principal">\n'
        '<p class="brand">GEA<span>Grupo 7</span></p>\n<ul>\n' + "\n".join(items) + "\n</ul>\n</nav>"
    )


def footer_html(content_hash: str) -> str:
    return (
        '<footer class="site-footer">\n'
        f'<p>Hash de contenido (SHA-256): <code>{content_hash}</code></p>\n'
        f'<p>Estado: <span class="cert-status">{escape(CERT_STATUS)}</span></p>\n'
        "</footer>"
    )


def document(title: str, description: str, current: str | None, body: str, content_hash: str) -> str:
    return (
        "<!DOCTYPE html>\n"
        '<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{escape(title)}</title>\n"
        f'<meta name="description" content="{escape(description)}">\n'
        '<link rel="stylesheet" href="assets/site.css">\n</head>\n<body>\n'
        '<a class="skip" href="#contenido">Saltar al contenido</a>\n'
        '<div class="layout">\n'
        f"{nav_html(current)}\n"
        '<div class="page">\n<main id="contenido">\n'
        f"{body}\n"
        "</main>\n"
        f"{footer_html(content_hash)}\n"
        "</div>\n</div>\n</body>\n</html>\n"
    )


# --------------------------------------------------------------------------- verificacion

VOID = {"meta", "link", "img", "br", "hr", "input", "source", "wbr"}


class Probe(HTMLParser):
    """Parsea HTML construido: balance de etiquetas y estructura para la rubrica."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.errors: list[str] = []
        self.blocks: list[dict] = []
        self.nav: list[tuple[str, str, bool]] = []
        self.imgs: list[str] = []
        self.sections: list[str] = []
        self.doctype = False
        self.lang = None
        self.viewport = False
        self.bufs: list[list[str]] = []
        self.skip = 0
        self.in_nav = False
        self.in_footer = False
        self.footer_text: list[str] = []
        self.all_text: list[str] = []
        self.in_thead = False
        self.table = None
        self.row = None
        self.cur_list = None
        self.a_attrs = None
        self.h1_count = 0

    def handle_decl(self, decl):
        if decl.lower().startswith("doctype html"):
            self.doctype = True

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "meta" and a.get("name") == "viewport":
            self.viewport = True
        if tag in VOID:
            if tag == "img":
                self.imgs.append(a.get("src") or "")
                if not self.skip:
                    self.blocks.append({"t": "img", "src": a.get("src")})
            return
        self.stack.append(tag)
        if tag == "nav":
            self.in_nav = True
            self.skip += 1
        elif tag == "footer":
            self.in_footer = True
            self.skip += 1
        elif tag == "section" and "doc-section" in (a.get("class") or ""):
            self.sections.append(a.get("id") or "")
        elif tag == "header" and "cover" in (a.get("class") or ""):
            self.skip += 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "th", "td", "li", "figcaption"):
            self.bufs.append([])
        if tag == "a" and self.in_nav:
            self.bufs.append([])
            self.a_attrs = a
        if tag == "thead":
            self.in_thead = True
        if tag == "table" and not self.skip:
            self.table = {"t": "table", "header": [], "rows": []}
        if tag == "tr":
            self.row = {"cells": [], "head": False}
        if tag in ("ul", "ol") and not self.skip:
            self.cur_list = {"t": "list", "kind": tag, "items": []}

    def handle_data(self, data):
        for b in self.bufs:
            b.append(data)
        self.all_text.append(data)
        if self.in_footer:
            self.footer_text.append(data)

    def _pop_text(self) -> str:
        return re.sub(r"\s+", " ", "".join(self.bufs.pop())).strip()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"cierre inesperado </{tag}> (abierto: {self.stack[-1] if self.stack else None})")
            if tag in self.stack:
                while self.stack and self.stack[-1] != tag:
                    self.stack.pop()
                self.stack.pop()
            return
        self.stack.pop()
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            text = self._pop_text()
            if tag == "h1":
                self.h1_count += 1
            if not self.skip:
                self.blocks.append({"t": "h", "level": int(tag[1]), "text": text})
        elif tag == "p":
            text = self._pop_text()
            if not self.skip:
                self.blocks.append({"t": "p", "text": text})
        elif tag in ("th", "td"):
            text = self._pop_text()
            if self.row is not None:
                self.row["cells"].append(text)
                if tag == "th":
                    self.row["head"] = True
        elif tag == "tr":
            if self.table is not None and self.row is not None:
                if self.in_thead or self.row["head"]:
                    self.table["header"] = self.row["cells"]
                else:
                    self.table["rows"].append(self.row["cells"])
            self.row = None
        elif tag == "thead":
            self.in_thead = False
        elif tag == "table":
            if self.table is not None:
                self.blocks.append(self.table)
            self.table = None
        elif tag == "li":
            text = self._pop_text()
            if self.cur_list is not None:
                self.cur_list["items"].append(text)
        elif tag in ("ul", "ol"):
            if self.cur_list is not None:
                self.blocks.append(self.cur_list)
            self.cur_list = None
        elif tag == "figcaption":
            self._pop_text()
        elif tag == "a" and self.in_nav:
            text = self._pop_text()
            a = self.a_attrs or {}
            self.nav.append((a.get("href", ""), text, "current" in (a.get("class") or "") or "aria-current" in a))
            self.a_attrs = None
        elif tag == "nav":
            self.in_nav = False
            self.skip -= 1
        elif tag == "footer":
            self.in_footer = False
            self.skip -= 1
        elif tag == "header" and self.skip:
            self.skip -= 1

    def close(self):
        super().close()
        if self.stack:
            self.errors.append(f"etiquetas sin cerrar: {self.stack}")


def probe_file(path: Path) -> Probe:
    p = Probe()
    p.feed(path.read_text(encoding="utf-8"))
    p.close()
    return p


def section_blocks(doc: Probe, prefix: str, level: int = 2) -> list[dict]:
    blocks = doc.blocks
    for idx, b in enumerate(blocks):
        if b["t"] == "h" and b["level"] == level and b["text"].startswith(prefix):
            res = []
            for nb in blocks[idx + 1:]:
                if nb["t"] == "h" and nb["level"] <= level:
                    break
                res.append(nb)
            return res
    raise KeyError(prefix)


def first(blocks: list[dict], kind: str, list_kind: str | None = None):
    for b in blocks:
        if b["t"] == kind and (list_kind is None or b.get("kind") == list_kind):
            return b
    return None


def rubric(docs: dict[str, Probe]) -> tuple[list[str], dict[str, object]]:
    problems: list[str] = []
    info: dict[str, object] = {}

    def need(label: str, ok: bool, detail: str):
        if not ok:
            problems.append(f"{label}: {detail}")

    def sec(page: str, prefix: str):
        try:
            return section_blocks(docs[page], prefix)
        except KeyError:
            problems.append(f"{page}: falta el subtitulo '{prefix}'")
            return None

    # Calidad
    b = sec("calidad.html", "Paso 1. Modelo de calidad")
    if b is not None:
        t = first(b, "table")
        nrows = len(t["rows"]) if t else 0
        need("Calidad", nrows == 3, f"caracteristicas del modelo={nrows}, se esperaban 3")
        just = next((x["text"] for x in b if x["t"] == "p" and x["text"].startswith("Justificación")), None)
        words = len(just.split(":", 1)[1].split()) if just else -1
        need("Calidad", 0 < words <= 100, f"justificacion={words} palabras (max 100)")
        info["Calidad"] = {"caracteristicas": nrows, "justificacion_palabras": words}
    b = sec("calidad.html", "Paso 2. Métricas de calidad")
    if b is not None:
        t = first(b, "table")
        ids = [r[0] for r in t["rows"]] if t else []
        need("Calidad", ids == ["M-01", "M-02", "M-03"], f"metricas={ids}")
        info.setdefault("Calidad", {})["metricas"] = len(ids)

    # Pruebas
    b = sec("pruebas.html", "3a. Tipos de prueba")
    ntypes = 0
    if b is not None:
        t = first(b, "table")
        ntypes = len(t["rows"]) if t else 0
        need("Pruebas", ntypes == 3, f"tipos de prueba={ntypes}, se esperaban 3")
    b = sec("pruebas.html", "3b. Casos de prueba")
    ids: list[str] = []
    if b is not None:
        t = first(b, "table")
        ids = [r[0] for r in t["rows"]] if t else []
        need("Pruebas", ids == [f"CP-0{i}" for i in range(1, 6)], f"casos={ids}")
    b = sec("pruebas.html", "3c. Criterios de aceptación")
    ncrit = 0
    if b is not None:
        lst = first(b, "list", list_kind="ol")
        ncrit = len(lst["items"]) if lst else 0
        need("Pruebas", ncrit == 3, f"criterios de aceptacion={ncrit}, se esperaban 3")
    info["Pruebas"] = {"tipos": ntypes, "casos": len(ids), "criterios": ncrit}

    # Configuracion
    b = sec("configuracion.html", "4b. Repositorio y ramas")
    nb = 0
    if b is not None:
        t = first(b, "table")
        nb = len(t["rows"]) if t else 0
        need("Configuración", nb >= 3, f"ramas={nb}, minimo 3")
    info["Configuración"] = {"ramas": nb}

    # Despliegue
    d: dict[str, int] = {}
    b = sec("despliegue.html", "5a. Requisitos técnicos mínimos")
    if b is not None:
        t = first(b, "table")
        d["requisitos"] = len(t["rows"]) if t else 0
        need("Despliegue", d["requisitos"] >= 5, f"requisitos={d['requisitos']}, minimo 5")
    b = sec("despliegue.html", "5b. Procedimiento de instalación")
    if b is not None:
        lst = first(b, "list", list_kind="ol")
        d["pasos"] = len(lst["items"]) if lst else 0
        need("Despliegue", 6 <= d["pasos"] <= 10, f"pasos de instalacion={d['pasos']}, esperado 6-10")
    b = sec("despliegue.html", "5c. Plan de reversión")
    if b is not None:
        lst = first(b, "list", list_kind="ol")
        d["reversion"] = len(lst["items"]) if lst else 0
        need("Despliegue", d["reversion"] >= 3, f"pasos de reversion={d['reversion']}, minimo 3")
    d["imagenes"] = len(docs["despliegue.html"].imgs)
    need("Despliegue", d["imagenes"] >= 2, f"imagenes={d['imagenes']}, minimo 2")
    info["Despliegue"] = d

    # Soporte
    s: dict[str, int] = {}
    b = sec("soporte.html", "6b. Niveles de severidad")
    if b is not None:
        t = first(b, "table")
        s["severidades"] = len(t["rows"]) if t else 0
        need("Soporte", s["severidades"] == 4, f"severidades={s['severidades']}, se esperaban 4")
    b = sec("soporte.html", "6c. Ciclo de mantenimiento")
    if b is not None:
        t = first(b, "table")
        s["mantenimiento"] = len(t["rows"]) if t else 0
        need("Soporte", s["mantenimiento"] == 2, f"tipos de mantenimiento={s['mantenimiento']}, se esperaban 2")
    info["Soporte"] = s

    # Documentacion
    b = sec("documentacion.html", "Paso 7. Artefactos de documentación")
    na = 0
    if b is not None:
        t = first(b, "table")
        na = len(t["rows"]) if t else 0
        need("Documentación", na == 5, f"artefactos={na}, se esperaban 5")
    info["Documentación"] = {"artefactos": na}

    # Referencias
    apa = [x for x in docs["referencias.html"].blocks
           if x["t"] == "p" and re.search(r"\((\d{4}|s\. f\.)\)", x["text"])]
    need("Referencias", len(apa) >= 3, f"entradas APA={len(apa)}, minimo 3")
    info["Referencias"] = {"entradas_apa": len(apa)}
    return problems, info


# --------------------------------------------------------------------------- main

def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    if not SRC_MD.is_file():
        print(f"ERROR: no existe {SRC_MD}", file=sys.stderr)
        return 1
    if not CSS_SRC.is_file():
        print(f"ERROR: no existe {CSS_SRC}", file=sys.stderr)
        return 1

    raw, text, preamble, sections = load_source()

    # Secciones obligatorias y menu
    if len(MENU) != 8:
        fail(f"el menu tiene {len(MENU)} paginas, se esperaban 8")
    for num, (fn, name) in enumerate(MENU, start=1):
        if num not in sections:
            fail(f"falta el encabezado de seccion '## {num}. {name}'")
        elif sections[num][0] != name:
            fail(f"la seccion {num} se llama '{sections[num][0]}', se esperaba '{name}'")
    if ERRORS:
        for e in ERRORS:
            print("ERROR:", e, file=sys.stderr)
        return 1

    # Metadatos de portada tomados del MD
    pre = "\n".join(preamble)
    activity = (re.search(r"\*\*Actividad:\*\*\s*(.+?)\s*·", pre) or [None, ""])[1]
    group = (re.search(r"\*\*(Grupo \d+)\*\*", pre) or [None, "Grupo 7"])[1]
    author = (re.search(r"\*\*Grupo \d+\*\*\s*·\s*(.+)", pre) or [None, ""])[1].strip()
    proj = next((m.group(2) for ln in sections[1][1] if (m := HEAD_RE.match(ln)) and len(m.group(1)) == 3),
                "GEA — Gestión Estratégica de Activos")

    # Render de cada seccion (sin escribir aun) para detectar imagenes faltantes
    page_ctx = {fn: Ctx(first_level=2, link_imgs=True) for fn, _ in MENU}
    page_body = {}
    for num, (fn, name) in enumerate(MENU, start=1):
        page_body[fn] = render_blocks(sections[num][1], page_ctx[fn])
    print_ctx = Ctx(first_level=3, link_imgs=False)
    print_sections = []
    for num, (fn, name) in enumerate(MENU, start=1):
        html = render_blocks(sections[num][1], print_ctx)
        sid = f"sec-{slugify(name)}"
        print_sections.append(
            f'<section class="doc-section" id="{sid}">\n<h2>{num}. {escape(name)}</h2>\n{html}\n</section>'
        )
    if ERRORS:
        for e in sorted(set(ERRORS)):
            print("ERROR:", e, file=sys.stderr)
        return 1

    used_imgs = sorted({f for c in page_ctx.values() for f in c.imgs})

    # Directorios, imagenes, CSS
    (SITE / "assets").mkdir(parents=True, exist_ok=True)
    (SITE / "img").mkdir(parents=True, exist_ok=True)
    for old in (SITE / "img").iterdir():
        if old.is_file() and old.name not in used_imgs:
            old.unlink()
    for f in used_imgs:
        shutil.copyfile(ROOT / f, SITE / "img" / f)
    shutil.copyfile(CSS_SRC, SITE / "assets" / "site.css")

    # Hash de contenido (solo entradas): MD normalizado + imagenes de img/
    inputs = {SRC_MD.name: sha256_bytes(raw)}
    for p in sorted((SITE / "img").iterdir()):
        if p.is_file():
            inputs[f"img/{p.name}"] = sha256_bytes(p.read_bytes())
    manifest = "\n".join(f"{inputs[k]}  {k}" for k in sorted(inputs)) + "\n"
    content_hash = sha256_bytes(manifest.encode("utf-8"))
    status_json = CERT_STATUS if CERT_STATUS != PENDING_TEXT else "pendiente de certificación"
    (SITE / "hash.json").write_text(
        json.dumps({"content_hash": content_hash, "inputs": dict(sorted(inputs.items())),
                    "status": status_json}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n")

    # Paginas
    hash_box = (
        '<aside class="hash-box" aria-label="Hash de contenido">\n'
        "<h2>Hash de contenido (SHA-256)</h2>\n"
        f"<p><code>{content_hash}</code></p>\n"
        f'<p>Estado: <span class="cert-status">{escape(CERT_STATUS)}</span></p>\n'
        "</aside>"
    )
    for fn, name in MENU:
        body = f"<h1>{escape(name)}</h1>\n"
        if fn == "index.html":
            body += hash_box + "\n"
            cb = cert_block_html("h2")
            if cb:
                body += cb + "\n"
        pb = page_body[fn]
        if fn == "documentacion.html":
            cb = cert_block_html("h3")
            marker = "</tbody></table></div>"
            if cb and marker in pb:
                k = pb.index(marker) + len(marker)  # primera tabla = tabla de artefactos
                pb = pb[:k] + "\n" + cb + pb[k:]
        body += pb
        html = document(f"{name} — GEA Grupo 7", f"{name}: {proj}", fn, body, content_hash)
        (SITE / fn).write_text(html, encoding="utf-8", newline="\n")

    toc = "\n".join(f'<li><a href="#sec-{slugify(n)}">{escape(n)}</a></li>' for _, n in MENU)
    cover = (
        '<header class="cover">\n'
        f'<p class="eyebrow">{escape(activity)}</p>\n'
        f"<h1>{escape(proj)}</h1>\n"
        f'<p class="meta"><strong>{escape(group)}</strong> · {escape(author)}</p>\n'
        f'<p class="meta hash">Hash de contenido (SHA-256): <code>{content_hash}</code></p>\n'
        f'<p class="meta">Estado: <span class="cert-status">{escape(CERT_STATUS)}</span></p>\n'
        f"<ol>\n{toc}\n</ol>\n</header>"
    )
    (SITE / "print.html").write_text(
        document(f"{proj} — {group} (versión impresa)", f"{proj}: documento completo", None,
                 cover + "\n" + "\n".join(print_sections), content_hash),
        encoding="utf-8", newline="\n")

    # ---------------- Verificacion sobre el HTML construido
    problems: list[str] = []
    docs: dict[str, Probe] = {}
    expected_nav = [(fn, name) for fn, name in MENU]
    for fn in [f for f, _ in MENU] + ["print.html"]:
        path = SITE / fn
        if not path.is_file():
            problems.append(f"falta {fn}")
            continue
        p = probe_file(path)
        docs[fn] = p
        for e in p.errors:
            problems.append(f"{fn}: HTML desbalanceado: {e}")
        if not p.doctype:
            problems.append(f"{fn}: falta <!DOCTYPE html>")
        if p.lang != "es":
            problems.append(f"{fn}: lang != es")
        if not p.viewport:
            problems.append(f"{fn}: falta meta viewport")
        if [(h, t) for h, t, _ in p.nav] != expected_nav:
            problems.append(f"{fn}: menu incorrecto: {[t for _, t, _ in p.nav]}")
        cur = [h for h, _, c in p.nav if c]
        if fn != "print.html" and cur != [fn]:
            problems.append(f"{fn}: pagina actual mal marcada: {cur}")
        foot = "".join(p.footer_text)
        if content_hash not in foot or CERT_STATUS not in foot:
            problems.append(f"{fn}: el pie no muestra hash y estado")
        for src in p.imgs:
            if not src.startswith("img/") or not (SITE / src).is_file():
                problems.append(f"{fn}: imagen inexistente {src}")
    if "index.html" in docs and content_hash not in "".join(docs["index.html"].all_text).replace("\n", ""):
        problems.append("index.html: no muestra el hash")
    if len([f for f, _ in MENU if f in docs]) != 8:
        problems.append("el conteo de paginas de menu construidas no es 8")
    if "print.html" in docs:
        ids = docs["print.html"].sections
        if ids != [f"sec-{slugify(n)}" for _, n in MENU]:
            problems.append(f"print.html: secciones fuera de orden o incompletas: {ids}")
    if not problems and all(fn in docs for fn, _ in MENU):
        rp, info = rubric(docs)
        problems += rp
    else:
        info = {}

    if problems:
        for e in problems:
            print("ERROR:", e, file=sys.stderr)
        return 1

    # Avisos de marcadores de posicion (no fallan el build)
    warns = []
    for num, (fn, name) in enumerate(MENU, start=1):
        for ln in sections[num][1]:
            for m in re.finditer(r"\[(Captura[^\]]*|fecha|solicitante)\]", ln):
                warns.append(f"{name}: [{m.group(1)}]")

    print("Construccion OK")
    print(f"content_hash = {content_hash}")
    print(f"Estado       = {CERT_STATUS}")
    print(f"Paginas      = {', '.join(f for f, _ in MENU)}, print.html")
    print(f"Imagenes     = {len(used_imgs)} copiadas a site/img/")
    print("Conteos de rubrica:")
    for k, v in info.items():
        print(f"  {k}: " + ", ".join(f"{a}={b}" for a, b in v.items()))
    if warns:
        print(f"AVISO: {len(warns)} marcadores de posicion sin resolver:")
        for w in warns:
            print("  -", w)
    return 0


if __name__ == "__main__":
    code = main()
    if ERRORS and code == 0:
        code = 1
    sys.exit(code)
