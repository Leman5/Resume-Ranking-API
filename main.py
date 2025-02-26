from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import io
import pandas as pd
import json
import uvicorn

# Import custom helpers (services) here
from services.file_extractor import extract_text_from_file
from services.criteria_extractor import extract_criteria_from_text
from services.scorer import score_resume, shorten_criteria_text

# Initialize FastAPI application
app = FastAPI(
    title="Resume Ranking API",
    description="API for extracting ranking criteria from job descriptions and scoring resumes.",
    version="1.0.1"
)

# Endpoint to extract ranking criteria
@app.post("/extract-criteria", summary="Extract Ranking Criteria from Job Description", tags=["Criteria Extraction"])
async def extract_criteria(file: UploadFile = File(...)):
    """
    Extracts key ranking criteria from a job description file (PDF or DOCX).
    Returns a structured JSON response with the extracted criteria.
    """
    try:
        file_bytes = await file.read()
        text_content = extract_text_from_file(file_bytes, file.filename)
        criteria_list = extract_criteria_from_text(text_content)
        return JSONResponse(content={"criteria": criteria_list})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to score resumes
@app.post("/score-resumes", summary="Score Resumes Against Extracted Criteria", tags=["Resume Scoring"])
async def score_resumes_endpoint(
    criteria_json: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """
    Scores multiple resumes (PDF or DOCX) against given ranking criteria.
    Returns a CSV file with individual and total scores for each candidate.
    """
    try:
        criteria = json.loads(criteria_json)["criteria"]
        results = []
        for resume_file in files:
            file_bytes = await resume_file.read()
            resume_text = extract_text_from_file(file_bytes, resume_file.filename)
            score_dict = score_resume(resume_text, criteria)
            score_dict["CandidateName"] = resume_file.filename
            results.append(score_dict)

        df = pd.DataFrame(results)
        short_criteria = shorten_criteria_text(criteria)
        columns_in_order = ["CandidateName"] + criteria + ["TotalScore"]
        df = df[columns_in_order]
        mapping = {original: short for original, short in zip(criteria, short_criteria)}
        df.rename(columns=mapping, inplace=True)

        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=resume_scores.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
