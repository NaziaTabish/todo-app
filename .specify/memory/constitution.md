<!--
SYNC IMPACT REPORT
===================
Version Change: 1.0.0 → 2.0.0
Version Rationale: MAJOR - Complete replacement of constitution from research paper project to Hackathon II Todo App Evolution project with entirely different domain, principles, and constraints

Modified Principles: All principles completely replaced (6 removed, 8 added)
Removed Sections:
  - Accuracy Through Primary Source Verification
  - Academic Clarity
  - Reproducibility and Traceability
  - Rigorous Source Quality
  - Key Standards (academic citation format)
  - Project Constraints (academic scope)

Added Sections:
  - Spec-Driven Development (NON-NEGOTIABLE)
  - Phase-Based Evolution
  - Monorepo Organization
  - Clean Code Standards
  - WSL 2 for Windows
  - Security & Secrets
  - AI-First Development
  - Cloud-Native Architecture
  - Technology Stack by Phase (5 phases)
  - Project Constraints (hackathon-specific)

Template Updates:
  ✅ .specify/templates/plan-template.md - Constitution Check section remains compatible; no changes needed
  ⚠ .specify/templates/spec-template.md - Consider adding phase-specific requirements sections for 5-phase evolution
  ✅ .specify/templates/tasks-template.md - Compatible with spec-driven workflow; no changes needed

Follow-up TODOs:
  - TODO(RATIFICATION_DATE): Constitution initial ratification date not yet established - awaiting project kickoff
  - TODO(SPEC_TEMPLATE): Consider enhancing spec-template.md with phase progression requirements

Deferred Placeholders: None
-->

# Hackathon II - Todo App Evolution Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All code MUST be generated via Claude Code from specifications. Manual coding is prohibited. Every code change MUST map back to spec/plan/tasks artifacts. The development flow is: user intent → spec.md → plan.md → tasks.md → implementation → review. This traceability chain is mandatory for all work.

Rationale: Hackathon timeframe requires efficient, auditable development. Spec-driven workflow ensures traceability, prevents drift, and enables rapid iteration with full documentation.

### II. Phase-Based Evolution

The project MUST progress through 5 phases in strict order. Each phase builds on the previous phase's foundation. Phase sequence: Console (I) → Web (II) → Chatbot (III) → Local K8s (IV) → Cloud (V). No phase may be skipped or implemented out of sequence.

Rationale: Incremental complexity management. Each phase introduces specific technologies and architectural patterns. Sequential progression ensures foundational understanding before advanced topics.

### III. Monorepo Organization

Single repository structure MUST be maintained with clear frontend/backend separation. Phase I: console app only. Phase II+: backend/ and frontend/ directories. All artifacts (specs, code, deployment) live in one repository. Cross-cutting concerns (shared types, utilities) go in appropriate shared locations.

Rationale: Monorepo simplifies hackathon logistics, enables atomic commits across layers, and simplifies demo preparation. Clear separation prevents monolithic coupling.

### IV. Clean Code Standards

All code MUST follow clean code practices: descriptive names (no abbreviations except well-known), docstrings for public functions/classes, proper module structure (models, services, APIs, etc.), and consistent formatting. Code MUST be self-documenting through meaningful names and structure.

Rationale: Hackathon time pressure incentivizes shortcuts. Clean code standards maintain quality and readability despite rapid development pace. Good names and structure reduce cognitive load during demos.

### V. WSL 2 for Windows

Windows users MUST use WSL 2 for all development commands and shell operations. All commands in plans, tasks, and docs assume WSL 2 environment. Docker and Kubernetes tools MUST run in WSL 2 context. Cross-platform compatibility (macOS/Linux) should be maintained but Windows paths are WSL 2 normalized.

Rationale: Native Windows tooling incompatibility with container ecosystems. WSL 2 provides Linux environment without dual-boot. Ensures consistent toolchain across team members.

### VI. Security & Secrets

All secrets (API keys, database credentials, tokens) MUST be stored in environment variables or secrets management systems. No hardcoded credentials in code or configuration files. Secrets MUST never be committed to repository. Use .env files (in .gitignore) for local development.

Rationale: Security is non-negotiable even in hackathon context. Preventing credential leaks is essential for demo credibility and production readiness.

### VII. AI-First Development

AI capabilities MUST be considered core functionality, not add-ons. Use OpenAI Agents SDK for agent orchestration, Official MCP SDK for tool integration, and OpenAI ChatKit for chatbot UI. Conversational interfaces MUST be stateless and designed for extensibility. Claude Code Subagents MUST be used for reusable intelligence patterns.

Rationale: AI integration is the project's primary value proposition. Phase III specifically introduces AI chatbot, and principles must support AI-native architecture throughout.

### VIII. Cloud-Native Architecture

Cloud-native patterns MUST be used from Phase IV onward. Docker containers, Kubernetes orchestration, event-driven architecture with Kafka (Redpanda/Strimzi), and Dapr sidecars for microservices primitives. Infrastructure as code via Helm charts and kubectl-ai for K8s management.

Rationale: Modern deployment practices, scalability requirements, and event-driven patterns require cloud-native foundation. Phase IV/V constraints mandate these technologies.

## Key Standards

### Development Workflow Standards

- **Traceability Requirement**: Every feature MUST have spec.md → plan.md → tasks.md chain
- **Claude Code Usage**: All code generation via Claude Code; no manual editing of generated code unless correcting bugs
- **Review Process**: Each phase MUST pass acceptance before proceeding to next phase
- **Demo Deliverables**: 90-second demo video per phase submission showing working features

