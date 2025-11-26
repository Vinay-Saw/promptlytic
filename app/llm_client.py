import os
from .settings import settings
import openai
from typing import Optional

openai.api_key = settings.OPENAI_API_KEY
openai.api_base = settings.OPENAI_BASE_URL

def build_prompt(page_url: str, page_html: str) -> str:
    prompt = f"""You are an autonomous agent. You will be given a web page's full HTML and its URL.
Your job:

1) Read the HTML and find the quiz question and the submission endpoint (a URL containing 'submit' or 'answer' or '/api/').
2) Produce a single, self-contained Python script (single file) that:
   - Uses only the Python stdlib plus 'requests' and 'beautifulsoup4' if required.
   - Fetches any required resources, computes the answer and POSTs it to the submission endpoint.
   - Prints exactly one JSON object to stdout: {{ "submitted": true/false, "submit_response": <json or text>, "url": "<next_url_if_any>" }}
3) Return only the script (you may wrap it in triple backticks; the server will strip them).

Task URL: {page_url}

PAGE HTML:
{page_html}
"""
    return prompt

def call_llm(prompt: str, model: Optional[str] = None, temperature: float = 0.0) -> str:
    model = model or settings.MODEL_NAME
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role":"system","content":"You are a python developer assistant. Output only the script."},
            {"role":"user","content": prompt}
        ],
        temperature=temperature,
        max_tokens=4500
    )
    return resp["choices"][0]["message"]["content"]
