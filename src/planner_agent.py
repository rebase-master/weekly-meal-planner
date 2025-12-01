from typing import List, Dict
from openai import OpenAI

client = OpenAI()

class PlannerAgent:
    """
    Generates a weekly meal plan based on dietary preferences,
    allergies, cuisine choices and number of meals required.
    """

    def __init__(self):
        pass

    def run(self, dietary_info: Dict, memory: Dict) -> List[str]:
        """
        Returns a list of meals for the week (e.g., 5 dinners).
        """
        allergies = ", ".join(dietary_info.get("allergies", []))
        diet_type = dietary_info.get("diet_type", "none")
        cuisine_prefs = ", ".join(dietary_info.get("cuisine_preferences", []))
        meals_needed = dietary_info.get("meals_needed", ["5 dinners"])[0]

        past_meals = memory.get("past_meals", [])

        prompt = f"""
        You are a professional meal planner.
        Create a meal plan matching:
        • diet type: {diet_type}
        • allergies: {allergies}
        • cuisine preference: {cuisine_prefs}
        • meals needed: {meals_needed}

        Use vegetarian meals where required.
        Avoid all allergens completely.
        Prioritize Mediterranean cuisine if possible.

        DO NOT repeat past meals:
        {past_meals}

        Return meals ONLY in a bullet point list format, 1 item per line, nothing else.
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content.strip()
        meals = [line.lstrip("-• ").strip() for line in content.split("\n") if line]
        return meals
