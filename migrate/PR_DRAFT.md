# Migration PR - Draft

**Summary**
- This PR imports scraped content from the live site into Eleventy content folders (`src/pages`, `src/products`, `src/applications`).
- Generated artifacts included in this PR: `migrate/sitemap-urls-full.csv`, `migrate/assets.txt`, `migrate/converted_manifest.csv`, and converted Markdown files under `src/`.

**Counts**
- URLs (from sitemap): 50
- Converted Markdown: 50 (pages) + 3 (products) + 2 (applications)
- Media references discovered: 325 lines listed in `migrate/assets.txt` (media not downloaded in this PR)

---

## What this PR changes
- Adds converted Markdown files under `src/` (pages/products/applications) as a first import pass.
- Adds migration artifacts under `migrate/` for reviewer inspection.
- Adds suggested redirects list: `migrate/redirects-suggested.txt` (review & finalize)
- Adds utility scripts `scripts/suggest_slug_mappings.py` and `scripts/normalize_frontmatter_report.py` to help review and further normalization.

---

## Review checklist (please complete before merging)
- [ ] Run `python3 scripts/check_migration.py` and fix any remaining ERRORS.
- [ ] Inspect `src/` markdown for title correctness and empty content blocks (some pages are block-based; manual cleanup may be required).
- [ ] Confirm handling for PDFs and large media: do not commit >5MB files — use S3/Netlify Large Media/Git LFS instead.
- [ ] Confirm slug strategy: many auto-generated slugs contain URL-encoded characters (`en-%e...`). Consider running `python3 scripts/suggest_slug_mappings.py` to generate friendly slug proposals and approve changes.
- [ ] Verify 3 sample pages (Home, Catalogue, Product example) visually in a local build before merging.

---

## How to preview locally
1. Install dependencies and run Eleventy (see `README-CMS-SETUP.md`).
2. Build and preview to confirm pages render:

   ```bash
   npm install
   npm run build
   npm run start  # if configured
   ```

3. Check sample pages in browser and confirm PDF links / contact map links / forms work as expected.

---

## Notes & next steps (post-merge)
- Normalize slugs and update links (I can prepare a follow-up PR that renames files & adds 301 redirects).  
- Plan media handling (upload images and PDFs to S3 or Netlify Large Media, update `assets.txt` with storage locations).  
- Add automated tests / CI checks for front-matter completeness and presence of canonical metadata.

---

**Action**: If you approve, push this branch and I will open the PR (or I can open it for you once branch is pushed).