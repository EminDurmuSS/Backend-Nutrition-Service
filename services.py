# services.py
from typing import Dict, Any
from embeddings import get_embedding, query_pinecone

def map_ingredient(ingredient_text: str, top_k: int = 7) -> Dict[str, Any]:
    """
    For the given ingredient_text, compute its embedding,
    query Pinecone for the top_k USDA candidates, and return:
      - the original input,
      - the default mapping (using the candidate’s ingredientId if available),
      - and a list of candidate mappings (each with name, score, and ingredientId).
    """
    # 1) Get embedding from OpenAI.
    embedding = get_embedding(ingredient_text)
    # 2) Query Pinecone.
    matches = query_pinecone(embedding, top_k)
    # 3) Build a list of candidate dicts.
    candidates = []
    for match in matches:
        candidate = {
            "input": ingredient_text,
            "best_usda_name": match.get("metadata", {}).get("ingredientName"),
            "score": float(match.get("score", 0.0)),
            "ingredientId": match.get("id")
        }
        print("for debug: ", candidate)
        candidates.append(candidate)
    # 4) Default mapping = top1's "ingredientId" if available.
    if candidates:
        top_candidate = candidates[0]
        default_mapping = top_candidate["ingredientId"] or top_candidate["best_usda_name"]
    else:
        default_mapping = None

    return {
        "input": ingredient_text,
        "default_mapping": default_mapping,
        "candidates": candidates
    }
