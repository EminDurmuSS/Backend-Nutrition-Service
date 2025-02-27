# app/utils/nutrition_data.py
import os
import pickle

PKL_FILE_PATH = os.getenv("NUTRITION_PKL_PATH", "data/nutrition_data.pkl")
if not os.path.exists(PKL_FILE_PATH):
    raise FileNotFoundError(
        f"Could not find {PKL_FILE_PATH}. Have you run scripts/prepare_nutrition_data.py to generate it?"
    )

with open(PKL_FILE_PATH, "rb") as f:
    nutrition_data = pickle.load(f)

def get_nutrition_by_id(ingredient_id: str):
    """Return nutrition info for the given ingredientId from the precomputed dictionary."""
    return nutrition_data.get(ingredient_id)

# Daily values for a 2,000 calorie diet:
DAILY_VALUES = {
    "fat": 78.0,
    "saturatedFat": 20.0,
    "cholesterol": 300.0,
    "sodium": 2300.0,
    "carbohydrates": 275.0,
    "fiber": 28.0,
    "addedSugars": 50.0,
    "protein": 50.0,
    "vitaminD": 20.0,
    "calcium": 1300.0,
    "iron": 18.0,
    "potassium": 4700.0,
}

def calc_daily(nutrient_amount, daily_reference):
    """Calculate the daily percentage value."""
    return round((nutrient_amount / daily_reference) * 100, 2) if daily_reference else 0.0

def aggregate_recipe_nutrition(ingredients: list) -> dict:
    """
    Given a list of ingredients (each a dict with:
         - "ingredientId": the USDA ingredient id,
         - "amountInGrams": the amount in grams used in the recipe),
    look up each ingredient’s per–100g nutrient data, scale by (amountInGrams/100),
    sum the values, and compute daily percentages.
    """
    totals = {
        "calories": 0.0,
        "protein": 0.0,
        "carbohydrates": 0.0,
        "fat": 0.0,
        "saturatedFat": 0.0,
        "transFat": 0.0,
        "cholesterol": 0.0,
        "sodium": 0.0,
        "fiber": 0.0,
        "sugars": 0.0,
        "addedSugars": 0.0,
        "vitaminD": 0.0,
        "calcium": 0.0,
        "iron": 0.0,
        "potassium": 0.0,
    }
    for ing in ingredients:
        ing_id = ing.get("ingredientId")
        amount = float(ing.get("amountInGrams", 100))
        factor = amount / 100.0
        data = get_nutrition_by_id(ing_id)
        if not data:
            continue
        nutrients = data.get("nutrients", {})
        totals["calories"]      += nutrients.get("Energ Kcal", 0.0) * factor
        totals["protein"]       += nutrients.get("Protein (g)", 0.0) * factor
        totals["carbohydrates"] += nutrients.get("Carbohydrt (g)", 0.0) * factor
        totals["fat"]           += nutrients.get("Lipid Tot (g)", 0.0) * factor
        totals["saturatedFat"]  += nutrients.get("FA Sat (g)", 0.0) * factor
        totals["transFat"]      += nutrients.get("FA_Trans (g)", 0.0) * factor
        totals["cholesterol"]   += nutrients.get("Cholestrl (mg)", 0.0) * factor
        totals["sodium"]        += nutrients.get("Sodium (mg)", 0.0) * factor
        totals["fiber"]         += nutrients.get("Fiber TD (g)", 0.0) * factor
        sugar = nutrients.get("Sugar (g)", 0.0) or nutrients.get("Sugar Tot (g)", 0.0)
        totals["sugars"]        += sugar * factor
        if "Added Sugars (g)" in nutrients:
            totals["addedSugars"] += nutrients.get("Added Sugars (g)", 0.0) * factor
        totals["vitaminD"]      += nutrients.get("Vit D (µg)", 0.0) * factor
        totals["calcium"]       += nutrients.get("Calcium (mg)", 0.0) * factor
        totals["iron"]          += nutrients.get("Iron (mg)", 0.0) * factor
        totals["potassium"]     += nutrients.get("Potassium (mg)", 0.0) * factor

    daily = {
        "fatDailyValue": calc_daily(totals["fat"], DAILY_VALUES["fat"]),
        "saturatedFatDailyValue": calc_daily(totals["saturatedFat"], DAILY_VALUES["saturatedFat"]),
        "cholesterolDailyValue": calc_daily(totals["cholesterol"], DAILY_VALUES["cholesterol"]),
        "sodiumDailyValue": calc_daily(totals["sodium"], DAILY_VALUES["sodium"]),
        "carbohydratesDailyValue": calc_daily(totals["carbohydrates"], DAILY_VALUES["carbohydrates"]),
        "fiberDailyValue": calc_daily(totals["fiber"], DAILY_VALUES["fiber"]),
        "addedSugarsDailyValue": calc_daily(totals["addedSugars"], DAILY_VALUES["addedSugars"]) if totals["addedSugars"] else None,
        "proteinDailyValue": calc_daily(totals["protein"], DAILY_VALUES["protein"]),
        "vitaminDDailyValue": calc_daily(totals["vitaminD"], DAILY_VALUES["vitaminD"]),
        "calciumDailyValue": calc_daily(totals["calcium"], DAILY_VALUES["calcium"]),
        "ironDailyValue": calc_daily(totals["iron"], DAILY_VALUES["iron"]),
        "potassiumDailyValue": calc_daily(totals["potassium"], DAILY_VALUES["potassium"]),
    }

    aggregated = {
        "calories": round(totals["calories"], 2),
        "protein": round(totals["protein"], 2),
        "carbohydrates": round(totals["carbohydrates"], 2),
        "fat": round(totals["fat"], 2),
        "saturatedFat": round(totals["saturatedFat"], 2),
        "transFat": round(totals["transFat"], 2),
        "cholesterol": round(totals["cholesterol"], 2),
        "sodium": round(totals["sodium"], 2),
        "fiber": round(totals["fiber"], 2),
        "sugars": round(totals["sugars"], 2),
        "addedSugars": round(totals["addedSugars"], 2) if totals["addedSugars"] else None,
        "vitaminD": round(totals["vitaminD"], 2),
        "calcium": round(totals["calcium"], 2),
        "iron": round(totals["iron"], 2),
        "potassium": round(totals["potassium"], 2),
        "fatDailyValue": daily["fatDailyValue"],
        "saturatedFatDailyValue": daily["saturatedFatDailyValue"],
        "cholesterolDailyValue": daily["cholesterolDailyValue"],
        "sodiumDailyValue": daily["sodiumDailyValue"],
        "carbohydratesDailyValue": daily["carbohydratesDailyValue"],
        "fiberDailyValue": daily["fiberDailyValue"],
        "addedSugarsDailyValue": daily["addedSugarsDailyValue"],
        "proteinDailyValue": daily["proteinDailyValue"],
        "vitaminDDailyValue": daily["vitaminDDailyValue"],
        "calciumDailyValue": daily["calciumDailyValue"],
        "ironDailyValue": daily["ironDailyValue"],
        "potassiumDailyValue": daily["potassiumDailyValue"],
        "servingSize": "Entire Recipe"
    }
    return aggregated
