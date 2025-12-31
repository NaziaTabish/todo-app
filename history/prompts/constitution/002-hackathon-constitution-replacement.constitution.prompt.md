---
id: 002
title: Hackathon Constitution Replacement
stage: constitution
date: 2025-12-31
surface: agent
model: claude-sonnet-4.5-20250929
feature: none
branch: master
user: Syed
command: /sp.constitution
labels: ["constitution","hackathon","spec-driven","phases"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md (MAJOR update v1.0.0→v2.0.0 with 8 new principles, 5-phase tech stack, hackathon constraints)
tests:
  - Constitution validation: No unexplained placeholders, testable principles, phase progression rules, governance complete
---

## Prompt

"Project: Hackathon II - Todo App Evolution

Core principles:
- Spec-Driven Development (NON-NEGOTIABLE) - All code must be generated via Claude Code from specs, no manual coding
- Phase-Based Evolution - 5 phases in order: Console → Web → Chatbot → Local K8s → Cloud
- Monorepo Organization - Single repository with frontend/backend separation
- Clean Code Standards - Descriptive names, docstrings, proper structure
- WSL 2 for Windows - Use WSL 2 for all development commands
- Security & Secrets - Environment variables, no hardcoded credentials
- AI-First Development - OpenAI Agents SDK, MCP tools for conversational interface
- Cloud-Native Architecture - Docker, Kubernetes, event-driven with Kafka and Dapr

Key standards:
- All code changes must map back to spec/plan/tasks
- Use Claude Code Subagents for reusable intelligence
- Technology stack fixed per phase
- Better Auth with JWT for frontend/backend communication
- Neon PostgreSQL for database (Phase II+)
- OpenAI ChatKit for chatbot UI (Phase III+)

Technology Stack by Phase:
Phase I: Python 3.13+, uv, Claude Code, Spec-Kit Plus, in-memory storage
Phase II: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth with JWT
Phase III: OpenAI ChatKit, OpenAI Agents SDK, Official MCP SDK, stateless chat endpoint
Phase IV: Docker, Minikube, Helm charts, kubectl-ai, Kagent, Gordon (Docker AI)
Phase V: Kafka (Redpanda/Strimzi), Dapr, DigitalOcean DOKS/Azure AKS/Google GKE, event-driven architecture

Constraints:
- No manual coding allowed - must use spec-driven workflow
- All phases must be completed in order
- WSL 2 required for Windows users
- Demo video under 90 seconds for each phase submission

Success criteria:
- All phases completed with working applications
- Specs/plan/tasks traceable for every feature
- Deployed applications at each phase
- Demo videos demonstrating features"
cqh-pxjr-azr

## Response snapshot

Successfully replaced constitution at `.specify/memory/constitution.md` with hackathon-focused governance (v2.0.0, MAJOR bump due to complete domain change):

1. **Eight Core Principles**:
   - Spec-Driven Development (NON-NEGOTIABLE): All code via Claude Code, mandatory spec→plan→tasks→code traceability
   - Phase-Based Evolution: 5 phases in strict order (Console→Web→Chatbot→Local K8s→Cloud)
   - Monorepo Organization: Single repo with frontend/backend separation
   - Clean Code Standards: Descriptive names, docstrings, proper structure
   - WSL 2 for Windows: All development commands in WSL 2 environment
   - Security & Secrets: Environment variables only, no hardcoded credentials
   - AI-First Development: OpenAI Agents SDK, MCP SDK, ChatKit, Claude Code Subagents
   - Cloud-Native Architecture: Docker, Kubernetes, Kafka, Dapr from Phase IV

2. **Key Standards Section**:
   - Development Workflow: Traceability requirement, Claude Code usage, review process, 90s demo videos
   - Technology Standards: Fixed stacks per phase, Better Auth, Neon PostgreSQL, ChatKit, Agents SDK, Docker, K8s, Kafka
   - Code Quality Standards: Naming, documentation, structure, testing, error handling

3. **Technology Stack by Phase** (5 detailed phases):
   - Phase I (Console): Python 3.13+, uv, Claude Code, in-memory storage
   - Phase II (Web): Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth JWT
   - Phase III (Chatbot): OpenAI ChatKit, Agents SDK, MCP SDK, stateless endpoint
   - Phase IV (Local K8s): Docker, Minikube, Helm charts, kubectl-ai, Kagent, Gordon
   - Phase V (Cloud): Kafka (Redpanda/Strimzi), Dapr, DOKS/AKS/GKE, event-driven

4. **Project Constraints Section**:
   - Scope: Phase order mandatory, monorepo, 90s demo videos, hackathon timeline
   - Process: No manual coding, WSL 2 required, env variables, artifact traceability
   - Technical: Fixed stacks, cloud-native (IV+), event-driven (V), Better Auth JWT (II+)

5. **Governance Section**:
   - Amendment Procedure: Documented changes, unanimous approval for Spec-Driven Development, phase impact analysis
   - Versioning Policy: MAJOR/MINOR/PATCH semantic rules
   - Compliance Review: Pre-phase checks, spec-driven validation, technology audit, security review, clean code check, demo verification
   - Principle Supremacy: Constitution overrides conflicting guidance; Spec-Driven Development NON-NEGOTIABLE

Version: 2.0.0 (MAJOR - complete replacement)
Last Amended: 2025-12-31
Ratification Date: TODO pending project kickoff

Sync Impact Report appended showing:
- 6 principles removed (academic research paper focus)
- 8 principles added (hackathon/software development focus)
- 5-phase technology stack documentation
- Templates: plan and tasks compatible; spec-template flagged for potential phase progression enhancements
- TODOs for ratification date and spec-template enhancement

## Outcome

- ✅ Impact: Constitution successfully transformed from academic research paper to hackathon software development project with comprehensive 5-phase architecture and spec-driven workflow
- 🧪 Tests: Constitution validation passed - no unexplained placeholders, all principles declarative and testable, phase progression rules clear, governance section complete with amendment procedures
- 📁 Files: `.specify/memory/constitution.md` completely replaced with 218 lines covering 8 principles, key standards, 5-phase tech stack, constraints, and governance framework
- 🔁 Next prompts: User may proceed with `/sp.specify` to create spec for Phase I (Console Application) or overall project specification
- 🧠 Reflection: Constitution captures hackathon constraints well. Key strength is the clear phase progression with locked technology stacks, enabling focused development per phase. Spec-Driven Development as NON-NEGOTIABLE principle ensures traceability throughout hackathon timeline. 90s demo constraint reinforces pace. Potential improvement: spec-template could include phase-specific acceptance criteria sections.

## Evaluation notes (flywheel)

- Failure modes observed: None - all placeholders resolved or documented as intentional TODOs
- Graders run and results (PASS/FAIL): Constitution structure validation PASS; Principle testability PASS; Phase progression rules clear PASS; Governance completeness PASS
- Prompt variant (if applicable): N/A - standard /sp.constitution workflow with complete project replacement
- Next experiment (smallest change to try): N/A - constitution is complete and valid for hackathon use case; if spec-template enhancement is pursued, add phase progression validation checkpoints
