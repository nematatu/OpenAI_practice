from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_ky = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=api_ky)

print("hello")
