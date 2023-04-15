"""
Evaluate PDF loaders
"""
from langchain.document_loaders import UnstructuredHTMLLoader
# Produces: April 30th at the Qwest for our annual Woodstock for Capitalists
from langchain.document_loaders import UnstructuredPDFLoader
# Produces: April 30th at the  \nQwest for our annual W oodstock for Capitalists
from langchain.document_loaders import PyPDFLoader # for loading the pdf

# See:
# https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/unstructured_file.html

loader1 = UnstructuredPDFLoader("letters/2004ltr.pdf", mode="elements")
loader2 = UnstructuredPDFLoader("letters/2004ltr.pdf")
print(loader1.load())
print("==================")
print(loader2.load())
