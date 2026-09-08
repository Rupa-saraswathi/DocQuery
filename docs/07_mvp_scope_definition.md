# 07. MVP Scope Definition & Product Roadmap

---

## 1. Executive Summary
This document defines the strict boundaries of the **Minimum Viable Product (MVP)** for **DocQuery**. To guarantee rapid, focused execution and eliminate scope creep, features are explicitly divided into **In-Scope (P0 MVP)** and **Out-of-Scope (P1/P2 Future Releases)**.

---

## 2. MVP Boundary Matrix (P0 vs. Future Scope)

```
┌────────────────────────────────────────────────────────────────────────┐
│                          DOCQUERY MVP BOUNDARY                         │
├──────────────────────────────────┬─────────────────────────────────────┤
│      IN-SCOPE (MVP / P0)         │    OUT-OF-SCOPE (FUTURE / P1-P2)   │
├──────────────────────────────────┼─────────────────────────────────────┤
│ • Email/Password Auth (JWT)      │ • OAuth (Google / GitHub)           │
│ • Single PDF File Upload         │ • OCR for Scanned Image PDFs        │
│ • PyMuPDF Text & Page Extraction │ • Cross-Encoder Re-Ranking          │
│ • MiniLM Embedding & Qdrant DB   │ • Multi-Document Comparison Matrix  │
│ • Top-K Vector Retrieval         │ • Cloud S3 Storage (MVP is Local)   │
│ • Cosine Threshold (≥ 0.55)      │ • Team Shared Workspaces & RBAC     │
│ • Grounded LLM Q&A + Citations   │ • Audio/Voice Querying              │
│ • Split-Screen React UI          │ • Native Mobile Apps                │
│ • PDF.js Click Jump-to-Page      │ • Real-time Collaboration           │
└──────────────────────────────────┴─────────────────────────────────────┘
```

---

## 3. Detailed MVP Feature Scope (P0 - Must Have)

### 3.1 Authentication & Security (P0)
* Email and password registration with Argon2 password hashing.
* JWT Bearer token authentication for all secure API endpoints.
* Enforced per-user payload filtering on Qdrant vector queries (`user_id`).

### 3.2 Document Ingestion & Storage (P0)
* Multi-part file upload supporting `.pdf` files up to 50MB.
* Text extraction preserving page boundaries using `PyMuPDF`.
* Local disk storage for raw PDF files (`backend/uploads/`).
* PostgreSQL metadata storage (`documents`, `chunks_metadata`).

### 3.3 RAG Engine & Vector Search (P0)
* Recursive semantic chunking (500–800 tokens, 100–150 token overlap).
* Vector embedding generation using local `sentence-transformers/all-MiniLM-L6-v2`.
* Vector upsert and HNSW search in Qdrant.
* Cosine similarity confidence thresholding ($\ge 0.55$) with explicit refusal responses.
* LLM answer generation with structured document and page citations.

### 3.4 User Interface & Citation Jump (P0)
* Responsive split-screen dashboard (Chat Panel on left, PDF Viewer on right).
* Embedded PDF viewer using `PDF.js`.
* Clickable citation badges in chat messages that scroll PDF viewer to exact cited page.
* Document list sidebar with upload trigger and document deletion controls.

---

## 4. Out-of-Scope Items (Deferred to Future Releases)

| Feature | Priority | Deferred Reason | Planned Phase |
| :--- | :---: | :--- | :---: |
| **Tesseract OCR Integration** | **P1** | Scanned PDF OCR adds heavy dependencies and processing latency; text PDFs cover 90%+ MVP use cases. | Phase 2 Release |
| **Cross-Encoder Re-Ranking** | **P1** | Bi-encoder Qdrant similarity search provides high accuracy for initial MVP testing. | Phase 2 Release |
| **Cloud S3 / GCP Storage** | **P1** | Local mounted volume storage simplifies local development (`docker compose`). | Phase 2 Release |
| **Shared Team Workspaces** | **P2** | Enterprise access control requires complex RBAC tables deferred until post-MVP. | Phase 3 Release |
| **OAuth2 Social Sign-In** | **P2** | JWT email/password is sufficient for core authentication verification. | Phase 3 Release |

---

## 5. Release Milestones & Development Roadmap

```
  MILESTONE 1             MILESTONE 2             MILESTONE 3             MILESTONE 4
┌───────────────┐       ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ Core Setup &  │ ──►   │ RAG Ingestion │ ──►   │ Q&A Engine &  │ ──►   │ React UI &    │
│ Auth Engine   │       │ Pipeline      │       │ Citations API │       │ PDF.js Viewer │
└───────────────┘       └───────────────┘       └───────────────┘       └───────────────┘
   (Sprint 1)              (Sprint 2)              (Sprint 3)              (Sprint 4)
```

* **Milestone 1: Backend Foundation & Auth (Sprint 1)**
  * Repository initialization, Docker Compose configuration (PostgreSQL + Qdrant).
  * FastAPI setup, Alembic migrations, JWT Auth endpoints (`/api/auth/register`, `/login`).

* **Milestone 2: Ingestion & Vector Pipeline (Sprint 2)**
  * Document upload handler (`PyMuPDF`), text extraction, semantic chunking logic.
  * Embedding service (`all-MiniLM-L6-v2`), Qdrant client connection & HNSW collection indexing.

* **Milestone 3: Q&A Engine & Grounding Validator (Sprint 3)**
  * Vector search query builder, cosine similarity threshold validator ($\ge 0.55$).
  * LLM prompt wrapper (Gemini / OpenAI API), citation formatter endpoint (`/api/chat/sessions/{id}/query`).

* **Milestone 4: React UI & PDF.js Jump Integration (Sprint 4)**
  * React + TypeScript frontend skeleton, Tailwind CSS split-screen layout.
  * Chat component, PDF.js canvas viewer, click-to-page jump synchronization.
  * End-to-end integration testing and bug fixes.
