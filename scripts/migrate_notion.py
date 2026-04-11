#!/usr/bin/env python3
"""
Migrate Notion export to Hugo-compatible content with PaperMod theme.
Converts Notion markdown files to Hugo posts with YAML front matter,
copies images, and fixes internal links.
"""

import csv
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

# ─── Configuration ───────────────────────────────────────────────────────────

SITE_ROOT = Path(__file__).resolve().parent.parent
NOTION_ROOT = SITE_ROOT / "notion_export" / "Sandeep Gangarapu"
CONTENT_DIR = SITE_ROOT / "content"
STATIC_DIR = SITE_ROOT / "static"
IMAGES_DIR = STATIC_DIR / "images"
PDFS_DIR = STATIC_DIR / "pdfs"

AUTHOR = "Sandeep Gangarapu"
DEFAULT_DATE = "2020-08-18T00:00:00-06:00"

# UUID pattern in Notion filenames: space + 32 hex chars
UUID_PATTERN = re.compile(r'\s+[a-f0-9]{32}$')

# Date patterns in content
DATE_PATTERN = re.compile(
    r'^(?:Created(?:\s+time)?:\s*)(.+)$', re.MULTILINE
)
BY_PATTERN = re.compile(r'^By:\s*(.+)$', re.MULTILINE)
TAGS_PATTERN = re.compile(r'^Tags:\s*(.+)$', re.MULTILINE)

# Aside patterns
ASIDE_OPEN = re.compile(r'<aside>\s*')
ASIDE_CLOSE = re.compile(r'\s*</aside>')

# Image patterns in Notion markdown
NOTION_IMG_PATTERN = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
NOTION_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

# Icon image pattern in aside blocks
ICON_IMG_PATTERN = re.compile(
    r'<img\s+src="[^"]*"\s+alt="[^"]*"\s+width="[^"]*"\s*/?\s*>'
)

# ─── Metadata index from CSVs ───────────────────────────────────────────────

metadata_index = {}  # title -> {date, tags, author, category}


def parse_date(date_str):
    """Parse Notion date string to ISO 8601."""
    date_str = date_str.strip()
    for fmt in [
        "%B %d, %Y %I:%M %p",
        "%B %d, %Y %I:%M%p",
        "%B %d, %Y",
    ]:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%dT%H:%M:%S-06:00")
        except ValueError:
            continue
    return None


def build_metadata_index():
    """Parse CSV files to build authoritative metadata for posts."""
    blog_dir = NOTION_ROOT / "Blog"
    csv_files = [
        (blog_dir / "Stories e5b43fd3e2d244d98046e5b02797e281_all.csv", "Stories"),
        (blog_dir / "Technical d7dcb979391e4d27a324f931d546499e_all.csv", "Technical"),
        (blog_dir / "Rolling Blog c971fb7ac18c4d48967c94c15b7a3d2b_all.csv", "Rolling Blog"),
    ]

    recipes_csv = NOTION_ROOT / "Recipes 92ea7d5a81d64987ac4cebd6031c4cd9_all.csv"
    if recipes_csv.exists():
        csv_files.append((recipes_csv, "Recipes"))

    for csv_path, category in csv_files:
        if not csv_path.exists():
            print(f"  WARNING: CSV not found: {csv_path.name}")
            continue

        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get('Name', '').strip()
                if not name:
                    continue

                # Date column varies: "Created" or "Created time"
                date_str = row.get('Created', '') or row.get('Created time', '')
                date_iso = parse_date(date_str) if date_str else None

                tags_str = row.get('Tags', '').strip()
                tags = [t.strip() for t in tags_str.split(',') if t.strip()] if tags_str else []

                author = row.get('By', AUTHOR).strip() or AUTHOR

                metadata_index[name] = {
                    'date': date_iso,
                    'tags': tags,
                    'author': author,
                    'category': category,
                }


# ─── Slug generation ────────────────────────────────────────────────────────

