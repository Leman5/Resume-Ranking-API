import os
import json
from typing import List
from google import genai
import re

import json

with open('config.json') as config_file:
    config = json.load(config_file)
Gemini_KEY = config.get('gemini_key')


def extract_criteria_from_text(text: str) -> List[str]:
    """
    Uses Gemini (Google Generative AI) to parse the job description text and extract
    key hiring criteria (skills, certifications, qualifications, etc.).

    :param text: The raw text from the job description (PDF/DOCX).
    :return: A list of extracted criteria as strings.
    """
    client = genai.Client(api_key=Gemini_KEY)

    prompt = f"""
    You are an expert HR assistant. Extract all the important hiring criteria, mandatory requirements, core responsibilities, 
    and desired qualifications from the following job description:

    {text}

    Return ONLY valid JSON with a 'criteria' key (an array of strings). For example:

    {{
    "criteria": [
    "Criterion 1",
    "Criterion 2",
    ...
    ]
    }}
    """

    # 3. Call the Gemini API 
    try:
        response = client.models.generate_content(
            contents=prompt,
            model="gemini-2.0-flash", 
        )


        raw_response = response.text.strip()
        
        cleaned_response = re.sub(r"```[a-zA-Z]*", "", raw_response).replace("```", "").strip()

        data = json.loads(cleaned_response)
        if "criteria" in data and isinstance(data["criteria"], list):
            extracted_criteria = data["criteria"]
        else:
            extracted_criteria = []

    except Exception as e:
        print(f"Error extracting criteria: {e}")
        extracted_criteria = []

    top_reworded_criteria = reword_and_select_top_criteria(extracted_criteria)

    return top_reworded_criteria


def reword_and_select_top_criteria(criteria_list: List[str], max_criteria: int = 5) -> List[str]:
    """
    Calls Gemini to:
    1. Reword each extracted criterion into a concise single line.
    2. Select the top 3-5 that best assess a candidate (by default 5).
    Returns them in a list of strings.
    """
    if not criteria_list:
        return []

    # Make sure your API key is set, or reuse the same client
    client = genai.Client(api_key=Gemini_KEY)

    prompt = f"""
    You are an HR expert evaluating a list of job criteria. First, paraphrase each criterion into a concise, 
    single-line statement. Then select the top 3-5 criteria you believe are most important for assessing 
    a candidate for this role. Return ONLY valid JSON in the following format of those selected 3-5 criterias:

    {{
    "criteria": [
        "Reworded Criterion 1",
        "Reworded Criterion 2",
        ...
    ]
    }}

    Here is the original list of criteria (as a JSON array):
    {json.dumps(criteria_list)}
    """

    try:
        response = client.models.generate_content(
            contents=prompt,
            model="gemini-2.0-flash"
        )
        raw_response = response.text.strip()
        cleaned_response = re.sub(r"```[a-zA-Z]*", "", raw_response).replace("```", "").strip()

        data = json.loads(cleaned_response)
        if "criteria" in data and isinstance(data["criteria"], list):
            return data["criteria"]
        else:
            return []
    except Exception as e:
        print(f"Error rewording and selecting top criteria: {e}")
        return []
    