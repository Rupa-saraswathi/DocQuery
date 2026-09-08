# 05. Acceptance Criteria Specification

---

## 1. Overview
This document specifies formal **Given-When-Then** acceptance criteria for every functional requirement in DocQuery. A feature is considered **DONE** only when all corresponding acceptance tests pass.

---

## 2. Authentication & Access Control (FR-AUTH)

### AC-AUTH-01: User Registration
* **Given** a new visitor on the registration page,
* **When** they submit a valid email address and password,
* **Then** a new user record is created in PostgreSQL with an Argon2 password hash, returning `201 Created`.

### AC-AUTH-02: Authentication & Token Issuance
* **Given** a registered user,
* **When** they submit valid credentials to `POST /api/auth/login`,
* **Then** the server responds with HTTP `200 OK` and a valid JWT access token.

### AC-AUTH-03: Security Enforcement
* **Given** an unauthenticated request to `/api/documents/upload` without a Bearer token,
* **When** the backend receives the request,
* **Then** it must return HTTP `401 Unauthorized`.

### AC-AUTH-04: Tenant Document Isolation
* **Given** User A and User B both have uploaded documents,
* **When** User A calls `GET /api/documents` or submits a Q&A query,
* **Then** the backend must only query chunks and metadata matching User A's `user_id`.

---

## 3. Document Ingestion & Management (FR-DOC)

### AC-DOC-01: PDF Upload & Storage
* **Given** an authenticated user uploading a valid `.pdf` or `.docx` file under 50MB,
* **When** `POST /api/documents/upload` is invoked,
* **Then** the file is stored in local/cloud storage, a metadata row is inserted into PostgreSQL (`upload_status = processing`), and processing starts asynchronously.

### AC-DOC-02: Text Extraction & Page Tracking
* **Given** a 20-page PDF document,
* **When** `PyMuPDF` parses the file,
* **Then** all extracted text blocks must be tagged with exact 1-indexed page numbers (`page_number: 1..20`).

### AC-DOC-03: Complete Document Deletion
* **Given** a document with ID `doc_123`,
* **When** the owner calls `DELETE /api/documents/doc_123`,
* **Then** the raw PDF file, the PostgreSQL document row, metadata chunks, and Qdrant vector payload entries matching `doc_123` must be permanently deleted.

---

## 4. Chunking, Embedding & Retrieval (FR-RAG)

### AC-RAG-01: Chunking Bounds & Overlap
* **Given** extracted document text,
* **When** processed by `RecursiveCharacterTextSplitter`,
* **Then** chunk size must be between 500–800 tokens with 100–150 tokens overlap, and chunks smaller than 50 tokens must be discarded.

### AC-RAG-02: Grounded Retrieval Confidence Threshold
* **Given** a user question submitted to the Q&A session,
* **When** vector search matches against Qdrant,
* **Then** if no candidate chunk has a cosine similarity score $\ge 0.55$, the system returns: `"This isn't covered in the uploaded documents"` without making an LLM generation call.

### AC-RAG-03: Citation Structure Integrity
* **Given** a successful grounded LLM generation,
* **When** the response payload is returned,
* **Then** every claim cited must include the exact `document_id`, `page_number`, `chunk_id`, and `similarity_score` in the citation array.

---

## 5. Frontend & Citation Jump (FR-UI)

### AC-UI-01: PDF Viewer Synchronization
* **Given** an answer rendered in the chat panel with a citation badge `[Page 14]`,
* **When** the user clicks the citation badge,
* **Then** the PDF viewer pane must instantly focus on the cited document and scroll directly to Page 14.