def generate_slug(title):
    """Generate a clean URL slug from a title."""
    slug = title.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug[:80]


def strip_uuid(name):
    """Strip Notion UUID from a filename/dirname."""
    return UUID_PATTERN.sub('', name).strip()


# ─── File path mapping (for internal link resolution) ────────────────────────

# Maps notion path fragments -> hugo URLs
notion_to_hugo_url = {}


def register_url(notion_path_fragment, hugo_url):
    """Register a mapping from Notion path to Hugo URL."""
    notion_to_hugo_url[notion_path_fragment] = hugo_url
    # Also register decoded version
    decoded = unquote(notion_path_fragment)
    if decoded != notion_path_fragment:
        notion_to_hugo_url[decoded] = hugo_url


# ─── Image handling ──────────────────────────────────────────────────────────

def slugify_filename(filename):
    """Clean up a filename for static serving."""
    name = filename.lower().strip()
    name = re.sub(r'[^a-z0-9._-]', '-', name)
    name = re.sub(r'-+', '-', name)
    name = name.strip('-')
    return name


def copy_image(src_path, dest_section, dest_slug=None):
    """
    Copy an image to static/images/<section>/<slug?>/<filename>.
    Returns the Hugo-relative URL path.
    """
    if not src_path.exists():
        print(f"  WARNING: Image not found: {src_path}")
        return None

    clean_name = slugify_filename(src_path.name)
    if dest_slug:
        dest_dir = IMAGES_DIR / dest_section / dest_slug
    else:
        dest_dir = IMAGES_DIR / dest_section

    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / clean_name

    # Handle duplicates
    counter = 1
    while dest_file.exists() and not _files_same(src_path, dest_file):
        stem = dest_file.stem
        suffix = dest_file.suffix
        dest_file = dest_dir / f"{stem}-{counter}{suffix}"
        counter += 1

    if not dest_file.exists():
        shutil.copy2(src_path, dest_file)

    return "/" + str(dest_file.relative_to(STATIC_DIR))


def _files_same(a, b):
    """Quick check if two files are the same size."""
    try:
        return a.stat().st_size == b.stat().st_size
    except OSError:
        return False


# ─── Content transformation ──────────────────────────────────────────────────

def parse_notion_file(filepath):
    """
    Parse a Notion markdown file.
    Returns: (title, date, author, tags, body)
    """
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Extract title from first line
    title = ""
    body_start = 0
    if lines and lines[0].startswith('# '):
        title = lines[0][2:].strip()
        body_start = 1

    # Skip blank line after title
    if body_start < len(lines) and lines[body_start].strip() == '':
        body_start += 1

    # Extract metadata from next few lines
    date_iso = None
    author = AUTHOR
    tags = []
    metadata_end = body_start

    for i in range(body_start, min(body_start + 6, len(lines))):
        line = lines[i].strip()
        if not line:
            metadata_end = i + 1
            continue

        date_match = re.match(r'^Created(?:\s+time)?:\s*(.+)$', line)
        if date_match:
            date_iso = parse_date(date_match.group(1))
            metadata_end = i + 1
            continue

        by_match = re.match(r'^By:\s*(.+)$', line)
        if by_match:
            author = by_match.group(1).strip()
            metadata_end = i + 1
            continue

        tags_match = re.match(r'^Tags:\s*(.+)$', line)
        if tags_match:
            tags = [t.strip() for t in tags_match.group(1).split(',') if t.strip()]
            metadata_end = i + 1
            continue

        # Non-metadata line found, stop looking
        if not line.startswith('Created') and not line.startswith('By:') and not line.startswith('Tags:'):
            break

    body = '\n'.join(lines[metadata_end:]).strip()

    return title, date_iso, author, tags, body


