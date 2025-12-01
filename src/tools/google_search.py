import requests
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")  # CX value

def google_search(query: str, num_results: int = 5):
    """
    Performs a Google Custom Search and returns a simplified list of results.

    Output format:
    [
      { "title": "...", "link": "...", "snippet": "..." },
      ...
    ]
    """
    if not GOOGLE_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        print("WARNING: Google Search not configured. Returning empty results.")
        return []

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_SEARCH_ENGINE_ID,
        "q": query,
        "num": num_results,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
    except Exception:
        return []

    items = data.get("items", []) or []
    results = []
    for item in items:
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet", "")
        })

    return results
