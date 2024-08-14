from langchain_openai import ChatOpenAI
import os
import streamlit as st

def LLM(api_key):
    models = {
        "Falcon 180B": {
            "base_url": "https://api.ai71.ai/v1/",
            "api_key": os.getenv("AI71_API_KEY", api_key),
            "model": "tiiuae/falcon-180B-chat",
        },
        "Meta-Llama 3.1 70B Instruct-Turbo": {
            "base_url": "https://api.together.xyz/v1",
            "api_key": os.getenv("TOGETHER_API_KEY", api_key),
            "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        },
        "Gemma 2 9B": {
            "base_url": "https://api.together.xyz/v1",
            "api_key": os.getenv("TOGETHER_API_KEY", api_key),
            "model": "google/gemma-2-9b-it",
        },
        "Mistral 7B v.0.3": {
            "base_url": "https://api.together.xyz/v1",
            "api_key": os.getenv("TOGETHER_API_KEY", api_key),
            "model": "mistralai/Mistral-7B-Instruct-v0.3",
        },
    }

    # Model selection dropdown
    selected_model_name = st.selectbox(
        "Choose a model:",
        list(models.keys()),
        help="Falcon model requires AI71 api key all other from TOGETHER.AI",
    )

    # Initialize the selected model
    model_config = models[selected_model_name]
    llm = ChatOpenAI(**model_config)
    return llm, model_config['api_key']
