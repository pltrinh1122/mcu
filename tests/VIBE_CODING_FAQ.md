# VIBE_CODING FAQ
*Generated 2025-08-07*

This document provides answers to frequently asked questions about the VIBE_CODING workflow, addressing both AI-Agent and Operator perspectives.

**Impact scores**: **[H]** High (critical for safe operation), **[M]** Medium (important but not blocking), **[L]** Low (nice-to-have).

---

## AI-Agent Perspective

### 1. Create

**Q1.1 [H] Which directory patterns or templates take precedence when multiple examples exist?**
**A**: Component-specific VIBE_CODING.md files take precedence over global patterns. When multiple component files exist, the AI must ask the Operator to resolve conflicts.

**Q1.2 [H] Are there component-specific file naming rules that must override global ones?**
**A**: Yes, component-specific naming conventions override global rules. The AI must check for component-specific VIBE_CODING.md files before applying global naming patterns.

**Q1.3 [M] What minimum documentation is "good enough" for a newly generated file?**
**A**: All generated files must include appropriate documentation without emojis. The AI should follow established patterns in the codebase for documentation style and depth.

**Q1.4 [L] Should the AI auto-generate placeholder tests when none exist?**
**A**: The AI should generate basic tests for new functionality as part of implicit testing, but should not create extensive test suites without explicit Operator request.

**Q1.5 [H] How should the AI formally present naming-rule conflicts to the Operator (diff snippet, table, or inline comment)?**
**A**: The AI should present conflicts in a clear table format showing the conflicting rules, their sources, and recommended resolution. The AI should not make resolution decisions.

**Q1.6 [H] What definition of component should the AI use when scanning for override files (directory depth, repo label, or config entry)?**
**A**: The AI should scan for VIBE_CODING.md files in the current directory and all parent directories up to the project root. The AI should report all found files to the Operator.

**Q1.7 [M] When generating placeholder tests, which CI labels (e.g., unit, smoke) should the AI apply so they run in the correct stage?**
**A**: The AI should follow project-specific CI label conventions. If no conventions are documented, the AI should ask the Operator for guidance on appropriate labels.

### 2. Validate

**Q2.1 [H] How should the AI proceed when essential validation tools (e.g., shellcheck) are absent?**
**A**: The AI must provide recommendations and hand the decision to the Operator. The AI should not proceed with validation until the Operator decides how to handle missing tools.

**Q2.2 [H] What error-severity threshold requires escalation versus silent auto-fix?**
**A**: Security-related errors and validation failures during explicit testing require escalation. Syntax errors during implicit validation can be auto-fixed. The AI must ask the Operator for guidance on any unclear error severity.

**Q2.3 [M] Are schema validations mandatory or optional for YAML/JSON?**
**A**: Schema validations are mandatory when schemas are available. The AI must check for component-specific validation requirements and apply them.

**Q2.4 [L] When multiple formatters conflict (e.g., black vs. project style), which wins?**
**A**: Project-specific formatting rules take precedence. The AI should check for component-specific formatting requirements before applying global formatters.

**Q2.5 [H] What is the maximum wait or retry strategy for installing missing validation tools before escalation?**
**A**: The AI should not attempt to install tools automatically. The AI should immediately report missing tools to the Operator and ask for guidance on how to proceed.

**Q2.6 [M] Is there a machine-readable map of error codes → severity levels that the AI can consult for consistent triage?**
**A**: The AI should check for project-specific error severity mappings. If none exist, the AI should ask the Operator for guidance on error classification.

### 3. Test

**Q3.1 [H] If no integration tests are defined, what constitutes "workable" test coverage?**
**A**: The AI should run unit tests for modified components and verify basic functionality. If no tests exist, the AI must report this to the Operator and ask for guidance on test requirements.

**Q3.2 [M] How should the AI mark manual verification steps as complete?**
**A**: The AI should report manual verification requirements to the Operator and wait for confirmation before proceeding. The AI cannot mark manual steps as complete.

