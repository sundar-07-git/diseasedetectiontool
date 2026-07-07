# AuraHealth Clinical Intake Core

An advanced medical triage assistant built with **Streamlit** and powered by **Google Gemini 2.5 Flash** for predictive diagnostic triage and specialist routing.

---

## How to Run the Application Locally

Follow these steps to run the application on your computer:

### 1. Prerequisites
Make sure you have **Python 3.9 or higher** installed on your system. You can check your version by running:
```bash
python --version
```

### 2. Clone the Repository
Download the code using Git:
```bash
git clone https://github.com/sundar-07-git/diseasedetectiontool.git
cd diseasedetectiontool
```

### 3. Install Dependencies
Install the required Python packages:
```bash
pip install streamlit google-genai
```

### 4. Configure Your API Key
The application requires a Gemini API Key to run.
1. Create a folder named `.streamlit` in the root of the project directory (if it doesn't already exist).
2. Inside that folder, create a file named `secrets.toml`.
3. Add your API key in the following format:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key-here"
   ```

*Note: The `.streamlit/secrets.toml` file is ignored by Git, ensuring your API key is never leaked.*

### 5. Launch the Application
Run the Streamlit server from your terminal:
```bash
streamlit run app.py
```

This will spin up a local server and automatically open the application in your web browser (usually at `http://localhost:8501`).

---

## Project Structure
- `app.py`: Main Streamlit application file containing the UI layout and LLM logic.
- `knowledge_base.csv`: Reference database mapping symptoms to diseases, medications, and specialists.
- `.gitignore`: Configured to exclude API secrets and temporary caches.

---

*Disclaimer: This software functions strictly as an educational screening prototype. It does not replace formal clinical validation or professional medical consultation.*
