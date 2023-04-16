"""
Uses VectorstoreIndexCreator.from_loaders to index a directory of HTML and PDF files.

Index is an instance of VectorStoreIndexWrapper.

Chain is an instance of OpenAI(temperature=0). Alternatives: stuff, map_reduce, refine,map-rerank

Retrieve is an instance of TODO.

To access the vector store use:
index.vectorstore

To access the VectorstoreRetriever use:
index.vectorstore.as_retriever()

This happens behind VectorstoreIndexCreator when documents are loaded:

    1. Split documents into chunks
    2. Create embeddings for each document
    3. Store documents and embeddings in the vectorstore

For details, see:
https://python.langchain.com/en/latest/modules/indexes/getting_started.html#walkthrough

For source, see:
https://github.com/hwchase17/langchain/blob/master/langchain/indexes/vectorstore.py#L51-L74
https://github.com/hwchase17/langchain/blob/master/langchain/indexes/vectorstore.py#L21-L48
"""
import os
import logging
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.document_loaders import UnstructuredHTMLLoader

logging.basicConfig(level=logging.INFO)

INDEX_DIR = os.getenv('OUTPUT', default='db')
FILES_DIR = os.getenv('INPUT', default='letters')
HTML_ENC = os.getenv('HTML_ENC', default='Windows-1252')

def index_files(directory=FILES_DIR, html_encoding=HTML_ENC):
    if os.path.exists(INDEX_DIR):
        raise AssertionError(f"Index directory '{INDEX_DIR}' already exists. Please delete it. You can also use it as-is.")

    loaders = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            logging.info(f"Indexing {file_path}")
            if file_ext == '.pdf':
                #
                # NOTE: PyPDFLoader is not very accurate:
                # Produces: April 30th at the  \nQwest for our annual W oodstock for Capitalists

                # UnstructuredPDFLoader is more accurate, but very slow:
                # Produces: April 30th at the Qwest for our annual Woodstock for Capitalists
                #
                loader = UnstructuredPDFLoader("letters/2004ltr.pdf", mode="elements")
            elif file_ext == '.html':
                loader = UnstructuredHTMLLoader(file_path, encoding=html_encoding)
            else:
                raise AssertionError(f"Unsupported file type: {file_path}")
            loaders.append(loader)
    if len(loaders) == 0:
        raise AssertionError(f"No loaders found for files in {directory}")
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": INDEX_DIR}).from_loaders(loaders)
    return index

if __name__ == "__main__":
    index_files()
