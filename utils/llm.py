from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)
groq_api_key=os.getenv("GROQ_API_KEY")
openrouter_api_key=os.getenv("OPENROUTER_API_KEY")

groq_url="https://api.groq.com/openai/v1"
openrouter_url="https://openrouter.ai/api/v1"
groq=OpenAI(base_url=groq_url,api_key=groq_api_key)
openrouter=OpenAI(base_url=openrouter_url,api_key=openrouter_api_key)


def llm(user_prompt,system_prompt,response_format=None):
    messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}]
    if response_format is None:
        response=groq.chat.completions.create(model="llama-3.3-70b-versatile",messages=messages)
        return response.choices[0].message.content
    else:
        response = openrouter.beta.chat.completions.parse(
        model="google/gemma-4-26b-a4b-it:free",
        messages=messages,
        response_format=response_format,
        )
        return response.choices[0].message.parsed