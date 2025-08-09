# VIBE_CODING – Follow‑Up Question Bank (Post‑FAQ)
*Generated 2025‑08‑07*

Building on the answered FAQ, the lists below surface **remaining or newly‑emergent gaps** that require clarification. Impact scores follow the same legend: **[H]** High, **[M]** Medium, **[L]** Low.

---

## AI‑Agent Perspective

### 1. Create
1. **[H]** How should the AI formally present naming‑rule conflicts to the Operator (diff snippet, table, or inline comment)?  
2. **[H]** What definition of *component* should the AI use when scanning for override files (directory depth, repo label, or config entry)?  
3. **[M]** When generating placeholder tests, which CI labels (e.g., *unit*, *smoke*) should the AI apply so they run in the correct stage?  

### 2. Validate
1. **[H]** What is the maximum wait or retry strategy for installing missing validation tools before escalation?  
2. **[M]** Is there a machine‑readable map of error codes → severity levels that the AI can consult for consistent triage?  

### 3. Test
1. **[H]** What specific heuristics define “basic functionality” when no tests exist (API health check, CLI exit‑code 0, etc.)?  
2. **[M]** Should the AI stub integration test scaffolds when it detects external service calls?  

### 4. Commit
1. **[H]** Is there a commit‑message template (header/body/footer) the AI must populate to pass compliance checks?  
2. **[M]** For multi‑component fixes, may the AI open a draft PR before splitting commits to gather early review?  

### 5. Component Overrides
1. **[H]** How should the AI flag *potentially stale* overrides (mtime > N days, missing referenced files, or checksum drift)?  
2. **[M]** Is the AI allowed to suggest consolidating duplicate override directives across components?  

### 6. Implicit vs Explicit Boundaries
1. **[H]** What idle timeout before the AI re‑pings the Operator on an unanswered explicit‑task prompt?  
2. **[M]** Can the AI cache Operator approvals for identical future tasks, and if so, for how long?  

### 7. Communication Protocol
1. **[H]** Which secondary channel (email, Slack, pager) should the AI use first upon chat outage?  
2. **[L]** Should diagnostic code blocks be collapsed/hidden by default in escalations larger than X lines?  

### 8. Tools & Dependencies
1. **[H]** Where is the authoritative list of pinned tool versions stored (lockfile, wiki, or CI env)?  
2. **[M]** May the AI propose deprecating unused optional tools, and what evidence is required?  

### 9. Risk Mitigation & Error Handling
1. **[H]** Which linter/validator IDs are classified as *security‑blocking* vs. *quality‑blocking*?  
2. **[M]** After rollback, should the AI automatically reopen the original issue or create a new incident ticket?  

### 10. Metrics & Success
1. **[H]** What concrete cycle‑time target (in minutes/hours) constitutes “rapid iteration” for this project?  
2. **[M]** Is documentation coverage measured by LOC percentage, file count, or another metric?  

---

## Operator Perspective

### 1. Create
1. **[H]** Have we documented an escalation path when no authoritative template exists for a directory the AI must modify?  
2. **[M]** What acceptance criteria qualify placeholder tests as “good enough” before full suites are authored?  

### 2. Validate
1. **[H]** What lead‑time is acceptable for provisioning missing validation tools in constrained environments?  
2. **[M]** Do we need a signed‑off severity matrix aligning error classes to required Operator actions?  

### 3. Test
1. **[H]** What percentage of lines or branches must be covered before a PR can merge without additional review?  
2. **[M]** How will manual test evidence be version‑controlled for traceability?  

### 4. Commit
1. **[H]** Do compliance policies mandate GPG‑signed commits for AI‑generated changes?  
2. **[M]** Will the Operator enforce a single‑commit squash at merge time, or preserve the AI’s atomic history?  

### 5. Component Overrides
1. **[H]** What review cadence ensures override files do not drift beyond N days old?  
2. **[L]** Should we archive deleted override files for audit or remove them entirely?  

### 6. Implicit vs Explicit Boundaries
1. **[H]** Have we enumerated tasks that, while normally implicit, become explicit during production freeze windows?  
2. **[M]** What log format captures Operator approvals for task reclassification decisions?  

### 7. Communication Protocol
1. **[H]** Which backup channel is considered authoritative for audit logs when primary chat fails?  
2. **[L]** Do we require daily heartbeat pings from the AI during extended idle periods?  

### 8. Tools & Dependencies
1. **[H]** Who signs off on tool version upgrades that affect reproducibility?  
2. **[M]** Do we maintain a retired‑tools list to prevent re‑introduction?  

### 9. Risk Mitigation & Error Handling
1. **[H]** What is the maximum rollback window before we must issue external communication to stakeholders?  
2. **[M]** Who owns the security review of AI‑generated hotfixes post‑incident?  

### 10. Metrics & Success
1. **[H]** Which leading indicators (e.g., escaped defects per release) trigger a mandatory process audit?  
2. **[M]** How frequently should we recalibrate KPI thresholds as the project matures?

