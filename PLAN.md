# log-report — Submission Plan

Plan for bringing the `dynamo/log-report` task into compliance with the updated Dynamo evaluation pipeline and reaching RTD submission.

**Last updated:** 2026-07-13  
**Official reference:** [Dynamo Updates](https://project-dynamo.learn.joinhandshake.com/updates)

---

## 1. Goal

Submit a high-quality Dynamo task that:

1. Passes structural and alignment checks on the platform
2. Clears **Stage 1 (Pass@2)** — at least 1 genuine failure in 2 trials (GPT-5.4 + Terminus-2, extra-high reasoning)
3. Clears **Stage 2 (Pass@5)** — at least 3 genuine failures in 5 trials (current difficulty bar; see §2.1)
4. Reaches the **RTD layer** (eligible for the **$50 incentive** during the 2-day push)

---

## 2. Official Dynamo Platform Updates

This section mirrors the [Updates page](https://project-dynamo.learn.joinhandshake.com/updates). **June 30 supersedes June 24 on difficulty metrics** (pass@8 → pass@5).

### 2.1 June 30, 2026 — Difficulty metric: pass@8 → pass@5

| Item | Detail |
|------|--------|
| **New difficulty bar** | **Pass@5** — reference agent runs **5 times** (was 8) |
| **Failure requirement** | Task must produce **≥ 3 valid failures out of 5** |
| **Acceptance bands** | **0–2/5 valid failures → accepted** (0/5 = strongest — fully stumped, oracle still solves it) |
| **Rejection bands** | **3–5/5 valid failures → rejected** as too easy |
| **Valid failure rules** | Unchanged — see §2.3 |
| **Unchanged** | Reference model/agent (**GPT-5.4** + **Terminus-2**), Pass@2 behavior, **3600s timeout ceiling**, all other guidance |

### 2.2 June 24, 2026 — task.toml structure

The reference `task.toml` is now a **single canonical block**, identical between:

- Workflow step 7: *"Instruction.md and task.toml"*
- Workflow step 9: *"Task.toml reference"*

**Top-level structure:**

```toml
artifacts = [...]          # top-level artifact paths

[task]
name = "..."
description = "..."

[metadata]
# Grouped into: pre-seeded / fixed-dataset / fellow-set fields
# See §2.5 for what contributors edit

[verifier]
timeout_sec = ...
# environment_mode — LEAVE UNSET

[agent]
timeout_sec = ...

[environment]
build_timeout_sec = ...
cpus = ...
memory_mb = ...
storage_mb = ...
gpus = ...
allow_internet = ...
mcp_servers = []
```

**Removed everywhere:** `avg_at_8` — pass@ acceptance is now handled by the evaluation pipeline (§2.4), not a `task.toml` field.

### 2.3 June 24, 2026 — Difficulty bar and evaluation pipeline

The acceptance bar was raised. Submissions are **blocked** until all checks pass.

#### What counts as a valid (genuine) failure

- Agent produces incorrect output or misses stated requirements
- Verifier correctly rejects the agent's output

#### What does NOT count

- **Timeouts**
- **Infrastructure issues** (Docker build failures, environment setup errors)
- **Instruction ↔ verifier misalignment** — these are **blocking**; fix before proceeding; they never count toward the failure quota

#### Reference agent configuration

| Setting | Value |
|---------|-------|
| Model | **GPT-5.4** |
| Agent | **Terminus-2** |
| Reasoning effort | **Extra-high** |
| Timeout ceiling | **3600s** (platform-wide cap) |

#### Two-stage evaluation pipeline

| Stage | When | Trials | Requirement | Notes |
|-------|------|--------|-------------|-------|
| **Stage 1 — Pass@2** | First | 2 | ≥ **1** valid failure | Includes LLM analysis of the runs |
| **Stage 2 — Pass@5** | After Pass@2 passes | 5 | ≥ **3** valid failures | Replaces former Pass@8 (was ≥ 4/8) |

> **Note:** Announcement email (pre–June 30) referenced Pass@8 with ≥ 4/8 failures. The live Updates page (June 30) is authoritative: use **Pass@5 with ≥ 3/5**.

### 2.4 June 24, 2026 — Verifier and environment model

| Rule | Detail |
|------|--------|
| `[verifier].environment_mode` | **Leave unset** |
| Verifier runtime | Runs inside the task's **single** `environment/Dockerfile` image (canonical **TB2**) |
| Test overlay | **Harbor overlays `tests/`** at verification time |
| No `tests/Dockerfile` | There is no separate tests image |
| pytest location | Install verifier deps (pytest, pytest-json-ctrf) in `environment/Dockerfile` |

### 2.5 June 24, 2026 — Taxonomy: pre-seeded vs fellow-set

| Field | Who sets it | Notes |
|-------|-------------|-------|
| `category` | **Dynamo team (pre-seeded)** | Do **not** modify |
| `subcategory` | **Dynamo team (pre-seeded)** | Do **not** modify |
| `task_objective` | **Contributor (fellow-set)** | Lowercase snake_case from `.dynamo/diversity-taxonomy.toml` |
| `artifact_type` | **Contributor (fellow-set)** | Lowercase snake_case from `.dynamo/diversity-taxonomy.toml` |

### 2.6 June 24, 2026 — Instruction length and structured output

| Rule | Detail |
|------|--------|
| `instruction.md` length | **1,500-token limit** |
| Structured output schema | Document **directly in the prompt** or in a **referenced specification file** |
| Removed | Separate `structured-output` line in `task.toml` / workflow |

### 2.7 June 24, 2026 — Common errors and self-check

New content on the [Errors & Examples (Pitfalls)](https://project-dynamo.learn.joinhandshake.com/pitfalls) page:

- **"Common errors and examples"** — four worked failure cases, each with:
  - Problem description
  - Code excerpts
  - Guidance on how to avoid the issue
- **"Before you submit: quick self-check"** — five-item checklist (see §9)

### 2.8 June 24, 2026 — Proposal guidance

- Added a **fourth justification question** (with accompanying callout) in the **Proposal** workflow step (step 2)

### 2.9 2-Day Push Incentive

During the focused 2-day push:

- **+$50** for every task that reaches the **RTD layer**
- Requires passing all platform checks including Pass@2 and Pass@5

---

## 3. Evaluation Rules (Quick Reference)

```
                    ┌──────────────────────────────────────┐
                    │  Valid failure = agent wrong,        │
                    │  verifier correct. NOT: timeout,     │
                    │  infra, or misalignment.             │
                    └──────────────────────────────────────┘

  Local          Platform         Stage 1           Stage 2          RTD
  checks    →    submit      →    Pass@2       →    Pass@5      →   layer
  oracle/nop                      2 trials          5 trials         (+$50)
  self-check                      ≥ 1 failure       ≥ 3 failures
                                  (genuine)         (genuine)

  Too easy (Pass@5): 0–2 valid failures → ACCEPTED on difficulty
  Too easy (Pass@5): 3–5 valid failures → REJECTED
  Sweet spot: agent fails 3+ times but oracle always passes
```

| Stage | Trials | Requirement | Too easy? |
|-------|--------|-------------|-----------|
| Pass@2 | 2 | ≥ 1 valid failure | Blocked if 0 failures (can't proceed) |
| Pass@5 | 5 | ≥ 3 valid failures for difficulty bar | 0–2/5 accepted; 3–5/5 rejected |

---

## 4. Current Task Snapshot

### 4.1 What the task does today

Parse a 6-line Apache-style access log at `/app/access.log` and write `/app/report.json` with:

| Field | Rule |
|-------|------|
| `total_requests` | Count of non-empty log lines |
| `unique_ips` | Distinct client IPs (first field per line) |
| `top_path` | Most frequent request path from quoted HTTP request; any tie-break OK |

### 4.2 Fixed dataset (`environment/access.log`)

| Metric | Value |
|--------|-------|
| Non-empty lines | 6 |
| Unique IPs | 3 (`192.168.0.1`, `192.168.0.2`, `10.0.0.5`) |
| Path counts | `/index.html` × 3, `/about.html` × 2, `/api/login` × 1 |
| Expected `top_path` | `/index.html` |

### 4.3 Local validation status

| Check | Result | Notes |
|-------|--------|-------|
| Oracle agent | **PASS** (reward 1.0) | 4/4 pytest tests pass |
| Nop agent | **FAIL** (reward 0.0) | Verifier rejects empty/wrong output |
| Single `environment/Dockerfile` | **OK** | pytest baked in; no `tests/Dockerfile` |
| `[verifier].environment_mode` unset | **OK** | Per §2.4 |
| `avg_at_8` absent | **OK** | Removed per §2.2 |
| `instruction.md` token limit | **OK** | ~15 lines, well under 1,500 tokens |
| JSON schema in prompt | **OK** | Fields documented inline per §2.6 |
| `category` / `subcategory` in `task.toml` | **FIX** | Should not be set by contributor per §2.5 |

### 4.4 Required layout (canonical TB2)

```
log-report/
├── instruction.md          # Agent prompt (≤ 1,500 tokens)
├── task.toml               # Canonical block — see §12
├── environment/
│   ├── Dockerfile          # Single image; verifier deps here
│   └── access.log          # Fixed input dataset (never in image: tests/, solution/)
├── solution/
│   ├── solve.sh            # Oracle entrypoint
│   └── solve.py            # Reference implementation
└── tests/
    ├── test.sh             # Verifier entrypoint (Harbor overlays at runtime)
    └── test_outputs.py     # Pytest assertions
```

**Never put in the Docker image:** `tests/`, `solution/` (Harbor mounts/overlays these).

---

## 5. Gap Analysis

### 5.1 Blockers

| # | Issue | Severity | Action |
|---|-------|----------|--------|
| 1 | **Task is too easy** for Pass@5 | **Critical** | Increase difficulty so GPT-5.4 fails ≥ 3/5 with genuine mistakes (ideally 3–4/5, not 5/5) |
| 2 | `category` / `subcategory` in `task.toml` | Medium | Remove — pre-seeded by Dynamo (§2.5) |
| 3 | Ambiguous tie-break ("choose any one") | Low | Use deterministic rule before expanding scope |

### 5.2 Already aligned

- Canonical `task.toml` block structure (§2.2)
- Verifier runs inside task Docker image; Harbor overlays `tests/` (§2.4)
- Instruction success criteria map 1:1 to pytest tests
- No hidden test requirements beyond the prompt
- Structured output schema in `instruction.md` (§2.6)

### 5.3 Risk: instruction ↔ verifier misalignment

Every rule in `instruction.md` **must** have a matching test. See §10 for the four common error patterns from the Pitfalls page.

---

## 6. Difficulty Redesign Plan

The current 6-line log is trivial for GPT-5.4 extra-high. Target: **3+ genuine failures in 5 trials** while oracle passes 100%.

### 6.1 Recommended scope expansion

Expand `/app/report.json` with subtle parsing rules:

| Field | Proposed rule | Why agents fail |
|-------|---------------|-----------------|
| `total_requests` | Non-empty lines only | Miscount blank or "invalid" lines |
| `unique_ips` | Distinct first-field IPs, including IPv6 | IPv6 breaks naive `split()[0]` |
| `top_path` | Most frequent path after **normalization** | Miss normalization steps |
| `status_4xx_count` | HTTP status codes 400–499 | Wrong column for status code |
| `total_bytes` | Sum of response-size field | Column-position errors |
| `excluded_health_checks` | Lines with `GET /health ` excluded from path tally | Include/exclude wrong lines |

### 6.2 Recommended log additions (~30–40 lines)

- IPv4 and IPv6 client addresses
- Query strings: `/search?q=foo` → normalize to `/search`
- Trailing slashes: `/about/` vs `/about`
- `GET /health HTTP/1.1` lines (excluded from path frequency)
- Blank lines (explicit skip/count rule)
- Mixed HTTP methods
- 4xx and 5xx status codes
- At least one tie with a **deterministic** tie-break rule

### 6.3 Tie-break rule (must be explicit)

Replace "choose any one" with e.g.:

> If multiple paths share the highest count, choose the **lexicographically smallest** path.

### 6.4 Path normalization spec (add to `instruction.md`)

```
Path normalization (apply before counting frequency):
1. Extract path from quoted request: METHOD <path> HTTP/x.x
2. Remove query string (everything from ? onward)
3. Remove trailing slash unless path is exactly "/"
4. Do not lowercase
```

---

## 7. File-by-File Change Checklist

### 7.1 `instruction.md`

- [ ] All output fields with types and precise rules
- [ ] Path normalization, exclusions, malformed-line handling
- [ ] Deterministic tie-break rule
- [ ] Numbered success criteria, 1:1 with tests
- [ ] Stay under **1,500 tokens** (§2.6)
- [ ] No ambiguous language ("approximately", "usually", "etc.")

### 7.2 `environment/access.log`

- [ ] Expanded fixed dataset with edge cases (§6.2)
- [ ] Manually compute all expected values (§8)

### 7.3 `environment/Dockerfile`

- [ ] Single image only — no `tests/Dockerfile` (§2.4)
- [ ] `COPY access.log /app/access.log`
- [ ] Pin pytest + pytest-json-ctrf
- [ ] Pin base image digest

### 7.4 `solution/solve.py` + `solution/solve.sh`

- [ ] Reference solution matches instruction exactly
- [ ] `solve.sh` remains thin wrapper

### 7.5 `tests/test_outputs.py` + `tests/test.sh`

- [ ] One test per numbered success criterion
- [ ] Hardcoded expected values OK for fixed dataset
- [ ] `test.sh`: pytest → `/logs/verifier/reward.txt`

### 7.6 `task.toml`

- [ ] Remove `category` and `subcategory` (§2.5)
- [ ] Set only `task_objective` and `artifact_type` from taxonomy
- [ ] Leave `[verifier].environment_mode` **unset** (§2.4)
- [ ] Do **not** add `avg_at_8` (§2.2)
- [ ] Match canonical block in §12

Current fellow-set metadata:

```toml
task_objective = ["transform", "generate"]
artifact_type = ["text_or_log_file", "generated_output_artifact"]
```

---

## 8. Expected-Value Worksheet

Compute from final `access.log` before writing tests:

| Field | Computed value | Verified by |
|-------|----------------|-------------|
| `total_requests` | ___ | `test_total_requests` |
| `unique_ips` | ___ | `test_unique_ips` |
| `top_path` | ___ | `test_top_path` |
| _(each new field)_ | ___ | _(matching test)_ |

**Tip:** One-off script → print expected JSON → populate tests and cross-check oracle.

---

## 9. Pre-Submit Self-Check (5 items)

From Dynamo [Pitfalls — Before you submit](https://project-dynamo.learn.joinhandshake.com/pitfalls):

| # | Check | Status |
|---|-------|--------|
| 1 | Every numbered success criterion in `instruction.md` has exactly one corresponding test | ☐ |
| 2 | Every test assertion maps back to a stated criterion (no hidden requirements) | ☐ |
| 3 | Output schema (field names, types, rules) fully specified in prompt or referenced spec | ☐ |
| 4 | Fixed dataset → deterministic values; oracle passes 100% | ☐ |
| 5 | Task hard enough: Pass@2 ≥ 1/2 failures; Pass@5 ≥ 3/5 failures (genuine) | ☐ |

---

## 10. Common Errors (Pitfalls Page)

Four worked failure patterns — avoid these in `log-report`:

### Error 1 — Hidden test requirements

**Problem:** Tests assert behavior never stated in `instruction.md`.

**Example:** Test checks JSON key ordering or field presence not listed in the prompt.

**Fix:** Every assertion must trace to a numbered success criterion.

### Error 2 — Untested prompt requirements

**Problem:** `instruction.md` requires something tests never verify.

**Example:** Prompt says "exclude health-check paths" but no test checks exclusion logic.

**Fix:** Add criterion + test together when adding any rule.

### Error 3 — Ambiguous success criteria

**Problem:** Agent and verifier can interpret the prompt differently.

**Example:** "Break ties by choosing any one path" — verifier picks one deterministically, agent picks another.

**Fix:** Use deterministic rules (lexicographic tie-break, explicit normalization steps).

### Error 4 — Instruction/verifier misalignment (blocking)

**Problem:** Failures are caused by spec mismatch, not agent capability.

**Example:** Prompt says count all lines; test expects non-empty only.

**Fix:** Treat as **blocking** — does not count toward Pass@2/Pass@5 quota. Align instruction, solution, and tests before resubmitting.

---

## 11. Local Validation Commands

```bash
# Oracle must pass
harbor run --agent oracle --path .

# Nop must fail
harbor run --agent nop --path .

# Optional: build environment image
docker build -t log-report-env ./environment
```

| Agent | Expected reward |
|-------|-----------------|
| oracle | `1.0` |
| nop | `0.0` |

---

## 12. Submission Pipeline

```
┌─────────────────┐
│  Local checks   │  oracle PASS, nop FAIL, §9 self-check
└────────┬────────┘
         ▼
┌─────────────────┐
│  Platform PR    │  Push + open PR (see Submit workflow)
│  + checks       │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Stage 1        │  Pass@2 — GPT-5.4 + Terminus-2, extra-high
│  Pass@2         │  2 trials → ≥ 1 genuine failure
│                 │  Includes LLM run analysis
└────────┬────────┘
         │ pass
         ▼
┌─────────────────┐
│  Stage 2        │  Pass@5 — 5 trials → ≥ 3 genuine failures
│  Pass@5         │  0–2/5 failures = accepted difficulty
│                 │  3–5/5 failures = rejected (too easy)
└────────┬────────┘
         │ pass
         ▼
┌─────────────────┐
│  RTD layer      │  +$50 if during 2-day push window
└─────────────────┘
```

**Misalignment at any stage:** fix instruction/tests/solution — blocking, does not count.

**Too easy (Pass@5):** fewer than 3 failures in 5 trials → return to §6.

---

## 13. Implementation Order

| Step | Task | Done |
|------|------|------|
| 1 | Finalize field spec + normalization rules | ☐ |
| 2 | Build new `access.log` (30–40 lines) | ☐ |
| 3 | Fill expected-value worksheet (§8) | ☐ |
| 4 | Update `instruction.md` (≤ 1,500 tokens) | ☐ |
| 5 | Update `solution/solve.py` | ☐ |
| 6 | Update `tests/test_outputs.py` | ☐ |
| 7 | Clean `task.toml` — remove pre-seeded fields (§2.5) | ☐ |
| 8 | Run oracle + nop locally (§11) | ☐ |
| 9 | Run self-check (§9) | ☐ |
| 10 | Submit → Pass@2 → Pass@5 → RTD | ☐ |

---

## 14. task.toml Target State

Canonical block — contributor edits noted:

```toml
artifacts = ["/app/report.json"]

[task]
name = "dynamo/log-report"
description = "Parse an Apache-style access log into a JSON summary report with normalization rules."

[metadata]
# PRE-SEEDED by Dynamo — do NOT set:
#   category, subcategory

# FELLOW-SET — contributor sets from .dynamo/diversity-taxonomy.toml:
task_objective = ["transform", "generate"]
artifact_type = ["text_or_log_file", "generated_output_artifact"]

# Fixed-dataset / platform fields (set per workflow guidance):
expert_time_estimate_hours = 0.5
model_tested = "GPT-5.4"
agent_tested = "Terminus-2"
difficulty_explanation = "..."
solution_explanation = "..."
verification_explanation = "..."

[verifier]
timeout_sec = 120.0
# environment_mode — LEAVE UNSET

[agent]
timeout_sec = 120.0

[environment]
build_timeout_sec = 600.0
cpus = 1
memory_mb = 2048
storage_mb = 10240
gpus = 0
allow_internet = true
mcp_servers = []
```

**Do not include:** `avg_at_8`, `environment_mode`, separate structured-output line.

---

## 15. Proposal Step Reminder

Workflow step 2 (Proposal) now includes a **fourth justification question**. Prepare answers for:

1. Why this task is a good fit for the category
2. What makes it gradable / verifiable
3. Why the model will struggle (difficulty justification)
4. *(New)* Fourth justification — see platform callout in Proposal step

---

## 16. Useful Platform Links

| Page | URL |
|------|-----|
| Updates | https://project-dynamo.learn.joinhandshake.com/updates |
| Errors & Examples (Pitfalls) | https://project-dynamo.learn.joinhandshake.com/pitfalls |
| Pass@ & Timeouts | https://project-dynamo.learn.joinhandshake.com/submit/pass-at |
| Final checklist | https://project-dynamo.learn.joinhandshake.com/submit/checklist |
| How to stump the model | https://project-dynamo.learn.joinhandshake.com/stump-the-model |
| Task.toml reference (step 9) | https://project-dynamo.learn.joinhandshake.com/workflow/step-9 |
| Calibration loop | https://project-dynamo.learn.joinhandshake.com/setup/single-task |

---

## 17. Open Decisions

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Field scope | Minimal vs full (§6.1) | Full — needed for Pass@5 |
| Log size | 20 vs 40 lines | 30–40 lines |
| Tie-break | Lexicographic vs first-seen | Lexicographic |
| Health-check exclusion | Yes / No | Yes — good failure mode |
| Target failure rate | 3/5 vs 4/5 | Aim for 3–4/5 (≥ 3 required; 5/5 = too easy) |

---

## 18. Next Action

**Start with Steps 1–3 (§13):** lock field spec → build log → compute expected values → then instruction → solution → tests.

Current task verdict: **structurally ready, difficulty not ready** — 6-line log will likely score 0–2/5 failures (accepted band) but risks failing Pass@2 if the model always succeeds.
