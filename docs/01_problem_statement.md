# 01. Problem Statement Document

---

## 1. Executive Summary

Students, researchers, and working professionals interact daily with large volumes of unstructured PDF documents (textbooks, lecture slides, research papers, compliance manuals, and technical specifications). While accessing these documents is easy, **retrieving accurate, verifiable insights from them remains slow, tedious, and error-prone**.

Existing tools force users into an unacceptable trade-off between **manual skimming speed** and **AI accuracy/trustworthiness**. DocQuery is designed specifically to eliminate this dilemma.

---

## 2. The Core Problem

### 2.1 The Information Bottleneck
As knowledge work digitizes, document volume grows exponentially. However, existing document exploration methods suffer from fundamental flaws:

1. **Keyword Search (Ctrl+F) Limitations:**
   * Exact-string matching fails when the user does not know the specific author terminology.
   * `Ctrl+F` cannot answer conceptual questions (e.g., *"What are the core differences between bagging and boosting according to the slides?"*).
   * It cannot synthesize findings spread across multiple chapters or separate files.
   * Users spend hours manually scrolling through hundreds of pages to locate isolated facts.

2. **The "Trust & Hallucination" Dilemma with General AI:**
   * General-purpose conversational AI models (e.g., standard ChatGPT, Claude) rely on static parametric training memory.
   * They lack access to private, unpublished, or domain-specific user files.
   * When queried about custom documents, general AI models frequently produce **confident hallucinations**—inventing facts, quotes, or page numbers that do not exist in the source text.
   * Users cannot trust general AI for critical tasks (such as exam preparation or financial/legal analysis) because there is no automated way to audit or trace an answer back to the source page.

```
                           THE ACCURACY VS. SPEED DILEMMA
                           
┌───────────────────────────┐         ┌───────────────────────────┐
│     Manual Skimming       │    VS   │    General AI Chatbot     │
├───────────────────────────┤         ├───────────────────────────┤
│ • High Accuracy           │         │ • High Speed              │
│ • Extremely Slow          │         │ • High Hallucination Risk │
│ • No Synthesis Capability │         │ • Zero Source Auditing    │
└───────────────────────────┘         └───────────────────────────┘
                                  │
                                  ▼
                     ┌───────────────────────────┐
                     │     Target Solution       │
                     ├───────────────────────────┤
                     │  ✓ High Speed             │
                     │  ✓ 100% Fact Grounding    │
                     │  ✓ Verifiable Page Links │
                     └───────────────────────────┘
```

---

## 3. Target Users & Audience Segmentation

### 3.1 User Cohort Analysis

| Cohort | Primary Use Cases | Key Pain Points |
| :--- | :--- | :--- |
| **Primary: Students & Academic Learners** | Preparing for exams across multi-chapter textbooks, lecture slides, and course packages. | Drowning in 500+ pages of reading materials; spending hours scanning slides before exams; fear of missing key concepts. |
| **Secondary: Researchers & Analysts** | Conducting literature reviews, cross-referencing research papers, financial reports, and internal manuals. | Cannot expose confidential or unreleased papers to public LLMs; standard tools cannot cross-reference multiple dense PDFs safely. |
| **Future: Enterprise & Legal Teams** | Auditing contracts, compliance manuals, corporate knowledge bases, and onboarding documents. | Needs strict per-user document isolation, compliance audits, and precise source attribution. |

---

## 4. User Personas

### Persona 1: Alex — Computer Science Student
* **Background:** Undergraduate student preparing for midterm and final exams across 15 lecture slide decks and 2 core textbooks.
* **Goal:** Quickly revise complex topics (e.g., database indexing algorithms) without re-reading full 60-page slide decks.
* **Pain Point:** Skimming through PDFs takes hours, and general ChatGPT often hallucinates terms that aren't in his professor's specific syllabus.
* **Core Need:** A tool where he can ask natural-language questions and instantly get an answer tied to the exact slide number.

### Persona 2: Sarah — Junior Research Analyst
* **Background:** Analyst reviewing quarterly earnings reports and regulatory filings across multiple tech companies.
* **Goal:** Extract financial risk factors and compare balance metrics across 10 PDF documents.
* **Pain Point:** Manual Ctrl+F is too slow, but general AI tools risk hallucinating financial metrics which could ruin her reports.
* **Core Need:** Absolute evidence grounding with clickable citations to verify every single figure against the source document.
