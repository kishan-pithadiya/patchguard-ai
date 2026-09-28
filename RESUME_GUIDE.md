# PatchGuard AI: Resume & Technical Interview Guide (DevSecOps / SRE Focus)

Use this guide to effectively position **PatchGuard AI** on your resume and in technical interviews. This project provides strong technical diversity alongside your **Multi-Agent Clinica** healthcare project.

---

## 🎯 Portfolio Diversity Strategy: How These Two Projects Complement Each Other

| Aspect | Project 1: Multi-Agent Clinica | Project 2: PatchGuard AI (This Project) |
| :--- | :--- | :--- |
| **Domain** | Healthcare & Clinical Intelligence | DevSecOps, SRE & Platform Reliability |
| **Primary Value** | Clinical decision support & medical data workflows | Zero-downtime automated incident remediation & self-healing |
| **Core Architecture** | Clinical RAG & medical multi-agent dialogs | AST call-graph blast-radius analysis & CI/CD quality gates |
| **Safety Invariant** | Clinical accuracy & hallucination mitigation | Sandboxed subprocesses, branch coverage (≥70%), and atomic Git rollback |
| **Target Roles** | GenAI Engineer, Applied AI Scientist | SRE, DevSecOps Engineer, Backend Platform Engineer |

Recruiters immediately see that you can build both **high-stakes vertical applications (healthcare)** and **low-level systems infrastructure (DevSecOps/developer tooling)**!

---

## 📄 Resume Bullet Points (Ready to Copy-Paste)

### Option 1: DevSecOps / SRE (Site Reliability Engineer) Focus
> **PatchGuard AI | Autonomous DevSecOps & Self-Healing SRE Remediation Engine** *(Python 3.12, CrewAI, AST, Pytest, Git, Streamlit)*
> - Engineered an autonomous DevSecOps remediation engine utilizing specialized **CrewAI** agents to triage production crashes, isolate root causes, and synthesize verified bug and security patches.
> - Implemented an AST call-graph dependency analyzer (`ast.parse`) that maps function caller-callee hierarchies to compute regression blast radii before patch deployment.
> - Architected a self-healing patch loop with sandboxed subprocess execution, Git savepoints, and automated atomic rollback if patches fail quality thresholds.
> - Enforced multi-tiered CI/CD quality gates requiring 100% test pass, branch coverage floor (≥70%), Ruff AST linting, and Ty static type integrity.

### Option 2: Backend Platform / AI Infrastructure Focus
> **PatchGuard AI | Distributed Incident Remediation & Self-Healing Engine** *(Python, CrewAI, Git CLI, Subprocess Sandboxing, AST)*
> - Designed a concurrent incident remediation pipeline with specialized CrewAI cognitive agents (SRE Architect, Backend Specialist, Reviewer, Regression Tester, Root-Cause Debugger).
> - Built a deterministic role-priority conflict resolution engine that mediates simultaneous file modifications from parallel agents, eliminating race conditions.
> - Integrated runtime token economics and budget guardrails (`max_tokens`, `max_cost_usd`) with real-time spend estimation across OpenAI, Google Gemini, and local Ollama models.
> - Produced machine-readable audit replay traces (`AUDIT_REPLAY.json`) capturing tool latencies, AST impact graphs, and Git commit shas for compliance post-mortems.

---

## 🎤 2-Minute Elevator Pitch (For Recruiter / Hiring Manager Screens)

> *"Alongside my Multi-Agent Clinica project in healthcare, I built **PatchGuard AI** to solve a critical problem in DevSecOps and Site Reliability Engineering: mean time to remediation (MTTR) for software bugs and security advisories.*
>
> *Traditional automated patching tools often cause silent regressions or break adjacent systems. To prevent that, PatchGuard uses an AST-driven code intelligence engine that maps caller-callee dependencies across Python files and computes the exact blast radius of any code change.*
>
> *It then deploys a team of specialized **CrewAI** agents—an SRE Architect plans the remediation, specialized coders write the patch in parallel, and a Test Engineer generates regression tests. What makes it production-safe is its closed-loop self-healing: code must pass a strict quality gate with a 70% coverage floor, Ruff linting, and Ty type checks. If any gate fails, the system automatically triggers an atomic Git rollback to the previous green savepoint. It runs fully offline with Ollama or against cloud LLM APIs."*

---

## 🧠 Technical Deep-Dive Interview Questions & Answers

### Q1: How does PatchGuard AI differ from standard AI code assistants like GitHub Copilot?
**Answer:**
- Copilot operates as an inline, turn-by-turn autocompletion tool without repository-wide dependency verification or execution safety guarantees.
- PatchGuard AI is an **autonomous remediation system**: it ingests stack traces, analyzes the AST call graph to determine the blast radius, writes multi-file patches, executes real test suites in sandboxed subprocesses, validates coverage and linting thresholds, and commits or rolls back using Git. It operates as an autonomous junior SRE rather than an autocomplete plugin.

### Q2: How does the AST Blast-Radius Analysis work in `codeintel.py`?
**Answer:**
- In `src/patchguard/codeintel.py`, `build_call_graph()` parses all Python workspace files into Abstract Syntax Trees using Python's built-in `ast` module. It maps each defined function to all function and attribute calls made within its body (`Caller -> [Callees]`).
- When a patch modifies certain files, `analyze_change_impact()` traverses this graph in reverse to find every external function across the repository that calls the modified symbols.
- This gives the Regression Test Engineer an exact list of affected callers that need explicit test verification before the patch is accepted.

### Q3: How do you guarantee that automated patches don't corrupt the codebase?
**Answer:**
1. **Sandboxed Path Resolution (`safe_file`)**: All filesystem operations are verified against the workspace root with `dest.is_relative_to(workspace.resolve())` to stop directory traversal attacks (`../`).
2. **Command Allowlisting (`shell.py`)**: Subprocess execution allows only explicit commands (`git`, `pytest`, `python -m pytest`, `node`), rejecting shell injection attempts.
3. **Atomic Git Rollbacks (`workspace.py`)**: Before modifying files, PatchGuard creates a snapshot commit (`git_savepoint`). If the Root-Cause Debugger cannot achieve a green test pass within the retry budget (default 3), `git_rollback()` executes `git reset --hard` to restore the last known green commit.

### Q4: How do parallel CrewAI agents resolve merge conflicts?
**Answer:**
- In `src/patchguard/collab.py`, parallel specialist roles (Backend Security Coder, Frontend Specialist, Database Architect) generate proposed file writes concurrently in memory.
- `resolve_writes()` compares the modified paths. If multiple roles target the same file, PatchGuard applies a deterministic **role priority hierarchy** (e.g., Database Architect takes precedence on database models, Backend Specialist on backend routes). Overlapping writes are merged and recorded in `conflicts.log`.

### Q5: How is compliance and auditability handled for SRE post-mortems?
**Answer:**
- Every execution generates an immutable `AUDIT_REPLAY.json` via `export_audit_replay()`.
- It records the full event timeline, agent decisions, tool execution latencies, pytest pass/fail metrics, terminal log lines, and git commit hashes. This provides SRE teams with an auditable incident post-mortem report.
