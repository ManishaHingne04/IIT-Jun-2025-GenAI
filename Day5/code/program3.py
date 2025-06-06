from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader

def function1():
    # create embeddings object
    embeddings = OllamaEmbeddings(model="llama3")

    # documents to be embedded
    docs = ["this is file1", "this is file2"]

    # convert the data into embeddings
    vectors = embeddings.embed_documents(docs)
    print(vectors)

# function1()

def function2():
    # read the data from pdf file
    loader = PyPDFLoader("./information.pdf")
    
    # load the documents
    documents = loader.load()

    # get all the text data
    docs = []

    # read the data from the document
    for document in documents:
        docs.append(document.page_content)

    # create embeddings object
    embeddings = OllamaEmbeddings(model="llama3")

    # add the docs
    vectors = embeddings.add_documents(docs)
    print(vectors)

# function2()