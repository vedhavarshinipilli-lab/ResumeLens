from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_match(resume_text: str, job_description: str):

    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_description])

    similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
    percentage = float(round(similarity * 100, 2))

    if percentage > 75:
        level = "High"
    elif percentage > 50:
        level = "Medium"
    else:
        level = "Low"

    return {
        "match_percentage": percentage,
        "match_level": level
    }