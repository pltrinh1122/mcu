# Gap‑Spotting Question Bank – Round 2

> *Objective*: Probe the **response set** to the first gap‑spotting round, surfacing any remaining ambiguities, unstated assumptions, or feasibility risks.

---
## 1  Problem Statements & Proposed Solutions

### 1.1 Duplication & Hierarchical Units
1. How will the **AI detect overlap** across incoming sources before a new integration unit is created?
2. If a *core* unit evolves, what mechanism updates or invalidates all referencing *integration* units automatically?
3. Does the “template inheritance” system support **multiple inheritance**? If so, how are conflicts in inherited fields resolved?
4. What governance ensures relationship descriptions stay current when units are refactored?

### 1.2 Governance & Conflict Resolution
5. What **criteria** distinguish a “significant change” (requires operator approval) from a routine AI update?
6. How is **operator workload** calibrated—can one operator realistically review all flagged conflicts at scale?
7. In the single‑source‑of‑truth model, how is temporary **forking** handled for experiments or A/B variants?

### 1.3 Comprehensive Coverage & Fragmentation Metrics
8. What threshold of **usage analytics** defines an “under‑accessed” unit requiring investigation (e.g., < 5% of hits)?
9. How does the AI’s “gap report” differentiate between genuinely missing content vs. low user demand topics?
10. Is the **coverage audit** manual or automated—and at what cadence to avoid stale audits?

### 1.4 Project‑Specific Context
11. When multiple versions of AIAI coexist, how does metadata disambiguate between **parallel releases**?
12. How will conflicting **project conventions** be surfaced to avoid silent divergence in shared tools?

### 1.5 Example Drift & Verification
13. What constitutes a **“pass”** in automated example verification—identical output, tolerance bands, or qualitative checks?
14. How are **long‑running examples** (e.g., async workflows) handled within weekly verification windows?

---
## 2  Context Memory Unit Design

### 2.1 Split vs. Merge Criteria
15. How is the 1–5 page guideline enforced—word count, token count, or human judgment?
16. Could the “single responsibility” rule lead to *over‑fragmentation* for highly interdependent concepts?

### 2.2 Deferred Embedding & Search
17. What interim strategy handles **cross‑unit search** before semantic embeddings are introduced?
18. How will adding embeddings later avoid **schema migrations** or rework of existing markdown units?

### 2.3 Storage & Infinite Memory (Deferred)
19. Without a defined retention policy, how will **file‑based storage** scale for multi‑year archives?
20. What backup and disaster‑recovery plan protects critical units in the interim file‑based system?

---
## 3  Reference Document Format & Templates

### 3.1 Mandatory Fields & Validation
21. How is **metadata validation** implemented—YAML schema, CI linting, or runtime checks?
22. What happens if a contributor omits a required field—blocking commit or auto‑fill defaults?

### 3.2 Executive Summary Rationale
23. Has the 2–3 sentence limit been **A/B tested** against alternatives (e.g., bullet lists) for comprehension?
24. How will the system detect when a summary becomes outdated relative to detailed sections?

### 3.3 Example Testing Environment
25. How are **side‑effects** (DB writes, file I/O) sandboxed in containerized tests to avoid polluting real systems?
26. What strategy ensures container images stay up‑to‑date with project dependencies?

### 3.4 Troubleshooting Completeness
27. What analytics identify **emerging errors** not yet in troubleshooting sections?
28. How are **false‑positive** error logs filtered to prevent noise in completeness metrics?

---
## 4  Quality & Verification Loop

### 4.1 Automation vs. Human Review
29. What escalation rules determine when an **AI‑suggested** change is auto‑merged vs. queued for human review?
30. How are **content quality KPIs** (readability, accuracy) measured and fed back into AI retraining?

### 4.2 External Source Link Validation
31. How is **link rot** mitigated for paywalled or ephemeral resources?
32. What legal framework covers storing cached copies of proprietary docs as fallback content?

### 4.3 Upstream Change Detection
33. How will the AI differentiate between **breaking changes** vs. backward‑compatible updates in tool releases?
34. Is there a **dependency graph** mapping units to tool versions for precise impact analysis?

---
## 5  Human‑AI Interaction & Usability

### 5.1 Authoring UX & Template Fatigue
35. How does the AI decide **which sections to hide** in progressive disclosure without omitting critical fields for edge cases?
36. Can power users bypass AI guidance to speed up advanced edits?

### 5.2 Non‑Technical Contributor Safety
37. What safeguards prevent non‑technical edits from inadvertently breaking code examples or metadata integrity?
38. Is there a **preview mode** showing how a unit renders after edits before publishing?

### 5.3 Collaborative Editing & Voice Preservation
39. How does diff visualization handle **rich media** (images, diagrams) for AI suggestions?
40. What metrics track user trust in AI suggestions over time?

---
## 6  Governance, Privacy, and Compliance (Deferred Items)

41. What interim measures protect **PII** in units before formal GDPR alignment?
42. Who is accountable if deferred compliance items cause a **regulatory breach** pre‑launch?

---
## 7  Future Enhancements & Roadmap

### 7.1 Embeddings & Migration
43. How will existing unit IDs map to new embedding IDs during migration?
44. What downtime window is acceptable for re‑indexing when embeddings go live?

### 7.2 Provenance Tracking
45. How will provenance tags be **displayed in UI** to avoid clutter while conveying trust?
46. What prevents malicious actors from **spoofing** provenance metadata?

### 7.3 Multimodal Expansion (Deferred)
47. How will multimodal payloads be **rendered** in markdown without bloating files?
48. Is a separate **binary store** needed for large assets, and how will links remain stable?

---
*End of Round 2 Questions.*

