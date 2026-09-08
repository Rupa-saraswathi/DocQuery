# 06. Non-Functional Requirements (NFR)

---

## 1. Overview
This document specifies all non-functional performance constraints, security standards, scalability targets, and quality bounds required for **DocQuery**.

---

## 2. Performance & Latency Constraints

| Operation | Target Performance Bound | Measurement Context |
| :--- | :---: | :--- |
| **Document Processing & Indexing** | **< 15 seconds** | Full ingestion pipeline for a 20-page PDF document (text extraction, chunking, embedding, vector upsert). |
| **Query Vector Embedding** | **< 100 ms** | Embedding a user query string using `all-MiniLM-L6-v2`. |
| **Vector Similarity Search** | **< 300 ms** | Top-K HNSW index search in Qdrant across 100,000 indexed chunks. |
| **End-to-End Q&A Answer Latency** | **< 3.0 seconds** | Complete flow: Query embedding + Qdrant search + re-ranking + LLM generation + response return. |

---

## 3. System Scalability & Capacity Bounds

1. **User Capacity:** Tested to support up to 50 concurrent active documents or ~5,000 pages per user workspace.
2. **Vector Index Performance:** Qdrant collection configured with HNSW index ($M=16, \text{ef\_construct}=100$) maintaining sub-second search under high concurrency.
3. **Database Concurrency:** PostgreSQL connection pool sized to handle up to 100 concurrent async backend connections.

---

## 4. Security, Isolation & Compliance

```
┌─────────────────────────────────────────────────────────────────┐
│                     SECURITY LAYER STANDARDS                    │
├─────────────────────────────────────────────────────────────────┤
│ • Transport Security: HTTPS / TLS 1.3                           │
│ • Password Hashing: Argon2id with random salt                   │
│ • Authentication: Stateless Bearer JWT tokens (HS256 / RS256)  │
│ • Tenant Isolation: Forced `user_id` payload filter on Qdrant   │
│ • Storage Protection: Encryption at rest for stored PDF files   │
└─────────────────────────────────────────────────────────────────┘
```

* **Authentication & Authorization:** Argon2 for password hashing; signed JWT tokens passed in `Authorization: Bearer <token>` for all API requests.
* **Tenant Document Isolation:** Every Qdrant vector query and PostgreSQL read operation is enforced with `WHERE user_id = current_user_id` at the database middleware layer. No cross-tenant data leaks.
* **Data Protection:** Original uploaded PDFs stored in encrypted disk storage; temporary parsed chunks purged from volatile memory after embedding.

---

## 5. Reliability & Availability

1. **Containerized Deployment:** Microservices orchestrated via Docker Compose (`fastapi`, `postgres`, `qdrant`) with automated restart policies (`restart: unless-stopped`).
2. **Graceful Degraded State:** If external LLM service (Gemini/OpenAI) experiences temporary downtime, vector search and document viewing remain fully functional, returning clear service alert messages.
3. **Data Integrity:** PostgreSQL foreign key constraints (`ON DELETE CASCADE`) ensure no orphaned metadata, citations, or chunks remain after document deletion.

---

## 6. System Quality & Maintainability

1. **Frontend Code Quality:** Built with React + TypeScript enforcing strict type checking (`tsconfig` strict mode).
2. **Backend API Validation:** All input forms and API payloads validated via Pydantic v2 schemas with automated OpenAPI documentation generated at `/docs`.
3. **Testing Standards:** Backend target test coverage $\ge 80\%$ across chunking, vector indexing, and API endpoint integration tests using `pytest`.
