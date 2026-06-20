import mysql.connector
import streamlit as st
import google.genai as genai
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

API_KEY = os.getenv("GOOGLE_API_KEY")
c=genai.Client(api_key=API_KEY)

st.title("Natural Language to SQL Query Generator")
st.write("Ask questions about your database in plain English!")

def get_schema_from_database():
    conn = mysql.connector.connect(
        host= "localhost",        # Host name or IP address of the MySQL server
        port= "3306",
        user="root",    # Your MySQL username
        password="root",  # Your MySQL password
        database="loans_dataset"  # Name of the database you want to work with
    )
    cursor = conn.cursor()

    #Query to fetch table and column details
    cursor.execute("""
        select table_name, column_name, data_type
        from information_schema.columns
        where table_schema = 'loans_dataset';
    """)

    #Fetch schema details
    schema = cursor.fetchall()
    conn.close()
    return schema

#Get schema description dynamically from the database
schema = get_schema_from_database()
schema_df = pd.DataFrame(schema, columns=["Table Name", "Column Name", "Data Type"])
st.subheader("Database Schema")
st.dataframe(schema_df, width='stretch')

#User Question
user_question = st.text_input("Enter your question: ")

#Only run when button is clicked
if st.button("Generate & Run Query"):
    if not user_question.strip():
        st.warning("Please enter a question first.")
    else:
        question_with_schema = f"{schema} Based on the above schema, convert this question into a SQL query. Return only the raw SQL, no markdown, no explanation: {user_question}, if the question is not answerable based on the schema, then show an error message that says 'Question cannot be answered based on the provided schema.'"

#Generate SQL query using Google Gemini API
        with st.spinner("Generating SQL query..."):
                    response = c.models.generate_content(model="gemini-2.5-flash", contents=question_with_schema)
                    sql_query = response.text.strip()
                    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        
        st.subheader("Generated SQL Query")
        st.code(sql_query, language="sql")

# Execute the generated SQL and show results
        conn = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="root",
            database="loans_dataset"
        )
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()

        st.subheader("Query Results")
        if results:
                results_df = pd.DataFrame(results, columns=columns)
                st.dataframe(results_df, use_container_width=True)
                st.caption(f"{len(results_df)} row(s) returned.")
        else:
                st.info("Query ran successfully but returned no results.")