**Q3.3 [M] What performance regression budget is acceptable before Operator review?**
**A**: The AI should report any performance impacts to the Operator and ask for guidance on acceptable thresholds. The AI cannot make decisions about performance trade-offs.

**Q3.4 [L] Should test artifacts be persisted or discarded after CI runs?**
**A**: The AI should follow project-specific conventions for test artifacts. If no convention exists, the AI should ask the Operator for guidance.

**Q3.5 [H] What specific heuristics define "basic functionality" when no tests exist (API health check, CLI exit-code 0, etc.)?**
**A**: The AI should check for project-specific functionality verification procedures. If none exist, the AI should ask the Operator for guidance on what constitutes basic functionality verification.

**Q3.6 [M] Should the AI stub integration test scaffolds when it detects external service calls?**
**A**: The AI should report detected external service calls to the Operator and ask for guidance on whether to create integration test scaffolds.

### 4. Commit

**Q4.1 [H] What branch naming convention must the AI follow to avoid CI rejection?**
**A**: The AI must follow project-specific branch naming conventions. If no convention is documented, the AI should ask the Operator for guidance before creating branches.

**Q4.2 [H] When the commit touches multiple components, is a single atomic commit acceptable?**
**A**: The AI should create atomic commits for related changes. If changes span multiple components, the AI should ask the Operator whether to split into multiple commits.

**Q4.3 [M] What metadata (issue IDs, risk tags) must appear in the commit message?**
**A**: The AI should include relevant issue IDs and reference related components. The AI must not include emojis in commit messages.

**Q4.4 [L] How should the AI handle large auto-generated diffs that exceed review limits?**
**A**: The AI should report large diffs to the Operator and ask for guidance on how to proceed. The AI should not split commits without Operator approval.

**Q4.5 [H] Is there a commit-message template (header/body/footer) the AI must populate to pass compliance checks?**
**A**: The AI should check for project-specific commit message templates. If no template exists, the AI should ask the Operator for guidance on required commit message format.

**Q4.6 [M] For multi-component fixes, may the AI open a draft PR before splitting commits to gather early review?**
**A**: The AI should ask the Operator for guidance before opening draft PRs. The AI should not create PRs without explicit Operator approval.

### 5. Component Overrides

**Q5.1 [H] How will the AI detect stale component-level VIBE_CODING.md files?**
**A**: The AI should report the discovery of component-specific files and ask the Operator to verify their currency. The AI cannot determine if files are stale.

**Q5.2 [H] What merge strategy resolves direct conflicts between global and local rules?**
**A**: The AI must ask the Operator to resolve conflicts between global and component-specific requirements. The AI cannot make decisions about rule precedence.

**Q5.3 [M] What logging of discovered overrides is sufficient for audit?**
**A**: The AI must report which component-specific files were found and incorporated, including the specific requirements that were merged.

**Q5.4 [L] Should the AI propose deleting empty override files?**
**A**: The AI should report empty override files to the Operator and ask for guidance on whether to remove them.

**Q5.5 [H] How should the AI flag potentially stale overrides (mtime > N days, missing referenced files, or checksum drift)?**
**A**: The AI should report any potential staleness indicators to the Operator and ask for verification. The AI should not make decisions about file currency.

**Q5.6 [M] Is the AI allowed to suggest consolidating duplicate override directives across components?**
**A**: The AI can suggest consolidation to the Operator, but should not implement changes without explicit approval.

### 6. Implicit vs Explicit Task Boundaries

**Q6.1 [H] Which tasks are always Operator-explicit, regardless of context?**
**A**: Security-related changes, architectural decisions, and any changes that could have irrecoverable consequences are always explicit tasks requiring Operator approval.

**Q6.2 [H] How is Operator intent captured to re-classify a task from implicit to explicit?**
**A**: The AI must ask the Operator for explicit guidance when reclassifying tasks. The AI should not assume task classification without Operator input.