def transform_aside_blocks(body):
    """Convert Notion <aside> blocks to blockquotes or clean text."""
    result = []
    lines = body.split('\n')
    i = 0
    in_aside = False
    aside_content = []

    while i < len(lines):
        line = lines[i]

        # Check for aside open
        if '<aside>' in line:
            in_aside = True
            aside_content = []
            # Check if there's content on the same line after <aside>
            after = re.sub(r'<aside>\s*', '', line).strip()
            if after and '</aside>' not in after:
                aside_content.append(after)
            elif after and '</aside>' in after:
                # Single-line aside
                content = re.sub(r'</aside>', '', after).strip()
                if content:
                    result.append(f"> {content}")
                in_aside = False
            i += 1
            continue

        if in_aside:
            if '</aside>' in line:
                in_aside = False
                # Process accumulated aside content
                before_close = re.sub(r'\s*</aside>', '', line).strip()
                if before_close:
                    aside_content.append(before_close)

                # Convert aside to blockquote
                converted = convert_aside_content(aside_content)
                if converted:
                    result.append(converted)
                i += 1
                continue
            else:
                aside_content.append(line)
                i += 1
                continue

        result.append(line)
        i += 1

    return '\n'.join(result)


def convert_aside_content(lines):
    """Convert aside content lines to a blockquote."""
    # Join and clean
    text = '\n'.join(lines).strip()
    if not text:
        return ''

    # Remove icon images (nounproject, flaticon icons used for decoration)
    text = ICON_IMG_PATTERN.sub('', text).strip()

    # Check if it's a social link block (LinkedIn/Twitter with icon) - skip these
    if re.search(r'\*\*Linkedin\*\*|\*\*Twitter\*\*', text) and 'flaticon' in '\n'.join(lines):
        return ''

    # Check for emoji at the start (Notion callout pattern)
    emoji_match = re.match(r'^(\S{1,4})\s*\n\s*\n?(.*)', text, re.DOTALL)
    if emoji_match:
        emoji = emoji_match.group(1)
        content = emoji_match.group(2).strip()
        # Check if the emoji is actually an emoji (not regular text)
        if len(emoji) <= 2 or all(ord(c) > 127 for c in emoji):
            if content:
                # Multi-line blockquote
                bq_lines = content.split('\n')
                result = f"> **{emoji}** {bq_lines[0]}"
                for bql in bq_lines[1:]:
                    result += f"\n> {bql}"
                return result

    # Default: convert to blockquote
    if text:
        bq_lines = text.split('\n')
        result = f"> {bq_lines[0]}"
        for bql in bq_lines[1:]:
            result += f"\n> {bql}"
        return result

    return ''


def fix_image_paths(body, source_dir, section, slug):
    """Fix image references to point to Hugo static paths."""
    def replace_img(match):
        alt = match.group(1)
        raw_path = unquote(match.group(2))

        # External URL - keep as is
        if raw_path.startswith('http://') or raw_path.startswith('https://'):
            return match.group(0)

        # Resolve the image path relative to the source file's directory
        img_path = source_dir / raw_path
        if not img_path.exists():
            # Try from the parent directory
            img_path = source_dir.parent / raw_path
        if not img_path.exists():
            print(f"  WARNING: Image not found: {raw_path} (from {source_dir})")
            return match.group(0)

        # Copy image and get Hugo URL
        hugo_url = copy_image(img_path, section, slug)
        if hugo_url:
            return f"![{alt}]({hugo_url})"
        return match.group(0)

    return NOTION_IMG_PATTERN.sub(replace_img, body)


