import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def get_similarity_score(resume_text, job_description):
    payload = {
        "inputs": {
            "source_sentence": resume_text,
            "sentences": [job_description]
        }
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload
    )

    result = response.json()

    # If API gives error
    if isinstance(result, dict):
        raise Exception(f"Hugging Face Error: {result}")

    # It returns list like [0.83]
    return result[0]