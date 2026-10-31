# Compatibility and verification status

## Package compatibility

- **Status:** reviewed source-only package, unreleased, version `0.1.0`; added after collection v0.3.0.
- **Required runtime/dependencies:** none specified. The procedure is host-neutral and can be followed with ordinary file-reading/writing and, only when explicitly allowed, source-retrieval and calculation capabilities. No host-specific tool names, integrations, installer, or runtime are required.
- **Offline behavior:** supplied evidence can be handled offline; network access is never assumed. A permitted-source request may require a host retrieval capability, but its availability and correctness are not asserted here.
- **Verified source:** package resources, frontmatter, notices and relative Markdown links are source-contract tested.
- **Observed tasks:** [three explicitly loaded offline task attempts](../../evaluations/decision-brief/offline-tasks-001/README.md) through the existing Hermes delegation system produced a conditional recommendation, a missing-evidence deferral, and an output-collision refusal. The configured model was reported as `gpt-6-luna`; a runtime build version was not captured. The parent inspected the actual artifacts and input hashes. These are narrow observations, not native client installation or automatic discovery tests.
- **Not established:** general support across models/harnesses, automatic discovery, runtime safety, reliable quality or factual accuracy for arbitrary decisions, or improved performance. There was one attempt per condition, no control or repeated/held-out comparison, and no separate injection-only or symlink-collision execution.

The maintainer example is [`../../examples/decision-brief/README.md`](../../examples/decision-brief/README.md) in the repository source tree and is not required in an installed package. Any example facts, sources, calculations, and output must be checked separately; an authored fixture is not runtime evidence.

See [`provenance.md`](provenance.md) for source pin, adaptation, hashes, exclusions, and complete notice. Source-contract checks validate documented files/metadata/links only; they do not prove task success or agent behavior.