**Q6.3 [M] What timeout defines "no response" before proceeding autonomously?**
**A**: The AI should not proceed autonomously without Operator guidance for explicit tasks. The AI should wait for Operator response.

**Q6.4 [L] Can the AI suggest boundary re-definitions when patterns emerge?**
**A**: The AI can suggest boundary redefinitions to the Operator, but cannot implement changes without explicit approval.

**Q6.5 [H] What idle timeout before the AI re-pings the Operator on an unanswered explicit-task prompt?**
**A**: The AI should wait for Operator response and not proceed autonomously. The AI should not set arbitrary timeouts for explicit tasks.

**Q6.6 [M] Can the AI cache Operator approvals for identical future tasks, and if so, for how long?**
**A**: The AI should not cache approvals without explicit Operator permission. Each task should be evaluated individually.

### 7. Communication Protocol

**Q7.1 [H] What escalation channels exist if the primary chat is unavailable?**
**A**: The AI should report communication issues to the Operator and ask for alternative communication methods. The AI cannot proceed without Operator guidance.

**Q7.2 [M] How should the AI package technical logs to remain professional yet concise?**
**A**: The AI should provide clear, professional summaries of technical logs without emojis. The AI should focus on actionable information.

**Q7.3 [L] Under what conditions may the AI use code blocks for diagnostics?**
**A**: The AI can use code blocks for technical diagnostics when they help clarify issues. The AI should keep diagnostic output concise and relevant.

**Q7.4 [H] Which secondary channel (email, Slack, pager) should the AI use first upon chat outage?**
**A**: The AI should ask the Operator for guidance on backup communication channels. The AI should not assume which channel to use.

**Q7.5 [L] Should diagnostic code blocks be collapsed/hidden by default in escalations larger than X lines?**
**A**: The AI should keep diagnostic output concise and relevant. The AI should ask the Operator for guidance on output formatting preferences.

### 8. Tools & Dependencies

**Q8.1 [H] What baseline tool versions are assumed "workable" across all environments?**
**A**: The AI should check for project-specific tool version requirements. If no requirements are documented, the AI should ask the Operator for guidance.

**Q8.2 [M] When multiple security scanners are listed, which order should they run?**
**A**: The AI should follow the order specified in component-specific requirements. If no order is specified, the AI should ask the Operator for guidance.

**Q8.3 [L] Should optional tools be auto-installed or proposed first?**
**A**: The AI should propose optional tool installation to the Operator rather than auto-installing them.

**Q8.4 [H] Where is the authoritative list of pinned tool versions stored (lockfile, wiki, or CI env)?**
**A**: The AI should check for project-specific tool version documentation. If none exists, the AI should ask the Operator for guidance on tool version management.

**Q8.5 [M] May the AI propose deprecating unused optional tools, and what evidence is required?**
**A**: The AI can suggest tool deprecation to the Operator, but should not implement changes without explicit approval.

### 9. Risk Mitigation & Error Handling

**Q9.1 [H] Which validation failures are classified as potentially irrecoverable security risks?**
**A**: Any validation failure that could introduce security vulnerabilities is classified as irrecoverable. The AI must escalate these to the Operator immediately.

**Q9.2 [H] How often should rollback checkpoints be created during multi-step fixes?**
**A**: The AI should create rollback checkpoints before each major step in multi-step fixes. The AI should ask the Operator for guidance on checkpoint frequency.

**Q9.3 [M] What data is logged for post-mortem when an automatic fix fails?**
**A**: The AI should log the original error, the attempted fix, and the failure reason. The AI should provide this information to the Operator for analysis.

**Q9.4 [L] Can the AI auto-silence non-critical linter warnings?**
**A**: The AI should report non-critical warnings to the Operator and ask for guidance on whether to suppress them.

