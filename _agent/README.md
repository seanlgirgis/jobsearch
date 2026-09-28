# Agent control plane

This is the shared, vendor-neutral operating contract for every LLM coding
agent used in this repository. It is intentionally plain Markdown: no provider
prompts, model assumptions, or tool-specific syntax.

## Startup contract

Read in this order:

1. `AGENTS.md`
2. `CONSTITUTION.md` — stable principles; change rarely.
3. `RULES.md` — operational boundaries and safety procedures.
4. `MEMORY.md` — durable project decisions and facts.
5. `STATE.md` — current implementation status.
6. `HANDOFF.md` — current next action and open risks.
7. Only the task-specific route and files needed for the request.

## Route map

- Pipeline, resumes, applications, gigs: `docs/PIPELINE_OPERATOR.md`.
- Pipeline architecture or failure diagnosis: `docs/PIPELINE_ARCHITECTURE.md`.
- Script allowlist and legacy filter: `scripts/README.md` and
  `docs/SCRIPT_SURFACE_AUDIT.md`.
- Search bots: `search_bots/agent_work/README.md`, then its `HANDOFF.md`,
  `NEXT.md`, and `documentation/LIVE.md`.
- Candidate facts: `data/master/` and `docs/RUNTIME_PROFILE.md`.
- Workspace organization: `docs/WORKSPACE_CONTROL_AUDIT.md`.

## Operating modes

- **Execute:** perform the requested step, then verify it.
- **Discuss:** answer from evidence without changing files or making paid calls.
- **Diagnose:** inspect read-only evidence and explain the cause; fix only when
  asked.
- **Maintain:** edit only the explicitly requested control, code, or document
  surface.

## File ownership

- `CONSTITUTION.md`: principles, not task status.
- `RULES.md`: repeatable procedures and boundaries.
- `MEMORY.md`: durable decisions only; no transient notes.
- `STATE.md`: current status only.
- `HANDOFF.md`: the next agent's concise starting packet.

After a meaningful change, update `STATE.md` and `HANDOFF.md`. Update
`MEMORY.md` only when a decision is durable. Do not casually edit the
constitution.

Historical root instruction filenames are archived under
`archive/2026-09-28/root_cleanup/compatibility/`; they do not create competing
policy.
