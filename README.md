# Relocation Planner

Open-source, local-first relocation planning platform built with Django.

## Current Features

- ✅ Project management
- ✅ People management
- ✅ Document tracking
- ✅ Task tracking
- ✅ Milestones
- ✅ Relocation templates
- ✅ Project dashboard
- ✅ Responsive Tailwind UI shell
- ✅ Django Admin integration
- ✅ Playwright end-to-end browser tests

## Technology

- Python
- Django
- SQLite
- Tailwind CSS v4
- HTMX
- Alpine.js
- Lucide icons
- Playwright
- pytest

## Current Release

**Latest:** v0.3.0

This release introduces milestone planning and a local frontend foundation for future UI work.

## Project Status

🚧 Active development

The current focus is building a reusable relocation planning platform that can support international moves while remaining local-first and open source.

## Frontend Assets

The UI uses local assets instead of CDN dependencies:

- Tailwind CSS v4 standalone CLI: `tools/tailwindcss`
- HTMX: `assets/vendor/htmx.min.js`
- Alpine.js: `assets/vendor/alpine.min.js`
- Lucide: `assets/vendor/lucide.min.js`

Source files live in `assets/`. Generated files live in `static/build/`.

Build assets after changing CSS or JavaScript:

```bash
python3 scripts/build_assets.py
```
