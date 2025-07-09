import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    # temperature=0.4,
    # convert_system_message_to_human=True,
    # max_output_tokens=2048,
    # request_timeout=120,
    # streaming=False
)