def fix_internal_links(body):
    """Fix internal Notion links to Hugo URLs."""
    def replace_link(match):
        text = match.group(1)
        raw_path = match.group(2)

        # External URL - keep as is
        if raw_path.startswith('http://') or raw_path.startswith('https://') or raw_path.startswith('mailto:'):
            return match.group(0)

        # Anchor links - keep as is
        if raw_path.startswith('#'):
            return match.group(0)

        decoded = unquote(raw_path)

        # Try to find a matching Hugo URL
        # Check exact match
        if decoded in notion_to_hugo_url:
            return f"[{text}]({notion_to_hugo_url[decoded]})"

        # Check just the filename part
        filename = decoded.split('/')[-1]
        if filename in notion_to_hugo_url:
            return f"[{text}]({notion_to_hugo_url[filename]})"

        # Strip UUID and try again
        clean_name = strip_uuid(filename.replace('.md', ''))
        for key, url in notion_to_hugo_url.items():
            clean_key = strip_uuid(key.replace('.md', '').split('/')[-1])
            if clean_name and clean_key and clean_name.lower() == clean_key.lower():
                return f"[{text}]({url})"

        # CSV links - convert to section links
        if decoded.endswith('.csv'):
            return f"[{text}](/blog/)"

        # PDF links
        if decoded.endswith('.pdf'):
            pdf_name = Path(decoded).name
            clean_pdf = slugify_filename(strip_uuid(pdf_name.replace('.pdf', '')) + '.pdf')
            return f"[{text}](/pdfs/{clean_pdf})"

        print(f"  WARNING: Could not resolve link: [{text}]({raw_path})")
        return match.group(0)

    # Only replace non-image links (don't match ! before [)
    return re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)', replace_link, body)


def strip_social_footer(body):
    """Remove repeated LinkedIn/Twitter social blocks at the end of pages."""
    # Pattern: last aside blocks that contain LinkedIn/Twitter
    lines = body.rstrip().split('\n')
    # Work backwards to find social footer
    end = len(lines)
    i = end - 1
    found_social = False

    while i >= 0:
        line = lines[i].strip()
        if not line:
            i -= 1
            continue
        if '</aside>' in line or '<aside>' in line:
            i -= 1
            continue
        if 'flaticon' in line and ('Linkedin' in line or 'Twitter' in line):
            found_social = True
            i -= 1
            continue
        if 'linkedin' in line.lower() or 'twitter' in line.lower() or 'x.com' in line.lower():
            if found_social or '<img' in lines[min(i+1, end-1)]:
                i -= 1
                continue
        break

    if found_social:
        # Remove from the detected start of social footer
        # Find the actual start of the social block
        while i < end and lines[i].strip() == '':
            i += 1
        return '\n'.join(lines[:i]).rstrip()

    return body


def generate_front_matter(title, date, author, tags, categories, series=None, draft=False, show_toc=True):
    """Generate YAML front matter string."""
    fm_lines = ['---']
    # Escape title for YAML
    safe_title = title.replace('"', '\\"')
    fm_lines.append(f'title: "{safe_title}"')
    fm_lines.append(f'date: {date}')
    fm_lines.append(f'author: "{author}"')
    fm_lines.append(f'draft: {str(draft).lower()}')
    fm_lines.append(f'ShowToc: {str(show_toc).lower()}')
    fm_lines.append(f'TocOpen: false')

    if tags:
        tags_yaml = ', '.join(f'"{t}"' for t in tags)
        fm_lines.append(f'tags: [{tags_yaml}]')

    if categories:
        cats_yaml = ', '.join(f'"{c}"' for c in categories)
        fm_lines.append(f'categories: [{cats_yaml}]')

    if series:
        series_yaml = ', '.join(f'"{s}"' for s in series)
        fm_lines.append(f'series: [{series_yaml}]')

    fm_lines.append('---')
    return '\n'.join(fm_lines)


# ─── Processing functions ────────────────────────────────────────────────────

def get_companion_dir(md_file):
    """
    Get the companion directory for a Notion markdown file.
    Notion creates a directory with the same name (minus extension) for images.
    """
    # The companion dir name matches the md file name without .md
    dir_name = md_file.stem
    # But we also need to check without UUID since dirs might not have UUIDs
    clean_name = strip_uuid(dir_name)

    parent = md_file.parent

    # Try exact match
    candidate = parent / dir_name
    if candidate.is_dir():
        return candidate

    # Try without UUID
    for d in parent.iterdir():
        if d.is_dir() and strip_uuid(d.name) == clean_name:
            return d

    return None


