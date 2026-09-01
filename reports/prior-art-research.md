# Prior-Art Research

## Re-package ai-signal v1.0.0 (2026-09-01)

- Researched at: 2026-09-01
- Source material: existing `ai-signal` skill runtime (SKILL.md, scripts/, references/, prompts/, config/, tests/, feeds/) at the `rework/meta-skill-package` baseline
- Package conventions studied: [`fastagent-meta-skill`](https://github.com/tokenaissance/fastagent-meta-skill) (`~/.agents/skills/fastagent-meta-skill` v2.9.0) — validate contract, trigger eval, Skill IR, release gates, README playbook
- License: MIT (both)

### Context

`ai-signal` already existed as a mature, public, Agent-side content-curator skill with a full Python runtime and daily CI feed updates. This is a re-package (重新封装), not a greenfield creation: the job was to bring the package into conformance with the fastagent-meta-skill package contract without touching the runtime behavior.

### Keep

- Agent-first architecture: central service only provides JSON feeds; the user's Agent reads them and produces the personalized digest.
- JSON-first default path; central Chinese summaries remain legacy/debug-only.
- Runtime layout (scripts/, references/, prompts/, config/sources.json, feeds/, tests/).
- Install path conventions (git clone + mirror prefixes for mainland China; `~/.ai-signal/` user config).
- No content API keys required from users.

### Adapt

- Added `agents/interface.yaml` (display name, default prompt, permissions, trust, degradation, gates) per the fastagent-meta-skill Production+ interface contract.
- Added `manifest.json` with semver `1.0.0`, `maturity_tier: library`, and declared release gates.
- Added `evals/trigger_cases.json` — trigger-boundary smoke eval tuned to the ai-signal description (digest / source / install / expand / deliver requests).
- Rewrote README.md to the meta-skill template: badge row, one-line install (`npx skills add`), natural-language examples, capability comparison, directory tree, workflow, prerequisites, troubleshooting, design philosophy, credits, security/evidence boundary. Language decision: Chinese-primary (`readme_languages: ["zh-CN"]`) because the audience is Chinese AI users (mirror prefixes, mainland-China hardening).
- Marked `render_digest.py` and `podcast_transcripts.py` as internal modules so the package-validate contract passes.
- Added MIT LICENSE crediting both the fork maintainer (Tokenaissance) and the original author (Benboerba620 / 公众号「奔波儿r」).

### Reject

- Bundling the skill into `fastagent/skills/` (user explicitly declined).
- Rewriting the README to English-primary: the product is Chinese-audience-only; Chinese-primary is the playbook's accepted exception.
- ~~Changing user-facing install URLs to the fork~~ — **reversed by user decision in v1.0.1**: install source is now the Tokenaissance repo (`tokenaissance/ai-signal`), not upstream; the upstream `Benboerba620/ai-signal` remains attribution-only (credits, `upstream_inspiration`, LICENSE).
- Introducing a separate discovery or creator skill.

### Invent

- None for the runtime; the package scaffold (interface.yaml, manifest, trigger cases, reports) is adapted from the meta-skill contract rather than invented.

## Missing evidence

- No independent user-survey or adoption metric was collected; install/download numbers are not treated as quality evidence.
- No provider-backed or human blind-review output eval was run for digest quality (digest generation is user-side agent behavior, out of this package's evidence boundary).
