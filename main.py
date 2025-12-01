import json
from src.planner_agent import PlannerAgent
from src.recipe_finder_agent import RecipeFinderAgent
from src.shopping_list_agent import ShoppingListAgent
from src.session_memory import SessionMemory

def load_input(path="input.json"):
    with open(path, "r") as f:
        return json.load(f)

def run():
    # Load user input
    user_input = load_input()
    dietary_info = user_input.get("dietary_info", {})

    # Initialize session memory
    memory = SessionMemory()
    past_memory = memory.get()

    # Initialize agents
    planner = PlannerAgent()
    recipe_finder = RecipeFinderAgent()
    shopping_list_agent = ShoppingListAgent()

    # STEP 1 — generate weekly meal plan
    meals = planner.run(dietary_info, past_memory)
    print("\n=== Weekly Meal Plan ===")
    for m in meals:
        print("•", m)

    # STEP 2 — find recipes for each meal
    recipes = recipe_finder.run(meals, dietary_info)

    # STEP 3 — aggregate shopping list
    result = shopping_list_agent.run(recipes)

    print("\n=== Consolidated Shopping List ===")
    for item in result["shopping_list"]:
        print("•", item)

    # Save memory for future runs
    memory.update_with_new_meals(meals)
    memory.update_dietary_info(dietary_info)

    # Save full result to output.json
    with open("output.json", "w") as f:
        json.dump(result, f, indent=2)

    print("\nResults written to output.json")
    print("Memory updated in memory.json")

if __name__ == "__main__":
    run()
