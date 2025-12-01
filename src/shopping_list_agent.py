from typing import List, Dict
from openai import OpenAI

client = OpenAI()

class ShoppingListAgent:
    """
    Aggregates ingredients from multiple recipes and produces
    a clean, consolidated shopping list.
    """

    def __init__(self):
        pass

    def run(self, recipes: List[Dict]) -> Dict:
        """
        Input:
            recipes: list of recipe dicts from RecipeFinderAgent
        Output:
            {
              "shopping_list": [...],
              "recipes": recipes
            }
        """

        all_ingredients = []
        for recipe in recipes:
            ingredients = recipe.get("ingredients", [])
            all_ingredients.extend(ingredients)

        prompt = f"""
        Create a consolidated shopping list from these ingredients:

        {all_ingredients}

        Requirements:
        - Remove duplicates
        - Group similar items together (e.g., "olives" and "black olives")
        - Prefer generic names (e.g., "bell peppers" instead of colors)
        - Keep the list simple and grocery-friendly
        - Output as bullet points only

        Return JSON only:
        {{
          "shopping_list": ["ingredient 1", "ingredient 2", ...]
        }}
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content.strip()

        # JSON extraction
        try:
            result = eval(content)
        except Exception:
            result = {"shopping_list": list(set(all_ingredients))}

        # Include recipes for downstream agents or logging
        result["recipes"] = recipes
        return result
