# Strapi setup for Datatronic (guide)

Purpose: provide quick steps and example models to run a Strapi demo for managing Pages, Products, Applications, Catalogue, Settings and Contact info. This guide assumes Strapi v4.

## Quick start (local)

1. Install Node.js (16+ recommended) and Yarn/NPM.
2. Create a new Strapi project (local):

```bash
# using npx
npx create-strapi-app datatronic-strapi --quickstart
cd datatronic-strapi
```

3. Start Strapi and open the admin UI (http://localhost:1337/admin). Create an admin user.

## Content types (recommended)

Create the following collection types in the Strapi Admin UI or by placing schema files under `src/api/<type>/content-types/<name>/schema.json`.

- Page
  - title (string)
  - slug (uid)
  - content (richtext)
  - featured (boolean)
  - layout (json)
  - seo_title (string)
  - seo_description (text)
  - publishedAt (datetime; use draft/publish)

- Product
  - title (string)
  - slug (uid)
  - short_description (text)
  - description (richtext)
  - pdfs (media, multiple)
  - images (media, multiple)
  - featured (boolean)
  - categories (relation, optional)
  - seo_*
  - publishedAt

- Application
  - title, slug, body, images, featured, seo_*

- Catalogue (special page/item for catalogue PDFs)
  - title, slug, body, pdf (media single), images, seo_*

- Contact/Settings
  - site_title, address, map_embed (text/html), phone, email, ga_measurement_id, gtm_container_id, other site-wide settings

## Media storage (S3)

For production, configure Strapi to use S3 via the upload provider plugin. Example env variables to set:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- AWS_BUCKET

See Strapi docs: https://docs.strapi.io/developer-docs/latest/plugins/upload.html#using-a-provider

## API access

- Public read (GET) endpoints will be at e.g. `/api/pages` with `?populate=deep` to include media fields.
- For secure editing via API, create an API token in Strapi Settings (Use a token for migration scripts).

## Deploy

- DigitalOcean / Render / VPS are simple choices. Use Docker or direct Node process. Ensure you set up TLS (Let's Encrypt) and environment variables for S3 and DB.
- Use PostgreSQL or MySQL in production (avoid SQLite for multi-instance deployments).

## Migration / Seed

- Use Strapi import plugins or write a small script to POST converted Markdown/JSON into Strapi using the REST API with the admin token or created API tokens.

## Eleventy integration

- The repo includes `scripts/fetch_strapi.py` which will fetch published entries and write Markdown files into `src/` for Eleventy to build. Configure `STRAPI_URL` and `STRAPI_TOKEN` in your environment before running.

---

If you want, I can:
- Create the Strapi schema JSON files in this repo as examples.
- Deploy a demo Strapi instance (DigitalOcean/Render) and seed it with converted content.
- Add CI steps to pull from Strapi before Eleventy builds.
