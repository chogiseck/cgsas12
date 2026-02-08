# CLAUDE.md

## Project Overview

This repository (`cgsas12`) contains static HTML/CSS presentation materials for Korean school staff training. The primary deliverable is a self-contained HTML infographic presentation designed for vice principals conducting new school year preparation sessions.

## Repository Structure

```
cgsas12/
├── README.md                       # Project title
├── CLAUDE.md                       # This file
└── staff-training-infographic.html # Main presentation (on feature branch)
```

## Tech Stack

- **HTML5/CSS3** — No build tools, no JavaScript frameworks, no package manager
- **Google Fonts** — Noto Sans KR (loaded via CDN for Korean language support)
- **No dependencies** — Fully self-contained static files

## Branches

- `main` — Base branch with README
- `claude/staff-training-infographics-W1TAX` — Contains the staff training infographic HTML

## Development Workflow

### Viewing the Presentation

Open `staff-training-infographic.html` directly in a browser. No build step required.

### No Build System

There is no `package.json`, no bundler, no compiler. Files are served as-is.

### No Tests or Linting

No automated testing or linting tools are configured.

## CSS Conventions

The HTML presentation uses these patterns:

- **CSS custom properties** defined in `:root` for theming (`--primary`, `--accent`, etc.)
- **Kebab-case class names** (e.g., `slide-cover`, `timeline-item`, `stat-card`)
- **Component-based CSS** — Reusable classes for cards, charts, grids, process flows
- **Color palette**: Primary blues (`#1a365d`, `#2b6cb0`), orange accent (`#ed8936`), teal (`#38b2ac`), purple (`#9f7aea`), red (`#f56565`), green (`#48bb78`)
- **Print styles** included for PDF export via browser print

## Slide Structure

Each slide is a `<section class="slide" id="slideN">` element. The presentation contains 11 slides with consistent layout: numbered section headers, card-based content, and footers with slide counters.

## Key Guidelines for AI Assistants

1. **Content is in Korean** — All presentation text is in Korean. Maintain language consistency.
2. **Self-contained files** — Keep HTML files standalone with embedded CSS. Do not introduce build tooling unless explicitly requested.
3. **Preserve the design system** — Use existing CSS variables and component classes rather than adding inline styles.
4. **No over-engineering** — This is a static presentation project. Keep it simple.
5. **Branch awareness** — The main content lives on feature branches, not `main`.
