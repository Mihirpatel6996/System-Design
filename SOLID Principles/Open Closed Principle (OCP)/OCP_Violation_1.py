# Navie Implementation of Open Closed Principle

class Retriever:

    def retrieve(self, query_embedding, strategy="length"):
        
        if strategy == "length":
            return self._length_based(query_embedding)

        elif strategy == "keyword":
            return self._keyword_based(query_embedding)

        elif strategy == "cosine":
            return self._cosine_similarity(query_embedding)

        else:
            raise ValueError("Unknown strategy")

    def _length_based(self, query_embedding):
        return "patient_1"

    def _keyword_based(self, query_embedding):
        return "patient_2"

    def _cosine_similarity(self, query_embedding):
        return "patient_3"

## Every time we have to add a new strategy we have to modify the retriever class which violates the open closed principle
## This is not a good design as we have to modify the existing code to add new functionality.

'''
Stop and Think

Answer this:

What happens when we add BM25 retrieval?
What happens when we add Hybrid retrieval?
What happens when ML team experiments weekly?

Every time → you modify this class.

'''


'''
Why this violated OCP 

1. The class is not open for extension. Every time we want to add a new retrieval strategy, we have to modify the existing class. This violates the open-closed principle which states that classes should be open for extension but closed for modification.
2. The class is not closed for modification. Every time we want to add a new retrieval strategy, we have to modify the existing class. This violates the open-closed principle which states that classes should be open for extension but closed for modification.
'''


## solution --> one Interface and multiple implementations

## refer OCP_Example_1.py for solution

