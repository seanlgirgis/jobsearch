# Website Refactor and Training Roadmap

## Scope
This document captures only the website-focused work:
- Learning Hub refactor decisions
- Website layout and navigation changes
- Technology roadmap and training placeholders
- Operational rules for adding new learning pages

## Website Architecture Decisions
- Learning Hub is a SPA entry (`#learning`) that loads `components/learning.html` via router mapping.
- Individual learning pages under `learning/*.html` are standalone full HTML pages (direct URL), not SPA fragments.
- Navigation from hub cards to detail pages uses regular `href` links.

## Media Hosting Decisions
- OneDrive links were unreliable for native `<audio>`/`<video>` playback due to cross-origin behavior.
- Cloudflare R2 became the canonical media host for website audio/video.
- Media optimization commands used:
  - Audio: `ffmpeg -i input.m4a -c:a aac -b:a 64k output_small.m4a`
  - Video: `ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output_small.mp4`

## Learning Hub Structure
The hub now follows a 3-layer model:

### Layer 1: Technology References
Purpose: architecture and platform/topic deep references.

Live examples already represented:
- AWS S3
- AWS Athena
- AWS Glue
- AWS Redshift
- AWS Lambda
- AWS EC2
- AWS ECS
- Apache Kafka

### Layer 2: Engineering Craft and Patterns
Purpose: practical implementation patterns and trade-offs.

Planned placeholders:
- File Formats and Serialization (Parquet, Pickle, Arrow)
- Pandas Patterns for Data Engineering
- PySpark Hands-On Patterns
- Pipeline Design Patterns (idempotency, incremental, backfill)
- SQL Patterns for Data Engineers
- Data Quality Patterns
- Data Modeling Patterns (SCD, star schema)
- Python Performance Patterns
- API and Integration Patterns
- Debugging Data Pipelines
- Capacity Planning and Forecasting Patterns
- Testing Data Pipelines

### Layer 3: System Design
Purpose: open-ended design scenarios for data systems.

Planned placeholders:
- High-Volume Event Ingestion Pipeline
- Batch ETL Pipeline on AWS
- Slowly Changing Dimension System
- Data Quality Monitoring Platform
- Real-Time + Batch Hybrid Pipeline
- Metrics Aggregation System
- Multi-Tenant Data Lake
- Late-Arriving Data Handling Pipeline
- Cost-Optimized Analytics Platform on AWS
- Third-Party API Ingestion System
- Forecasting Pipeline for Infrastructure Capacity
- Text-to-SQL Agent for Data Access

## Website Layout and UX Changes
- Shifted long guides to single, scrollable pages for smoother reading.
- Added section-level back-to-top links (`#top`) in learning pages.
- Added a compact jump-navigation map on the Learning Hub.
- Added anchor IDs across section headings so users can jump directly to areas.
- Improved mobile behavior with responsive grid wrapping in the jump nav.

## Integration Rules for New Pages
Every new learning page must update all three:
1. `learning/[new-page].html`
2. `components/learning.html` (add live card)
3. `components/site_map.html` (add link under Learning Hub)

## File Touchpoints in the Website Repo
- `D:\StudyBook\temp\seanlgirgis.github.io\assets\js\router.js`
- `D:\StudyBook\temp\seanlgirgis.github.io\components\learning.html`
- `D:\StudyBook\temp\seanlgirgis.github.io\components\site_map.html`
- `D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-s3.html`
- `D:\StudyBook\temp\seanlgirgis.github.io\learning\aws-athena.html`
- `D:\StudyBook\temp\seanlgirgis.github.io\.gitignore`

## Notes
- Language/content rules for public learning pages avoid company-specific references.
- Prompt-driven page generation should keep layout/style consistent with the existing learning template.
