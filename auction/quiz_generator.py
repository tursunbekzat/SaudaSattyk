import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_quiz():
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "Generate a quiz with 5 general knowledge questions. Format the response as a Python list of dictionaries, where each dictionary contains 'question', 'options' (a list of 4 options), and 'correct_answer' keys."
    response = model.generate_content(prompt)
    return eval(response.text)
