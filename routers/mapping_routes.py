# routers/mapping_routes.py
from fastapi import APIRouter, HTTPException
from schemas import (
    MapIngredientRequest,
    MapIngredientResponse,
    MappingCandidate,
    UpdateMappingRequest,
    UpdateMappingResponse,
    GetMappingResponse,
)
from services import map_ingredient
from repositories.mapping_repository import update_mapping, get_mapping

router = APIRouter()

@router.post("/map-ingredient", response_model=MapIngredientResponse)
async def map_ingredient_endpoint(request: MapIngredientRequest):
    """
    Request JSON:
      - ingredient_text: the text to map.
      - top_k (optional): number of candidate matches (default: 7)
    """
    try:
        result = map_ingredient(request.ingredient_text, request.top_k)
        candidates = [MappingCandidate(**cand) for cand in result["candidates"]]
        return MapIngredientResponse(
            input=result["input"],
            default_mapping=result["default_mapping"],
            candidates=candidates
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update-mapping", response_model=UpdateMappingResponse)
async def update_mapping_endpoint(request: UpdateMappingRequest):
    """
    Request JSON:
      - user_id
      - ingredient_id
      - mapped_ingredient
    """
    update_mapping(request.user_id, request.ingredient_id, request.mapped_ingredient)
    return UpdateMappingResponse(
        message="Mapping updated successfully",
        user_id=request.user_id,
        ingredient_id=request.ingredient_id,
        mapped_ingredient=request.mapped_ingredient
    )

@router.get("/get-mapping", response_model=GetMappingResponse)
async def get_mapping_endpoint(user_id: str, ingredient_id: str):
    """
    Query parameters:
      - user_id
      - ingredient_id
    """
    mapped = get_mapping(user_id, ingredient_id)
    return GetMappingResponse(
        user_id=user_id,
        ingredient_id=ingredient_id,
        mapped_ingredient=mapped
    )
