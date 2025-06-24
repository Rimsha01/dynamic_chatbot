from langchain_community.utils.math import cosine_similarity
from . import models
from langchain_ollama import OllamaLLM
from . service import embeddings_model
from sqlalchemy.orm import Session
from . database import SessionLocal
import numpy as np


mistral_llm =OllamaLLM(model = "mistral")

def generate_response(query:str,db:Session,file_id :int )-> str:
    document_chunks = db.query(models.DocumentChunk).filter(models.DocumentChunk.file_id == file_id).all()
    query_embedding = np.array(embeddings_model.embed_query(query)).squeeze().reshape(1,-1)

    relevant_chunks = []
    for chunk in document_chunks:
        chunk_embedding = np.array(chunk.embeddings).reshape(1,-1)
        similarity_score = cosine_similarity(chunk_embedding,query_embedding)
        if similarity_score >= 0.3:
            relevant_chunks.append(
                {"chunk": chunk,
                 "similarity" :similarity_score},

            )


    relevant_chunks.sort(key = lambda x: x["similarity"], reverse = True)
    top_chunks= relevant_chunks[:5]


    if not top_chunks:
       return "I could not find relevant information to answer your question"

    # Build context from relevant chunks
    context = "\n\n".join([chunk["chunk"].chunk_text  for chunk in top_chunks])

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
    resp = generate_response("give the exact pricing detail for Hyundai car wash interior and exterior",SessionLocal(),20)
    print(resp)
