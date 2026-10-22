class PDFRAGPipeline:
    def run(self, file_path):
        print("Loading PDF")
        print("Chunking PDF")
        print("Embedding chunks")
        print("Storing in vector DB")


class WebRAGPipeline:
    def run(self, url):
        print("Fetching webpage")
        print("Cleaning HTML")
        print("Chunking content")
        print("Embedding chunks")
        print("Storing in vector DB")


# usage

if __name__ == "__main__":
    print("=== PDF RAG Pipeline ===")
    pdf_pipeline = PDFRAGPipeline()
    pdf_pipeline.run("data/sample.pdf")

    print("\n=== Web RAG Pipeline ===")
    web_pipeline = WebRAGPipeline()
    web_pipeline.run("https://example.com")


    """

    Problems (same as before, but worse now)
        - Duplicate logic
        - No observability hooks
        - No retry control
        - No consistency across pipelines


    At scale:
        10 ingestion types → 10 duplicated pipelines

    """