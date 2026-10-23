class DocumentReader:
    def unlock_pdf(self, file_path: str, password: str):
        print(f"[DocumentReader] Unlocking PDF: {file_path}")
        print(f"[DocumentReader] PDF unlocked using password: {password}")
        print("[DocumentReader] Displaying PDF content...")


class User:
    def __init__(self, name: str, premium_membership: bool):
        self.name = name
        self.premium_membership = premium_membership

user = User("Rohan", False)

reader = DocumentReader()

reader.unlock_pdf(
    "protected_document.pdf",
    "secret123"
)

"""
We have a problem.
Rohan is:
premium_membership = False

Yet nothing prevents him from calling:
reader.unlock_pdf(...)

"""