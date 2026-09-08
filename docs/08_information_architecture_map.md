# 08. Information Architecture Map & User Navigation Flows

---

## 1. Executive Summary
This document maps out the **Information Architecture (IA)**, page hierarchy, component tree, and core user navigation flows for the **DocQuery** application.

---

## 2. App Page Hierarchy & Site Map

```
                                  DocQuery Web App
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 │                                               │
          Unauthenticated                                  Authenticated
                 │                                               │
     ┌───────────┴───────────┐                       ┌───────────┴───────────┐
     │                       │                       │                       │
 Auth Page               Auth Page               Dashboard              Document Details
 (`/login`)             (`/register`)           (`/dashboard`)        (`/documents/:doc_id`)
```

---

## 3. Screen & Component Hierarchy

### 3.1 Unauthenticated Views
1. **Login Screen (`/login`):**
   * Email/Password input form.
   * Authentication trigger button.
   * Navigation link to Registration screen.

2. **Register Screen (`/register`):**
   * User registration form (Email, Password, Confirm Password).
   * Validation feedback messages.
   * Navigation link to Login screen.

---

### 3.2 Main Workspace Dashboard (`/dashboard`)
The main workspace adopts a **Split-Screen Layout** enabling simultaneous interaction between the chat interface and the PDF viewer.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 TOP HEADER BAR                                         │
│  [Logo: DocQuery]                 Active Doc: Machine_Learning.pdf      [User: Alex (Logout)]│
├───────────────────┬───────────────────────────────────┬────────────────────────────────┤
│    SIDEBAR        │          CHAT PANEL               │          PDF VIEWER            │
│  (Navigation)     │         (Left Window)             │         (Right Window)         │
├───────────────────┼───────────────────────────────────┼────────────────────────────────┤
│ 📁 Documents      │  🤖 Assistant:                    │  Page 149 of 250   [Zoom +/-]  │
│  • ML_Textbook.pdf│   Bagging trains models in        │ ┌────────────────────────────┐ │
│  • Physics_Notes  │   parallel (p. 142). Boosting     │ │ ...Boosting algorithms    │ │
│                   │   trains sequentially.            │ │ sequentially adjust       │ │
│ 💬 Chat Sessions  │   [Source: p. 149] ◄──(Click!)    │ │ weights on misclassified  │ │
│  • Exam Prep 1    │                                   │ │ samples...                 │ │
│  • Ch 6 Revision  │ ───────────────────────────────── │ └────────────────────────────┘ │
│                   │ [ Ask a question...        ] [Send]│  ◄── PDF.js Canvas Auto-Jump   │
│ ➕ Upload PDF     │                                   │      Scrolls to Page 149       │
└───────────────────┴───────────────────────────────────┴────────────────────────────────┘
```

---

## 4. User Navigation & Data Flows

### Flow 1: Authentication & Workspace Entry

```
[ Visitor ] ──► Opens App ──► Redirected to `/login`
                                   │
                                   ▼
                         Submits Credentials
                                   │
                                   ▼
                   FastAPI validates & returns JWT Token
                                   │
                                   ▼
                     Token stored in LocalStorage
                                   │
                                   ▼
                     Redirected to `/dashboard`
```

---

### Flow 2: Document Upload & Async Processing Flow

```
[ User ] ──► Clicks "Upload PDF" in Sidebar ──► Selects file (`textbook.pdf`)
                                                          │
                                                          ▼
                                            Submits to `/api/documents/upload`
                                                          │
                                                          ▼
                                            FastAPI stores raw PDF on disk
                                                          │
                                                          ▼
                                            Background Task Triggered:
                                            • PyMuPDF extracts text per page
                                            • Chunking engine splits into 600t chunks
                                            • MiniLM generates vector embeddings
                                            • Upsert vectors to Qdrant Collection
                                                          │
                                                          ▼
                                            Dashboard Document List updates
                                            status: `processing` ──► `completed`
```

---

### Flow 3: Q&A Query & Click-to-Verify Page Jump Flow

```
[ User ] ──► Types query into Chat Input: "Explain bagging vs boosting"
                 │
                 ▼
          Sends request to `POST /api/chat/sessions/{id}/query`
                 │
                 ▼
          FastAPI Backend Execution:
          1. Embed query string using MiniLM
          2. Match top-K chunks in Qdrant (filtered by `user_id`)
          3. Validate Cosine Similarity Threshold (≥ 0.55)
          4. Prompt Gemini/OpenAI API with context chunks
                 │
                 ▼
          Returns Response JSON with answer & citations array:
          `[{ doc_id: "doc_123", page_number: 149, similarity: 0.84 }]`
                 │
                 ▼
          React Chat Panel renders message + Citation Badge `[Page 149]`
                 │
                 ▼
[ User ] ──► Clicks Citation Badge `[Page 149]`
                 │
                 ▼
          Event Listener passes `target_page: 149` to PDF.js Viewer state
                 │
                 ▼
          PDF Viewer automatically scrolls right-hand pane to Page 149
```
