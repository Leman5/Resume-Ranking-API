# Resume Ranking API

This project provides an automated solution for ranking resumes based on job descriptions using FastAPI and Google Gemini (Generative AI). It consists of two main API endpoints:

1. **`/extract-criteria`:** Extracts key ranking criteria from a job description file (PDF or DOCX) and returns a structured JSON response.
2. **`/score-resumes`:** Scores multiple resumes against the extracted criteria and returns a CSV sheet with detailed scores for each candidate.

---

## Features
- **Text Extraction:** Supports both PDF and DOCX file formats.
- **AI-Powered Analysis:** Utilizes Google Gemini (Generative AI) to extract and score relevant criteria.
- **Bulk Resume Scoring:** Allows multiple resume files to be uploaded and evaluated in one request.
- **Structured Output:** Returns structured JSON responses and downloadable CSV reports.
- **Interactive UI:** Beautiful web interface for uploading files and viewing results.
- **Swagger UI Documentation:** Auto-generated interactive API documentation using FastAPI's built-in OpenAPI support.

---

## Getting Started

### Prerequisites
- Python 3.8+
- FastAPI
- Uvicorn
- PyMuPDF
- python-docx
- pandas
- Google Gemini (Generative AI) SDK

---

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/YOUR_USERNAME/resume-ranking-api.git
    cd resume-ranking-api
    ```

2. **Create a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up your environment variables:**
    ```sh
    export GENAI_API_KEY='your-google-genai-api-key'
    ```
    On Windows, use:
    ```sh
    set GENAI_API_KEY='your-google-genai-api-key'
    ```

---

## Running the Server

To start the FastAPI server with static UI support:
```sh
uvicorn main:app --reload
```
This will start the FastAPI server at `http://127.0.0.1:8000`.

---

## Accessing the UI

You can access the interactive UI for this project at:
```
http://127.0.0.1:8000/static/index.html
```

- **Home Page (`index.html`)**:
  - Lists the two main functionalities:
    - **Extract Ranking Criteria:** Redirects to `task1.html`.
    - **Score Resumes:** Redirects to `task2.html`.

- **Task 1: Extract Ranking Criteria (`task1.html`)**:
  - Upload a job description file (PDF or DOCX).
  - Displays the extracted criteria in JSON format.
  - Option to copy the extracted criteria for use in scoring.

- **Task 2: Score Resumes (`task2.html`)**:
  - Paste the extracted criteria as JSON.
  - Upload multiple resume files (PDF or DOCX).
  - Displays the scores as a table on the webpage.
  - Option to download the scores as a CSV file.

---

## API Endpoints

### 1. Extract Ranking Criteria
```
POST /extract-criteria
```
- **Description:** Extracts key ranking criteria from a job description (PDF/DOCX).
- **Input:** Multipart Form-Data with a single file.
- **Output:** JSON with extracted criteria list.

### 2. Score Resumes
```
POST /score-resumes
```
- **Description:** Scores multiple resumes against the extracted criteria.
- **Input:** JSON string of criteria + multiple files (PDF/DOCX).
- **Output:** CSV file containing individual and total scores for each candidate.

---

## Swagger UI Documentation

You can access the auto-generated Swagger UI documentation at:
```
http://127.0.0.1:8000/docs
```
This allows you to:
- Test the endpoints directly from the browser.
- View detailed request and response examples.
- Explore the API structure and capabilities.

---

## Project Structure
```
resume-ranking-api/
│
├── main.py                # Main FastAPI application
├── services/              # Service modules for modular logic
│   ├── file_extractor.py  # Text extraction from PDF/DOCX
│   ├── criteria_extractor.py  # Extracting criteria using Gemini
│   └── scorer.py          # Scoring resumes against criteria
├── static/                # Static HTML files for UI
│   ├── index.html         # Home page linking to tasks
│   ├── task1.html         # UI for extracting criteria
│   └── task2.html         # UI for scoring resumes
└── requirements.txt       # Python dependencies
```

---

## Usage Instructions

1. **Extract Ranking Criteria**:
   - Go to `http://127.0.0.1:8000/static/task1.html`
   - Upload a job description file (PDF/DOCX).
   - Copy the extracted criteria JSON.

2. **Score Resumes**:
   - Go to `http://127.0.0.1:8000/static/task2.html`
   - Paste the extracted criteria JSON.
   - Upload multiple resumes (PDF/DOCX).
   - View the scores on the page or download as a CSV.


