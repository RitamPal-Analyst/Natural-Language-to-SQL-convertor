# Natural Language to SQL Query Generator

A Streamlit web app that lets users ask questions about a MySQL database in plain English and get back a generated SQL query along with live results — powered by Google's Gemini AI.

## Overview

This tool bridges the gap between non-technical users and databases. Instead of writing SQL manually, users simply type a question (e.g. *"How many customers are married?"*) and the app:

1. Reads the live schema of the connected MySQL database
2. Sends the schema + question to Google Gemini
3. Generates a valid SQL query
4. Executes the query against the database
5. Displays the results in an interactive table

## Features

- **Live schema viewer** — displays all tables, columns, and data types from the connected database
- **Natural language input** — ask questions in plain English, no SQL knowledge required
- **AI-powered query generation** — uses Google Gemini (`gemini-2.5-flash`) to convert questions into SQL
- **Instant execution** — runs the generated query and shows results directly in the app
- **Clean output** — strips markdown formatting from the AI response automatically
- **Unanswerable question handling** — if a question can't be answered from the schema, the app flags it instead of generating an invalid query

## Tech Stack

| Component | Technology |
|---|---|
| Frontend / App | Streamlit |
| Database | MySQL |
| AI Model | Google Gemini (`gemini-2.5-flash`) |
| Language | Python |
| Key Libraries | `mysql-connector-python`, `google-genai`, `pandas`, `python-dotenv` |

## Project Structure

```
├── Streamlit_app.py         # Main Streamlit application
├── Natural_language_to_SQL  # Python File without Streamlit
├── .env                     # Environment variables (not committed to GitHub)
└── README.md                # Project documentation
```

## Setup & Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Install dependencies

```bash
pip install streamlit mysql-connector-python google-genai pandas python-dotenv
```

### 3. Configure environment variables

Create a `.env` file in the project root with your Gemini API key:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

> Get your API key from [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key).

### 4. Update database credentials

This app assumes a MySQL database named `loans_dataset` already exists and is accessible. Update the connection details in `Streamlit_app.py` if your setup differs:

```python
host="localhost"
port="3306"
user="root"
password="root"
database="loans_dataset"
```

### 5. Run the app

```bash
streamlit run Streamlit_app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## How It Works

1. **Schema extraction** — On load, the app queries `information_schema.columns` to fetch all table and column metadata, displaying it as a reference table.
2. **Prompt construction** — The schema and the user's question are combined into a single prompt sent to Gemini, instructing it to return only raw SQL.
3. **Query generation** — Gemini's response is cleaned (markdown code blocks stripped) to produce an executable SQL string.
4. **Query execution** — The generated SQL is run against the MySQL database using `mysql-connector-python`.
5. **Results display** — Output rows are converted into a `pandas` DataFrame and rendered with `st.dataframe()`.

## Example Usage

**Question:** `What is the total number of female customers?`

**Generated SQL:**
```sql
SELECT COUNT(*) FROM customers WHERE Gender = 'Female';
```

**Result:** Displayed instantly as a table in the app.

## Screenshots

> _Add screenshots of the app here_

| Schema View | Query Generation | Results |
|---|---|---|
| _screenshot_ | _screenshot_ | _screenshot_ |

## Future Improvements

- Add support for multiple databases / dynamic database selection
- Visualize results with charts for numeric queries
- Add query history within the session
- Deploy to Streamlit Community Cloud for public access

## Author

**Ritam**
Aspiring Data Analyst | Python · SQL · Power BI · GenAI

---

*This project was built as part of a Generative AI + SQL integration exercise at Ivy Pro School.*
