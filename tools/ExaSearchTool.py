# tools/ExaSearchTool.py

import os
from exa_py import Exa
from langchain.agents import Tool  # For crewai v0.11.0

exa = Exa(api_key=os.environ["EXA_API_KEY"])

def search(query: str):
    try:
        raw_results = exa.search(query, use_autoprompt=True, num_results=3)

        cleaned_results = []
        for r in raw_results.results:
            cleaned_results.append({
                "id": getattr(r, "id", ""),
                "title": getattr(r, "title", ""),
                "url": getattr(r, "url", ""),
                "text": getattr(r, "text", "")
            })

        return {"results": cleaned_results}

    except Exception as e:
        return {"results": [], "error": str(e)}

def find_similar(url: str):
    try:
        return exa.find_similar(url, num_results=3)
    except Exception as e:
        return {"results": [], "error": str(e)}

def get_contents(ids: str):
    try:
        # Convert from string to list if needed
        if isinstance(ids, str):
            ids = eval(ids)

        results = exa.get_contents(ids)

        contents = []
        for r in results:
            if hasattr(r, "text"):
                contents.append(r.text[:1000])
            elif isinstance(r, dict) and "text" in r:
                contents.append(r["text"][:1000])
            else:
                contents.append(str(r)[:1000])  # fallback

        return "\n\n".join(contents)

    except Exception as e:
        return f"⚠️ Error fetching contents: {e}"

def get_exa_tools():
    return [
        Tool(name="Search", func=search, description="Search webpages for a query using Exa"),
        Tool(name="FindSimilar", func=find_similar, description="Find similar pages to a given URL"),
        Tool(name="GetContents", func=get_contents, description="Get webpage contents for given IDs")
    ]
