__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
import sqlite3
from langchain_chroma import Chroma


import os
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_together.embeddings import TogetherEmbeddings
from visualize import map
from llm import model, prompt
from utils import datasources
from dotenv import load_dotenv

# load env vars
load_dotenv()


# init session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "default_model" not in st.session_state:
    st.session_state["default_model"] = ""

# show some text on page
st.title("FalconsEyeView")
st.text("Your 🦅 business consultant")
st.markdown("""###### Get answer for questions like:
            
##### Why? How? 🤔
With natural language processing and the power of foundational models like **Falcon**🦅 at the chat below.
##### How many? How much? 🔢
With quantitative data and visualizations on the left sidebar.
            
##### For example:
###### Customer satisfaction 😊
- What is the most favourite aspect of experiance? 
###### Product/Service impovements 🛍️ 
- What features or improvements could be added?
###### Business planning 💼
- Develop a perfect business concept based on market feedback.
- Create an ideal business model using customer insights.
### Have a chat with 🦅""")

with st.sidebar:
    try:
        api_key = st.text_input("API KEY", key="chatbot_api_key", type="password")
        try:
        # init LLM
            llm, api_key = model.LLM(api_key)
        except Exception as e:
            st.info("Enter Api Key")

        # datasource selection
        datasources_path = "./data"
        datasets = datasources.get_datasources(datasources_path)
        selected_datasource = st.selectbox("Choose a datasource:", datasets)

        # quantatative column for map visualization
        selected_column = "rating"
        if selected_datasource:
            selected_column = st.selectbox(
                "Choose a quantatative column for map visualization:",
                ("rating", "userRatingCount","scaledUserRatingCount"),
            )

        # load map
        map.load(datasources_path, selected_datasource, selected_column)
    except Exception as e:
        st.error(e)

# RAG
if api_key:
    try:
        # embeddings for rag
        embeddings = TogetherEmbeddings(model="togethercomputer/m2-bert-80M-8k-retrieval",together_api_key=os.getenv('TOGETHER_API_KEY'))
        db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        retriever = db.as_retriever(
            search_kwargs={"k": 4, "filter": {"query": selected_datasource}}
        )

        prompt = prompt.get_prompt()

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
    except Exception as e:
        st.error(e)

try:
    # chat
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    if prompt := st.chat_input():
        if not api_key:
            st.error("Enter api key.")
            st.stop()
        if not selected_datasource:
            st.info("Please select datasource")
            st.stop()
        # user
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = rag_chain.invoke(prompt).rstrip("User:")
        # assistant
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
except Exception as e:
    st.session_state.messages = []
    st.error(e)
