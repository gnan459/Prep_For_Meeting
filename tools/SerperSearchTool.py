import json
import os
import requests
from langchain.tools import Tool

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_ENDPOINT = "https://google.serper.dev/search"

def search_with_serper(query: str) -> str:
    """Search Google using Serper API and return top LinkedIn results."""
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"q": f"{query} site:linkedin.com/in"}

    try:
        response = requests.post(SERPER_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        results = data.get("organic", [])[:3]

        person_info = {
            "name": query,
            "linkedin_url": None,
            "snippets": []
        }

        for result in results:
            link = result.get("link", "")
            snippet = result.get("snippet", "")
            if "linkedin.com/in" in link and not person_info["linkedin_url"]:
                person_info["linkedin_url"] = link
            if snippet:
                person_info["snippets"].append(snippet)

        return json.dumps(person_info)  # always stringified for LLM use

    except Exception as e:
        return json.dumps({"error": f"❌ Serper search failed: {str(e)}"})

def get_serper_tools():
    return [
        Tool.from_function(
            func=search_with_serper,
            name="SerperSearch",
            description="Searches Google for LinkedIn bios and profile URLs using the Serper API."
        )
    ]
