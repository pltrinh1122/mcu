# VIBE_CODING Gap‑Spotting Question Bank  
*Generated 2025‑08‑07*  

This document lists targeted questions to surface gaps in the **VIBE_CODING.md** workflow from two complementary viewpoints:

* **AI‑Agent** – Ensuring safe, autonomous execution.  
* **Operator** – Maintaining control, transparency, and accountability.  

**Impact scores**: **[H]** High (critical for safe operation), **[M]** Medium (important but not blocking), **[L]** Low (nice‑to‑have).

---

## AI‑Agent Perspective

### 1. Create  
1. [H] Which directory patterns or templates take precedence when multiple examples exist?  
2. [H] Are there component‑specific file naming rules that must override global ones?  
3. [M] What minimum documentation is “good enough” for a newly generated file?  
4. [L] Should the AI auto‑generate placeholder tests when none exist?  

### 2. Validate  
1. [H] How should the AI proceed when essential validation tools (e.g., **shellcheck**) are absent?  
2. [H] What error‑severity threshold requires escalation versus silent auto‑fix?  
3. [M] Are schema validations mandatory or optional for YAML/JSON?  
4. [L] When multiple formatters conflict (e.g., *black* vs. project style), which wins?  

### 3. Test  
1. [H] If no integration tests are defined, what constitutes “workable” test coverage?  
2. [M] How should the AI mark manual verification steps as complete?  
3. [M] What performance regression budget is acceptable before Operator review?  
4. [L] Should test artifacts be persisted or discarded after CI runs?  

### 4. Commit  
1. [H] What branch naming convention must the AI follow to avoid CI rejection?  
2. [H] When the commit touches multiple components, is a single atomic commit acceptable?  
3. [M] What metadata (issue IDs, risk tags) must appear in the commit message?  
4. [L] How should the AI handle large auto‑generated diffs that exceed review limits?  

### 5. Component Overrides  
1. [H] How will the AI detect stale component‑level **VIBE_CODING.md** files?  
2. [H] What merge strategy resolves direct conflicts between global and local rules?  
3. [M] What logging of discovered overrides is sufficient for audit?  
4. [L] Should the AI propose deleting empty override files?  

### 6. Implicit vs Explicit Task Boundaries  
1. [H] Which tasks are *always* Operator‑explicit, regardless of context?  
2. [H] How is Operator intent captured to re‑classify a task from implicit to explicit?  
3. [M] What timeout defines “no response” before proceeding autonomously?  
4. [L] Can the AI suggest boundary re‑definitions when patterns emerge?  

### 7. Communication Protocol  
1. [H] What escalation channels exist if the primary chat is unavailable?  
2. [M] How should the AI package technical logs to remain professional yet concise?  
3. [L] Under what conditions may the AI use code blocks for diagnostics?  

### 8. Tools & Dependencies  
1. [H] What baseline tool versions are assumed “workable” across all environments?  
2. [M] When multiple security scanners are listed, which order should they run?  
3. [L] Should optional tools be auto‑installed or proposed first?  

### 9. Risk Mitigation & Error Handling  
1. [H] Which validation failures are classified as potentially *irrecoverable* security risks?  
2. [H] How often should rollback checkpoints be created during multi‑step fixes?  
3. [M] What data is logged for post‑mortem when an automatic fix fails?  
4. [L] Can the AI auto‑silence non‑critical linter warnings?  

### 10. Metrics & Success  
1. [H] What KPI thresholds trigger a performance alert to the Operator?  
2. [M] How is “rapid iteration” quantified (e.g., average cycle time target)?  
3. [L] Does documentation coverage include inline code comments or only top‑level docs?  

---

## Operator Perspective

### 1. Create  
1. [H] Have we defined authoritative patterns/templates for every directory the AI may touch?  
2. [M] What evidence is required to accept “good enough” documentation from the AI?  
3. [L] Will we permit the AI to introduce new third‑party dependencies in generated code?  

### 2. Validate  
1. [H] Which validation tools are *mandatory* for compliance or licensing reasons?  
2. [H] What is our policy for approving AI‑applied auto‑fixes that alter business logic?  
3. [M] How will we audit skipped validations approved under time pressure?  

### 3. Test  
1. [H] What constitutes the minimal acceptable test suite for a production change?  
2. [M] How do we record manual test evidence to satisfy audit trails?  
3. [L] What is the Operator’s SLA for responding to AI test‑failure escalations?  

### 4. Commit  
1. [H] Do we require signed commits or other provenance controls for AI changes?  
2. [M] Will the Operator review be per‑commit or batched?  
3. [L] How will we handle commit‑message overrides—inline edit or follow‑up commit?  

### 5. Component Overrides  
1. [H] How frequently should component‑level rules be reviewed for drift?  
2. [M] What documentation proves that a conflict resolution decision was made?  
3. [L] Do we sunset component overrides that simply mirror global defaults?  

### 6. Implicit vs Explicit Task Boundaries  
1. [H] Have we enumerated high‑risk tasks that *always* require explicit Operator sign‑off?  
2. [H] What mechanism records the Operator’s decision when reclassifying a task?  
3. [M] Is there a rubric for determining when a task graduates from explicit to implicit?  

### 7. Communication Protocol  
1. [H] What backup communication channel exists if chat access is lost?  
2. [M] How detailed should AI escalation reports be to remain actionable but concise?  
3. [L] Do we require periodic check‑ins even when no issues occur?  

### 8. Tools & Dependencies  
1. [H] Who approves new tool installations proposed by the AI?  
2. [M] How do we verify that tool versions remain within supported ranges?  
3. [L] Do we maintain a central registry of optional tools for visibility?  

### 9. Risk Mitigation & Error Handling  
1. [H] What rollback window is acceptable before customer impact is deemed irrecoverable?  
2. [H] How will we verify that AI‑made fixes do not introduce new security risks?  
3. [M] Who owns the post‑mortem process for AI‑caused incidents?  

### 10. Metrics & Success  
1. [H] Which metrics will serve as *leading indicators* of quality drift?  
2. [M] How often will we review AI performance against the defined KPIs?  
3. [L] What threshold of documentation coverage is acceptable before release?  