### Technology Standards

- **Fixed Stacks**: Technology choices are locked per phase; substitutions require documented rationale
- **Authentication**: Better Auth with JWT for frontend/backend communication (Phase II+)
- **Database**: Neon PostgreSQL for persistent storage (Phase II+)
- **Chatbot UI**: OpenAI ChatKit (Phase III+)
- **AI Integration**: OpenAI Agents SDK + Official MCP SDK (Phase III+)
- **Containerization**: Docker with multi-stage builds (Phase IV+)
- **Orchestration**: Minikube for local, cloud K8s for production (Phase IV+)
- **Event Streaming**: Kafka via Redpanda or Strimzi (Phase V)

### Code Quality Standards

- **Naming**: Descriptive names, avoid abbreviations (except GET, POST, etc.)
- **Documentation**: Docstrings for all public functions and classes
- **Structure**: Organize by layer (models, services, api/routes, tests)
- **Testing**: Tests MUST accompany new functionality (unit tests minimum, integration for critical paths)
- **Error Handling**: Proper error messages, logging, and graceful degradation

## Technology Stack by Phase

### Phase I: Console Application

- **Language**: Python 3.13+
- **Package Manager**: uv
- **Tools**: Claude Code, Spec-Kit Plus
- **Storage**: In-memory (Python data structures)
- **Architecture**: Single process, command-line interface
- **Output**: Executable CLI with CRUD operations

### Phase II: Web Application

- **Frontend**: Next.js 16+
- **Backend**: FastAPI (Python)
- **Database**: SQLModel + Neon PostgreSQL
- **Authentication**: Better Auth with JWT
- **Architecture**: REST API + React Server Components
- **Output**: Full-stack web application deployed locally

### Phase III: Chatbot Interface

- **Chat UI**: OpenAI ChatKit
- **AI Backend**: OpenAI Agents SDK
- **Tool Integration**: Official MCP SDK
- **API Endpoint**: Stateless chat endpoint
- **Architecture**: Conversational interface over existing backend
- **Output**: AI-powered todo assistant with natural language operations

### Phase IV: Local Kubernetes Deployment

- **Containers**: Docker with multi-stage builds
- **Orchestration**: Minikube
- **Package Management**: Helm charts
- **K8s AI**: kubectl-ai, Kagent, Gordon (Docker AI)
- **Architecture**: Containerized microservices in local K8s cluster
- **Output**: Local K8s deployment with all services orchestrated

### Phase V: Cloud-Native Event-Driven Architecture

- **Event Streaming**: Kafka (Redpanda or Strimzi)
- **Microservices Primitives**: Dapr sidecars
- **Cloud Provider**: DigitalOcean DOKS, Azure AKS, or Google GKE
- **Architecture**: Event-driven, cloud-native, microservices
- **Output**: Production-grade cloud deployment with scalability

## Project Constraints

### Scope Constraints

- **Phase Order**: 5 phases MUST be completed in sequence; no skipping
- **Monorepo**: Single repository with proper separation of concerns
- **Demo Videos**: Under 90 seconds for each phase submission
- **Hackathon Timeline**: All phases must be completed within hackathon duration

### Process Constraints

- **No Manual Coding**: All code MUST be spec-driven and generated via Claude Code
- **WSL 2 Required**: Windows users must use WSL 2 for all development
- **Environment Variables**: Secrets in .env files, never in code
- **Artifact Traceability**: Every feature traced from spec → plan → tasks → code

### Technical Constraints

- **Fixed Stacks**: Technology choices locked per phase document
- **Cloud-Native**: Phase IV+ MUST use Docker/Kubernetes
- **Event-Driven**: Phase V MUST use Kafka and Dapr
- **Authentication**: Better Auth with JWT from Phase II onward

## Governance

### Amendment Procedure

- **Proposed amendments**: MUST document principle/standard change, rationale, impact on phase progression
- **Approval requirement**: Changes to Spec-Driven Development principle require unanimous approval from all team members
- **Documentation**: Amendments recorded in constitution version history with phase impact analysis
- **Migration**: If amendment affects completed phases, affected phases MUST be re-validated before proceeding

### Versioning Policy

- **MAJOR version (X.0.0)**: Removal or fundamental redefinition of core principles (e.g., removing Spec-Driven Development requirement)
- **MINOR version (0.X.0)**: Addition of new principles, expansion of technology stack per phase
- **PATCH version (0.0.X)**: Clarifications, wording improvements, non-semantic refinements
- **Version display**: MUST include ratification date and last amended date in footer

### Compliance Review

- **Pre-phase check**: All principles and standards verified before starting each phase
- **Spec-driven validation**: Code changes MUST have traceable spec/plan/tasks artifacts
- **Technology audit**: Verify phase-appropriate technology stack is used
- **Security review**: Secrets in environment variables only; no hardcoded credentials
- **Clean code check**: Descriptive names, docstrings, proper structure enforced
- **Demo verification**: Each phase demo MUST show working features under 90 seconds

### Principle Supremacy

This constitution supersedes any conflicting project guidance, templates, or informal practices. When in doubt, constitutional principles take priority. Team MUST resolve ambiguities through documented decision-making, not expedient compromise. Spec-driven development principle is NON-NEGOTIABLE.

**Version**: 2.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Awaiting project kickoff | **Last Amended**: 2025-12-31
