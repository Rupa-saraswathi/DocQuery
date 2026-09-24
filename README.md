*# DocQuery — Setup \& Run Instructions*



*A RAG-based document Q\&A assistant. Upload a PDF, ask questions, get answers grounded in the document with page citations.*



*## Prerequisites*



*- Python 3.10+ installed*

*- A free Gemini API key (see below)*



*## 1. Clone the repo*



*```*

*git clone https://github.com/Rupa-saraswathi/DocQuery.git*

*cd DocQuery*

*```*



*## 2. Create and activate a virtual environment*



*\*\*Windows:\*\**

*```*

*python -m venv venv*

*venv\\Scripts\\activate*

*```*



*\*\*Mac/Linux:\*\**

*```*

*python -m venv venv*

*source venv/bin/activate*

*```*



*## 3. Install dependencies*



*```*

*pip install -r requirements.txt*

*```*



*## 4. Get your own Gemini API key*



*1. Go to https://aistudio.google.com/apikey*

*2. Sign in and click "Create API key"*

*3. Copy the key*



*\*\*Do not use someone else's key\*\* — each person should use their own.*



*## 5. Create your own `.env` file*



*In the project root (same folder as this README), create a file named `.env` containing:*



*```*

*GEMINI\_API\_KEY=your\_key\_here*

*```*



*This file is git-ignored and will never be pushed — keep it private.*



*## 6. Run the app (two terminals needed)*



*\*\*Terminal 1 — backend:\*\**

*```*

*cd backend*

*uvicorn main:app --reload*

*```*

*Leave this running. It serves the API at `http://127.0.0.1:8000`.*



*\*\*Terminal 2 — frontend:\*\**

*```*

*venv\\Scripts\\activate    (Windows)  /  source venv/bin/activate    (Mac/Linux)*

*streamlit run app.py*

*```*

*This opens the chat UI in your browser at `http://localhost:8501`.*



*## 7. Use it*



*1. Upload a PDF from the sidebar → click "Upload \& Index"*

*2. Ask a question in the chat box*

*3. Answers include page citations; if something isn't in the document, it will say so instead of guessing*



*## Project structure*



*```*

*DocQuery/*

*├── backend/*

*│   └── main.py        # FastAPI: upload, chunking, embeddings, retrieval, query*

*├── app.py              # Streamlit UI*

*├── requirements.txt*

*├── .env                 # your own API key (not committed)*

*├── chroma\_db/          # local vector store (auto-created, not committed)*

*└── docs/                # project documentation*

*```*



*## Notes*



*- Uses `gemini-3.5-flash-lite` for generation and a local `all-MiniLM-L6-v2` model for embeddings (free, runs on your machine).*

*- Vector storage is local (ChromaDB) — each person's uploaded documents stay on their own machine.*

