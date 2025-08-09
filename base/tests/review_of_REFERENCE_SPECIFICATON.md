# Gap‑Spotting Question Bank for the Reference Specification (CMI‑Enhanced Docs)

> *Role lens:* Cognitive Researcher, Scientist, and AI Engineer.
> *Purpose:* Probe the specification for unaddressed assumptions, feasibility risks, and clarity gaps.

---
## 1. Problem Statements & Proposed Solutions

1. **Information Fragmentation → “Self‑contained context memory units”**  
   - How will self‑contained context units avoid duplication across units when two sources overlap?  
   - What governance process ensures conflicting information in distinct units is reconciled?  
   - How do you measure that “comprehensive coverage” has truly eliminated fragmentation?
2. **Context Loss → “Context‑aware examples with AIAI project integration”**  
   - How is “project‑specific context” formally captured— via metadata fields, examples, or dynamic embedding?  
   - What prevents examples from drifting out of sync with the live project over time?  
   - How will context units adapt if multiple projects share the same tool but differ in conventions?
3. **AI Consumption Inefficiency → “Structured, consistent format”**  
   - Which specific schema or standard (e.g., OpenAPI, Markdown front‑matter) guarantees AI‑friendliness?  
   - Have you benchmarked parsing speed or retrieval accuracy against baseline unstructured docs?  
   - How will backward compatibility be handled if the format evolves?
4. **Human Cognitive Load → “Digestible summary chunks”**  
   - What empirical readability or comprehension metrics will validate that cognitive load is reduced?  
   - How do summary chunks stay aligned with deep‑dive details during iterative edits?  
   - Could progressive disclosure hide critical caveats unless users drill down?
5. **Staleness and Accuracy → “Automated verification”**  
   - What toolchain (CI, tests, linters) performs verification, and at what cadence?  
   - How are unverifiable examples flagged and surfaced to users?  
   - Who owns remediation when automated tests fail—docs team or component owners?
6. **Lack of Memory Continuity → “Persistent identifiers”**  
   - How do you guarantee global uniqueness of IDs across distributed teams?  
   - What happens when a context unit is deprecated—do references break or redirect?  
   - How will versioning semantics interact with external citations (URLs, bookmarks)?

---
## 2. CMI Context Memory Unit Design

1. **Unit Granularity**  
   - What criteria decide when to split vs. merge content into distinct units?  
   - How does unit size affect retrieval latency and embedding quality?  
   - Is there an upper limit to payload length before the embedding loses fidelity?
2. **Embedding Strategy**  
   - Which model family (e.g., BERT, OpenAI Ada‑002) is used, and how often will embeddings be refreshed?  
   - How are language‑agnostic or multimodal (image, code) payloads embedded and aligned?  
   - What is the fallback when an embedding model deprecates or drifts?
3. **Infinite Memory Claim**  
   - How will storage costs scale—what budget or archival policy keeps “infinite” practical?  
   - Are there retention or compliance constraints (GDPR “right to forget”) that contradict infinite memory?  
   - When memory is pruned, how are downstream embeddings and links updated?
4. **Context‑Aware Retrieval**  
   - What ranking algorithm combines semantic similarity with metadata filters?  
   - How is “project relevance” distinguished from global relevance in hybrid corpora?  
   - How will retrieval be evaluated for precision/recall metrics in real workflows?

---
## 3. Reference Document Format & Templates

1. **Metadata Completeness**  
   - Which fields are mandatory for every template, and how is omission detected?  
   - How does the schema evolve when new metadata (e.g., security classification) is needed?  
   - Can users define custom fields without breaking downstream tooling?
2. **Executive Summary Length**  
   - Why limit to 2–3 sentences—has this been validated with user research?  
   - How will summaries be kept current when detailed sections evolve?  
   - Could AI auto‑summaries introduce subtle inaccuracies?
3. **Examples & Patterns Validation**  
   - What environment is used to “test” examples—containerized CI, mock services?  
   - How are flaky tests or environment drifts surfaced to maintainers?  
   - Do examples include performance implications, not just correctness?
4. **Troubleshooting Section Scope**  
   - How is completeness measured—user error logs, support tickets, survey feedback?  
   - How frequently are troubleshooting steps re‑verified against new software versions?  
   - What mechanism encourages users to contribute newly discovered issues?

---
## 4. Quality & Verification Loop

1. **Automated vs. Human Review**  
   - Which tasks stay automated (syntax, code execution) vs. require expert human validation?  
   - How is reviewer accountability tracked across versions?  
   - What SLAs exist for resolving failed verifications?
2. **Source Attribution Integrity**  
   - How are external source links validated over time (link rot)?  
   - What citation standard is used (MLA, APA, custom) and does AI parse it robustly?  
   - How are proprietary or confidential sources referenced without exposing IP?
3. **Change Detection**  
   - How does the system detect upstream tool changes (API v2) and flag affected units?  
   - Is there a dependency graph to propagate impact analysis?  
   - How is obsolete content surfaced to users (soft warnings vs. hard blocks)?

---
## 5. Human–AI Interaction & Usability

1. **Operator Workflow Integration**  
   - How is authoring UX designed so humans don’t feel “template fatigue”?  
   - Can non‑technical contributors add or edit context units safely?  
   - How are accessibility standards (a11y) met in rendered docs?
2. **AI Feedback Loop**  
   - How can AI suggest edits without overriding human voice or introducing hallucinations?  
   - Is there inline diff visualization to accept/reject AI suggestions?  
   - How is trust calibrated when AI recommends deleting outdated units?
3. **Performance Metrics & KPIs**  
   - Which metrics prove reduced cognitive load (task completion time, error rate)?  
   - How will you A/B test new template iterations?  
   - What success benchmarks transition the spec from beta to “approved”?

---
## 6. Governance, Privacy, and Compliance

1. **Data Ownership & Rights**  
   - Who legally owns the embedded context units—organization or individual author?  
   - How is user consent captured for personal data stored in units?  
   - What export formats guarantee portability if the platform is sunset?
2. **Security Posture**  
   - What threat model covers embedding leakage or adversarial retrieval attacks?  
   - Is encryption applied to embeddings and metadata, not just payload?  
   - How are access logs retained for audit purposes?
3. **Regulatory Alignment**  
   - Does the system align with GDPR, CCPA, HIPAA where applicable?  
   - How is “right to be forgotten” handled when embeddings persist semantic traces?  
   - Are there sector‑specific documentation standards (e.g., FDA, ISO) that must map to unit metadata?

---
## 7. Future Enhancements & Roadmap Assumptions

1. **Embedding Model Upgrades**  
   - What migration path exists when embedding dimensions change?  
   - How do you re‑index petabytes of vectors with zero downtime?  
   - Will older units be re‑embedded or kept in legacy format?
2. **Generative AI Co‑Authoring**  
   - How will AI auto‑generation be distinguished from human content (provenance tags)?  
   - What guardrails prevent the AI from citing non‑public internal data?  
   - Can AI suggest new context unit links automatically, and how are false links pruned?
3. **Multimodal Expansion**  
   - How will image, audio, and code snippets be uniformly embedded and retrieved?  
   - What UX mechanisms let users preview multimodal payloads inline?  
   - Does the schema need a "modality" field beyond type?

---
*End of Gap‑Spotting Question Bank.*

