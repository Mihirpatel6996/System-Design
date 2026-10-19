1. Problem (Real-World Framing)
You are building something like:
- File system (your example)
- UI tree (buttons, panels, containers)
- Organization hierarchy (CEO → Managers → Employees)
- Product catalog (Category → Subcategory → Product)
Common pattern:
Everything forms a tree (hierarchical structure)

Now ask yourself:
- You want to calculate total size
- You want to print structure
- You want to apply operation recursively
👉 The key tension:
- Files are leaf nodes
- Folders are containers
But you want to treat them uniformly
2. Definition (What Composite Actually Solves)
Composite Pattern:
Treat individual objects (leaf) and groups of objects (composite) the same way using a common interface.

Why this matters (don’t skip this)
Without composite:
- You write:if isinstance(obj, File):    ...elif isinstance(obj, Folder):    ...
- Logic spreads everywhere
- Every new operation = duplicated branching
With composite:
- You just call:obj.get_size()obj.open()obj.ls()
- And each object handles itself
3. First — Naive Implementation (Python)
Let’s intentionally NOT use composite properly.
Problem approach:
- Files and Folders are different types
- Caller needs to know what type it’s dealing with
class File:    def __init__(self, name, size):        self.name = name        self.size = size    def get_size(self):        return self.sizeclass Folder:    def __init__(self, name):        self.name = name        self.children = []    def add(self, item):        self.children.append(item)    def get_size(self):        total = 0        for item in self.children:            # ❌ Type checking everywhere            if isinstance(item, File):                total += item.get_size()            elif isinstance(item, Folder):                total += item.get_size()        return total


Usage
root = Folder("root")root.add(File("a.txt", 10))docs = Folder("docs")docs.add(File("b.txt", 20))root.add(docs)print(root.get_size())  # 30


4. What’s Wrong Here?
1. Type Awareness Everywhere
You must know:
- Is it File?
- Is it Folder?
👉 Violates abstraction
2. Adding New Type = Break Everything
Now suppose you add:
class ZipFile:    def get_size(self):        ...


Now you must update:
if isinstance(item, ZipFile):


👉 Every place breaks
3. Caller Complexity
Imagine this:
def print_structure(item):    if isinstance(item, File):        print(item.name)    elif isinstance(item, Folder):        ...


👉 Logic duplication across system
5. Core Insight (This is the “aha”)
Instead of:
“What type are you?”

We want:
“I don’t care what you are, just do your job.”

So we enforce:
item.get_size()item.ls()item.open()


6. What Composite Changes (Mentally)
You stop thinking:
Folder → contains Files

You start thinking:
Node → contains Nodes

And:
Node = File OR Folder

Good. Now we fix everything that was messy in the naive version.
We are not changing the problem.
We are changing how we model the system.
1. Goal (Reframe Before Code)
We want this to work:
item.get_size()item.ls()item.open_all()


Without caring:
is it File?is it Folder?


2. Core Design (Composite Thinking)
Instead of:
Folder → contains File

We move to:
FileSystemItem (base)
    ├── File (leaf)
    └── Folder (composite)
            └── contains List[FileSystemItem]

Key shift:
Folder does NOT store File or Folder
Folder stores FileSystemItem

3. Python Implementation (Composite Pattern)
Base Interface
from abc import ABC, abstractmethodclass FileSystemItem(ABC):    @abstractmethod    def ls(self, indent):        pass    @abstractmethod    def open_all(self, indent):        pass    @abstractmethod    def get_size(self):        pass    @abstractmethod    def get_name(self):        pass


Leaf → File
class File(FileSystemItem):    def __init__(self, name, size):        self.name = name        self.size = size    def ls(self, indent):        print(" " * indent + self.name)    def open_all(self, indent):        print(" " * indent + self.name)    def get_size(self):        return self.size    def get_name(self):        return self.name


Composite → Folder
class Folder(FileSystemItem):    def __init__(self, name):        self.name = name        self.children = []    def add(self, item: FileSystemItem):        self.children.append(item)    def ls(self, indent):        print(" " * indent + "+ " + self.name)        for child in self.children:            child.ls(indent + 4)    def open_all(self, indent):        print(" " * indent + "+ " + self.name)        for child in self.children:            child.open_all(indent + 4)    def get_size(self):        total = 0        for child in self.children:            # ✅ No type checking            total += child.get_size()        return total    def get_name(self):        return self.name


4. Usage
root = Folder("root")root.add(File("file1.txt", 10))root.add(File("file2.txt", 20))docs = Folder("docs")docs.add(File("resume.pdf", 30))docs.add(File("notes.txt", 40))images = Folder("images")images.add(File("photo.jpg", 50))root.add(docs)root.add(images)root.ls(0)print("\nOpen All:\n")root.open_all(0)print("\nTotal Size:", root.get_size())


5. What Just Changed (Critical Insight)
❌ Before (Naive)
if isinstance(item, File):    ...elif isinstance(item, Folder):    ...


✅ Now
item.get_size()item.ls()


No branching. No type checks.
6. Why This Works
Because:
- File knows how to behave
- Folder knows how to behave
- Caller does not need to know anything
7. Real System Analogy (Important)
Think about your RAG system.
You may have:
Retriever
    ├── BM25Retriever
    ├── VectorRetriever
    └── HybridRetriever

Now imagine:
QueryPlan
    ├── SingleRetriever
    └── MultiRetriever (contains list of retrievers)

👉 Composite lets you treat:
retrieve(query)


Same whether:
- Single retriever
- Chain of retrievers
8. Trade-offs
Pros
- Clean recursion
- Extensible (add new node types easily)
- No type checking
Cons (important for system design)
1. Harder to restrict behavior
Example:
- File should not have add()
- Folder should
But both share interface
→ You either:
- Throw runtime errors
- Or separate interfaces (more complexity)
2. Overkill for simple systems
If tree depth is small:
→ naive might be simpler
9. Complexity
Let:
- N = total nodes
get_size()
- Time: O(N)
- Space: O(H) recursion stack (H = height)
10. Where It Breaks at Scale
Think bigger system:
Millions of nodes (like real FS or org tree)

Problems:
1. Deep recursion → stack overflow
2. Traversal becomes expensive
3. Recomputing size repeatedly → slow
11. What You’d Do in Production
You won’t rely purely on composite.
You’ll add:
- Cachingfolder.size_cache
- Lazy loading
  (don’t load children until needed)
- Iterative traversal
  (avoid recursion)
12. Final Mental Model
Composite is NOT about files/folders.
It is about:
“Tree structures where individual and group should behave the same”