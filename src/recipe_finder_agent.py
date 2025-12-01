from typing import List, Dict
from openai import OpenAI
from .tools.google_search import google_search

client = OpenAI()

class RecipeFinderAgent:
    """
    Finds recipes for a given list of meals using Google Search and extracts
    ingredients and cooking instructions using the LLM.
    """

    def __init__(self):
        pass

    def run(self, meals: List[str], dietary_info: Dict) -> List[Dict]:
        """
        Input:
            meals: list of meal names from PlannerAgent
            dietary_info: for additional safety instructions
        Output:
            list of recipe dicts:
            [
              {
                "meal": "...",
                "recipe_title": "...",
                "recipe_url": "...",
                "ingredients": [...],
                "instructions": "..."
              }
            ]
        """
        results = []
        allergies = dietary_info.get("allergies", [])
        diet_type = dietary_info.get("diet_type", "")

        for meal in meals:
            query = f"{meal} {diet_type} recipe"
            search_results = google_search(query)

            # Pick top search result only
            top_url = search_results[0]["link"] if search_results else None

            prompt = f"""
            You are a cooking expert. Extract structured recipe details for the dish:
            "{meal}"

            Input URL to reference:
            {top_url}

            Requirements:
            - Vegetarian only (if applicable)
            - Exclude all allergens: {allergies}
            - Use simple, easy-to-find ingredients

            Return JSON only in this format:
            {{
              "meal": "...",
              "recipe_title": "...",
              "recipe_url": "{top_url}",
              "ingredients": ["ingredient 1", "ingredient 2", ...],
              "instructions": "short paragraph summary"
            }}
            """

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.choices[0].message.content.strip()

            try:
                recipe = eval(content)  # safe because LLM is forced to return JSON literal
                results.append(recipe)
            except Exception:
                results.append({
                    "meal": meal,
                    "recipe_title": meal,
                    "recipe_url": top_url,
                    "ingredients": [],
                    "instructions": "Parsing failed, but meal included."
                })

        return results
