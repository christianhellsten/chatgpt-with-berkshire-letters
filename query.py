"""
Tries to answer questions by using ChatGPT and embeddings stored locally in a vector database.
"""
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma

def load_index():
    vectorstore = Chroma(persist_directory='db', embedding_function=OpenAIEmbeddings())
    return VectorStoreIndexWrapper(vectorstore=vectorstore)

def query_index(index, question, chain_type='map_rerank'):
    """
    Default chain type:
    'stuff', 'map_reduce', 'refine', 'map_rerank'

    See:
    https://github.com/hwchase17/langchain/blob/master/langchain/chains/retrieval_qa/base.py#L77-L89
    """
    return index.query_with_sources(question, chain_type=chain_type)

def run_queries(index, queries):
    for query in queries:
        print(f"Query: {query}\nAnswer: {query_index(index, query)}\n")

def get_relevant_documents(index, query):
    retriever = index.vectorstore.as_retriever()
    docs = retriever.get_relevant_documents(query)
    return docs

def main():
    index = load_index()
    queries = [
        "Which year and month did Berkshire buy Coca-Cola?", # wrong
        "How much in cash dividend does Berkshire get from Coca-Cola each year?",
        "How much in cash dividend does Berkshire get from American Express each year?",
        "Why did Berkshire buy Alleghany Corporation?"
    ]
    # queries = [
    #     # "What is the dumbest investment decisions ever made by Berkshire?"
    #     # "Tell me about the textile business",
    #     "Why does Berkshire use float?", # I don't know
    #     # "You are an article writer for The Financial Times. Can you write 100 words about Warren Buffet?", # I don't know
    #     # "What happened in 1977?", # I don't know
    #     "Which year was the worst for Berkshire?", # The nine years following the merger of Berkshire Fine Spinning Associates and Hathaway Manufacturing in 1955 were the worst for Berkshire, with the company's net worth shrinking by 37%.
    # ]
    run_queries(index, queries)

if __name__ == "__main__":
    main()
