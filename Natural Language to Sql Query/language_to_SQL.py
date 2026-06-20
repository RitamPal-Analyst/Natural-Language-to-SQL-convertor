import mysql.connector
import google.genai as genai
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

API_KEY = os.getenv("GOOGLE_API_KEY")
c=genai.Client(api_key=API_KEY)

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

    #Format schema details as a string
    schema_description = ""
    for table, column, data_type in schema:
        schema_description += f"Table {table} has a Column {column} of Data Type {data_type}."

    return schema_description

#Get schema description dynamically from the database
schema_description = get_schema_from_database()

#User Question
user_question = input("Enter your question: ")

#Combine schema description and user question for the model input
question_with_schema = f"{schema_description} Based on the above schema, convert this question into a SQL query: {user_question}, if the question is not answerable based on the schema, then show an error message that says 'Question cannot be answered based on the provided schema.'"

#Generate SQL query using Google Gemini API
response = c.models.generate_content(model="gemini-2.5-flash",contents= question_with_schema)
sql_query = response.text.strip()
sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
print("Generated SQL Query:\n", sql_query)

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
conn.close()

print("\nQuery Results:")
for row in results:
    print(row)