#!/usr/bin/env python3
"""
Girl Scouts Troop Site Builder
================================
Converts content/*.md files into HTML pages for GitHub Pages.

Usage:  python _build/build.py
Output: Regenerates HTML files in the repo root and detail/ subdirectory.

Content folder layout:
  content/
    meetings/          ← one .md per meeting plan
    activities/        ← one .md per activity/craft/game
    communications/    ← one .md per parent communication
    resources/         ← one .md per template/checklist/guide
    onboarding/        ← onboarding sub-page docs (5 pages)
"""

import os
import re
import markdown
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"

# ---------------------------------------------------------------------------
# Shared HTML fragments
# ---------------------------------------------------------------------------

NAV = """\
  <nav class="navbar">
    <div class="container">
      <a href="{base}index.html" class="navbar-brand">
        <span class="logo">🍀</span>
        <span>GS Troop Materials</span>
      </a>
      <ul class="navbar-nav">
        <li><a href="{base}index.html">Home</a></li>
        <li><a href="{base}onboarding.html">Onboarding</a></li>
        <li><a href="{base}meetings.html">Meetings</a></li>
        <li><a href="{base}activities.html">Activities</a></li>
        <li><a href="{base}communications.html">Communications</a></li>
        <li><a href="{base}resources.html">Resources</a></li>
      </ul>
    </div>
  </nav>"""

FOOTER = """\
  <footer class="footer">
    <div class="container">
      <p>🍀 Girl Scouts Troop Materials • Auto-backed up via OpenClaw</p>
      <p style="margin-top: 0.5rem; font-size: 0.75rem;">For troop use only • Not affiliated with GSUSA</p>
    </div>
  </footer>"""


def nav(base=""):
    return NAV.format(base=base)


