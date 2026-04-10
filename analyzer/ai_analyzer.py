from groq import Groq
import json
from django.conf import settings

def analyze_resume(resume_text, job_description=None):
    client = Groq(api_key=settings.GROQ_API_KEY)

    jd_section = ""
    if job_description:
        jd_section = f"""
Also compare the resume against this job description and add these fields to your JSON:
"jd_match_score": <integer 0-100 showing how well resume matches the job description>,
"jd_match_details": {{
  "matched_skills": ["<skill 1>", "<skill 2>"],
  "missing_skills": ["<missing skill 1>", "<missing skill 2>"],
  "recommendation": "<one sentence recommendation>"
}}

Job Description:
\"\"\"
{job_description[:2000]}
\"\"\"
"""

    prompt = f"""
You are an expert resume reviewer. Analyze the following resume and return ONLY a valid JSON object with this exact structure:

{{
  "score": <integer 0-100>,
  "profile_summary": "<2-3 sentence summary of the candidate>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "weaknesses": ["<weakness 1>", "<weakness 2>", "<weakness 3>"],
  "missing_areas": ["<missing item 1>", "<missing item 2>"],
  "suggestions": ["<suggestion 1>", "<suggestion 2>", "<suggestion 3>"],
  "keywords": ["<keyword 1>", "<keyword 2>", "<keyword 3>", "<keyword 4>", "<keyword 5>", "<keyword 6>", "<keyword 7>", "<keyword 8>", "<keyword 9>", "<keyword 10>"],
  "section_scores": {{
    "contact_info": <integer 0-100>,
    "summary": <integer 0-100>,
    "experience": <integer 0-100>,
    "education": <integer 0-100>,
    "skills": <integer 0-100>,
    "projects": <integer 0-100>,
    "certifications": <integer 0-100>
  }}
}}

{jd_section}

Scoring guide:
- 80-100: Excellent
- 60-79: Good with some gaps
- 40-59: Average, needs improvement
- Below 40: Poor structure

Resume:
\"\"\"
{resume_text[:4000]}
\"\"\"

Return ONLY the JSON. No explanation, no markdown, no extra text.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an expert resume reviewer. Always respond with valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip().rstrip("```")

    return json.loads(raw)