def collect_sub_pages(parent_dir, parent_title):
    """
    Collect sub-pages from a parent directory.
    Returns list of (filepath, title, is_small) tuples.
    """
    if not parent_dir or not parent_dir.is_dir():
        return []

    sub_pages = []
    for item in sorted(parent_dir.iterdir()):
        if item.suffix == '.md':
            title = strip_uuid(item.stem)
            size = item.stat().st_size
            sub_pages.append((item, title, size < 300))
        elif item.is_dir():
            # Check for deeper sub-pages
            for sub_item in sorted(item.iterdir()):
                if sub_item.suffix == '.md':
                    title = strip_uuid(sub_item.stem)
                    size = sub_item.stat().st_size
                    sub_pages.append((sub_item, title, size < 300))

    return sub_pages


def process_single_page(md_file, hugo_path, section_name):
    """Process a standalone page (About, Projects, etc.)."""
    title, date_iso, author, tags, body = parse_notion_file(md_file)
    if not date_iso:
        date_iso = DEFAULT_DATE

    slug = generate_slug(title)

    # Copy companion images
    companion = get_companion_dir(md_file)
    if companion:
        for img_file in companion.iterdir():
            if img_file.suffix.lower() in ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'):
                copy_image(img_file, section_name)
            elif img_file.suffix.lower() == '.pdf':
                PDFS_DIR.mkdir(parents=True, exist_ok=True)
                clean_name = slugify_filename(img_file.name)
                shutil.copy2(img_file, PDFS_DIR / clean_name)

    # Transform body
    body = transform_aside_blocks(body)
    body = fix_image_paths(body, md_file.parent, section_name, None)
    body = strip_social_footer(body)

    # Front matter
    fm = generate_front_matter(title, date_iso, author, tags, [])

    # Write
    hugo_path.parent.mkdir(parents=True, exist_ok=True)
    hugo_path.write_text(fm + '\n\n' + body + '\n', encoding='utf-8')
    print(f"  Created: {hugo_path.relative_to(CONTENT_DIR)}")

    return slug


def process_blog_post(md_file, category, section_path, series_name=None):
    """
    Process a blog post. Returns the slug used.
    category: Stories, Technical, or Rolling Blog
    section_path: Hugo content path for this category
    """
    title, date_iso, author, tags, body = parse_notion_file(md_file)

    # Look up metadata from CSV index
    csv_meta = metadata_index.get(title, {})
    if not date_iso:
        date_iso = csv_meta.get('date', DEFAULT_DATE)
    if not tags and csv_meta.get('tags'):
        tags = csv_meta['tags']

    # Handle untitled post
    if title == "Untitled" or not title:
        # Try to generate a title from content
        first_line = body.strip().split('\n')[0] if body else "Untitled Post"
        title = first_line[:60].strip('*').strip()
        if not title:
            title = "Untitled Post"

    slug = generate_slug(title)

    # Determine Hugo URL for link mapping
    cat_slug = generate_slug(category)
    hugo_url = f"/blog/{cat_slug}/{slug}/"

    # Register this file for link resolution
    register_url(md_file.name, hugo_url)
    register_url(strip_uuid(md_file.name), hugo_url)

    # Copy companion images
    companion = get_companion_dir(md_file)
    if companion:
        for img_file in companion.iterdir():
            if img_file.is_file() and img_file.suffix.lower() in ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'):
                copy_image(img_file, f"blog/{cat_slug}", slug)

    # Handle sub-pages
    sub_page_dir = None
    clean_title = strip_uuid(md_file.stem)
    for d in md_file.parent.iterdir():
        if d.is_dir() and strip_uuid(d.name) == clean_title:
            sub_page_dir = d
            break

    sub_pages = collect_sub_pages(sub_page_dir, title)

    # Check if we should inline small sub-pages
    small_subs = [(fp, t, s) for fp, t, s in sub_pages if s]
    large_subs = [(fp, t, s) for fp, t, s in sub_pages if not s]

    # If ALL sub-pages are small, inline them
    inline_all = len(sub_pages) > 0 and len(large_subs) == 0

    # Inline small sub-pages into parent body
    if inline_all and sub_pages:
        for sub_fp, sub_title, _ in sub_pages:
            _, _, _, _, sub_body = parse_notion_file(sub_fp)
            if sub_body.strip():
                body += f"\n\n### {sub_title}\n\n{sub_body}"

    # Process large sub-pages as separate posts
    series = [series_name] if series_name else ([title] if large_subs else None)

    for sub_fp, sub_title, is_small in large_subs:
        if is_small:
            continue
        process_blog_post(
            sub_fp, category, section_path,
            series_name=series_name or title
        )

    # Also process small sub-pages that weren't inlined (when there's a mix)
    if not inline_all:
        for sub_fp, sub_title, is_small in small_subs:
            process_blog_post(
                sub_fp, category, section_path,
                series_name=series_name or title
            )

    # Transform body
    body = transform_aside_blocks(body)
    body = fix_image_paths(body, md_file.parent, f"blog/{cat_slug}", slug)
    body = strip_social_footer(body)

    # Determine categories
    categories = [category]

    # Front matter
    fm = generate_front_matter(
        title, date_iso, author, tags, categories,
        series=series
    )

    # Write
    dest_file = section_path / f"{slug}.md"
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    dest_file.write_text(fm + '\n\n' + body + '\n', encoding='utf-8')
    print(f"  Created: {dest_file.relative_to(CONTENT_DIR)}")

    return slug