def page_shell(title, body, css_base="", js_base=""):
    """Wrap content in a full HTML page."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - Girl Scouts Troop Materials</title>
  <link rel="stylesheet" href="{css_base}css/style.css">
</head>
<body>
{nav(css_base)}
{body}
{FOOTER}
  <script src="{js_base}js/search.js"></script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------

def parse_md(path):
    """Parse a .md file; return (frontmatter_dict, body_string)."""
    text = Path(path).read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
            except Exception:
                fm = {}
            return fm, parts[2].strip()
    return {}, text.strip()


def to_html(md_text):
    return markdown.markdown(md_text, extensions=["extra", "tables"])


def load_folder(folder_name):
    """Load all .md files from a content subfolder, sorted by filename."""
    folder = CONTENT / folder_name
    if not folder.exists():
        return []
    items = []
    for f in sorted(folder.glob("*.md")):
        fm, body = parse_md(f)
        items.append({"meta": fm, "body": body, "slug": f.stem})
    return items


def auto_description(fm, body):
    """Pull description from frontmatter or first paragraph of body."""
    if fm.get("description"):
        return fm["description"]
    if body:
        first = re.sub(r"^#+\s+", "", body.split("\n\n")[0]).strip()
        first = re.sub(r"[*_`]", "", first)
        return (first[:200] + "…") if len(first) > 200 else first
    return ""


# ---------------------------------------------------------------------------
# Card rendering
# ---------------------------------------------------------------------------

def render_card(item, detail_url=None):
    fm = item["meta"]
    title = fm.get("title", item["slug"].replace("-", " ").title())
    icon = fm.get("icon", "📄")
    tags = fm.get("tags", [])
    description = auto_description(fm, item["body"])
    search_terms = f"{title} {' '.join(str(t) for t in tags)} {description}".lower()
    tag_html = "".join(f'<span class="card-badge">{t}</span>' for t in tags)
    action = f'<a href="{detail_url}" class="btn btn-primary">View</a>' if detail_url else ""
    return f"""\
        <div class="card" data-searchable="{search_terms}">
          <div class="card-header">
            <span class="card-icon">{icon}</span>
            <div style="flex: 1;">
              <h3 class="card-title">{title}</h3>
              <div class="card-meta">{tag_html}</div>
            </div>
          </div>
          <p class="card-description">{description}</p>
          <div class="card-actions">{action}</div>
        </div>"""


def render_card_grid(items, detail_prefix, empty_icon, empty_label):
    """Render a grid of cards, or an empty state."""
    if not items:
        return f"""\
      <div class="empty-state">
        <div class="icon">{empty_icon}</div>
        <h3>No {empty_label} Yet</h3>
        <p>Add .md files to the <code>content/{empty_label.lower()}/</code> folder and commit — they'll appear here automatically.</p>
      </div>"""
    cards = "\n".join(
        render_card(item, f"{detail_prefix}{item['slug']}.html") for item in items
    )
    return f'<div class="cards-grid">\n{cards}\n      </div>'


# ---------------------------------------------------------------------------
# Detail page rendering
# ---------------------------------------------------------------------------

def render_detail_page(item, back_url, back_label, css_base="../../"):
    fm = item["meta"]
    title = fm.get("title", item["slug"].replace("-", " ").title())
    icon = fm.get("icon", "📄")
    tags = fm.get("tags", [])
    tag_html = "".join(f'<span class="card-badge">{t}</span>' for t in tags)
    content_html = to_html(item["body"]) if item["body"] else "<p><em>No content yet.</em></p>"

    body = f"""\
  <div class="container">
    <div class="page-header">
      <h1>{icon} {title}</h1>
      <div class="card-meta" style="margin-top: 0.5rem;">{tag_html}</div>
    </div>
  </div>
  <main class="main-content">
    <div class="container">
      <div class="card" style="max-width: 800px;">
        <div class="prose">
          {content_html}
        </div>
      </div>
      <div style="margin-top: 1.5rem;">
        <a href="{css_base}{back_url}" class="btn btn-secondary">← Back to {back_label}</a>
      </div>
    </div>
  </main>"""

    return page_shell(title, body, css_base=css_base, js_base=css_base)


# ---------------------------------------------------------------------------
# List page generators
# ---------------------------------------------------------------------------

SEARCH_BAR = """\
      <div class="search-container">
        <div class="search-box">
          <span class="search-icon">🔍</span>
          <input type="text" id="search-input" placeholder="{placeholder}" autocomplete="off">
        </div>
      </div>
      <div id="no-results" class="empty-state hidden">
        <div class="icon">🔍</div>
        <h3>No results for "<span class="search-term"></span>"</h3>
        <p>Try a different search term.</p>
      </div>"""


def build_meetings(items):
    grid = render_card_grid(items, "detail/meetings/", "📅", "Meetings")
    tips_md = (CONTENT / "pages" / "meetings-tips.md")
    tips_section = ""
    if tips_md.exists():
        _, tips_body = parse_md(tips_md)
        tips_html = to_html(tips_body)
        tips_section = f"""\
      <div class="section-group">
        <h2>Meeting Tips</h2>
        <div class="card">
          <div class="card-header">
            <span class="card-icon">💡</span>
            <h3 class="card-title">Best Practices for Troop Meetings</h3>
          </div>
          <div class="prose" style="margin-top: 1rem; color: var(--gray-700);">
            {tips_html}
          </div>
        </div>
      </div>"""

    search = SEARCH_BAR.format(placeholder="Search meetings by date, theme, or activity...")
    body = f"""\
  <div class="container">
    <div class="page-header">
      <h1>📅 Meetings</h1>
      <p>Meeting plans, agendas, and schedules for your troop</p>
    </div>
  </div>
  <main class="main-content">
    <div class="container">
{search}
      <div class="section-group">
        <h2>Meeting Plans</h2>
        {grid}
      </div>
{tips_section}
    </div>
  </main>"""
    return page_shell("Meetings", body)


def build_activities(items):
    grid = render_card_grid(items, "detail/activities/", "🎨", "Activities")
    search = SEARCH_BAR.format(placeholder="Search activities by badge, skill, or theme...")
    body = f"""\
  <div class="container">
    <div class="page-header">
      <h1>🎨 Activities</h1>
      <p>Badge activities, crafts, and skill-building exercises for ages 6–7</p>
    </div>
  </div>
  <main class="main-content">
    <div class="container">
{search}
      <div class="section-group">
        <h2>Badge Activities &amp; Crafts</h2>
        {grid}
      </div>
    </div>
  </main>"""
    return page_shell("Activities", body)


def build_communications(items):
    grid = render_card_grid(items, "detail/communications/", "📧", "Communications")
    search = SEARCH_BAR.format(placeholder="Search communications by type, date, or topic...")
    body = f"""\
  <div class="container">
    <div class="page-header">
      <h1>📧 Communications</h1>
      <p>Parent emails, permission slips, newsletters, and schedules</p>
    </div>
  </div>
  <main class="main-content">
    <div class="container">
{search}
      <div class="section-group">
        <h2>Parent Communications</h2>
        {grid}
      </div>
    </div>
  </main>"""
    return page_shell("Communications", body)


def build_resources(items):
    grid = render_card_grid(items, "detail/resources/", "📚", "Resources")
    search = SEARCH_BAR.format(placeholder="Search resources by type, category, or topic...")

    links_section = """\
      <div class="section-group">
        <h2>Helpful Links</h2>
        <div class="card">
          <div class="card-header">
            <span class="card-icon">🔗</span>
            <h3 class="card-title">External Resources</h3>
          </div>
          <ul style="margin-left: 1.5rem; margin-top: 1rem; color: var(--gray-700); line-height: 1.8;">
            <li><a href="https://www.girlscouts.org/" target="_blank" style="color: var(--gs-green); font-weight: 500;">Girl Scouts USA Official Site</a></li>
            <li><a href="https://www.girlscouts.org/en/activities-for-girls.html" target="_blank" style="color: var(--gs-green); font-weight: 500;">GSUSA Activity Finder</a></li>
            <li><a href="https://www.girlscouts.org/en/our-program/badges.html" target="_blank" style="color: var(--gs-green); font-weight: 500;">Badge Explorer</a></li>
            <li><strong>Volunteer Toolkit:</strong> Access leader resources and planning tools</li>
          </ul>
        </div>
      </div>"""

    body = f"""\
  <div class="container">
    <div class="page-header">
      <h1>📚 Resources</h1>
      <p>Templates, checklists, and helpful references for troop leaders</p>
    </div>
  </div>
  <main class="main-content">
    <div class="container">
{search}
      <div class="section-group">
        <h2>Templates, Checklists &amp; Guides</h2>
        {grid}
      </div>
{links_section}
    </div>
  </main>"""
    return page_shell("Resources", body)


def build_onboarding_hub(items):
    """Build onboarding.html hub page."""
    cards = []
    for i, item in enumerate(items, 1):
        fm = item["meta"]
        title = fm.get("title", item["slug"].replace("-", " ").title())
        icon = fm.get("icon", "📖")
        description = auto_description(fm, item["body"])
        slug = item["slug"]
        url = f"onboarding-{slug}.html"
        cards.append(f"""\
          <div class="card">
            <div class="card-header">
              <span class="card-icon">{icon}</span>
              <h3 class="card-title">{i}. {title}</h3>
            </div>
            <p class="card-description">{description}</p>
            <div class="card-actions">
              <a href="{url}" class="btn btn-primary">Read Guide</a>
            </div>
          </div>""")
    cards_html = "\n".join(cards)

    body = f"""\
  <div class="container">
    <div class="hero">
      <h1>🌼 Daisy Troop Onboarding Package</h1>
      <p>Everything Megan &amp; Sasha need to launch an amazing troop of 8 Daisies, ages 6–7</p>
    </div>
  </div>
  <main class="main-content">
    <div class="container">
      <div class="section-group">
        <h2>Your Onboarding Roadmap</h2>
        <p style="color: var(--gray-700); margin-bottom: 1.5rem;">Work through these guides in order. Each one builds on the last. You've got this! 💪</p>
        <div class="cards-grid">
{cards_html}
        </div>
      </div>
    </div>
  </main>"""
    return page_shell("Onboarding", body)


def build_onboarding_page(item):
    """Build an individual onboarding sub-page."""
    fm = item["meta"]
    title = fm.get("title", item["slug"].replace("-", " ").title())
    icon = fm.get("icon", "📖")
    content_html = to_html(item["body"]) if item["body"] else "<p><em>No content yet.</em></p>"

    body = f"""\
  <div class="container">
    <div class="page-header">
      <h1>{icon} {title}</h1>
    </div>
  </div>
  <main class="main-content">
    <div class="container">
      <div class="card" style="max-width: 800px;">
        <div class="prose">
          {content_html}
        </div>
      </div>
      <div style="margin-top: 1.5rem;">
        <a href="onboarding.html" class="btn btn-secondary">← Back to Onboarding</a>
      </div>
    </div>
  </main>"""
    return page_shell(title, body)


def build_index(meetings, activities, communications, resources):
    """Rebuild index.html with live counts."""
    m_count = len(meetings)
    a_count = len(activities)
    c_count = len(communications)
    r_count = len(resources)

    body = f"""\
  <div class="container">
    <div class="hero">
      <h1>🌟 Girl Scouts Troop Materials 🌟</h1>
      <p>Everything you need to lead an amazing troop of 8 girls, ages 6–7</p>
      <div class="hero-actions">
        <a href="meetings.html" class="btn btn-light">View Meetings</a>
        <a href="activities.html" class="btn btn-light">Browse Activities</a>
        <a href="resources.html" class="btn btn-light">Get Resources</a>
      </div>
    </div>
  </div>
  <main class="main-content">
    <div class="container">
      <div class="stats">
        <div class="stat-card">
          <span class="stat-value">{m_count}</span>
          <span class="stat-label">Meeting Plans</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{a_count}</span>
          <span class="stat-label">Activities &amp; Badges</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{c_count}</span>
          <span class="stat-label">Communications</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{r_count}</span>
          <span class="stat-label">Resources</span>
        </div>
      </div>

      <div class="section-group">
        <h2>Quick Access</h2>
        <div class="cards-grid">
          <div class="card">
            <div class="card-header">
              <span class="card-icon">📅</span>
              <h3 class="card-title">Meetings</h3>
            </div>
            <p class="card-description">Meeting plans, agendas, and schedules for your troop.</p>
            <div class="card-actions"><a href="meetings.html" class="btn btn-primary">View Meetings</a></div>
          </div>
          <div class="card">
            <div class="card-header">
              <span class="card-icon">🎨</span>
              <h3 class="card-title">Activities</h3>
            </div>
            <p class="card-description">Badge activities, crafts, and skill-building exercises for ages 6–7.</p>
            <div class="card-actions"><a href="activities.html" class="btn btn-primary">Browse Activities</a></div>
          </div>
          <div class="card">
            <div class="card-header">
              <span class="card-icon">📧</span>
              <h3 class="card-title">Communications</h3>
            </div>
            <p class="card-description">Parent emails, permission slips, newsletters, and schedules.</p>
            <div class="card-actions"><a href="communications.html" class="btn btn-primary">View Communications</a></div>
          </div>
          <div class="card">
            <div class="card-header">
              <span class="card-icon">📚</span>
              <h3 class="card-title">Resources</h3>
            </div>
            <p class="card-description">Templates, checklists, and references to make troop leadership easier.</p>
            <div class="card-actions"><a href="resources.html" class="btn btn-primary">Get Resources</a></div>
          </div>
        </div>
      </div>

      <div class="section-group">
        <h2>Getting Started</h2>
        <div class="card">
          <div class="card-header">
            <span class="card-icon">💡</span>
            <h3 class="card-title">How to Use This Site</h3>
          </div>
          <ul style="margin-left: 1.5rem; margin-top: 1rem; color: var(--gray-700);">
            <li><strong>Meetings:</strong> Find meeting plans organized by date and theme</li>
            <li><strong>Activities:</strong> Browse badge activities and crafts by category</li>
            <li><strong>Communications:</strong> Access parent emails, permission slips, and schedules</li>
            <li><strong>Resources:</strong> Download templates, checklists, and helpful guides</li>
            <li><strong>Search:</strong> Use the search bar on any page to quickly find what you need</li>
          </ul>
        </div>
      </div>
    </div>
  </main>"""
    return page_shell("Home", body)


# ---------------------------------------------------------------------------
# File writer
# ---------------------------------------------------------------------------

def write(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")
    print(f"  ✓ {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("🔨 Building Girl Scouts Troop site...")

    meetings = load_folder("meetings")
    activities = load_folder("activities")
    communications = load_folder("communications")
    resources = load_folder("resources")
    onboarding = load_folder("onboarding")

    # Top-level list pages
    write(ROOT / "index.html", build_index(meetings, activities, communications, resources))
    write(ROOT / "meetings.html", build_meetings(meetings))
    write(ROOT / "activities.html", build_activities(activities))
    write(ROOT / "communications.html", build_communications(communications))
    write(ROOT / "resources.html", build_resources(resources))
    write(ROOT / "onboarding.html", build_onboarding_hub(onboarding))

    # Onboarding sub-pages
    for item in onboarding:
        write(ROOT / f"onboarding-{item['slug']}.html", build_onboarding_page(item))

    # Detail pages
    for item in meetings:
        html = render_detail_page(item, "meetings.html", "Meetings")
        write(ROOT / "detail" / "meetings" / f"{item['slug']}.html", html)

    for item in activities:
        html = render_detail_page(item, "activities.html", "Activities")
        write(ROOT / "detail" / "activities" / f"{item['slug']}.html", html)

    for item in communications:
        html = render_detail_page(item, "communications.html", "Communications")
        write(ROOT / "detail" / "communications" / f"{item['slug']}.html", html)

    for item in resources:
        html = render_detail_page(item, "resources.html", "Resources")
        write(ROOT / "detail" / "resources" / f"{item['slug']}.html", html)

    print(f"\n✅ Done! {len(meetings)} meetings, {len(activities)} activities, "
          f"{len(communications)} communications, {len(resources)} resources, "
          f"{len(onboarding)} onboarding pages.")


if __name__ == "__main__":
    main()
