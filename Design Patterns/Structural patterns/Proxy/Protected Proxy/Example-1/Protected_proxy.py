from abc import ABC, abstractmethod


class IDocumentReader(ABC):

    @abstractmethod
    def unlock_pdf(self, file_path: str, password: str):
        pass


# this is real pdf unlocker that does the actual work of unlocking and displaying the pdf but it is not protected and can be called by anyone

class RealDocumentReader(IDocumentReader):

    def unlock_pdf(self, file_path: str, password: str):

        print(
            f"[RealDocumentReader] Unlocking PDF at: {file_path}"
        )

        print(
            f"[RealDocumentReader] PDF unlocked successfully "
            f"with password: {password}"
        )

        print(
            "[RealDocumentReader] Displaying PDF content..."
        )

# user class to represent a user with a name and premium membership status

class User:

    def __init__(
        self,
        name: str,
        premium_membership: bool
    ):
        self.name = name
        self.premium_membership = premium_membership

#protection proxy that checks if the user has premium membership before allowing access to the real document reader

class DocumentProxy(IDocumentReader):

    def __init__(self, user: User):
        self.user = user
        self.real_reader = RealDocumentReader()

    def unlock_pdf(self, file_path: str, password: str):

        if not self.user.premium_membership:

            print(
                f"[DocumentProxy] Access denied for {self.user.name}. "
                "Only premium members can unlock PDFs."
            )

            return

        self.real_reader.unlock_pdf(
            file_path,
            password
        )

if __name__ == "__main__":

    rohan = User(
        name="Rohan",
        premium_membership=False
    )

    rashmi = User(
        name="Rashmi",
        premium_membership=True
    )

    print("=== Rohan tries to unlock PDF ===")

    reader: IDocumentReader = DocumentProxy(rohan)

    reader.unlock_pdf(
        "protected_document.pdf",
        "secret123"
    )

    print("\n=== Rashmi tries to unlock PDF ===")

    reader = DocumentProxy(rashmi)

    reader.unlock_pdf(
        "protected_document.pdf",
        "secret123"
    )