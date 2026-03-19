import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model="llama3-8b-8192", 
temperature=0.1, 
response_format={"type": "json_object"}

SHEET_URL = os.getenv("SHEET_URL")