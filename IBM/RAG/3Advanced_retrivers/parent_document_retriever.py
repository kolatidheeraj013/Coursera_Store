from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.retrievers import ParentDocumentRetriever
from langchain.schema import Document

# --- NOTE: Ensure you have initialized your watsonx LLM and Embedding models ---
# def watsonx_embedding(): return <Your Watsonx Embedding Instance>

def main():
    # 1. Sample text mimicking a long document (like your company policy)
    txt_data = [
        Document(page_content="""COMPANY POLICY DOCUMENT:
        Section 1: Attendance. Employees are expected to be at their desks by 9 AM.
        Section 2: Smoking Policy. Smoking is strictly prohibited indoors. There is a designated smoking area behind the cafeteria.
        Section 3: Vacation. Employees get 20 days of paid time off per year.""")
    ]

    # 2. Define Splitters (Parent chunks vs Child chunks)
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)

    # 3. Initialize empty storage containers
    vectordb = Chroma(collection_name="split_parents", embedding_function=watsonx_embedding())
    store = InMemoryStore()

    # 4. Initialize the Parent Document Retriever
    retriever = ParentDocumentRetriever(
        vectorstore=vectordb,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
    )

    # 5. Ingest the data (This splits and routes data to vectordb and store)
    retriever.add_documents(txt_data)

    print(f"Number of parent chunks stored: {len(list(store.yield_keys()))}\n")

    # 6. Execute search (Fetches child, returns parent)
    print("Executing Parent Document Search...\n")
    retrieved_docs = retriever.invoke("What is the smoking policy?")
    
    for idx, doc in enumerate(retrieved_docs):
        print(f"Parent Document {idx + 1}:")
        print(doc.page_content)

if __name__ == "__main__":
    main()