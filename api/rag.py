from langchain_huggingface import HuggingFaceEmbeddings
from numpy.linalg import norm

from service import embeddings
import numpy as np

embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)


def cosine_similarity(a, b):
    return np.dot(a, b)/(norm(a)*norm(b))

def generate_response(query ):
    query_embedding =embeddings_model.embed_query(query)

    for e, q in zip (embeddings,query_embedding):
        similarity_score = cosine_similarity(e,q)
        if similarity_score >= 0.4:
            print()



    return