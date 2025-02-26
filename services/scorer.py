# my_project/services/scorer.py

import os
import json
from typing import List, Dict
from google import genai
import re

import json

with open('config.json') as config_file:
    config = json.load(config_file)
Gemini_KEY = config.get('gemini_key')

def score_resume(resume_text: str, criteria: List[str]) -> Dict[str, int]:
    """
    Uses Gemini (Google Generative AI) to assign a 0-5 score for each criterion
    based on the resume text. Returns a dict: { criterion: score, ..., "TotalScore": total }.
    """
    client = genai.Client(api_key=Gemini_KEY)

    

    prompt = f"""
    You are an expert HR assistant. The following resume text needs to be evaluated against each
    of these criteria. For each criterion, assign a numeric score from 0 to 5:
    - 0 means the resume doesn't satisfy the criterion at all.
    - 5 means the resume strongly satisfies it.

    Return ONLY valid JSON. The JSON structure should look like:

    {{
    "scores": [
        {{ "criterion": "Criterion 1", "score": 3 }},
        {{ "criterion": "Criterion 2", "score": 5 }},
        ...
    ],
    "total": 8
    }}

    ---
    Resume Text:
    {resume_text}

    ---
    Criteria:
    {json.dumps(criteria)}

    Remember:
    1. The "scores" list must have one entry per criterion (in the same order).
    2. Each entry has "criterion" and "score".
    3. "total" is the sum of all "score" values.
    4. Return ONLY valid JSON with no code fences or additional text.
    """

    try:
        response = client.models.generate_content(
            contents=prompt,
            model="gemini-2.0-flash",  
        )

        raw_text = response.text.strip()
        cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()

        data = json.loads(cleaned_text)

        scores = {}
        total_score = 0

        if "scores" in data and isinstance(data["scores"], list):
            for item in data["scores"]:
                c = item.get("criterion", "")
                s = item.get("score", 0)
                scores[c] = s
                total_score += s
        else:
            # If "scores" key is missing or not a list, handle gracefully
            print("Gemini JSON did not contain 'scores' in the expected format.")
            return {criterion: 0 for criterion in criteria} | {"TotalScore": 0}

        # We expect "total" in data, but if it's missing, we can fallback to sum
        if "total" in data and isinstance(data["total"], (int, float)):
            total_score = data["total"]

        scores["TotalScore"] = total_score

        return scores

    except Exception as e:
        # If anything goes wrong (API error, JSON parse error, etc.), log and return zeros
        print(f"Error in score_resume with Gemini: {e}")
        fallback_scores = {criterion: 0 for criterion in criteria}
        fallback_scores["TotalScore"] = 0
        return fallback_scores



def shorten_criteria_text(criteria: List[str]) -> List[str]:
    """
    Uses Gemini to convert each criterion into a short 2-3 word summary.
    Returns a parallel list of shortened criteria.
    """
    client = genai.Client(api_key=Gemini_KEY)


    prompt = f"""
    I have a list of job criteria. Each item is a sentence or phrase. 
    Please produce a concise 2-3 word label for each. Return ONLY valid JSON 
    with a "summaries" field (an array of strings) in the same order.

    Example:
    If the criteria is:
    ["Must have certification XYZ", "5+ years of experience in Python development", "Strong background in Machine Learning"]

    Return something like:
    {{
    "summaries": [
        "Certification XYZ",
        "Python Experience",
        "Machine Learning"
    ]
    }}

    No Markdown code fences. No additional text. Only valid JSON.
    ---
    Here are the criteria:

    {json.dumps(criteria)}
    """

    try:
        response = client.models.generate_content(
            contents=prompt,
            model="gemini-2.0-flash",
        )

        raw_text = response.text.strip()
        cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()

        data = json.loads(cleaned_text)

        if "summaries" in data and isinstance(data["summaries"], list):
            return data["summaries"]
        else:
            return criteria  
    except Exception as e:
        print(f"Error in shorten_criteria_text: {e}")
        # If anything goes wrong, just return original criteria
        return criteria