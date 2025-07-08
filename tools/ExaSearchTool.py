# tools/ExaSearchTool.py
import os
from exa_py import Exa
from langchain.agents import Tool  # For crewai v0.11.0

exa = Exa(api_key=os.environ["EXA_API_KEY"])

def search(query: str):
    return exa.search(f"{query}", use_autoprompt=True, num_results=3)

def find_similar(url: str):
    return exa.find_similar(url, num_results=3)

def get_contents(ids: str):
    ids = eval(ids)
    contents = str(exa.get_contents(ids))
    contents = contents.split("URL:")
    contents = [content[:1000] for content in contents]
    return "\n\n".join(contents)

def get_exa_tools():
    return [
        Tool(name="Search", func=search, description="Search webpages for a query using Exa"),
        Tool(name="FindSimilar", func=find_similar, description="Find similar pages to a given URL"),
        Tool(name="GetContents", func=get_contents, description="Get webpage contents for given IDs")
    ]
