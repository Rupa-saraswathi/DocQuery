# 02. Product Vision & Core Value Proposition

---

## 1. Executive Summary

**DocQuery** is a Retrieval-Augmented Generation (RAG) based Document Q&A Assistant designed to turn any collection of private PDFs or study notes into a queryable, interactive knowledge base.

Users upload their documents, ask questions in plain natural language, and receive accurate answers that are **strictly grounded in the source material—complete with exact, click-to-verify page citations**.

---

## 2. Product Vision

### 2.1 Why It Exists
Students and professionals do not have a "search" problem—they have a **"trust" problem**. 

Manual skimming and `Ctrl+F` are slow but accurate. General-purpose AI chatbots are fast but hallucinate unverified answers. Neither existing approach provides the speed of artificial intelligence with the reliability of going straight to the exact page in the document.

DocQuery exists to bridge this gap: combining the natural language convenience of AI with the unwavering trustworthiness of click-to-verify page citations.

### 2.2 What It Does
1. **Document Knowledge Conversion:** Accepts private PDFs, notes, textbooks, and reports, converting them into an indexed vector knowledge base.
2. **Natural Language Querying:** Allows users to ask questions in plain English across single or multiple documents simultaneously.
3. **Grounded Answer Generation:** Generates concise, accurate responses using *only* retrieved passages from the user's uploaded material.
4. **Interactive Citation Jump:** Links every claim in the response directly to the specific page number in the source PDF, allowing instant side-by-side inspection via PDF.js.

---

## 3. Core Value Proposition

> **"For students and early-career professionals drowning in unstructured PDFs, DocQuery is a document Q&A assistant that gives grounded, page-cited answers instead of generic or hallucinated ones—unlike general AI chatbots, which have no access to private documents and no way to prove where an answer came from."**

---

## 4. One-Line Pitch

> **"Ask your documents anything — and know exactly where the answer came from."**

---

## 5. Core Operating Principles & Guarantees

```
                   THE THREE-LAYER GROUNDING MODEL
                   
           ┌───────────────────────────────────────────────┐
           │                 User Question                 │
           └───────────────────────────────────────────────┘
                                   │
                                   ▼
           ┌───────────────────────────────────────────────┐
           │        Semantic Retrieval & Evidence          │
           │    (Cosine Similarity Threshold Check ≥ 0.55) │
           └───────────────────────────────────────────────┘
                                   │
                                   ▼
           ┌───────────────────────────────────────────────┐
           │              Grounded Generation              │
           │     (Prompted ONLY with retrieved chunks)     │
           └───────────────────────────────────────────────┘
                                   │
                                   ▼
           ┌───────────────────────────────────────────────┐
           │            Verified Page Citation             │
           │        (Clickable PDF.js jump-to-page)        │
           └───────────────────────────────────────────────┘
```

1. **100% Evidence Grounding:** No answer is ever generated from the model's general parametric memory alone. Every claim traces directly back to a retrieved text chunk.
2. **Explicit Refusal Over Hallucination:** If retrieved chunks fall below the confidence threshold ($\text{similarity score} < 0.55$), DocQuery explicitly states: *"This isn't covered in the uploaded documents"* rather than guessing.
3. **Exact Source Traceability:** Every citation points to the specific document name and page number.
4. **Per-User Isolation:** Each user's document collection is strictly isolated with vector payload security filtering.

---

## 6. Key Feature Differentiators

| Capability | General AI Chatbots | Traditional Search (Ctrl+F) | DocQuery |
| :--- | :---: | :---: | :---: |
| **Private Document Support** | ❌ No | 🟢 Yes | 🟢 Yes |
| **Natural Language Synthesizing** | 🟢 Yes | ❌ No | 🟢 Yes |
| **Page-Level Citations** | ❌ No | ❌ No | 🟢 Yes (Clickable PDF.js link) |
| **Hallucination Protection** | ❌ No | 🟢 N/A | 🟢 Yes (Explicit Refusal Logic) |
| **User Data Privacy** | ❌ Public Training Risks | 🟢 Local | 🟢 Isolated Storage |
