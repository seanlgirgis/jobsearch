# Interview Prep Cleanup Audit (2026-05)

## Canonical Location
- `D:\Workarea\jobsearch\data\interview_prep`

## Policy Summary
1. Real company interview prep belongs in `jobsearch\data\interview_prep`.
2. StudyBook is for reusable study/course/lab material.
3. DataCamp folders are source learning material, not active interview package homes.
4. Worktree copies under `.claude\worktrees` are non-canonical.
5. Do not duplicate the same interview package across StudyBook and jobsearch.

## Classification Legend
- `CANONICAL`: official active home
- `HISTORICAL_JOB_PREP`: prior company-specific prep kept for reference
- `REUSABLE_STUDY_MATERIAL`: reusable learning assets and skill maps
- `WORKTREE_COPY_IGNORE`: transient copy in a worktree; do not treat as source of truth
- `CLEANUP_CANDIDATE`: likely duplicate/legacy location to normalize later
- `UNKNOWN_REVIEW_NEEDED`: not enough confidence; Sean should decide

## Specifically Requested Folder Classifications

1. `D:\Workarea\jobsearch\interview_prep`
- Classification: `CLEANUP_CANDIDATE`
- Why: Parallel interview-prep tree outside canonical `data\interview_prep`; likely legacy path creating ambiguity.
- Recommended action later: `move later` (or `archive later` after contents are mapped into canonical tree).

2. `D:\Workarea\jobsearch\data\interview_prep`
- Classification: `CANONICAL`
- Why: Matches official rule and now contains policy + active Wipro package.
- Recommended action later: `keep`.

3. `D:\Workarea\StudyBook\interview`
- Classification: `REUSABLE_STUDY_MATERIAL`
- Why: In StudyBook root, so should remain reusable practice/reference content.
- Recommended action later: `keep` (review if any company-specific active prep leaked in).

4. `D:\Workarea\StudyBook\interview_prep`
- Classification: `CLEANUP_CANDIDATE`
- Why: Name implies active interview prep but location is StudyBook (reusable-only by policy).
- Recommended action later: `review manually` then `move later` any real company-active material to canonical home.

5. `D:\Workarea\StudyBook\interview_skills`
- Classification: `REUSABLE_STUDY_MATERIAL`
- Why: Skill-based reusable domain prep (Databricks/PySpark/AWS/etc.).
- Recommended action later: `keep`.

6. `D:\Workarea\jobsearch\.claude\worktrees\determined-cori-b1ea34\data\interview_prep`
- Classification: `WORKTREE_COPY_IGNORE`
- Why: Inside `.claude\worktrees`; non-canonical by tooling design.
- Recommended action later: `ignore`.

## Additional Interview/Prep Folders Found (High-Level)

### Under `D:\Workarea\jobsearch`
- `D:\Workarea\jobsearch\data\interview_prep\Wipro_ProgrammersIO_Senior_PySpark_Developer_2026_05`
  - Classification: `CANONICAL`
  - Why: Active company package in official home.
  - Action later: `keep`.
- `D:\Workarea\jobsearch\data\interview_prep\Carla_Apple`
  - Classification: `HISTORICAL_JOB_PREP`
  - Why: Company-specific prep folder in canonical tree.
  - Action later: `keep` or `archive later` when inactive.
- `D:\Workarea\jobsearch\data\interview_prep\ShaekeforceConsulting`
  - Classification: `HISTORICAL_JOB_PREP`
  - Why: Prior company-specific prep.
  - Action later: `keep` or `archive later`.
- `D:\Workarea\jobsearch\data\interview_prep\SharkforceConsulting`
  - Classification: `CLEANUP_CANDIDATE`
  - Why: Potential spelling-variant duplicate of `ShaekeforceConsulting`.
  - Action later: `review manually` then consolidate.
- `D:\Workarea\jobsearch\data\interview_prep\audio_prep`
  - Classification: `REUSABLE_STUDY_MATERIAL`
  - Why: Topic-based reusable content, not one company package.
  - Action later: `keep`.
- `D:\Workarea\jobsearch\data\interview_prep\active_interviews`
  - Classification: `UNKNOWN_REVIEW_NEEDED`
  - Why: Could contain active company packages or mixed formats; needs naming/policy alignment check.
  - Action later: `review manually`.

### Under `D:\Workarea\StudyBook`
- `D:\Workarea\StudyBook\interview`
  - Classification: `REUSABLE_STUDY_MATERIAL`
  - Action later: `keep`.
- `D:\Workarea\StudyBook\interview_prep`
  - Classification: `CLEANUP_CANDIDATE`
  - Action later: `review manually`.
- `D:\Workarea\StudyBook\interview_skills`
  - Classification: `REUSABLE_STUDY_MATERIAL`
  - Action later: `keep`.
- `D:\Workarea\StudyBook\playground\prep`
  - Classification: `REUSABLE_STUDY_MATERIAL`
  - Why: Sandbox/playground path, not company package naming.
  - Action later: `keep`.
- `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\course\09_aws_observability_interview_bridge\interview`
  - Classification: `REUSABLE_STUDY_MATERIAL`
  - Action later: `keep`.
- `D:\Workarea\StudyBook\study_maps\Observability\interview`
  - Classification: `REUSABLE_STUDY_MATERIAL`
  - Action later: `keep`.

## Recommended Next-Step Cleanup Plan (No Changes Applied Yet)
1. Inventory `D:\Workarea\jobsearch\interview_prep` and `D:\Workarea\StudyBook\interview_prep` for company-specific active folders.
2. For each confirmed active company folder, map to canonical naming: `<Company>_<VendorOrRecruiterIfUseful>_<Role>_<YYYY_MM>`.
3. Merge or archive spelling duplicates (example: `ShaekeforceConsulting` vs `SharkforceConsulting`) after manual content diff.
4. Keep StudyBook paths as reusable references only; add pointers from canonical company packages if useful.
5. Continue ignoring `.claude\worktrees` copies.
