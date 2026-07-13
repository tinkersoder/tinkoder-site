# CLAUDE.md — Tinkoder

Instructions for any AI agent (Claude Code or otherwise) working in this repository. These override default behavior — follow them exactly.

## Background (from the second-brain vault)

Canonical source of truth for everything below: `/mnt/ssdintenso/projects/claude/` (Joona's second-brain vault, mirrored as Claude Project files). If anything here conflicts with the vault, the vault wins — update this file to match rather than the vault.

- **Owner:** Joona Söder, 35, Tampere, Finland. Corporate day job (M365/Power Automate), building a portfolio of self-employed income streams to **exit corporate employment before summer 2027**. Target: 2 000 €/mo net minimum, 3 000 €/mo goal, across the whole portfolio — Tinkoder does not need to cover this alone.
- **Tinkoder** is Joona's technical-solutions business (3D printing, CAD, electronics prototyping, smart-home) and is likely to become the main Oy brand. Services: 3D printing/CAD/spare parts, electronics prototyping/embedded, Home Assistant/smart-home, product development/small-batch, repairs/reverse engineering, technical consulting.
- **Proven demand:** repeated miniatures & board-game-insert print jobs (strongest signal), one WLED lighting install (~100 €). Everything else on the services page is unproven — weight suggestions toward the proven line before the aspirational ones.
- **Legal status:** all revenue so far is off-the-books. An **Oy (osakeyhtiö)** is the decided entity (not toiminimi) but not yet founded — timing is an open founder decision (❓, see `gaps.md` / `decisions.md` in the vault). Do not treat Tinkoder as having a legal entity yet unless the vault says otherwise.
- **Brand guide:** Nordic workshop — calm, precise, quietly playful, technical but never intimidating ("let's see what's possible" not "no"). Tagline FI: *"Me rakennamme sen, mitä ei ole olemassa."* / EN: *"We build what doesn't exist yet."* Palette: Birch paper `#F6F7F4`, Spruce `#1B5E4A`, Signal amber `#E9A13B`, Ink `#182420`, Night `#0F1513`. Fonts: Bricolage Grotesque (display), Instrument Sans (body), Spline Sans Mono (spec/labels, CAD-motif). Preserve this identity in any content or design change.
- **Local compute:** Arch Linux desktop (NVIDIA GTX 1660 Ti, 6 GB VRAM, NVENC) running Ollama (Qwen3 4B daily driver, bge-m3 embeddings); TrueNAS box with Docker/Dockge, n8n, Qdrant. Assume reachable, use them per the compute-economy rules below.
- **Working style:** practical, hands-on, low-cost, self-hosted/open-source preferred, prototype-grade code is fine (Joona iterates himself). Skepticism and tradeoff analysis are wanted, not cheerleading. Never invent numbers or answers for anything marked ❓ in the vault — leave it open or ask.

---

## 1. Context you must respect

**Website:** tinkoder.fi is a live, bilingual (Finnish/English) static site deployed on Cloudflare Pages, with contact forms via Web3Forms, DNS at Domainhotelli, and email via Purelymail. Do not break the live deployment. Any change must keep both language versions in sync.

**Business:** Solo founder plus a remote business partner (Singapore). Finnish VAT (ALV), Finnish invoicing conventions (viitenumero reference numbers, Finvoice-friendly data where practical), EUR as base currency. Standing rules: one venture at a time, revenue routes through the Finnish side, nothing that creates live support obligations.

**Local compute available:** an Arch Linux machine with an NVIDIA GTX 1660 Ti (6 GB VRAM, NVENC-capable) running Ollama (Qwen3 4B daily driver, bge-m3 embeddings), plus a TrueNAS box with Docker/Dockge, n8n, and Qdrant. Assume these are reachable and use them.

**Philosophy:** Practical, low-cost, self-hostable, automation-first. No enterprise bloat. Prefer static + serverless over servers that need babysitting.

## 2. Compute economy — CPU/GPU over tokens

You are running a long unattended session. Spend local compute, not context tokens. Concretely:

- **Run code instead of reasoning about code.** When you need to know what data looks like, what a function returns, or whether something works — write a small script and execute it. Read its output, not the whole codebase.
- **Targeted reads only.** Use grep/ripgrep, head, and line-range reads to find what you need. Never dump entire large files or directories into context when a search would answer the question. Never re-read files you haven't changed.
- **Edit with diffs, not rewrites.** Modify files with targeted patches. Never regenerate a large file to change ten lines.
- **Delegate bulk LLM work to local models.** Anything high-volume and tolerant of a small model — story scoring, classification, tagging, summarizing scraped posts, embedding — goes to Ollama (Qwen3 4B / bge-m3) via its API, called from scripts you write. Reserve your own generation for design decisions, code, and final-quality prose.
- **Delegate media work to the GPU.** TTS (Kokoro), video encoding (FFmpeg with NVENC), image optimization — all run as local jobs. You write the script, launch it, check the exit code and a sample of the output. You do not narrate or babysit long-running jobs; start them, work on something else, poll periodically.
- **Batch and cache.** Batch API calls, cache intermediate results to disk (JSON/SQLite), and make every pipeline stage idempotent and resumable so reruns are cheap.
- **Terse working style.** Keep your own intermediate commentary minimal. Verbosity goes into commit messages, docs, and the end-of-session reports — not into thinking out loud.

*(Sections 3–7 are reserved for future capability/scope rules — not yet defined. Don't infer content for them.)*

## 8. Repository & Git Workflow

Apply this to every repo you touch:

- **Small, logical commits.** One concern per commit.
- **Auto-generated commit messages** following Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `chore:`, `test:`), where the body summarizes what changed and why based on the actual diff — never generic messages like "update files."
- **Push to GitHub after each logical unit of work** passes its tests. Never push broken states to the default branch; use a feature branch if work is incomplete, and push those branches too so nothing is lost overnight.
- **Checkpoint frequently.** During a long unattended run, commit and push at least at every completed sub-task. Work that only exists in your context is work that can be lost.
- **Keep `.gitignore` correct**; never commit secrets, API keys, or generated artifacts that can be rebuilt (rendered videos, TTS audio, STL exports — commit the generators, not the output, unless the output is small and canonical).
- **Keep each repo's README accurate** as a side effect of your work.

## 9. Overnight Operation Protocol

- **Never block on a question.** If a decision is needed, choose the safest reasonable default, record the decision and its alternatives in `DECISIONS.md`, and continue.
- **Prioritize by value density:** (1) fix anything broken, (2) finish half-done work, (3) tasks from `NEXT_STEPS.md`, (4) new capabilities from §4–§7, (5) refactoring and polish.
- **Risk-order the night:** do changes touching the live site or destructive migrations early while budget remains to verify and fix; leave low-risk polish for last.
- **Long jobs run in the background.** Launch renders/encodes/test suites detached (`nohup`/`&`, logs to file), continue other work, poll results.
- **Watch your context.** When context is getting long, immediately update `SESSION_PLAN.md`, `NEXT_STEPS.md`, and `DECISIONS.md`, commit, and push — then continue with whatever room remains. The written state, not your context, is the source of truth.
- **If a task fails twice for the same reason, stop retrying:** document the failure and blocker in `NEXT_STEPS.md` and move to the next task.

## 10. Engineering Standards

- **Code quality:** Refactor poor code, remove duplication, improve naming, increase modularity and maintainability.
- **Testing:** Write tests for everything you create; add tests around existing code before refactoring it. Run tests locally — they are cheap; regressions are not.
- **Error handling:** Handle edge cases explicitly; fail loudly in development, gracefully in production.
- **Logging:** Meaningful, structured logging where it aids debugging — no noise. Long-running pipeline stages log progress to files.
- **Configuration:** Environment variables for anything deployment-specific or secret. No hardcoded values, URLs, or credentials.
- **Security:** Review all business functionality for security issues — especially the admin GUI (authentication, no exposed write endpoints), form handling, scraped-content handling, and anything touching customer or financial data. Customer data stays local/self-hosted wherever possible (GDPR-conscious by default).
- **Documentation:** Every module gets documentation, updated in the same commit as the code it describes.

## 11. Hard Rules

- Never remove working functionality.
- Never break the live tinkoder.fi deployment.
- Preserve backwards compatibility whenever practical.
- Both site languages must always stay in sync.
- No paid dependencies and no new external accounts without flagging it in `NEXT_STEPS.md` as a founder decision.
- Never publish content to social platforms or send real emails during an unattended run — build up to the final send/upload step and gate it behind a config flag.
- Never commit or log secrets.
- Do not start new ventures; do not ask for confirmation; when a task finishes, autonomously pick the next highest-value one.
