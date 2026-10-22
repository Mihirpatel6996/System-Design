from abc import ABC, abstractmethod


class RAGIngestionPipeline(ABC):

    def run(self, source):
        data = self.load(source)
        chunks = self.chunk(data)
        embeddings = self.embed(chunks)
        self.store(embeddings)

    # Common/default steps
    def embed(self, chunks):
        print("[Common] Generating embeddings")

    def store(self, embeddings):
        print("[Common] Storing in vector DB")

    # Variable steps
    @abstractmethod
    def load(self, source):
        pass

    @abstractmethod
    def chunk(self, data):
        pass


# Data Load from PDF pipeline

class PDFPipeline(RAGIngestionPipeline):

    def load(self, file_path):
        print("[PDF] Reading PDF file")

    def chunk(self, data):
        print("[PDF] Splitting into semantic chunks")
        return ["chunk1", "chunk2"]


class WebPipeline(RAGIngestionPipeline):

    def load(self, url):
        print("[Web] Fetching HTML content")

    def chunk(self, data):
        print("[Web] Cleaning + chunking HTML")
        return ["chunk1", "chunk2"]

pdf = PDFPipeline()
pdf.run("file.pdf")

print()

web = WebPipeline()
web.run("https://example.com")



