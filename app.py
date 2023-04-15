from query import load_index
from query import query_index

if __name__ == "__main__":
    index = load_index()
    while True:
        print("Question:")
        question = input()
        print("Answer:")
        print(query_index(index, question))
