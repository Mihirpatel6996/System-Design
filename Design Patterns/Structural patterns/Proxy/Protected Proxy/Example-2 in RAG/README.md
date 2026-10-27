his is exactly where Protection Proxy becomes critical in production.
1. Problem Statement (Real-world)
You are building a RAG system for a company :
Data sources:
- HR docs (policies, leaves)
- Finance docs (salary, budgets)
- Engineering docs (architecture, APIs)
Users:
- Employee → can access HR + Engineering
- Finance team → HR + Finance
- Admin → everything
🔴 Critical Problem
Without access control:
query = "salary structure"docs = retriever.search(query)


👉 Any user can retrieve finance documents
This is a data leak.
2. Naive RAG (No Protection)
Let’s first build the wrong system.
2.1 Real Retriever
class RealRetriever:    def __init__(self):        print("Connecting to Vector DB...")        # simulate document store        self.documents = {            "hr": ["leave policy", "holiday list"],            "finance": ["salary structure", "budget report"],            "engineering": ["system design doc", "api spec"]        }    def search(self, query: str):        print(f"[Retriever] Searching for: {query}")        # naive: return everything (simulate vector match)        results = []        for category in self.documents:            results.extend(self.documents[category])        return results


2.2 User
class User:    def __init__(self, name, role, allowed_collections):        self.name = name        self.role = role        self.allowed_collections = allowed_collections


2.3 Client
retriever = RealRetriever()user = User(    name="Mihir",    role="employee",    allowed_collections=["hr", "engineering"])docs = retriever.search("salary")print(docs)


🔴 Output
['leave policy', 'holiday list',
 'salary structure', 'budget report',
 'system design doc', 'api spec']

❌ Problem
User is employee, but still sees:
salary structure
budget report

👉 Security violation
3. Where is the design flaw?
The flaw is:
RealRetriever is doing:
- retrieval
- AND (implicitly) no access control

It doesn’t even know who the user is.
4. Introduce Protection Proxy
We insert a control layer:
User
  ↓
RetrieverProxy (authorization)
  ↓
RealRetriever (data access)

5. Protection Proxy Implementation
5.1 Proxy Retriever
class RetrieverProxy:    def __init__(self, user: User):        self.user = user        self.real_retriever = RealRetriever()    def search(self, query: str):        print(f"\n[Proxy] User: {self.user.name} | Role: {self.user.role}")        all_results = self.real_retriever.search(query)        # apply access control filtering        filtered_results = []        for category, docs in self.real_retriever.documents.items():            if category in self.user.allowed_collections:                filtered_results.extend(docs)        return filtered_results


5.2 Client
if __name__ == "__main__":    employee = User(        name="Mihir",        role="employee",        allowed_collections=["hr", "engineering"]    )    finance_user = User(        name="Rashmi",        role="finance",        allowed_collections=["hr", "finance"]    )    admin = User(        name="Admin",        role="admin",        allowed_collections=["hr", "finance", "engineering"]    )    # Employee access    proxy = RetrieverProxy(employee)    print(proxy.search("salary"))    # Finance access    proxy = RetrieverProxy(finance_user)    print(proxy.search("salary"))    # Admin access    proxy = RetrieverProxy(admin)    print(proxy.search("salary"))


6. Output Analysis
Employee:
[Proxy] User: Mihir | Role: employee
['leave policy', 'holiday list', 'system design doc', 'api spec']

✔ Finance docs removed
Finance:
[Proxy] User: Rashmi | Role: finance
['leave policy', 'holiday list', 'salary structure', 'budget report']

✔ Correct access
Admin:
[Proxy] User: Admin | Role: admin
['leave policy', 'holiday list',
 'salary structure', 'budget report',
 'system design doc', 'api spec']

✔ Full access
7. System Design View
Now think beyond code.
Architecture
Client
  ↓
API Layer
  ↓
RetrieverProxy  ← (Authorization boundary)
  ↓
Vector DB / Index

Why proxy here is critical
Because:
Vector DB does NOT understand business-level permissions

It only understands:
embedding similarity

8. Real-world equivalent (very important)
This pattern exists in:
1. OpenAI / Azure AI
- API gateway checks API key, quotas → proxy
2. LangChain / LlamaIndex
- You wrap retrievers with filters
3. Enterprise RAG systems
- Tenant isolation
- Role-based filtering
9. What breaks at scale (important)
Let’s stress this design.
Problem 1: Inefficient filtering
all_results = self.real_retriever.search(query)


Then filter.
👉 Bad because:
- you fetch unauthorized data first
- then discard
Better design:
Push filter down to DB layer
RetrieverProxy → passes allowed_collections → DB query

Problem 2: Tight coupling
Proxy directly accessing:
self.real_retriever.documents


👉 Not scalable
Problem 3: No caching / batching
Each request:
- hits DB
- does filtering
10. Production-grade evolution
Real system becomes:
User
 ↓
Auth Service (JWT / roles)
 ↓
Retriever Proxy
 ↓
Query Builder (adds filters)
 ↓
Vector DB (filtered search)
 ↓
LLM

11. Key Insight (This is what you should remember)
Protection Proxy in RAG =
“Never allow raw retrieval without access control”