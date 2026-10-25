"""Build Mirajane's bubbly Markdown blog for GitHub Pages.

Markdown files in ``content/`` are the database, Jinja templates are the
views, and ``public/`` is the deployable static site.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
import json
import re
import shutil
import unicodedata

import markdown
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape


ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
ASSETS = ROOT / "assets"
PUBLIC = ROOT / "public"

SITE = {
    "title": "Mirajane's tiny internet corner",
    "author": "Mirajane",
    "url": "https://mymirajane.github.io",
    "description": "Technical notes about computer science, mathematics, statistics, and the small joys around them.",
    "bio": "I study computer science, math, and statistics. This is where I keep playful explanations, research notes, code, and links.",
    "social_links": [
        {"name": "GitHub", "url": "https://github.com/mymirajane/mymirajane.github.io"},
    ],
}

MARKDOWN_EXTENSIONS = ["extra", "fenced_code", "tables", "sane_lists", "attr_list"]


@dataclass(frozen=True)
class Post:
    title: str
    date: date
    slug: str
    kind: str
    description: str
    html: str
    tags: tuple[str, ...]
    reading_minutes: int
    source: Path

    @property
    def date_label(self) -> str:
        return f"{self.date:%b} {self.date.day}, {self.date.year}"


def parse_scalar(raw: str, path: Path, line_number: int) -> str:
    """Parse the small YAML scalar subset used by the blog."""
    value = raw.strip()
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid quoted value") from exc
        if not isinstance(parsed, str):
            raise ValueError(f"{path}:{line_number}: expected a string")
        return parsed
    if value.startswith("'"):
        if not value.endswith("'") or len(value) < 2:
            raise ValueError(f"{path}:{line_number}: unclosed quoted value")
        return value[1:-1].replace("''", "'")
    return value.split(" #", 1)[0].strip()


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: expected YAML frontmatter starting with ---")
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError(f"{path}: frontmatter has no closing ---") from exc

    metadata: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, raw_value = line.partition(":")
        key = key.strip().lower()
        if not separator or not re.fullmatch(r"[a-z][a-z0-9_-]*", key):
            raise ValueError(f"{path}:{number}: expected a key: value line")
        if key in metadata:
            raise ValueError(f"{path}:{number}: duplicate frontmatter key {key!r}")
        metadata[key] = parse_scalar(raw_value, path, number)
    return metadata, "\n".join(lines[end + 1 :]).strip() + "\n"


def slugify(value: str) -> str:
    value = value.strip().casefold().replace("đ", "d")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def parse_tags(value: str) -> tuple[str, ...]:
    """Accept ``tags: math, python`` and ``tags: [math, python]``."""
    value = value.strip().strip("[]")
    tags = []
    for raw_tag in value.split(","):
        tag = raw_tag.strip().strip('"\'')
        if tag:
            tags.append(tag)
    return tuple(tags)


def load_posts() -> list[Post]:
    if not CONTENT.is_dir():
        raise ValueError(f"Missing content directory: {CONTENT}")
    posts: list[Post] = []
    seen_slugs: set[str] = set()
    for path in sorted(CONTENT.rglob("*.md")):
        meta, body = parse_frontmatter(path)
        if meta.get("draft", "false").lower() == "true":
            continue
        title = meta.get("title", "").strip()
        if not title:
            raise ValueError(f"{path}: title is required")
        try:
            published = date.fromisoformat(meta["date"])
        except (KeyError, ValueError) as exc:
            raise ValueError(f"{path}: date must be YYYY-MM-DD") from exc
        slug = slugify(meta.get("slug") or path.stem)
        if not slug:
            raise ValueError(f"{path}: slug is empty after normalization")
        if slug in seen_slugs or slug in {"assets", "content", "templates", "public"}:
            raise ValueError(f"{path}: duplicate or reserved slug {slug!r}")
        seen_slugs.add(slug)
        kind = meta.get("type", "writing").lower()
        if kind not in {"writing", "note", "link"}:
            raise ValueError(f"{path}: type must be writing, note, or link")
        description = meta.get("description", "").strip() or title
        html = markdown.markdown(body, extensions=MARKDOWN_EXTENSIONS)
        tags = parse_tags(meta.get("tags", ""))
        words = len(re.findall(r"\b\w+\b", body, flags=re.UNICODE))
        posts.append(
            Post(
                title=title,
                date=published,
                slug=slug,
                kind=kind,
                description=description,
                html=html,
                tags=tags,
                reading_minutes=max(1, round(words / 220)),
                source=path,
            )
        )
    posts.sort(key=lambda post: (-post.date.toordinal(), post.slug))
    return posts


def rss_feed(posts: list[Post]) -> str:
    origin = SITE["url"].rstrip("/")
    items: list[str] = []
    for post in posts:
        link = f"{origin}/{post.slug}/"
        published = datetime.combine(post.date, time(12), tzinfo=timezone.utc)
        items.append(
            "<item>"
            f"<title>{xml_escape(post.title)}</title>"
            f"<link>{xml_escape(link)}</link>"
            f"<guid>{xml_escape(link)}</guid>"
            f"<pubDate>{format_datetime(published, usegmt=True)}</pubDate>"
            f"<description>{xml_escape(post.description)}</description>"
            "</item>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<rss version=\"2.0\"><channel>"
        f"<title>{xml_escape(SITE['title'])}</title>"
        f"<link>{xml_escape(origin)}/</link>"
        f"<description>{xml_escape(SITE['description'])}</description>"
        "<language>en</language>"
        + "".join(items)
        + "</channel></rss>\n"
    )


def sitemap(posts: list[Post]) -> str:
    origin = SITE["url"].rstrip("/")
    urls = [f"<url><loc>{xml_escape(origin)}/</loc></url>"]
    urls.extend(
        f"<url><loc>{xml_escape(origin)}/{post.slug}/</loc>"
        f"<lastmod>{post.date.isoformat()}</lastmod></url>"
        for post in posts
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(urls)
        + "</urlset>\n"
    )


def build() -> None:
    posts = load_posts()  # Validate all Markdown before deleting the prior build.
    environment = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(["html", "xml"]),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    base = environment.get_template("base.html")
    index = environment.get_template("index.html")
    shared = {"site": SITE, "year": date.today().year}
    writings = [post for post in posts if post.kind == "writing"]
    notes = [post for post in posts if post.kind in {"note", "link"}]
    pages: dict[Path, str] = {
        Path("index.html"): index.render(
            **shared,
            page_title=None,
            description=SITE["description"],
            canonical=SITE["url"].rstrip("/") + "/",
            recent_writing=writings,
            notes=notes,
            posts=posts,
        ),
        Path("feed.xml"): rss_feed(posts),
        Path("sitemap.xml"): sitemap(posts),
        Path("robots.txt"): "User-agent: *\nAllow: /\nSitemap: "
        + SITE["url"].rstrip("/")
        + "/sitemap.xml\n",
    }
    for post in posts:
        pages[Path(post.slug) / "index.html"] = base.render(
            **shared,
            page_title=post.title,
            description=post.description,
            canonical=SITE["url"].rstrip("/") + f"/{post.slug}/",
            post=post,
            content=post.html,
        )

    if PUBLIC.is_symlink() or PUBLIC.resolve().parent != ROOT:
        raise ValueError("Refusing to clear a public directory outside this project")
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir()
    for relative_path, text in pages.items():
        destination = PUBLIC / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
    if ASSETS.is_dir():
        shutil.copytree(ASSETS, PUBLIC / "assets")
    print(f"Built {len(posts)} published posts in {PUBLIC}")


if __name__ == "__main__":
    build()
