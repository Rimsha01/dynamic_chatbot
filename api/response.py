from langchain_community.utils.math import cosine_similarity
import models
from langchain_ollama import OllamaLLM
from service import embeddings_model
from sqlalchemy.orm import Session
from database import SessionLocal


mistral_llm =OllamaLLM(model = "mistral")

def generate_response(query:str,db:Session,file_id :int )-> str:
    document_chunks = db.query(models.DocumentChunk).filter(models.DocumentChunk.file_id == file_id).all()
    query_embedding = embeddings_model.embed_query(query)

    relevant_chunks = []
    for chunk in document_chunks:
        print(chunk)
        chunk_embedding = chunk.embeddings.reshape(1,-1)
        print(chunk_embedding)
        print(chunk_embedding.shape())
        similarity_score = cosine_similarity(chunk_embedding,query_embedding)
        if similarity_score >= 0.4:
            relevant_chunks.append(
                {"chunk": chunk,
                 "similarity" :similarity_score}
            )

    relevant_chunks.sort(key = lambda x: x["similarity"], reverse = True)
    top_chunks = []
    for chunk in relevant_chunks[:5]:
        top_chunks.append(chunk)

    if not top_chunks:
       return "I could not find relevant information to answer your question"

    # Build context from relevant chunks
    context = "\n\n".join([chunk["chunk"].content for chunk in top_chunks])

    # Create prompt for the LLM
    prompt = f"""You are a Dynamic Ai chatbot based on the provided context generate response.
    Context:
    {context}
    Question: {query}
    Answer:"""
    #Generate response using the LLM
    response = mistral_llm.invoke(prompt)

    return response


if __name__ == "__main__":
    generate_response("hyundai creta oil change price",SessionLocal(),20)
