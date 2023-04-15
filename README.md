# ChatGPT + LangChain + Berkshire Hathaway Letters

Fine tuning ChatGPT is expensive, so let's instead use:

- Python
- LangChain: ”LangChain primary focuses on constructing indexes with the goal of using them as a Retriever.”
- Chroma: a vector database that we use for storing and searching for OpenAI embeddings created from chunks of text

## Installation

```bash
$ brew install poppler pipenv
$ pipenv install
$ export OPENAI_API_KEY=sk-abc123de45fghij6789k0lmnopq12r3st4uvwxyz
$ python download.py
$ python index.py
$ python app.py
```

## References

https://github.com/hwchase17/langchain/blob/master/langchain/chains/qa_with_sources/stuff_prompt.py
https://github.com/hwchase17/langchain/blob/master/langchain/chains/qa_with_sources/map_reduce_prompt.py
https://github.com/hwchase17/langchain/blob/master/langchain/chains/qa_with_sources/refine_prompts.py
