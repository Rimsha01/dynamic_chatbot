from fastapi import HTTPException, status
import  models
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path


print("loading model")
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)
print("success")



def validate_file_extension(filename: str):
    if not filename.lower().endswith((".csv", ".txt")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Upload file in CSV or text format only"
        )

def validate_file_size(raw_data: bytes , max_file_size= 10*1024*1024 ):
    if len(raw_data) > max_file_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="file should be less than or equal to 10 mb"
        )

def create_upload_dir(upload_dir: str = "uploads") -> Path:
    upload_path = Path(upload_dir)
    upload_path.mkdir(exist_ok=True)
    return upload_path

def check_filename(filename:str = "uploads"):
    safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
    return safe_filename


def chunk_text(content: str,chunk_size: int = 250,chunk_overlap:int = 75 )-> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size= chunk_size,
        chunk_overlap=chunk_overlap
    )
    documents = [Document(page_content=content)]
    return text_splitter.split_documents(documents)

def generate_embeddings(texts:List[str]) -> List[List[float]]:
    return embeddings_model.embed_documents(texts)

def save_chunks(split_docs: List[Document], embeddings: List, file_id: int) -> List[models.DocumentChunk]:
    chunks = []
    for i, (doc, embedding) in enumerate(zip(split_docs, embeddings)):
        # Simple type assertion for safety
        if not isinstance(embedding, list):
            raise ValueError(f"Unexpected embedding type: {type(embedding)}")

        chunk = models.DocumentChunk(file_id=file_id,
                                     chunk_text=doc.page_content,
                                     embeddings=embedding,
                                     chunk_index=i
                                     )
        chunks.append(chunk)

    return chunks


