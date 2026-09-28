# Pipeline architecture

Current operational authority is [PIPELINE_OPERATOR.md](PIPELINE_OPERATOR.md),
under the AGENTS.md startup rules. [CUTOVER_REPORT.md](CUTOVER_REPORT.md) records
the Prompt 05 verification and the superseded Prompt 04 defects.

## Stages

job-runner.ps1 calls scripts/canonical_runner.py with an explicit repository root.
Local job identity uses SHA-256 of NFKC/casefolded text with collapsed whitespace.
Existing runner_<hash8> folders are retained, with a full-hash collision check.
All job writes occur under the exclusive data/pipeline_cache/runner.lock.

Tier 0 (local_gate.py) compares metadata hashes and raw descriptions in data/jobs
and data/applied_jobs; index_exclude entries are skipped. Similarity checks for
new runner jobs supplement exact matching. Otherwise the existing FAISS
inner-product index uses local-only MiniLM embeddings with cutoff 0.82, no age
expiry, and a 55-second worker timeout. Duplicates or unavailable checks require
a reasoned duplicate override. Eligibility blocks always stop paid work.

Tier 1 verifies the runtime profile/report against regenerated source projections,
then calls the `economy` profile by default (or the requested analysis profile)
once for structured analysis. Contracts and public-output
checks validate both new responses and cache hits. The packet and readable report
contain score, rationale, strengths, gaps, recommendation, keywords and plan.
Triage always stops before generation.

Explicit generate records user acceptance separately from the local gate and
model recommendation. REVIEW/SKIP also require a reasoned suitability override.
Tier 2 uses the `quality` profile by default (or the requested generation profile)
once for a resume/optional-cover selection package. Source
identity, dates, titles, education and accomplishment bullets are filled locally.
The existing renderers' pure functions produce DOCX/Markdown; content/structural
checks must pass. No paid company-research step is included.

Apply-only requires --assume-applied, method and a valid calendar date. It verifies
the completed artifact manifest and changes only that job's application block
and mirror. It makes no model/render calls, preserves history and deduplicates
identical events. Application status remains sticky on subsequent gate failures.

## States and records

| State | Meaning |
| --- | --- |
| BLOCKED | Local duplicate/check/eligibility prevents continuation |
| TIER0_CLEAR / TIER0_OVERRIDDEN | Local step finished; no paid call |
| ANALYZING / GENERATING | Work in progress |
| TRIAGED | Analysis available; no automatic acceptance |
| AWAITING_DECISION | Generation request needs suitability override |
| READY_TO_APPLY | Completed local package; no submission inferred |
| ASSUMED_APPLIED | Explicitly recorded application |
| FAILED | Safe failure; previous evidence and packages retained |

metadata.yaml persists status and last_runner_state; an applied job retains
ASSUMED_APPLIED even when a later runner command blocks. tier0_decision,
llm_decision and user_decision are separate in metadata and packet. Decision
history records authorization source, override reason and analysis cache key.
runner_result.json is the latest handoff, not submission evidence.

## Cache, provenance and artifacts

Prompt namespace is canonical-v2-cutover; previous cache claims are retained and
excluded from the new route. The cache identity includes the full job/profile
hashes, profile name, all model settings, prompt version, schema/request hashes,
and Tier 2 analysis hash/cover selection. A COMPLETE record has a result hash and
requested provider/model/profile provenance. ATTEMPTED and FAILED_OR_UNCERTAIN
claims never retry automatically. SDK retries are disabled; request timeout is
45 seconds. Selected primaries must support schemas and have empty fallback lists.
The selected generation profile's allow_artifacts policy is enforced.

A separate generated/packages/<package-id> directory is derived from Tier 2 cache
identity and renderer source hashes. Its manifest records inputs, source hash,
both stage provenance records, quality result and file hashes. Completed packages
are verified and reused without rendering or overwriting edits. New selections
create new package directories; incomplete ones stop for diagnosis. metadata
stores the active package's manifest hash and exact output paths.

## Remaining limits

- Local checks cannot prove every free-form prose claim or page layout. There is
  no automated visual gate. Review every document before sending.
- model_used records the exact requested single target, not a provider-resolved
  alias. Token usage, provider cost and Cline's own usage are not collected.
- --dry-run writes local gate records. Apply-only requires the unchanged intake
  to identify its existing job and an intact completed artifact package.
- Eligibility is a narrow deterministic gate, not a complete work-authorization,
  location, compensation, or employment-conflict determination.
- Metadata is atomically replaced per file, not in a multi-file transaction.
  Application JSON is a recoverable mirror. Existing unrelated metadata/history
  is retained. A stale lock needs operator diagnosis.
- No automatic FAISS rebuild, migration to data/applied_jobs, bulk cleanup,
  accept/reject-only CLI, provider retry override, or historical package migration.
  Existing legacy generated files remain in their original locations.
- Pre-cutover saved artifact layouts require review before using apply-only;
  the runner does not invent a manifest or reclassify old submissions.
