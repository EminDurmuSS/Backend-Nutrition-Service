# routers/nutrition_routes.py
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict
from utils.nutrition_data import get_nutrition_by_id, aggregate_recipe_nutrition

router = APIRouter()

# --- Existing endpoint: Get single ingredient nutrition ---
# FDA daily reference values are defined inside the utility module (if needed)
@router.get("/ingredients/{ingredient_id}/nutrition")
async def get_ingredient_nutrition(
    ingredient_id: str,
    measurement: str = Query("serving")
):
    """
    Returns the nutrition facts of the given ingredient_id.
    `measurement` can be 'serving' or '100g'.
    If 'serving' is selected, each nutrient value (which is stored per 100g)
    is scaled by the serving size using:
       scaled_value = original_value * (portionWeight / 100)
    """
    data = get_nutrition_by_id(ingredient_id)
    if not data:
        raise HTTPException(status_code=404, detail="Ingredient not found in nutrition_data")

    nutrients = data["nutrients"]
    portion_weight = data.get("portionWeight", 100.0)  # default to 100 if missing
    factor = portion_weight / 100.0 if measurement == "serving" else 1.0

    calories      = nutrients.get("Energ Kcal", 0.0) * factor
    protein       = nutrients.get("Protein (g)", 0.0) * factor
    carbohydrates = nutrients.get("Carbohydrt (g)", 0.0) * factor
    fat           = nutrients.get("Lipid Tot (g)", 0.0) * factor
    saturatedFat  = nutrients.get("FA Sat (g)", 0.0) * factor
    transFat      = nutrients.get("FA_Trans (g)", 0.0) * factor
    cholesterol   = nutrients.get("Cholestrl (mg)", 0.0) * factor
    sodium        = nutrients.get("Sodium (mg)", 0.0) * factor
    fiber         = nutrients.get("Fiber TD (g)", 0.0) * factor
    sugars        = (nutrients.get("Sugar (g)", 0.0) or nutrients.get("Sugar Tot (g)", 0.0)) * factor
    addedSugars   = nutrients.get("Added Sugars (g)")
    if addedSugars is not None:
        addedSugars = addedSugars * factor
    vitaminD      = nutrients.get("Vit D (µg)", 0.0) * factor
    calcium       = nutrients.get("Calcium (mg)", 0.0) * factor
    iron          = nutrients.get("Iron (mg)", 0.0) * factor
    potassium     = nutrients.get("Potassium (mg)", 0.0) * factor

    # For simplicity, here we return the scaled values (you can also add daily percentages)
    return {
        "ingredientName": data.get("ingredientName", ""),
        "calories": round(calories, 2),
        "protein": round(protein, 2),
        "carbohydrates": round(carbohydrates, 2),
        "fat": round(fat, 2),
        "saturatedFat": round(saturatedFat, 2),
        "transFat": round(transFat, 2),
        "cholesterol": round(cholesterol, 2),
        "sodium": round(sodium, 2),
        "fiber": round(fiber, 2),
        "sugars": round(sugars, 2),
        "addedSugars": round(addedSugars, 2) if addedSugars is not None else None,
        "vitaminD": round(vitaminD, 2),
        "calcium": round(calcium, 2),
        "iron": round(iron, 2),
        "potassium": round(potassium, 2),
        "servingSize": data["portionDescription"] if measurement == "serving" else "100g"
    }

# --- New endpoint: Aggregate nutrition for an entire recipe ---
@router.post("/recipes/aggregate-nutrition")
async def get_recipe_aggregated_nutrition(ingredients: List[Dict]):
    """
    Accepts a JSON payload (a list of ingredient objects):
      [
         { "ingredientId": "usda_id1", "amountInGrams": 150 },
         { "ingredientId": "usda_id2", "amountInGrams": 100 },
         ...
      ]
    Returns aggregated nutrition facts for the entire recipe.
    """
    if not ingredients:
        raise HTTPException(status_code=400, detail="No ingredients provided")
    try:
        aggregated = aggregate_recipe_nutrition(ingredients)
        return aggregated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
