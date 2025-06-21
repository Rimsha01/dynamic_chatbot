from  typing import List
from langchain_community.utils.math import cosine_similarity
from . import models
from langchain_ollama import OllamaLLM
from .service import embeddings_model

mistral_llm =OllamaLLM(model = "mistral")

def generate_response(query:str,
                      document_chunks : List[models.DocumentChunk],
                      max_context_chunks :int = 5,
                      similarity_threshold :float = 0.4
                      )-> str:
    query_embedding = embeddings_model.embed_query(query)

    relevant_chunks = []
    for chunk in document_chunks:
        chunk_embedding = chunk.embeddings
        similarity_score = cosine_similarity(chunk_embedding,query_embedding)
        if similarity_score >= similarity_threshold:
            relevant_chunks.append(
                {"chunk": chunk,
                 "similarity" :similarity_score}
            )

    relevant_chunks.sort(key = lambda x: ["similarity_score"], reverse = True)
    top_chunks = [c ["chunk"] for c in  relevant_chunks[:max_context_chunks]]

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


