With Virtual Proxy, the proxy controlled when the expensive object gets created.
With Protection Proxy, the proxy controls:
Who is allowed to access the real object or operation.

So the problem is no longer lazy loading. The problem is authorization.
1. Definition
A Protection Proxy sits between the client and the real object and checks whether the client has permission to perform an operation.
Architecture:
Client
  |
  v
Protection Proxy
  |
  | check permission
  |
  +---- denied ---> return / error
  |
  +---- allowed --> Real Object

The important part is that the client should ideally not bypass the proxy and directly call the real object.
2. First understand the problem without Proxy
Suppose we have a PDF service where only premium users can unlock protected PDFs.
A naive implementation might look like this:
class DocumentReader:    def unlock_pdf(self, file_path: str, password: str):        print(f"[DocumentReader] Unlocking PDF: {file_path}")        print(f"[DocumentReader] PDF unlocked using password: {password}")        print("[DocumentReader] Displaying PDF content...")class User:    def __init__(self, name: str, premium_membership: bool):        self.name = name        self.premium_membership = premium_membership


Client code:
user = User("Rohan", False)reader = DocumentReader()reader.unlock_pdf(    "protected_document.pdf",    "secret123")


Output:
[DocumentReader] Unlocking PDF: protected_document.pdf
[DocumentReader] PDF unlocked using password: secret123
[DocumentReader] Displaying PDF content...

We have a problem.
Rohan is:
premium_membership = False

Yet nothing prevents him from calling:
reader.unlock_pdf(...)


The DocumentReader only knows:
"Someone asked me to unlock a PDF."

It doesn't care who that person is.
3. One obvious solution
You could put the permission check directly inside DocumentReader.
class DocumentReader:    def unlock_pdf(self, user, file_path, password):        if not user.premium_membership:            print("Access denied")            return        print(f"Unlocking {file_path}")


This works.
But now the real document service has two responsibilities:
DocumentReader
    |
    +-- PDF handling
    |
    +-- Authorization

That's undesirable.
Tomorrow you may have:
Admin access
Enterprise access
Premium access
Region restrictions
Subscription expiry
Document ownership
Role permissions

Your PDF class starts turning into this:
if user.is_premium:    ...if user.subscription_active:    ...if user.region_allowed:    ...if user.role == "admin":    ...if document.owner == user.id:    ...


The document-reading logic gets buried under authorization logic.
4. Protection Proxy separates these responsibilities
We create:
DocumentProxy

whose responsibility is:
Decide whether the request is allowed.

And:
RealDocumentReader

whose responsibility is:
Actually perform the document operation.

Architecture:
User
 |
 v
DocumentProxy
 |
 | premium?
 |
 +------ No ------> Access denied
 |
 Yes
 |
 v
RealDocumentReader
 |
 v
Unlock PDF

5. Python implementation
First, let's define a common interface.
In Python we can use ABC.
from abc import ABC, abstractmethodclass IDocumentReader(ABC):    @abstractmethod    def unlock_pdf(self, file_path: str, password: str):        pass


Now the real implementation:
class RealDocumentReader(IDocumentReader):    def unlock_pdf(self, file_path: str, password: str):        print(            f"[RealDocumentReader] Unlocking PDF at: {file_path}"        )        print(            f"[RealDocumentReader] PDF unlocked successfully "            f"with password: {password}"        )        print(            "[RealDocumentReader] Displaying PDF content..."        )


Notice something important.
There is zero authorization logic here.
RealDocumentReader only knows how to work with documents.
6. User class
class User:    def __init__(        self,        name: str,        premium_membership: bool    ):        self.name = name        self.premium_membership = premium_membership


7. Protection Proxy
Now comes the important part.
class DocumentProxy(IDocumentReader):    def __init__(self, user: User):        self.user = user        self.real_reader = RealDocumentReader()    def unlock_pdf(self, file_path: str, password: str):        if not self.user.premium_membership:            print(                f"[DocumentProxy] Access denied for {self.user.name}. "                "Only premium members can unlock PDFs."            )            return        self.real_reader.unlock_pdf(            file_path,            password        )


This line is the heart of Protection Proxy:
if not self.user.premium_membership:


The proxy intercepts the request before the real object receives it.
8. Client code
if __name__ == "__main__":    rohan = User(        name="Rohan",        premium_membership=False    )    rashmi = User(        name="Rashmi",        premium_membership=True    )    print("=== Rohan tries to unlock PDF ===")    reader: IDocumentReader = DocumentProxy(rohan)    reader.unlock_pdf(        "protected_document.pdf",        "secret123"    )    print("\n=== Rashmi tries to unlock PDF ===")    reader = DocumentProxy(rashmi)    reader.unlock_pdf(        "protected_document.pdf",        "secret123"    )


Output:
=== Rohan tries to unlock PDF ===

[DocumentProxy] Access denied for Rohan.
Only premium members can unlock PDFs.


