import os
import json
import requests
from langchain.tools import Tool

# Load API key from environment
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_ENDPOINT = "https://google.serper.dev/search"

def search_with_serper(query: str) -> str:
    """Search Google using Serper API and return top search results for a person."""
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": query}

    try:
        response = requests.post(SERPER_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        results = data.get("organic", [])[:2]  # Limit to top 2
        if not results:
            return json.dumps({"query": query, "results": [], "note": "No results found"}, indent=2)

        extracted = []
        for result in results:
            extracted.append({
                "title": result.get("title", ""),
                "url": result.get("link", ""),
                "snippet": result.get("snippet", "")
            })

        return json.dumps({"query": query, "results": extracted}, indent=2)

    except Exception as e:
        return json.dumps({"query": query, "error": str(e)}, indent=2)

def get_serper_tools():
    """Return Serper search tool wrapped for use in CrewAI/Agents."""
    return [
        Tool.from_function(
            func=search_with_serper,
            name="SerperSearch",
            description="Searches Google for recent information, bios, or company details using the Serper API."
        )
    ]
