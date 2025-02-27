# schemas.py
from typing import List, Optional
from pydantic import BaseModel

class MapIngredientRequest(BaseModel):
    ingredient_text: str
    top_k: Optional[int] = 7

class MappingCandidate(BaseModel):
    input: str
    best_usda_name: Optional[str]
    score: float
    ingredientId: Optional[str]

class MapIngredientResponse(BaseModel):
    input: str
    default_mapping: Optional[str]
    candidates: List[MappingCandidate]

class UpdateMappingRequest(BaseModel):
    user_id: str
    ingredient_id: str
    mapped_ingredient: str

class UpdateMappingResponse(BaseModel):
    message: str
    user_id: str
    ingredient_id: str
    mapped_ingredient: str

class GetMappingResponse(BaseModel):
    user_id: str
    ingredient_id: str
    mapped_ingredient: Optional[str]
