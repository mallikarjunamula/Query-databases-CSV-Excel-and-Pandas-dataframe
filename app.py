import streamlit as st
from langchain.agents.agent_types import AgentType
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.sql_database import SQLDatabase
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
import os
os.environ['OPENAI_API_KEY'] ='your-openai-key'
st.title("How to Query DataBase/CSV/Excel?")
pick = st.selectbox(
    "Choose Database/CSV/Excel:",
    ("CSV/Excel", "MySQL DataBase"))
llm = ChatOpenAI(temperature=0, model_name="gpt-4")
def mysqldb_agent(db, llm, input):
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True
    )
    return agent_executor.run(input)
def csv_excel_agent(df, llm, input):
    agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True,
    handle_parsing_error = True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    )
    return agent.run(input)
if pick == 'MySQL DataBase':
    st.subheader("Query MySQL Database:",divider='rainbow')
    db_user = st.text_input("UserName:","root")
    db_password = st.text_input("Password:","root")
    db_host = st.text_input("Host:","localhost")
    db_name = st.text_input("DBName:","bankdata")
    try:
        db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
        print("Database connection successful!")
    except Exception as e:
        # If an exception occurs, print an error message
        print(f"Error connecting to the database: {str(e)}")

    input_text  = st.text_input("Enter your question here:","What is the maximum transaction in database table?")
    button = st.button("Generate Response")
    if button and input_text:
        with st.spinner("Generating Response!..."):
            reply = mysqldb_agent(db, llm, input_text)
        st.write(reply)

elif pick == 'CSV/Excel':
    st.subheader("Using CSV/EXCEL:",divider='rainbow')
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            df = pd.read_excel(uploaded_file)
    input_text  = st.text_input("Enter your question here","What is the maximum transaction in the given data?")
    button = st.button("Generate Response")
    if button and input_text:
        with st.spinner("Generating Response!..."):
            reply = csv_excel_agent(df, llm, input_text)
        st.write(reply)


