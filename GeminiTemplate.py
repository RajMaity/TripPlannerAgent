import google.generativeai as genai
from dotenv import dotenv_values

config = dotenv_values(".env")

# genai.configure(api_key=config["GEMINI_API_KEY"])

# model = genai.GenerativeModel("gemini-2.5-pro")

# response = model.generate_content("Hi")

# print(response.text)

from google import genai
client = genai.Client(api_key = config["GEMINI_API_KEY"])
response = client.models.generate_content(
    model = "gemini-2.5-pro",
    contents = "Hi"
)
print(response.text)