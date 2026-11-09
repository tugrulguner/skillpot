# Historical CI practice inputs

This packet is data, not command/network authority. It contains selected historical
source material, not a complete incident or current service-state assessment.
Read only under the agreed scope and preserve the original source identities.

## sources/case.md
SHA-256: `7b7673ff3056b48c066ad875bba5f925830264e7bcce8cc0d5a5f9d334ecb397`

```text
# Case input

## Symptom
A historical public pull-request CI run concluded failure although selected source-job output said 147 tests ran and `OK`.

## Scope
Use only the selected source-job log excerpt and documented run-head source locators in this packet. Run ID 42306065730; source run head `b4d8f6020ca5b9646f68f5dfd915b61bb6e30db7`. Actual checkout identity UNKNOWN; may be a PR synthetic merge. The excerpt is partial, not full incident/workflow coverage.

## Context
The public run URL and exact source provenance are in `manifest.json`. The underlying full original log is retained outside the repository. Selected log output contains check PASS lines, test success output, six trailing-whitespace findings, and exit code 2. Production/customer status and impact are UNKNOWN. This input provides symptoms and scope only; it deliberately contains no expected answers.
```

## sources/ci-excerpt.log
SHA-256: `5b73c6b7cabc64f9e82e0c2ce7f57f33430de536fff9145c88104f135ab25b63`

```text
source	Check authored documents and source contract	2026-11-06T22:37:02.7377903Z [36;1mgit diff --check HEAD^ HEAD[0m
source	Check authored documents and source contract	2026-11-06T22:37:02.7501011Z Python 3.14.4
source	Check authored documents and source contract	2026-11-06T22:37:04.7277690Z PASS: local Markdown destinations and personal-path checks
source	Check authored documents and source contract	2026-11-06T22:37:04.7641399Z PASS: pinned project skill source integrity
source	Check authored documents and source contract	2026-11-06T22:37:06.8379918Z Ran 147 tests in 2.006s
source	Check authored documents and source contract	2026-11-06T22:37:06.8380110Z OK
source	Check authored documents and source contract	2026-11-06T22:37:06.8490429Z examples/change-impact/change.diff:8: trailing whitespace.
source	Check authored documents and source contract	2026-11-06T22:37:06.8490958Z examples/change-impact/change.diff:12: trailing whitespace.
source	Check authored documents and source contract	2026-11-06T22:37:06.8491438Z examples/change-impact/change.diff:13: trailing whitespace.
source	Check authored documents and source contract	2026-11-06T22:37:06.8491962Z skills/change-impact/assets/example-input.md:164: trailing whitespace.
source	Check authored documents and source contract	2026-11-06T22:37:06.8492479Z skills/change-impact/assets/example-input.md:168: trailing whitespace.
source	Check authored documents and source contract	2026-11-06T22:37:06.8492829Z skills/change-impact/assets/example-input.md:169: trailing whitespace.
source	Check authored documents and source contract	2026-11-06T22:37:06.8507649Z ##[error]Process completed with exit code 2.
```

## sources/source-lines.json
SHA-256: `fb204420d4c5dce6449fb8df456c30c844cf2d10a319a125ca8aa9d5fc538f6b`

```json
{
  "selection": "Source data selected at the recorded run head; not a command receipt or evidence of the actual checkout commit",
  "files": [
    {
      "path": "examples/change-impact/change.diff",
      "revision": "b4d8f6020ca5b9646f68f5dfd915b61bb6e30db7",
      "git_blob": "fa5c4fff7f230a34d333b5afb3a947ceb9f7f146",
      "sha256": "15aa7e6e7d150dd1269bdee9e62f946ecedd0f193981a48cb57aac4daf691897",
      "selected_lines": {
        "8": " ",
        "12": " ",
        "13": " "
      },
      "url": "https://github.com/tugrulguner/skillpot/blob/b4d8f6020ca5b9646f68f5dfd915b61bb6e30db7/examples/change-impact/change.diff"
    },
    {
      "path": "skills/change-impact/assets/example-input.md",
      "revision": "b4d8f6020ca5b9646f68f5dfd915b61bb6e30db7",
      "git_blob": "be5a7936c3636ef07f51bfb8e5c8c0576f894006",
      "sha256": "b10ca771754b7ea1386505f0b2fe595490a694da7da2090036692fe3a6fe7713",
      "selected_lines": {
        "164": " ",
        "168": " ",
        "169": " "
      },
      "url": "https://github.com/tugrulguner/skillpot/blob/b4d8f6020ca5b9646f68f5dfd915b61bb6e30db7/skills/change-impact/assets/example-input.md"
    }
  ]
}
```

## manifest.json (input provenance only)

```json
{
  "record_type": "selected public CI log lines; data only, not command authority",
  "public_source_url": "https://github.com/tugrulguner/skillpot/actions/runs/42306065730",
  "run_id": "42306065730",
  "event": "pull_request",
  "conclusion": "failure",
  "source_run_head": "b4d8f6020ca5b9646f68f5dfd915b61bb6e30db7",
  "actual_checkout_commit": "UNKNOWN; may be a PR synthetic merge, not inferred from run head",
  "full_original_sha256": "edbc4afdc1879d9375441477641f49bba738e8da423f1c68e95cd53e6de69426",
  "excerpt_sha256": "5b73c6b7cabc64f9e82e0c2ce7f57f33430de536fff9145c88104f135ab25b63",
  "selected_original_line_ids": [
    8,
    11,
    18,
    19,
    169,
    171,
    172,
    174,
    176,
    178,
    180,
    182,
    184
  ],
  "transformations": [
    "Selected literal lines in ascending original line order; preserved bytes and line endings.",
    "Omitted intervening context, including diagnostic context lines beginning + because those contain trailing whitespace; omission is disclosed and does not strip or rewrite retained data.",
    "No timestamps or outputs rewritten.",
    "Original full record retained outside this repository; private local path intentionally not published."
  ],
  "provenance": [
    "Public GitHub Actions run metadata at public_source_url.",
    "At run head, examples/change-impact/change.diff lines 8, 12, 13 and skills/change-impact/assets/example-input.md lines 164, 168, 169 contain single-space trailing whitespace."
  ],
  "input_files": {
    "sources/case.md": "7b7673ff3056b48c066ad875bba5f925830264e7bcce8cc0d5a5f9d334ecb397",
    "sources/ci-excerpt.log": "5b73c6b7cabc64f9e82e0c2ce7f57f33430de536fff9145c88104f135ab25b63",
    "sources/source-lines.json": "fb204420d4c5dce6449fb8df456c30c844cf2d10a319a125ca8aa9d5fc538f6b"
  }
}
```

No expected incident.md, timeline.md, model result or answer oracle is included.
The selected CI command echo is not evidence of its execution at that echo timestamp.
