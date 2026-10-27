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


# protected proxy retriever

class RetrieverProxy:
    def __init__(self, user: User):
        self.user = user
        self.real_retriever = RealRetriever()

    def search(self, query: str):
        print(f"\n[Proxy] User: {self.user.name} | Role: {self.user.role}")

        all_results = self.real_retriever.search(query)

        # apply access control filtering
        filtered_results = []

        for category, docs in self.real_retriever.documents.items():
            if category in self.user.allowed_collections:
                filtered_results.extend(docs)

        return filtered_results



if __name__ == "__main__":

    employee = User(
        name="Mihir",
        role="employee",
        allowed_collections=["hr", "engineering"]
    )

    finance_user = User(
        name="Rashmi",
        role="finance",
        allowed_collections=["hr", "finance"]
    )

    admin = User(
        name="Admin",
        role="admin",
        allowed_collections=["hr", "finance", "engineering"]
    )

    # Employee access
    proxy = RetrieverProxy(employee)
    print(proxy.search("salary"))

    # Finance access
    proxy = RetrieverProxy(finance_user)
    print(proxy.search("salary"))

    # Admin access
    proxy = RetrieverProxy(admin)
    print(proxy.search("salary"))