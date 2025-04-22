import streamlit as st
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI
from langchain.chains.question_answering import load_qa_chain
import os
import yaml
import tempfile


with open("open-ai-credentials.yml", "r") as file:
    config = yaml.safe_load(file)


# Streamlit UI
if "history" not in st.session_state:
    st.session_state.history = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# Move the file uploader to the sidebar and adjust the layout to resemble ChatGPT
st.sidebar.title("📄 Chat with your PDF using Azure OpenAI")
uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    # Save uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_pdf_path = tmp_file.name

    # Step 1: Load and chunk the PDF content
    st.info("Reading and chunking PDF...")
    loader = PyMuPDFLoader(tmp_pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)

    # Step 2: Generate embeddings with AzureOpenAI
    st.info("Creating vector store with AzureOpenAIEmbeddings...")
    embeddings = AzureOpenAIEmbeddings(
        deployment="text-embedding-ada-002",
        model="text-embedding-ada-002",
        azure_endpoint="https://stm-openai.openai.azure.com/",
        openai_api_key="8cG87C825A2NyejvJBLZEjKImp4KAgwgQpBnE8DHS4UD0hnmHgCCJQQJ99BDACYeBjFXJ3w3AAABACOG18AL",
        chunk_size=1,
        validate_base_url=False)

    vectorstore = FAISS.from_documents(split_docs, embeddings)

    # Step 3: Input for questions
    query = st.text_input("Ask something about the PDF:")

    if query:
        st.info("Querying Azure OpenAI for an answer...")
        retriever = vectorstore.as_retriever()
        relevant_docs = retriever.get_relevant_documents(query)

        llm = AzureChatOpenAI(
            azure_endpoint=config["azure_openai"]["api_base"],
            openai_api_version=config["azure_openai"]["api_version"],
            deployment_name=config["azure_openai"]["deployment"],
            openai_api_key=config["azure_openai"]["api_key"],
            openai_api_type=config["azure_openai"].get("type", "azure")
            )

        qa_chain = load_qa_chain(llm, chain_type="stuff")
        response = qa_chain.run(input_documents=relevant_docs, question=query)

        st.success("Response:")
        st.write(response)

        # Append the query and response to the chat history
        st.session_state.history.append({"speaker": "You", "message": query})
        st.session_state.history.append({"speaker": "Azure OpenAI", "message": response})

if st.session_state.history:
    st.subheader("💬 Chat History")
    for entry in st.session_state.history:
        speaker = entry["speaker"]
        message = entry["message"]
        if speaker == "You":
            st.markdown(f"**🧑‍💼 {speaker}:** {message}")
        else:
            st.markdown(f"**🤖 {speaker}:** {message}")