def process_recipe(md_file, section_path):
    """Process a recipe post."""
    title, date_iso, author, tags, body = parse_notion_file(md_file)

    csv_meta = metadata_index.get(title, {})
    if not date_iso:
        date_iso = csv_meta.get('date', DEFAULT_DATE)
    if not tags and csv_meta.get('tags'):
        tags = csv_meta['tags']

    slug = generate_slug(title)
    hugo_url = f"/recipes/{slug}/"
    register_url(md_file.name, hugo_url)

    # Copy companion images
    companion = get_companion_dir(md_file)
    if companion:
        for img_file in companion.iterdir():
            if img_file.is_file() and img_file.suffix.lower() in ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'):
                copy_image(img_file, "recipes", slug)

    # Handle sub-pages (like Maggi-Microwave, Veg Ramen dirs)
    sub_page_dir = None
    clean_title = strip_uuid(md_file.stem)
    for d in md_file.parent.iterdir():
        if d.is_dir() and strip_uuid(d.name) == clean_title:
            sub_page_dir = d
            break

    if sub_page_dir:
        for item in sub_page_dir.iterdir():
            if item.suffix.lower() in ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'):
                copy_image(item, "recipes", slug)

    body = transform_aside_blocks(body)
    body = fix_image_paths(body, md_file.parent, "recipes", slug)

    fm = generate_front_matter(title, date_iso, author, tags, ["Recipes"])

    dest_file = section_path / f"{slug}.md"
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    dest_file.write_text(fm + '\n\n' + body + '\n', encoding='utf-8')
    print(f"  Created: {dest_file.relative_to(CONTENT_DIR)}")


# ─── First pass: register all URLs ──────────────────────────────────────────