**Q9.5 [H] Which linter/validator IDs are classified as security-blocking vs. quality-blocking?**
**A**: The AI should check for project-specific security classification rules. If none exist, the AI should ask the Operator for guidance on error classification.

**Q9.6 [M] After rollback, should the AI automatically reopen the original issue or create a new incident ticket?**
**A**: The AI should ask the Operator for guidance on post-rollback procedures. The AI should not make decisions about issue management.

### 10. Metrics & Success

**Q10.1 [H] What KPI thresholds trigger a performance alert to the Operator?**
**A**: The AI should report any performance degradation to the Operator and ask for guidance on acceptable thresholds.

**Q10.2 [M] How is "rapid iteration" quantified (e.g., average cycle time target)?**
**A**: The AI should focus on completing the create-validate-test-commit cycle efficiently while maintaining quality standards.

**Q10.3 [L] Does documentation coverage include inline code comments or only top-level docs?**
**A**: The AI should include appropriate inline comments and top-level documentation, following project-specific conventions.

**Q10.4 [H] What concrete cycle-time target (in minutes/hours) constitutes "rapid iteration" for this project?**
**A**: The AI should ask the Operator for guidance on specific cycle-time targets. The AI should not assume performance expectations.

**Q10.5 [M] Is documentation coverage measured by LOC percentage, file count, or another metric?**
**A**: The AI should check for project-specific documentation metrics. If none exist, the AI should ask the Operator for guidance.

---

## Operator Perspective

### 1. Create

**Q1.1 [H] Have we defined authoritative patterns/templates for every directory the AI may touch?**
**A**: The Operator should ensure that authoritative patterns are defined for all directories. The AI will report any missing patterns and ask for guidance.

**Q1.2 [M] What evidence is required to accept "good enough" documentation from the AI?**
**A**: The Operator should define documentation standards and review AI-generated documentation against these standards.

**Q1.3 [L] Will we permit the AI to introduce new third-party dependencies in generated code?**
**A**: The Operator should establish policies for third-party dependency introduction and communicate these to the AI.

**Q1.4 [H] Have we documented an escalation path when no authoritative template exists for a directory the AI must modify?**
**A**: The Operator should establish escalation procedures for missing templates and communicate these to the AI.

**Q1.5 [M] What acceptance criteria qualify placeholder tests as "good enough" before full suites are authored?**
**A**: The Operator should define acceptance criteria for placeholder tests and communicate these to the AI.

### 2. Validate

**Q2.1 [H] Which validation tools are mandatory for compliance or licensing reasons?**
**A**: The Operator should identify mandatory validation tools and ensure the AI has access to them.

**Q2.2 [H] What is our policy for approving AI-applied auto-fixes that alter business logic?**
**A**: The Operator should establish clear policies for business logic changes and communicate these to the AI.

**Q2.3 [M] How will we audit skipped validations approved under time pressure?**
**A**: The Operator should establish audit procedures for skipped validations and ensure proper documentation.

**Q2.4 [H] What lead-time is acceptable for provisioning missing validation tools in constrained environments?**
**A**: The Operator should establish lead-time requirements for tool provisioning and communicate these to the AI.

**Q2.5 [M] Do we need a signed-off severity matrix aligning error classes to required Operator actions?**
**A**: The Operator should establish error severity matrices and communicate these to the AI.

### 3. Test

**Q3.1 [H] What constitutes the minimal acceptable test suite for a production change?**
**A**: The Operator should define minimum test requirements and communicate these to the AI.

**Q3.2 [M] How do we record manual test evidence to satisfy audit trails?**
**A**: The Operator should establish procedures for recording manual test evidence.

**Q3.3 [L] What is the Operator's SLA for responding to AI test-failure escalations?**
**A**: The Operator should establish response time expectations for test-failure escalations.

**Q3.4 [H] What percentage of lines or branches must be covered before a PR can merge without additional review?**
**A**: The Operator should establish test coverage requirements and communicate these to the AI.