=== Rashmi tries to unlock PDF ===

[RealDocumentReader] Unlocking PDF at: protected_document.pdf
[RealDocumentReader] PDF unlocked successfully with password: secret123
[RealDocumentReader] Displaying PDF content...

9. Trace Rohan's request carefully
This is where the pattern becomes clear.
Client writes:
reader = DocumentProxy(rohan)


We now have:
reader
  |
  v
DocumentProxy
  |
  +-- user = Rohan
  |
  +-- real_reader = RealDocumentReader

Then:
reader.unlock_pdf(...)


Python enters:
DocumentProxy.unlock_pdf()


The proxy checks:
if not self.user.premium_membership:


Rohan:
premium_membership = False

Therefore:
return


Execution stops.
The following code is never reached:
self.real_reader.unlock_pdf(...)


So the real object never receives the unauthorized request.
10. Rashmi's request
Now:
reader = DocumentProxy(rashmi)


Rashmi has:
premium_membership = True

Therefore this condition:
if not self.user.premium_membership:


becomes false.
Execution continues:
self.real_reader.unlock_pdf(    file_path,    password)


Now:
Client
   ↓
Proxy
   ↓
permission check ✓
   ↓
RealDocumentReader
   ↓
PDF operation

That is Protection Proxy.
11. The clever part: same interface
Notice this:
class RealDocumentReader(IDocumentReader)


and:
class DocumentProxy(IDocumentReader)


Both provide:
unlock_pdf()


Therefore from the client's perspective:
reader.unlock_pdf(...)


The client doesn't need to care whether reader is:
RealDocumentReader

or:
DocumentProxy

This is important.
The proxy is designed to look like the real object.
That's what allows it to sit transparently between client and real service.
12. Why not just use an if statement in the client?
You could write:
if user.premium_membership:    reader.unlock_pdf(...)


But that's a weak design.
Imagine you have:
Web API
Mobile API
Desktop application
Admin dashboard
Background worker
CLI application

Every client must remember:
if user.premium_membership:


Eventually somebody forgets.
Then:
Client A → checks permission
Client B → checks permission
Client C → forgot permission check
                         ↓
                   security problem

Protection Proxy centralizes it:
Client A ─┐
Client B ─┼──> DocumentProxy ──> RealDocumentReader
Client C ─┘
                 ↑
           authorization
           happens here

That is much more important than merely avoiding duplicate if statements.
You're creating an access boundary.
13. One thing I would change from your Java example
Your Java code creates the real reader immediately:
public DocumentProxy(User user) {
    this.realReader = new RealDocumentReader();
    this.user = user;
}

That's completely valid for a Protection Proxy.
Remember:
Virtual Proxy
Usually does:
self.real_reader = None


because its purpose is lazy creation.
Protection Proxy
Can do:
self.real_reader = RealDocumentReader()


because its purpose is authorization.
These are two different Proxy motivations.
You could even combine them:
class DocumentProxy(IDocumentReader):    def __init__(self, user):        self.user = user        self.real_reader = None    def unlock_pdf(self, file_path, password):        # Protection Proxy behavior        if not self.user.premium_membership:            print("Access denied")            return        # Virtual Proxy behavior        if self.real_reader is None:            self.real_reader = RealDocumentReader()        self.real_reader.unlock_pdf(            file_path,            password        )


Now the same proxy is doing:
1. Authorization
2. Lazy initialization

Possible, although in a larger production system I'd generally separate concerns more carefully.
14. Think about this from a RAG/FDE perspective
This pattern becomes much more useful when you replace:
PDF Reader

with:
RAG Knowledge Base

Imagine Cognizant has:
HR documents
Finance documents
Engineering documents
Customer documents

A naive retriever:
retriever.search("salary policy")


might retrieve anything the vector database contains.
That's dangerous.
Instead:
User
 ↓
ProtectedRetrieverProxy
 ↓
Check:
 - tenant
 - role
 - document permissions
 ↓
RealRetriever
 ↓
Vector DB

For example:
class RetrieverProxy:    def __init__(self, user, real_retriever):        self.user = user        self.real_retriever = real_retriever    def search(self, query):        if "finance" not in self.user.allowed_collections:            raise PermissionError(                "User cannot access finance documents"            )        return self.real_retriever.search(query)


Now we're approaching something very real:
Authorization-aware RAG retrieval.

Without this, a multi-tenant RAG system can leak one customer's documents to another customer.
That is a far more important use of Protection Proxy than the PDF example.
15. Virtual Proxy vs Protection Proxy
Keep this distinction clear:
Virtual Proxy	Protection Proxy
Controls when real object is created/accessed	Controls who can access real object
Performance/resource optimization	Security/access control
Lazy loading	Authorization
Expensive object	Sensitive operation
if real_object is None	if user.has_permission()


The structure looks nearly identical:
Client → Proxy → Real Object

But the reason the proxy exists is different.
That distinction matters more than memorizing the code.