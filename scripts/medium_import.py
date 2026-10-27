#!/usr/bin/env python3
"""Import Medium posts (from the RSS feed) into Hugo page bundles.

Usage: python3 scripts/medium_import.py [--user danibonam] [--force]

Each post becomes content/post/<slug>/index.md, with its images downloaded
next to it. Existing bundles are skipped unless --force is given. Imported
posts keep canonicalUrl pointing at Medium, since that is where they were
first published.

Posts are also kept out of the sitemap, since search engines should index
the Medium original. Review the generated description before publishing.

Note: Medium's feed only contains the 10 most recent posts.
"""
import argparse
import html
import mimetypes
import re
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "content" / "post"
CONTENT_NS = "{http://purl.org/rss/1.0/modules/content/}encoded"
UA = {"User-Agent": "Mozilla/5.0 (bonam.cc medium importer)"}

PT_WORDS = {"não", "que", "uma", "para", "com", "são", "você", "das", "dos", "como", "também"}
EN_WORDS = {"the", "and", "with", "this", "that", "you", "are", "for", "from", "which"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read(), resp.headers.get_content_type()


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def slug_from_link(link):
    # https://user.medium.com/some-title-66d9905f454e?source=... -> some-title
    path = urllib.parse.unquote(urllib.parse.urlsplit(link).path).strip("/").split("/")[-1]
    path = re.sub(r"-[0-9a-f]{8,}$", "", path)
    return slugify(path)


def detect_language(text):
    words = re.findall(r"\w+", text.lower())
    pt = sum(w in PT_WORDS for w in words)
    en = sum(w in EN_WORDS for w in words)
    return "pt" if pt > en else "en"


class MediumToMarkdown(HTMLParser):
    """Converts the small subset of HTML Medium emits in its RSS feed."""

    def __init__(self, image_cb):
        super().__init__(convert_charrefs=True)
        self.image_cb = image_cb
        self.out = []
        self.lists = []
        self.href = None
        self.in_pre = False
        self.in_code = False

    def emit(self, text):
        self.out.append(text)

    def block(self):
        self.emit("\n\n")

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("p", "figure"):
            self.block()
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            # Medium uses h3/h4 for section headings; map them to ##/###
            level = max(2, int(tag[1]) - 1)
            self.block()
            self.emit("#" * level + " ")
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag == "code" and not self.in_pre:
            self.in_code = True
            self.emit("`")
        elif tag == "pre":
            self.in_pre = True
            self.block()
            self.emit("```\n")
        elif tag == "br":
            self.emit("\n" if self.in_pre else "  \n")
        elif tag == "a":
            self.href = a.get("href")
            self.emit("[")
        elif tag == "img":
            src = a.get("src", "")
            if "medium.com/_/stat" in src:
                return
            name = self.image_cb(src)
            if name:
                self.emit(f"![{a.get('alt', '')}]({name})")
        elif tag == "figcaption":
            self.emit("\n\n*")
        elif tag in ("ul", "ol"):
            self.lists.append([tag, 0])
            self.block()
        elif tag == "li":
            kind = self.lists[-1] if self.lists else ["ul", 0]
            kind[1] += 1
            indent = "  " * (len(self.lists) - 1)
            bullet = f"{kind[1]}." if kind[0] == "ol" else "-"
            self.emit(f"\n{indent}{bullet} ")
        elif tag == "blockquote":
            self.block()
            self.emit("> ")
        elif tag == "hr":
            self.block()
            self.emit("---")
            self.block()

    def handle_endtag(self, tag):
        if tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag == "code" and self.in_code:
            self.in_code = False
            self.emit("`")
        elif tag == "pre":
            self.in_pre = False
            self.emit("\n```")
            self.block()
        elif tag == "a":
            self.emit(f"]({self.href})" if self.href else "]")
            self.href = None
        elif tag == "figcaption":
            self.emit("*")
        elif tag in ("ul", "ol"):
            if self.lists:
                self.lists.pop()
            self.block()
        elif tag in ("p", "figure", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6"):
            self.block()

    def handle_data(self, data):
        self.emit(data)

    def markdown(self):
        text = "".join(self.out)
        text = re.sub(r"[ \t]+\n", lambda m: m.group(0) if m.group(0).endswith("  \n") else "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Bold/italic markers wrapping only whitespace break rendering
        text = re.sub(r"\*\*(\s*)\*\*", r"\1", text)
        # Medium headings are often bolded as well; the heading is enough
        text = re.sub(r"^(#+ )\*\*(.+?)\*\*\s*$", r"\1\2", text, flags=re.M)
        return text.strip() + "\n"


def summarize(markdown, limit=155):
    """First prose paragraph of the body, cut at a word boundary."""
    for para in markdown.split("\n\n"):
        para = para.strip()
        if para and not para.startswith(("#", "!", "```", "-", ">")):
            text = re.sub(r"[*`\[\]]|\(http[^)]*\)", "", para)
            text = re.sub(r"\s+", " ", text).strip()
            if len(text) <= limit:
                return text
            return text[:limit].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
    return ""


def yaml_str(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def import_item(item, force):
    title = item.findtext("title").strip()
    link = item.findtext("link").split("?")[0]
    date = parsedate_to_datetime(item.findtext("pubDate"))
    tags = [c.text for c in item.findall("category") if c.text]
    body_html = item.findtext(CONTENT_NS) or ""

    slug = slug_from_link(link)
    bundle = POSTS / slug
    if bundle.exists() and not force:
        print(f"skip  {slug} (exists)")
        return
    bundle.mkdir(parents=True, exist_ok=True)

    images = []

    def save_image(src):
        try:
            data, ctype = fetch(src)
        except Exception as exc:  # keep the remote URL if download fails
            print(f"  warn: could not download {src}: {exc}")
            return src
        base = Path(urllib.parse.urlsplit(src).path).name
        ext = Path(base).suffix.lower() or mimetypes.guess_extension(ctype) or ".png"
        name = f"{len(images) + 1:02d}-{slugify(Path(base).stem) or 'image'}{ext}"
        (bundle / name).write_bytes(data)
        images.append(name)
        return name

    # Medium's leading figure is the post's cover image
    cover = None
    lead = re.match(r'\s*<figure><img[^>]*src="([^"]+)"[^>]*/?>(?:<figcaption>.*?</figcaption>)?</figure>', body_html)
    if lead:
        cover = save_image(html.unescape(lead.group(1)))
        body_html = body_html[lead.end():]

    parser = MediumToMarkdown(save_image)
    parser.feed(body_html)
    body = parser.markdown()

    lang = detect_language(body)
    tags.append("português" if lang == "pt" else "english")

    lines = [
        "---",
        f"title: {yaml_str(title)}",
        f"date: {date.isoformat()}",
        f"slug: {yaml_str(slug)}",
        f"description: {yaml_str(summarize(body))}",
        f"locale: {yaml_str('pt_BR' if lang == 'pt' else 'en_US')}",
    ]
    if cover:
        lines.append(f"image: {yaml_str(cover)}")
    lines += [
        "tags:",
        *[f"    - {yaml_str(t)}" for t in tags],
        f"canonicalUrl: {yaml_str(link)}",
        f"mediumUrl: {yaml_str(link)}",
        "sitemap:",
        "    disable: true",
        "---",
        "",
    ]
    (bundle / "index.md").write_text("\n".join(lines) + body, encoding="utf-8")
    print(f"wrote {slug} ({lang}, {len(images)} images)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--user", default="danibonam", help="Medium username, without @")
    ap.add_argument("--force", action="store_true", help="overwrite existing bundles")
    args = ap.parse_args()

    data, _ = fetch(f"https://medium.com/feed/@{args.user}")
    root = ET.fromstring(data)
    for item in root.iter("item"):
        import_item(item, args.force)


if __name__ == "__main__":
    main()
