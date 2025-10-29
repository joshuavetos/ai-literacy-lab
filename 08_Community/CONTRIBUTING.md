# AI Literacy Lab — Contributor Guide

Welcome to the Lab.
All contributions must preserve **falsifiability**, **local-first execution**, and **pedagogical clarity**.

## Submission Rules
1. Follow the five-section lesson template (Objective → Illusion → Mechanism → Verification Method → Check).
2. Provide a runnable demo under `/sandbox/` proving your claim.
3. No online APIs or external datasets.
4. Include 3-question Verification Check at lesson end.
5. Run `pytest` locally; all tests must pass before pull request.

## Review Process
Each PR is peer-reviewed for:
- **Reproducibility:** demo runs in container.
- **Clarity:** explanations concise, jargon defined.
- **Integrity:** no unverifiable statements.

## Licensing
All content is MIT-licensed and must cite sources if derived from academic papers.
