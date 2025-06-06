from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate


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
        # add code to cleanse the data here
        # Document represents the contents to be added to the vector store
        docs.append(Document(id=id, page_content=document.page_content))
        id += 1

    return docs

def build_knowledge_base():
    # read the data from pdf file
    data = read_data_from_pdf()

    # chunking the data
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
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

# build_knowledge_base()

def rag_pipeline():
    # user input
    question = "what is Johns age?"

    # load the vector store
    chroma_store = Chroma(
        embedding_function=OllamaEmbeddings(model="llama3"),
        collection_name="my_collection",
        persist_directory="./chroma_db"
    )

    # find the context (similar vectors)
    context = chroma_store.search(question, search_type="similarity", k=5)
    # print(f"context: {context}")

    # template for the prompt
    template = """
    You are an assistance.
    Answer the question with the context provided.
    Answer with not more than 100 words.
    If the information is not available in the context, return "I don't know".
    Question: {question}
    Context: {context}
    Answer: 
    """

    # create the prompt template object
    prompt_template = ChatPromptTemplate.from_template(template)

    # create the prompt
    prompt = prompt_template.invoke({"question": question, "context": context})
    # print(prompt)
    
    # create the model
    model = ChatOllama(model="llama3")

    # send the prompt and get the response
    response = model.invoke(prompt)
    print(f"response: {response.content}")

rag_pipeline()