# Resume Ranking API

This project provides an automated solution for ranking resumes based on job descriptions using FastAPI and Google Gemini (Generative AI). It consists of two main API endpoints:

1. **`/extract-criteria`:** Extracts key ranking criteria from a job description file (PDF or DOCX) and returns a structured JSON response.
2. **`/score-resumes`:** Scores multiple resumes against the extracted criteria and returns a CSV sheet with detailed scores for each candidate.

## Features
- **Text Extraction:** Supports both PDF and DOCX file formats.
- **AI-Powered Analysis:** Utilizes Google Gemini (Generative AI) to extract and score relevant criteria.
- **Bulk Resume Scoring:** Allows multiple resume files to be uploaded and evaluated in one request.
- **Structured Output:** Returns structured JSON responses and downloadable CSV reports.
- **Beautiful Swagger UI:** Auto-generated interactive API documentation using FastAPI's built-in OpenAPI support.

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

### Installation
1. Clone the repository:
    ```sh
    git clone [https://github.com/Leman5/resume-ranking-api.git](https://github.com/Leman5/Resume-Ranking-API.git)
    cd resume-ranking-api
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up your environment variables:
    ```sh
    export GENAI_API_KEY='your-google-genai-api-key'
    ```
    On Windows, use:
    ```sh
    set GENAI_API_KEY='your-google-genai-api-key'
    ```

    And add it to a config.json file

---

## Running the Server
```sh
uvicorn main:app --reload
```
This will start the FastAPI server at `http://127.0.0.1:8000`.

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

## Usage
Access the interactive Swagger UI documentation at:
```
http://127.0.0.1:8000/docs
```
This allows you to test the endpoints and view detailed request/response examples.

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
└── requirements.txt       # Python dependencies
```

---

## Contribution Guidelines
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

---

## License
This project is licensed under the MIT License.

---

## Contact
For any issues or questions, please contact [Your Name](mailto:your.email@example.com).

Feel free to create issues or contribute to the project!
