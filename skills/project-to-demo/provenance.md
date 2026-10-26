# Provenance

Owner: SkillPot maintainers. This is an original public procedure and fixture, not extracted from or dependent on a private video kit. No unpublished local source, local skills, proprietary instructions, or media are included.

## Sources and licenses

- [Agent Skills specification](https://agentskills.io/specification) — public format reference; the local frontmatter uses portable string metadata values only. Checked 2026-10-26.
- [Playwright video recording documentation](https://playwright.dev/docs/videos) — public API procedure reference; Playwright is Apache-2.0. The documentation states recordings flush on browser-context closure and default video size may scale to fit 800×800, so the example explicitly sets 1280×720 and closes the context. Checked 2026-10-26.
- [FFmpeg legal considerations](https://ffmpeg.org/legal.html) — upstream licensing varies by enabled components; FFmpeg is generally LGPL 2.1-or-later, while optional GPL components cause GPL obligations. Checked 2026-10-26.
- Local FFmpeg 8.0.1 build reports `--enable-gpl`, `--enable-version3`, and `--enable-libx264`; this is a GPL-enabled local build. No FFmpeg or browser binaries are redistributed here. Users must independently review their own binary/build and distribution context; this note is not legal advice.

## Adaptation and maintenance

The example's page, row-grouping behavior, tests, capture harness, and documentation were authored for this repository. Playwright and FFmpeg remain separately installed external tools. npm lockfile pins the example's Playwright package; browser installation is an explicit separate setup step. Maintainers should recheck official APIs, versions, and licensing before updating dependencies or making release claims.
