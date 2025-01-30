# Autocomplete Application

This application provides a simple autocomplete feature using a React frontend and a FastAPI backend.

## Backend Setup

1.  Navigate to the `backend` directory.
2.  Create virtual environment:
    ```bash
    python -m venv venv
    ```
3.  Activate virtual environment:
    ```bash
    source venv/bin/activate
    ```
    (or `venv\Scripts\activate` on Windows)
4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Run the backend using `uvicorn app:app --reload --port 8000`. This will start the FastAPI server on `http://localhost:8000`.

6. You need to provide the `hunspell_US.txt` to the backend folder. This is a file containing every word in the english language.

## Frontend Setup

1.  Navigate to the `frontend` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3. Start the development server:
    ```bash
    npm run dev
    ```
    This will start the React development server, usually on `http://localhost:5173`.

## Usage

1.  Make sure both the backend and frontend servers are running.
2.  Open the frontend in your browser.
3.  Type into the input box, and you'll see suggestions appear.
4. Click on a suggestion to complete the form.

## Notes

*   The backend uses a SQLite database (`completions.db`) to store previously used completions.
*   The LLM integration in `llm.py` is unreliable, as per the assignment requirements.
*   The frontend uses basic accessibility features for the autocomplete functionality.