**Q3.5 [M] How will manual test evidence be version-controlled for traceability?**
**A**: The Operator should establish version control procedures for manual test evidence.

### 4. Commit

**Q4.1 [H] Do we require signed commits or other provenance controls for AI changes?**
**A**: The Operator should establish commit signing requirements and communicate these to the AI.

**Q4.2 [M] Will the Operator review be per-commit or batched?**
**A**: The Operator should establish review procedures and communicate these to the AI.

**Q4.3 [L] How will we handle commit-message overrides—inline edit or follow-up commit?**
**A**: The Operator should establish procedures for commit-message overrides.

**Q4.4 [H] Do compliance policies mandate GPG-signed commits for AI-generated changes?**
**A**: The Operator should establish compliance requirements for AI-generated changes and communicate these to the AI.

**Q4.5 [M] Will the Operator enforce a single-commit squash at merge time, or preserve the AI's atomic history?**
**A**: The Operator should establish merge procedures and communicate these to the AI.

### 5. Component Overrides

**Q5.1 [H] How frequently should component-level rules be reviewed for drift?**
**A**: The Operator should establish review schedules for component-level rules.

**Q5.2 [M] What documentation proves that a conflict resolution decision was made?**
**A**: The Operator should establish documentation requirements for conflict resolution decisions.

**Q5.3 [L] Do we sunset component overrides that simply mirror global defaults?**
**A**: The Operator should establish procedures for managing component overrides.

**Q5.4 [H] What review cadence ensures override files do not drift beyond N days old?**
**A**: The Operator should establish review cadence requirements and communicate these to the AI.

**Q5.5 [L] Should we archive deleted override files for audit or remove them entirely?**
**A**: The Operator should establish archiving procedures for deleted override files.

### 6. Implicit vs Explicit Task Boundaries

**Q6.1 [H] Have we enumerated high-risk tasks that always require explicit Operator sign-off?**
**A**: The Operator should identify high-risk tasks and communicate these to the AI.

**Q6.2 [H] What mechanism records the Operator's decision when reclassifying a task?**
**A**: The Operator should establish procedures for recording task reclassification decisions.

**Q6.3 [M] Is there a rubric for determining when a task graduates from explicit to implicit?**
**A**: The Operator should establish criteria for task reclassification.

**Q6.4 [H] Have we enumerated tasks that, while normally implicit, become explicit during production freeze windows?**
**A**: The Operator should establish production freeze procedures and communicate these to the AI.

**Q6.5 [M] What log format captures Operator approvals for task reclassification decisions?**
**A**: The Operator should establish logging procedures for task reclassification decisions.

### 7. Communication Protocol

**Q7.1 [H] What backup communication channel exists if chat access is lost?**
**A**: The Operator should establish backup communication channels and communicate these to the AI.

**Q7.2 [M] How detailed should AI escalation reports be to remain actionable but concise?**
**A**: The Operator should establish escalation report requirements.

**Q7.3 [L] Do we require periodic check-ins even when no issues occur?**
**A**: The Operator should establish check-in requirements.

**Q7.4 [H] Which backup channel is considered authoritative for audit logs when primary chat fails?**
**A**: The Operator should establish authoritative backup channels and communicate these to the AI.

**Q7.5 [L] Do we require daily heartbeat pings from the AI during extended idle periods?**
**A**: The Operator should establish heartbeat requirements and communicate these to the AI.

### 8. Tools & Dependencies

**Q8.1 [H] Who approves new tool installations proposed by the AI?**
**A**: The Operator should establish approval procedures for new tool installations.

**Q8.2 [M] How do we verify that tool versions remain within supported ranges?**
**A**: The Operator should establish tool version verification procedures.

**Q8.3 [L] Do we maintain a central registry of optional tools for visibility?**
**A**: The Operator should establish tool registry procedures.

**Q8.4 [H] Who signs off on tool version upgrades that affect reproducibility?**
**A**: The Operator should establish approval procedures for tool version upgrades.

