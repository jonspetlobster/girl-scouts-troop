# Girl Scouts Troop Materials - Static Site

A clean, searchable static website for organizing Girl Scouts troop materials for 8 girls, ages 6-7.

## 🌟 Features

- **Girl Scouts Branding** — Official GS green with warm, inviting design
- **Responsive** — Works on phones, tablets, and desktops
- **Searchable** — Real-time search across all pages
- **No Build Required** — Pure HTML, CSS, and JavaScript
- **Organized** — Meetings, Activities, Communications, Resources

## 📂 Adding Content

### Quick Start
1. Edit HTML files in this folder
2. Copy an example card and modify with your content
3. Commit and push — site updates automatically

### Each Page
- **Meetings** — Planning docs, agendas, themes
- **Activities** — Badges, crafts, games for ages 6-7
- **Communications** — Parent emails, forms, schedules
- **Resources** — Templates, checklists, guides

### Card Template
```html
<div class="card" data-searchable="keywords for search">
  <div class="card-header">
    <span class="card-icon">🎨</span>
    <h3 class="card-title">Your Title</h3>
  </div>
  <p class="card-description">Brief description</p>
  <div class="card-actions">
    <a href="file.pdf" class="btn btn-primary">View</a>
  </div>
</div>
```

## 🔍 Search

Real-time filtering on every page. Search looks at:
- Titles
- Descriptions  
- Badge types
- Keywords in `data-searchable` attribute

## 🚀 GitHub Pages

Site is automatically deployed to GitHub Pages. Any commit to `docs/` folder updates the live site within 1-2 minutes.

**Your site URL:** https://jonspetlobster.github.io/girl-scouts-troop/

## 💡 Tips

- Use emojis for icons (🎨, 📅, 🤝, etc.)
- Add dates in `card-date` for version tracking
- Use `data-searchable` for keywords that aren't visible
- Keep descriptions concise (1-2 sentences)
- Organize by category using `card-badge` tags

## 📝 Editing

**Via Terminal:**
```bash
cd girl-scouts-troop
# Edit any .html file
git add docs/
git commit -m "Add new activity"
git push
```

**Via GitHub Web:**
1. Go to github.com/jonspetlobster/girl-scouts-troop
2. Open docs/ folder
3. Click any .html file
4. Click ✏️ to edit
5. Commit directly

Changes go live in ~2 minutes.

---

Built with ❤️ for Girl Scouts Troop Leaders
