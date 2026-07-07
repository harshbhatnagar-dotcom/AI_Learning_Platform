from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=50
)

def create_chunks(text):
    chunks = splitter.split_text(text)
    return chunks