**Q8.5 [M] Do we maintain a retired-tools list to prevent re-introduction?**
**A**: The Operator should establish procedures for managing retired tools.

### 9. Risk Mitigation & Error Handling

**Q9.1 [H] What rollback window is acceptable before customer impact is deemed irrecoverable?**
**A**: The Operator should establish rollback window requirements.

**Q9.2 [H] How will we verify that AI-made fixes do not introduce new security risks?**
**A**: The Operator should establish security verification procedures.

**Q9.3 [M] Who owns the post-mortem process for AI-caused incidents?**
**A**: The Operator should establish post-mortem ownership and procedures.

**Q9.4 [H] What is the maximum rollback window before we must issue external communication to stakeholders?**
**A**: The Operator should establish external communication procedures and communicate these to the AI.

**Q9.5 [M] Who owns the security review of AI-generated hotfixes post-incident?**
**A**: The Operator should establish post-incident security review procedures.

### 10. Metrics & Success

**Q10.1 [H] Which metrics will serve as leading indicators of quality drift?**
**A**: The Operator should establish quality metrics and monitoring procedures.

**Q10.2 [M] How often will we review AI performance against the defined KPIs?**
**A**: The Operator should establish performance review schedules.

**Q10.3 [L] What threshold of documentation coverage is acceptable before release?**
**A**: The Operator should establish documentation coverage requirements.

**Q10.4 [H] Which leading indicators (e.g., escaped defects per release) trigger a mandatory process audit?**
**A**: The Operator should establish audit trigger procedures and communicate these to the AI.

**Q10.5 [M] How frequently should we recalibrate KPI thresholds as the project matures?**
**A**: The Operator should establish KPI recalibration procedures.

---

## Clarifying Questions for Future VIBE_CODING Iterations

### High Priority Questions

1. **Security Escalation Procedures**: What specific security validation failures require immediate Operator escalation versus automated handling?

2. **Tool Availability Fallbacks**: What are the specific fallback procedures when critical validation tools (yamllint, shellcheck, etc.) are unavailable?

3. **Component Conflict Resolution**: What is the specific process for resolving conflicts between global and component-specific VIBE_CODING.md requirements?

4. **Explicit Task Definition**: What specific criteria determine when a task transitions from implicit to explicit, and how is this communicated?

5. **Rollback Procedures**: What are the specific rollback procedures for different types of changes (security, data, configuration)?

6. **Performance Thresholds**: What are the specific performance degradation thresholds that require Operator notification?

7. **Commit Approval Process**: What is the specific process for Operator approval of commits, including timing and review requirements?

8. **Communication Backup**: What are the specific backup communication channels when primary chat is unavailable?

### Medium Priority Questions

9. **Test Coverage Standards**: What are the specific minimum test coverage requirements for different types of changes?

10. **Documentation Standards**: What are the specific documentation requirements for different types of generated files?

11. **Tool Version Management**: What are the specific procedures for managing tool versions and dependencies?

12. **Quality Metrics**: What are the specific quality metrics and thresholds for monitoring AI performance?

13. **Conflict Documentation**: What specific documentation is required when resolving conflicts between requirements?

14. **Escalation Timeouts**: What are the specific timeout periods for different types of escalations?

15. **Audit Trail Requirements**: What specific audit trail requirements exist for AI actions and decisions?

### Low Priority Questions

16. **Optional Tool Installation**: What are the specific procedures for proposing and installing optional tools?

17. **Test Artifact Management**: What are the specific procedures for managing test artifacts and outputs?

18. **Linter Warning Management**: What are the specific procedures for handling non-critical linter warnings?

19. **Component Override Cleanup**: What are the specific procedures for managing and cleaning up component overrides?

20. **Performance Optimization**: What are the specific procedures for AI-initiated performance optimizations?

These questions should be addressed in future iterations of VIBE_CODING to provide more specific guidance and reduce ambiguity in the workflow.
