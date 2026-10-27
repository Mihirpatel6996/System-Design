class RealRetriever:
    def __init__(self):
        print("Connecting to Vector DB...")

        # simulate document store
        self.documents = {
            "hr": ["leave policy", "holiday list"],
            "finance": ["salary structure", "budget report"],
            "engineering": ["system design doc", "api spec"]
        }

    def search(self, query: str):
        print(f"[Retriever] Searching for: {query}")

        # naive: return everything (simulate vector match)
        results = []
        for category in self.documents:
            results.extend(self.documents[category])

        return results


# user

class User:
    def __init__(self, name, role, allowed_collections):
        self.name = name
        self.role = role
        self.allowed_collections = allowed_collections


# client

retriever = RealRetriever()

user = User(
    name="Mihir",
    role="employee",
    allowed_collections=["hr", "engineering"]
)

docs = retriever.search("salary")

print(docs)