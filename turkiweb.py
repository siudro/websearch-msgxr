import streamlit as st
from openai import OpenAI
import requests
api_llm = st.secrets["api_llm"]
api_web = st.secrets["api_web"]
if "messages" not in st.session_state:
    st.session_state.messages = []
def web(question,api):
    url = "https://serpapi.com/search"
    params = {"q":question, "api_key": api, "engine":"google"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    results = data.get("organic_results", [])
    return " ".join(result.get("snippet", "") for result in results)
 
def respond(api, pormpt):
    clinet = OpenAI(api_key=api)
    response = clinet.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": "you are a helpful assistant using web search results to answer questions"}
            ,
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
st.title("chat with the whole internet😉")
st.subheader("ask me anything and i will search the web for you")
user = st.text_input("اسالني")
if user:
    result = web(user,api_web)
    if result: 
        prompt = f"based on on these search results, answer the qustion: '{user}'\n\nresults: '{result}'" 
        ai = respond(api_llm, prompt) 
        st.session_state.messages.append({'role"': "assistant", "content": ai})
for msg in st.session_state.messages:
    st.write(msg["content"])