def register_all_urls():
    """First pass: register all Notion files with their Hugo URLs for link resolution."""
    print("\n[Pass 1] Registering URL mappings...")

    # Single pages
    pages = {
        "About me": "/about/",
        "Activity Stream": "/activity-stream/",
        "Things I built": "/projects/",
        "Research": "/research/",
        "Learning Resources": "/resources/",
        "Blog": "/blog/",
        "Socials": "/about/",  # redirect socials to about
    }

    for md_file in NOTION_ROOT.iterdir():
        if md_file.suffix == '.md':
            clean = strip_uuid(md_file.stem)
            if clean in pages:
                register_url(md_file.name, pages[clean])

    # Blog posts
    blog_dir = NOTION_ROOT / "Blog"
    for category_name, cat_slug in [("Stories", "stories"), ("Technical", "technical"), ("Rolling Blog", "rolling-blog")]:
        cat_dir = blog_dir / category_name
        if not cat_dir.is_dir():
            continue

        for md_file in cat_dir.iterdir():
            if md_file.suffix == '.md':
                title = strip_uuid(md_file.stem)
                slug = generate_slug(title)
                hugo_url = f"/blog/{cat_slug}/{slug}/"
                register_url(md_file.name, hugo_url)
                # Also register by relative path patterns
                register_url(f"Blog/{category_name}/{md_file.name}", hugo_url)

                # Sub-pages
                companion = None
                clean_title = strip_uuid(md_file.stem)
                for d in cat_dir.iterdir():
                    if d.is_dir() and strip_uuid(d.name) == clean_title:
                        companion = d
                        break

                if companion:
                    for sub in companion.iterdir():
                        if sub.suffix == '.md':
                            sub_title = strip_uuid(sub.stem)
                            sub_slug = generate_slug(sub_title)
                            sub_url = f"/blog/{cat_slug}/{sub_slug}/"
                            register_url(sub.name, sub_url)
                            register_url(f"{category_name}/{companion.name}/{sub.name}", sub_url)

                            # Deeper sub-pages
                            sub_companion = None
                            for sd in companion.iterdir():
                                if sd.is_dir() and strip_uuid(sd.name) == strip_uuid(sub.stem):
                                    sub_companion = sd
                                    break
                            if sub_companion:
                                for deep in sub_companion.iterdir():
                                    if deep.suffix == '.md':
                                        deep_title = strip_uuid(deep.stem)
                                        deep_slug = generate_slug(deep_title)
                                        deep_url = f"/blog/{cat_slug}/{deep_slug}/"
                                        register_url(deep.name, deep_url)

    # Recipes
    recipes_dir = NOTION_ROOT / "Recipes"
    if recipes_dir.is_dir():
        for md_file in recipes_dir.iterdir():
            if md_file.suffix == '.md':
                title = strip_uuid(md_file.stem)
                slug = generate_slug(title)
                register_url(md_file.name, f"/recipes/{slug}/")

    print(f"  Registered {len(notion_to_hugo_url)} URL mappings")


