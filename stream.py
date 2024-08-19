# import streamlit as st
# import pandas as pd
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# from meta_ai_api import MetaAI
# import pymysql

# # db_url = "mysql+pymysql://root:Sritesh@1234@localhost:3306/student_db"

# db_url = pymysql.connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     password='Sritesh@1234',
#     database='student_db'
# )

# # Function to execute SQL queries
# def execute_query(query, params=None):
#     engine = create_engine(db_url)
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     try:
#         result = session.execute(text(query), params)
#         session.commit()
#         columns = result.keys()
#         rows = result.fetchall()
#         return pd.DataFrame(rows, columns=columns)
#     except Exception as e:
#         session.rollback()
#         st.error(f"An error occurred: {e}")
#         return None
#     finally:
#         session.close()

# # Function to fetch table names
# def get_table_names():
#     engine = create_engine(db_url)
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     try:
#         result = session.execute(text("SHOW TABLES"))
#         tables = [row[0] for row in result]
#         return tables
#     except Exception as e:
#         st.error(f"An error occurred: {e}")
#         return []
#     finally:
#         session.close()

# # Function to fetch schema description of a table
# def get_table_schema(table_name):
#     engine = create_engine(db_url)
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     try:
#         result = session.execute(text(f"DESCRIBE {table_name}"))
#         schema = ', '.join([f"{row[0]} {row[1]}" for row in result])
#         return schema
#     except Exception as e:
#         st.error(f"An error occurred: {e}")
#         return ""
#     finally:
#         session.close()

# # Function to interact with MetaAI
# def metaAi(schema_description, user_question):
#     ai = MetaAI()
    
#     prompt = f'I have the following database schema: "{schema_description}" Based on this schema, please generate an SQL query for the following user question: "{user_question}" Provide only the SQL query without any additional text and formatting. And if invalid question is provided then return "INVALID STATEMENT" '
#     response = ai.prompt(message=prompt)
#     print(response)
    
#     return response['message']

# # Streamlit UI
# def main():
#     st.title("QueryGenAI")

#     tables = get_table_names()
#     if not tables:
#         st.error("No tables found in the database.")
#         return

#     chosen_table = st.selectbox("Choose a table", tables)

#     if chosen_table:
#         schema = get_table_schema(chosen_table)
#         schema = str(chosen_table) + ":(" + str(schema) + ")"

#         ques = st.text_input("Please Ask Question:")
#         if st.button("Generate Query"):
#             query = metaAi(schema, ques)
#             if query == "INVALID STATEMENT":
#                 st.error("Ask a valid question.")
#             else:
#                 result_df = execute_query(query)
#                 if result_df is not None and not result_df.empty:
#                     st.write("Results:")
#                     st.dataframe(result_df)
#                 else:
#                     st.write("No results found or an error occurred.")

# if __name__ == "__main__":
#     main()



import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from meta_ai_api import MetaAI
import pymysql
import urllib.parse
from urllib.parse import quote_plus
import os


# Define the connection URL
db_url = os.environ["PATH"]


print(db_url)

# Function to execute SQL queries
def execute_query(query, params=None):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(text(query), params)
        session.commit()
        columns = result.keys()
        rows = result.fetchall()
        return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        session.rollback()
        st.error(f"An error occurred: {e}")
        return None
    finally:
        session.close()

# Function to fetch table names
def get_table_names():
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        return tables
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []
    finally:
        session.close()

# Function to fetch schema description of a table
def get_table_schema(table_name):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(text(f"DESCRIBE {table_name}"))
        schema = ', '.join([f"{row[0]} {row[1]}" for row in result])
        return schema
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""
    finally:
        session.close()

# Function to interact with MetaAI
def metaAi(schema_description, user_question):
    ai = MetaAI()
    
    prompt = f'I have the following database schema: "{schema_description}" Based on this schema, please generate an SQL query for the following user question: "{user_question}" Provide only the SQL query without any additional text and formatting. And if an invalid question is provided then return "INVALID STATEMENT".'
    response = ai.prompt(message=prompt)
    print(response['message'])
    return response['message']

# Streamlit UI
def main():
    st.title("QueryGenAI")

    tables = get_table_names()
    if not tables:
        st.error("No tables found in the database.")
        return

    chosen_table = st.selectbox("Choose a table", tables)

    if chosen_table:
        schema = get_table_schema(chosen_table)
        schema = str(chosen_table) + ":(" + str(schema) + ")"

        ques = st.text_input("Please Ask Question:")
        if st.button("Generate Query"):
            query = metaAi(schema, ques)
            if query == "INVALID STATEMENT":
                st.error("Ask a valid question.")
            else:
                result_df = execute_query(query)
                if result_df is not None and not result_df.empty:
                    st.write("Results:")
                    st.dataframe(result_df)
                else:
                    st.write("No results found or an error occurred.")

if __name__ == "__main__":
    main()

