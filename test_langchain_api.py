"""
Chat with Meta

wget "https://s21.q4cdn.com/399680738/files/doc_financials/2022/q4/Meta-12.31.2022-Exhibit-99.1-FINAL.pdf"
mv *.pdf pdfs
python test_langchain_api.py
"""
import os
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator

pdfs_folder = 'pdfs'
loaders = [UnstructuredPDFLoader(os.path.join(pdfs_folder, fn)) for fn in os.listdir(pdfs_folder)]
index = VectorstoreIndexCreator().from_loaders(loaders)

if __name__ == "__main__":
    while True:
        print("Question:")
        question = input()
        print("Answer:")
        print(index.query(question))
