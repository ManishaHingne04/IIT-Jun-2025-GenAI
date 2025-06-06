from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter


def read_data_from_pdf():
    # read the data from pdf file
    loader = PyPDFLoader("./information.pdf")
    
    # load the documents
    documents = loader.load()

    # get all the text data
    docs = []

    # read the data from the document
    id = 1
    for document in documents:
        # Document represents the contents to be added to the vector store
        docs.append(Document(id=id, page_content=document.page_content))
        id += 1

    return docs


def function1():
    # read the data from pdf file
    docs = read_data_from_pdf()

    # decide which embeddings to use
    embeddings = OllamaEmbeddings(model="llama3")

    # create a vector store to store the vectors
    vector_store = InMemoryVectorStore(embedding=embeddings)

    # store the data in vector store
    vector_store.add_documents(docs)

    # search the (k=2) 2 similar vectors
    similar_vectors = vector_store.search(
        "John Kulkarni?", 
        search_type="similarity", 
        k=2)
    
    # print the similar vectors
    print(similar_vectors)

# function1()

def function2():
    # read the data from pdf file
    data = read_data_from_pdf()

    # chunking the data
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=100
    )
    docs = splitter.split_documents(data)

    # decide which embeddings to use
    embeddings = OllamaEmbeddings(model="llama3")

    # create a vector store to store the vectors
    vector_store = Chroma(
        embedding_function=embeddings,
        collection_name="my_collection",
        persist_directory="./chroma_db"
    )

    # store the data in vector store
    vector_store.add_documents(docs)

    # search the (k=2) 2 similar vectors
    similar_vectors = vector_store.search(
        "John Kulkarni?", 
        search_type="similarity", 
        k=2)
    
    # print the similar vectors
    print(similar_vectors)

# function2()