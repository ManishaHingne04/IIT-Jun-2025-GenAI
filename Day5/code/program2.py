from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, DirectoryLoader


def read_from_pdf():
    # create the loader to load the file
    loader = PyPDFLoader("./information.pdf")

    # load the document
    documents = loader.load()

    # read the data from the document
    for document in documents:
        print(document.page_content)

# read_from_pdf()


def read_from_url():
    # create loader to load the data from url
    loader = WebBaseLoader(
        'https://en.wikipedia.org/wiki/Chanakya'
    )

    # load the document
    documents = loader.load()

    # read the data from the document
    for document in documents:
        # document here is an object of Document class
        print(document.page_content)

# read_from_url()


def read_from_directory():
    # DirectoryLoader used unstructured package to load the data from files
    # create the loader to load the data from directory
    loader = DirectoryLoader('./docs')

    # load the document
    documents = loader.load()

    # read the data from the document
    for document in documents:
        print(document.page_content)

# read_from_directory()
    