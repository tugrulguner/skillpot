# SkillPot product website

Product-owned Astro/Starlight source for `https://skillpot.modepot.io`. This directory
is an implementation, not proof the domain is live. Production requires a separately
approved merge/deployment and public content readback. Do not add a live-site About
link or switch umbrella discovery to the hostname before that verification succeeds.

## Local checks

Use Node **22.23.4 or newer supported by the lockfile's dependency engines**. Node
22.23.3 is below one dependency's declared floor; do not ignore that warning. From
this directory:

```sh
npm ci
npm run build
node node_modules/@playwright/test/cli.js install chromium
npm run test:browser
```

`npm run build` regenerates the guides, checks Astro/types/content, runs source tests,
builds the static site/search/sitemap, emits Markdown downloads and tests output.
The browser suite starts its own production preview on `127.0.0.1:4587`, with strict
port binding and no server reuse. It tests four viewport widths and Light/Dark/Auto,
first use, keyboard access, creator links, documentation, downloads and 404 behavior.
Do not run a second preview on that port. `npm run preview -- --port PORT` supports
an independently chosen free port for manual review.

## Canonical content and identity

- `src/content/docs/index.mdx` owns the overview, not a product runtime simulation.
- `scripts/sync-docs.mjs` generates six guides from repository README sections,
  `docs/` and `catalog/README.md`; edit those originals. Generated Markdown sources
  are ignored and created before check/build, so there is no second maintained manual.
  Markdown is parsed structurally: examples remain literal, reference definitions
  and encoded paths are rewritten, and headings inside code do not define sections.
- `scripts/emit-markdown-downloads.mjs` produces downloads from the same generated
  guides rendered as HTML. Markdown retains absolute canonical URLs for use outside
  the site; rendered guide links stay on their serving origin, including local preview.
  Download links save actual `.md` files. Source links point to canonical repository
  files and known internal documentation destinations.
- Public agent discovery is `/llms.txt`, linked in HTML head and homepage content.
  Contributor/coding-agent rules live separately at repository-root `AGENTS.md`.
- Canonical artwork under `public/assets/` must remain byte-identical to root `assets/`.
  Preserve the planned label and historical context of the original workflow image.
- The static canonical origin is `https://skillpot.modepot.io`; no fake playground,
  live model run or instruction-safety certification is provided.

Astro 7 currently emits non-fatal MDX head-injection bundler notices and a custom-404
route-priority notice. Do not confuse those with Astro check's type/content results;
verify actual emitted metadata, scripts, routes and browser behavior. Do not suppress
real failures or claim a warning-free production build when those notices remain.

## Deployment

`wrangler.toml` declares an independent static-assets Worker named `skillpot-site`
and custom domain `skillpot.modepot.io`, with the emitted 404 page.
`.github/workflows/ci.yml` calls the reusable `website.yml` workflow for PRs and main
pushes; its `verify` gate requires checks and browser verification to succeed. The separate
main-push/manual production workflow reruns source, site and browser gates before
uploading the exact build.
Manual deployment also requires the selected ref to be `main`; feature branches
cannot reach the production job. Website CI retains screenshots/failure traces for
seven days so review does not depend on local files.

Before production deployment, the maintainer must configure:

- Repository/production variable `CLOUDFLARE_ACCOUNT_ID` for the existing family account.
- Repository/production secret `CLOUDFLARE_API_TOKEN`, scoped to deploy this Worker and
  bind its custom hostname in the appropriate zone. Never paste its value into source,
  logs, issues, public instructions or chat.

The workflow fails with a clear configuration error when these values are absent;
it does not request credentials, reuse another profile, or silently claim deployment.
Merging a new PR requires explicit approval. No production deployment is executed by
local `build` or browser tests.

After upload, `node scripts/verify-site.mjs` checks seven public pages and twelve
assets/downloads byte-for-byte against `dist/`. It retries in deployment CI for DNS/TLS
propagation. For an owned local preview, an explicit origin may be supplied. The public
readback is required: a successful Wrangler upload alone does not prove DNS, TLS,
routing, asset loading or the approved artifact is served. Keep source/preview/live
states distinct and do not modify unrelated product deployments.
