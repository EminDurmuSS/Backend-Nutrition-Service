# repositories/mapping_repository.py
from typing import Dict, Tuple

# In‑memory Mapping "Repository"
mapping_store: Dict[Tuple[str, str], str] = {}

def update_mapping(user_id: str, ingredient_id: str, mapped_ingredient: str):
    mapping_store[(user_id, ingredient_id)] = mapped_ingredient

def get_mapping(user_id: str, ingredient_id: str):
    return mapping_store.get((user_id, ingredient_id))
