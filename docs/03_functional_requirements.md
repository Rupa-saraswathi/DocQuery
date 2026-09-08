# 03. Functional Requirements Document

---

## 1. Document Overview
This document enumerates all functional system capabilities for **DocQuery**. Every functional requirement (FR) is assigned a unique identifier, priority level, functional description, and target module.

### Priority Level Definitions
* **P0 (Must Have):** Core functionality required for MVP / initial release. System cannot function without these.
* **P1 (Should Have):** Important features that enhance UX, performance, or system capabilities.
* **P2 (Nice to Have):** Advanced features targeted for future scaling or enterprise extensions.

---

## 2. Authentication & Access Control (FR-AUTH)

| Requirement ID | Feature Name | Priority | Description | Target Component |
| :--- | :--- | :---: | :--- | :--- |
| **FR-AUTH-01** | User Registration | **P0** | System must allow new users to create an account with email and password. Passwords must be hashed using Argon2. | Backend API / PostgreSQL |
| **FR-AUTH-02** | User Authentication | **P0** | System must authenticate users via `/api/auth/login` and issue a signed JWT access token. | Backend API / JWT |
| **FR-AUTH-03** | Authorization Middleware | **P0** | All document and Q&A endpoints must require a valid Bearer JWT in the `Authorization` header. | Backend API Middleware |
| **FR-AUTH-04** | User Document Isolation | **P0** | All document list, upload, query, and delete operations must filter by `user_id` to guarantee tenant isolation. | Backend / Qdrant Payload |

---

## 3. Document Ingestion & Management (FR-DOC)

| Requirement ID | Feature Name | Priority | Description | Target Component |
| :--- | :--- | :---: | :--- | :--- |
| **FR-DOC-01** | PDF / DOCX Upload | **P0** | Users must be able to upload PDF or DOCX files via multi-part form (`/api/documents/upload`). | FastAPI / Storage |
| **FR-DOC-02** | Text & Page Extraction | **P0** | System must extract text using `PyMuPDF` preserving explicit page numbers, headings, and page boundaries. | Document Processor |
| **FR-DOC-03** | Metadata Extraction | **P0** | System must extract and record document metadata: title, filename, page count, upload timestamp, and status. | PostgreSQL (`documents`) |
| **FR-DOC-04** | Document Deletion | **P0** | Deleting a document (`DELETE /api/documents/{id}`) must remove the PDF file, database metadata, and Qdrant vector embeddings. | FastAPI / Qdrant / DB |
| **FR-DOC-05** | Document Listing | **P0** | Authenticated users can list all their uploaded documents with status and metadata (`GET /api/documents`). | FastAPI / PostgreSQL |
| **FR-DOC-06** | OCR for Scanned PDFs | **P1** | Optional processing pass using Tesseract OCR for scanned PDFs that contain zero extractable text layers. | Document Processor |

---

## 4. Chunking, Embedding & Vector Store (FR-RAG)

| Requirement ID | Feature Name | Priority | Description | Target Component |
| :--- | :--- | :---: | :--- | :--- |
| **FR-RAG-01** | Recursive Semantic Chunking | **P0** | Split document text into 500–800 token chunks with 100–150 token overlap, respecting Section > Paragraph > Sentence boundaries. | LangChain Splitter |
| **FR-RAG-02** | Chunk Metadata Tagging | **P0** | Attach `document_id`, `page_number`, `section_title`, and `chunk_index` to every extracted chunk. | RAG Pipeline |
| **FR-RAG-03** | Vector Embedding Generation | **P0** | Embed chunks using `all-MiniLM-L6-v2` (384-dim) or `text-embedding-3-small` (1536-dim). | Embedding Engine |
| **FR-RAG-04** | Vector Indexing | **P0** | Upsert vector embeddings into Qdrant vector database using HNSW indexing with cosine similarity. | Qdrant Vector Store |
| **FR-RAG-05** | Top-K Semantic Search | **P0** | Retrieve top 5–8 candidate text chunks matching a user query vector. | Retrieval Engine |
| **FR-RAG-06** | Cross-Encoder Re-Ranking | **P1** | Re-rank top-20 retrieved candidates down to top-5 using a cross-encoder before passing to LLM. | Re-ranking Service |
| **FR-RAG-07** | Confidence Thresholding | **P0** | Enforce a minimum cosine similarity score ($\ge 0.55$). If no chunk passes, return explicit refusal. | Retrieval Validator |
| **FR-RAG-08** | Grounded LLM Generation | **P0** | Prompt Gemini / OpenAI API using *only* retrieved chunks as context, enforcing strict citation requirements. | LLM Engine |

---

## 5. Q&A Sessions & Citation Verification (FR-CHAT)

| Requirement ID | Feature Name | Priority | Description | Target Component |
| :--- | :--- | :---: | :--- | :--- |
| **FR-CHAT-01** | Chat Session Creation | **P0** | Create new isolated Q&A sessions (`POST /api/chat/sessions`) attached to a user account. | FastAPI / DB |
| **FR-CHAT-02** | Grounded Q&A Query | **P0** | Submit natural language query (`POST /api/chat/sessions/{id}/query`) and receive answer with page citations. | Backend Q&A Engine |
| **FR-CHAT-03** | Citation Retrieval | **P0** | Fetch detailed chunk and page metadata behind an answer (`GET /api/chat/sessions/{id}/citations/{msg_id}`). | FastAPI / DB |
| **FR-CHAT-04** | Chat History | **P0** | Retrieve full turn-by-turn history for a session (`GET /api/chat/sessions/{id}/history`). | FastAPI / PostgreSQL |

---

## 6. Frontend & User Interface (FR-UI)

| Requirement ID | Feature Name | Priority | Description | Target Component |
| :--- | :--- | :---: | :--- | :--- |
| **FR-UI-01** | Document Upload UI | **P0** | Drag-and-drop file uploader with upload progress indicator and document list dashboard. | React Frontend |
| **FR-UI-02** | Conversational Chat Interface | **P0** | Split-screen interface featuring chat panel alongside document viewer. | React Frontend |
| **FR-UI-03** | In-App PDF Viewer | **P0** | Integrated PDF rendering via PDF.js supporting page scrolling and zoom. | React Frontend / PDF.js |
| **FR-UI-04** | Click-to-Verify Citation Jump | **P0** | Clicking a citation badge in chat automatically scrolls PDF viewer to the exact cited page number. | React Frontend / PDF.js |
