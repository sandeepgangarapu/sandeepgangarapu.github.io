# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal website for Sandeep Gangarapu built with Hugo and the PaperMod theme. Deployed to GitHub Pages at sandeepgangarapu.github.io via GitHub Actions on push to `main`.

## Common Commands

- **Local dev server:** `hugo server -D` (includes drafts)
- **Build for production:** `hugo --gc --minify`
- **Create new content:** `hugo new blog/stories/my-post.md` (uses `archetypes/default.md`, creates as draft)

## Architecture

- **Config:** `hugo.yaml` — site settings, menu structure, PaperMod theme params
- **Theme:** PaperMod, added as a git submodule at `themes/PaperMod`. Do not edit theme files directly; override via project-level `layouts/` if needed.
- **Content sections** (defined in `content/`):
  - `blog/stories/` — personal essays, career, finance
  - `blog/technical/` — data science, causal inference, statistics
  - `blog/rolling-blog/` — living/evolving posts (code snippets, lists, collections)
  - `recipes/` — cooking recipes
  - Top-level pages: `about.md`, `projects.md`, `research.md`, `resources.md`, `activity-stream.md`, `search.md`
- **Static assets:** `static/` (images, etc.)
- **Scripts:** `scripts/migrate_notion.py` — one-time migration from Notion export

## Deployment

GitHub Actions workflow (`.github/workflows/deploy.yml`) triggers on push to `main`. Uses Hugo Extended v0.160.1. The deploy branch is `main`.

## Content Conventions

- Front matter uses YAML (delimited by `---`)
- The archetype default uses TOML (`+++`), but existing content uses YAML — prefer YAML for consistency
- Markdown supports unsafe HTML rendering (`markup.goldmark.renderer.unsafe: true`)
- Taxonomies: `categories`, `tags`, `series`
