# 04. User Stories & Workflows

---

## 1. Overview
This document details the primary user stories and end-to-end operational scenarios for **DocQuery**. Each story is formatted using standard Agile syntax (*As a [role], I want to [action], so that [value/outcome]*).

---

## 2. Key User Stories

### Story 1: User Registration & Authentication (US-01)
* **Role:** Student / Professional
* **Action:** I want to create a secure account and log in using my email and password.
* **Value:** So that my uploaded documents, chat history, and index vectors remain private and isolated to my account.

---

### Story 2: Document Upload & Automated Indexing (US-02)
* **Role:** Student preparing for exams
* **Action:** I want to upload my 120-page textbook PDF into DocQuery.
* **Value:** So that the system parses, page-chunks, and indexes the material into a queryable knowledge base within seconds.

---

### Story 3: Natural Language Q&A with Exact Citations (US-03)
* **Role:** Student revising lecture notes
* **Action:** I want to ask plain-English questions like *"What is the difference between bagging and boosting, and which pages cover it?"*
* **Value:** So that I get a concise answer directly grounded in my textbook without reading all 120 pages again.

---

### Story 4: Click-to-Verify Page Jump (US-04)
* **Role:** Research Analyst
* **Action:** I want to click on a citation tag (e.g., `[Document.pdf, Page 142]`) in the chat response.
* **Value:** So that the embedded PDF viewer automatically opens the document and jumps to page 142 for instant manual verification.

---

### Story 5: Protection Against Hallucinations / Missing Evidence (US-05)
* **Role:** Financial Auditor
* **Action:** I want the system to decline answering when a topic is not present in my uploaded documents.
* **Value:** So that I am never lied to or given hallucinated facts that could compromise my work.

---

### Story 6: Document Deletion & Clean-up (US-06)
* **Role:** Privacy-conscious User
* **Action:** I want to delete a document from my dashboard.
* **Value:** So that all associated raw files, database metadata, and Qdrant vector embeddings are completely purged.

---

## 3. End-to-End Operational Scenarios

### Scenario A: Successful Exam Revision Workflow

```
[User Alex] ──► Uploads "Machine_Learning_Textbook.pdf" (120 pages)
                   │
                   ▼
            DocQuery parses pages, extracts text, chunks into 600-token sections,
            generates MiniLM embeddings, & upserts to Qdrant Vector Store (<15 sec)
                   │
                   ▼
[User Alex] ──► Asks: "Explain bagging vs boosting with page numbers."
                   │
                   ▼
            Retrieval Engine matches query to Chunks 142, 144, 149, 152 (Similarity > 0.78)
                   │
                   ▼
            LLM generates grounded summary:
            "Bagging trains models in parallel (p. 142). Boosting trains sequentially (p. 149)."
                   │
                   ▼
[User Alex] ──► Clicks citation badge `[p. 149]`
                   │
                   ▼
            PDF Viewer instantly jumps to Page 149 with Page 149 highlighted.
```

---

### Scenario B: Out-of-Scope Query Handling (Hallucination Refusal)

```
[User Sarah] ──► Queries: "What was the company's Q3 revenue in 2020?"
                    (Uploaded PDF only covers 2023 financial reports)
                   │
                   ▼
             Qdrant vector search performs similarity match against candidate chunks.
             Top candidate chunk similarity score = 0.38 (< 0.55 threshold).
                   │
                   ▼
             Retrieval confidence check FAILS threshold constraint.
                   │
                   ▼
             DocQuery surfaces explicit refusal message:
             "This isn't covered in the uploaded documents." (No LLM hallucination).
```
