1. Problem (Real-world framing)
You are building a system:
Client → Reporting System → expects JSON

But suddenly:
- A third-party provider gives you data in XML
- You cannot change that provider (external system)
So mismatch:
Client wants: JSON
Provider gives: XML

This is the core problem:
Two components exist, but their interfaces don’t match.

2. Definition (Simple, not textbook)
Adapter Pattern = Convert one interface into another that the client expects.
In simple terms:
“Don’t change existing code. Just put a translator in between.”

3. Naive Implementation (Without Adapter)
Let’s first write the bad version.
What happens in naive design?
Client directly talks to XML provider and converts manually.
Python Code (Naive)
class XmlDataProvider:    def get_xml_data(self, data: str) -> str:        name, id_ = data.split(":")        return f"<user><name>{name}</name><id>{id_}</id></user>"class Client:    def get_report(self, provider: XmlDataProvider, raw_data: str):        # Client is forced to understand XML 😐        xml = provider.get_xml_data(raw_data)        # Manual parsing inside client (bad)        name = xml.split("<name>")[1].split("</name>")[0]        id_ = xml.split("<id>")[1].split("</id>")[0]        json_data = f'{{"name": "{name}", "id": {id_}}}'        print("Processed JSON:", json_data)if __name__ == "__main__":    provider = XmlDataProvider()    client = Client()    client.get_report(provider, "Alice:42")


4. Why this is BAD (this is the real learning)
Now think like a system designer.
Problem 1: Tight coupling
Client now knows:
- XML structure
- Parsing logic
- Data format
If XML changes → client breaks
Problem 2: Violates Single Responsibility
Client is doing:
- Business logic ❌
- Data transformation ❌
Problem 3: No extensibility
Tomorrow:
- Another provider gives CSV
- Another gives YAML
Now client becomes:
if xml:
    parse xml
elif csv:
    parse csv
elif yaml:
    parse yaml

This is where systems die.
Problem 4: Code duplication
Every client will rewrite parsing logic.
5. Key Insight (This is where Adapter is born)
Ask yourself:
Why is the client doing conversion at all?

It shouldn't.
Instead:
Client → wants JSON → should always get JSON

So we need:
Something in between that converts XML → JSON

That “something” is the Adapter.
6. Mental Model
Think:
- Mobile charger vs different plug types
- You don’t change the phone
- You don’t change the socket
- You add an adapter
Socket (XML) → Adapter → Phone (JSON expectation)

7. Adapter Pattern 

1. Target Interface (What client expects)
Client should not care about XML, CSV, etc.
It should only know:
class IReports:    def get_json_data(self, data: str) -> str:        raise NotImplementedError


2. Adaptee (Existing system — unchanged)
class XmlDataProvider:    def get_xml_data(self, data: str) -> str:        name, id_ = data.split(":")        return f"<user><name>{name}</name><id>{id_}</id></user>"


This is external / legacy / third-party.
We do not touch this.
3. Adapter (Core of the pattern)
This is the important piece.
It:
- Implements IReports
- Internally uses XmlDataProvider
- Converts XML → JSON
Python Implementation
class XmlDataProviderAdapter(IReports):    def __init__(self, xml_provider: XmlDataProvider):        self.xml_provider = xml_provider    def get_json_data(self, data: str) -> str:        # Step 1: Get XML from adaptee        xml = self.xml_provider.get_xml_data(data)        # Step 2: Parse XML (same logic, but now isolated)        name = xml.split("<name>")[1].split("</name>")[0]        id_ = xml.split("<id>")[1].split("</id>")[0]        # Step 3: Convert to JSON        return f'{{"name": "{name}", "id": {id_}}}'


4. Client (Now CLEAN)
Notice the difference carefully.
class Client:    def get_report(self, report: IReports, raw_data: str):        print("Processed JSON:", report.get_json_data(raw_data))


Client:
- Doesn’t know XML exists
- Doesn’t parse anything
- Only talks to IReports
5. Execution (Flow)
if __name__ == "__main__":    # Step 1: Create adaptee    xml_provider = XmlDataProvider()    # Step 2: Wrap it inside adapter    adapter = XmlDataProviderAdapter(xml_provider)    # Step 3: Client uses adapter    client = Client()    client.get_report(adapter, "Alice:42")


6. Execution Trace (VERY IMPORTANT)
Let’s walk like a debugger:
Client.get_report(adapter, "Alice:42")

→ adapter.get_json_data("Alice:42")

    → xml_provider.get_xml_data("Alice:42")
        → "<user><name>Alice</name><id>42</id></user>"

    → parse XML
        → name = "Alice"
        → id = "42"

    → return JSON
        → {"name": "Alice", "id": 42}

→ Client prints result

7. What Problem Did We Actually Solve?
Compare with naive:
Before
Client = parsing + logic + format handling

After
Client → Interface → Adapter → Adaptee

8. Why This Matters (Real Systems)
Now think at scale.
Case: You add CSV provider
You just create:
class CsvDataProviderAdapter(IReports):    ...


Client code?
UNCHANGED
9. Architecture View
Client
   ↓
IReports (contract)
   ↓
Adapter (XML → JSON)
   ↓
XmlDataProvider

10. Trade-offs (Important)
Pros
- Decouples client from formats
- Easy to add new providers
- Clean separation of concerns
Cons
- Extra class layer
- Slight overhead (conversion cost)
- Can become messy if too many adapters
11. When This Fails
At scale:
1. Heavy transformation
If XML → JSON is huge (MBs of data):
- String parsing becomes bottleneck
- You need streaming / proper parsers
2. Too many formats
If 20+ formats:
- Adapter explosion happens
Solution:
- Use strategy + factory + adapter combo
3. Performance-sensitive systems
Adapters add:
- CPU cost
- Latency
12. Core Intuition (Final)
Adapter is NOT about code.
It’s about:
“I cannot change existing systems, but I still want them to work together.”