import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="DocQuery", page_icon="📄")
st.title("📄 DocQuery")
st.caption("Ask your documents anything — with page citations.")

# --- Sidebar: upload ---
with st.sidebar:
    st.header("Upload a document")
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Upload & Index"):
            with st.spinner("Extracting, chunking, and indexing..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{API_URL}/upload", files=files)

            if response.status_code == 200:
                data = response.json()
                st.success(
                    f"Indexed **{data['filename']}** — "
                    f"{data['total_pages']} pages, {data['total_chunks_stored']} chunks stored."
                )
            else:
                st.error(f"Upload failed: {response.text}")

# --- Main: chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Replay existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# New question
question = st.chat_input("Ask a question about your documents...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching your documents..."):
            response = requests.post(f"{API_URL}/query", json={"question": question, "top_k": 5})

        if response.status_code == 200:
            data = response.json()
            answer = data["answer"]
            pages = ", ".join(f"p.{s['page']}" for s in data["sources"])

            st.markdown(answer)
            if pages:
                st.caption(f"Sources: {pages}")

            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            error_msg = f"Something went wrong: {response.text}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})