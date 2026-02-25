Eleventy + Netlify CMS Setup (MVP)

Overview
- This repository now includes a minimal Eleventy scaffold in `src/` and a Netlify CMS admin in `admin/`.

Local setup
1. Install Node.js (>=16 recommended) and npm.
2. From project root run:
   npm install
   npm run start
3. Eleventy will build the site to `_site` and serve on http://localhost:8080 by default.

Netlify CMS notes
- `admin/config.yml` is configured to use `backend: git`. Update `repo` to your GitHub repo or switch to Git Gateway for Netlify Identity.
- Media uploads are placed in `src/uploads` and served from `/uploads`.
- Collections configured: settings, products, applications, pages.

Deployment
- Deploy on Netlify and enable Identity + Git Gateway if you want editors to log in via Netlify Identity.
- Alternatively, use `backend: git` and a GitHub token via the Netlify UI.

Next steps I can help with
- Connect Netlify site, enable Identity/Git Gateway and test CMS auth flow.
- Implement homepage templates to list featured Products/Applications and wire CMS fields into templates.
- Add sitemap generation and GA script integration in templates.