# ─── Main processing ─────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Notion → Hugo Migration Script")
    print("=" * 60)

    # Build metadata index
    print("\n[Setup] Building metadata index from CSVs...")
    build_metadata_index()
    print(f"  Found metadata for {len(metadata_index)} posts")

    # Register URLs first pass
    register_all_urls()

    # Create directory structure
    print("\n[Setup] Creating directory structure...")
    for d in [CONTENT_DIR, STATIC_DIR, IMAGES_DIR, PDFS_DIR,
              CONTENT_DIR / "blog" / "stories",
              CONTENT_DIR / "blog" / "technical",
              CONTENT_DIR / "blog" / "rolling-blog",
              CONTENT_DIR / "recipes"]:
        d.mkdir(parents=True, exist_ok=True)

    # ─── Copy profile image ─────────────────────────────────────────────
    print("\n[Profile] Copying profile image...")
    profile_img = NOTION_ROOT / "vivekkrishnanphotography-6_websize.jpg"
    if profile_img.exists():
        dest = IMAGES_DIR / "profile"
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(profile_img, dest / "vivekkrishnanphotography-6_websize.jpg")
        print(f"  Copied profile image")

    # Also copy headshot from About me
    headshot = NOTION_ROOT / "About me" / "sandeep_headshot.jpeg"
    if headshot.exists():
        dest = IMAGES_DIR / "profile"
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(headshot, dest / "sandeep_headshot.jpeg")
        print(f"  Copied headshot")

    # ─── Process single pages ────────────────────────────────────────────
    print("\n[Pages] Processing single pages...")

    single_pages = [
        ("About me", "about.md", "about"),
        ("Activity Stream", "activity-stream.md", "activity-stream"),
        ("Things I built", "projects.md", "projects"),
        ("Research", "research.md", "research"),
        ("Learning Resources", "resources.md", "resources"),
    ]

    for notion_name, hugo_filename, section in single_pages:
        # Find the markdown file
        md_file = None
        for f in NOTION_ROOT.iterdir():
            if f.suffix == '.md' and strip_uuid(f.stem) == notion_name:
                md_file = f
                break
        if md_file:
            process_single_page(md_file, CONTENT_DIR / hugo_filename, section)
        else:
            print(f"  WARNING: Not found: {notion_name}")

    # ─── Process blog posts ──────────────────────────────────────────────
    blog_dir = NOTION_ROOT / "Blog"

    for category_name, cat_slug in [("Stories", "stories"), ("Technical", "technical"), ("Rolling Blog", "rolling-blog")]:
        print(f"\n[Blog/{category_name}] Processing posts...")
        cat_dir = blog_dir / category_name
        section_path = CONTENT_DIR / "blog" / cat_slug

        if not cat_dir.is_dir():
            print(f"  WARNING: Category directory not found: {cat_dir}")
            continue

        for md_file in sorted(cat_dir.iterdir()):
            if md_file.suffix == '.md':
                process_blog_post(md_file, category_name, section_path)

    # ─── Process recipes ─────────────────────────────────────────────────
    print("\n[Recipes] Processing recipes...")
    recipes_dir = NOTION_ROOT / "Recipes"
    recipes_path = CONTENT_DIR / "recipes"

    if recipes_dir.is_dir():
        for md_file in sorted(recipes_dir.iterdir()):
            if md_file.suffix == '.md':
                process_recipe(md_file, recipes_path)

    # ─── Copy PDFs ───────────────────────────────────────────────────────
    print("\n[PDFs] Copying PDF files...")
    research_dir = NOTION_ROOT / "Research"
    if research_dir.is_dir():
        for pdf_file in research_dir.iterdir():
            if pdf_file.suffix == '.pdf':
                clean_name = slugify_filename(pdf_file.name)
                PDFS_DIR.mkdir(parents=True, exist_ok=True)
                shutil.copy2(pdf_file, PDFS_DIR / clean_name)
                print(f"  Copied: {clean_name}")

    # Also check Things I built directory for PDFs
    things_dir = NOTION_ROOT / "Things I built"
    if things_dir.is_dir():
        for pdf_file in things_dir.iterdir():
            if pdf_file.suffix == '.pdf':
                clean_name = slugify_filename(pdf_file.name)
                PDFS_DIR.mkdir(parents=True, exist_ok=True)
                shutil.copy2(pdf_file, PDFS_DIR / clean_name)
                print(f"  Copied: {clean_name}")

    # ─── Second pass: fix internal links ─────────────────────────────────
    print("\n[Pass 2] Fixing internal links in all content files...")
    fix_count = 0
    for md_file in CONTENT_DIR.rglob('*.md'):
        content = md_file.read_text(encoding='utf-8')
        fixed = fix_internal_links(content)
        if fixed != content:
            md_file.write_text(fixed, encoding='utf-8')
            fix_count += 1

    print(f"  Fixed links in {fix_count} files")

    # ─── Summary ─────────────────────────────────────────────────────────
    total_content = list(CONTENT_DIR.rglob('*.md'))
    total_images = list(IMAGES_DIR.rglob('*'))
    total_images = [f for f in total_images if f.is_file()]
    total_pdfs = list(PDFS_DIR.rglob('*.pdf')) if PDFS_DIR.exists() else []

    print("\n" + "=" * 60)
    print("Migration Summary")
    print("=" * 60)
    print(f"  Content files: {len(total_content)}")
    print(f"  Images copied: {len(total_images)}")
    print(f"  PDFs copied:   {len(total_pdfs)}")
    print(f"  URL mappings:  {len(notion_to_hugo_url)}")
    print("=" * 60)


if __name__ == '__main__':
    main()
