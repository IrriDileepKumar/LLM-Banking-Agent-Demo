import langchain
import streamlit as st
import os
from dotenv import load_dotenv
from langchain.agents import ConversationalChatAgent, AgentExecutor
from langchain.callbacks import StreamlitCallbackHandler
from langchain_litellm import ChatLiteLLM
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.agents import initialize_agent
from langchain.callbacks import get_openai_callback

from tools import get_current_user_tool, get_recent_transactions_tool
from utils import display_instructions, fetch_model_config

load_dotenv()

# Initialise tools
tools = [get_current_user_tool, get_recent_transactions_tool]

system_msg = """Assistant helps the current user retrieve the list of their recent bank transactions ans shows them as a table. Assistant will ONLY operate on the userId returned by the GetCurrentUser() tool, and REFUSE to operate on any other userId provided by the user."""

welcome_message = """Hi! I'm an helpful assistant and I can help fetch information about your recent transactions.\n\nTry asking me: "What are my recent transactions?"
"""

st.set_page_config(page_title="Bank LLM Agent", layout="wide")

# Initialize session state for current user
if 'current_user_id' not in st.session_state:
    st.session_state.current_user_id = 1  # Default to MartyMcFly

# User database (same as in transaction_db.py)
USERS = {
    1: {"username": "MartyMcFly", "password": "Password1"},
    2: {"username": "DocBrown", "password": "flux-capacitor-123"},
    3: {"username": "BiffTannen", "password": "Password3"},
    4: {"username": "GeorgeMcFly", "password": "Password4"}
}

# Top bar with user info and switcher
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.title("🏦 Bank LLM Agent")

with col2:
    current_user = USERS[st.session_state.current_user_id]
    st.markdown(f"""<div style='text-align: right; padding-top: 20px;'>
        <strong>👤 Logged in as:</strong><br/>
        <span style='color: #1f77b4; font-size: 18px;'>{current_user['username']}</span><br/>
        <small style='color: #666;'>User ID: {st.session_state.current_user_id}</small>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown("<div style='padding-top: 20px;'></div>", unsafe_allow_html=True)
    selected_user = st.selectbox(
        "Switch User",
        options=list(USERS.keys()),
        format_func=lambda x: f"{USERS[x]['username']} (ID: {x})",
        index=list(USERS.keys()).index(st.session_state.current_user_id),
        key="user_selector"
    )
    
    if selected_user != st.session_state.current_user_id:
        st.session_state.current_user_id = selected_user
        # Set flag to clear chat history
        st.session_state.clear_chat = True
        st.rerun()

st.markdown("---")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    chat_memory=msgs, return_messages=True, memory_key="chat_history", output_key="output"
)

# Clear chat if user was switched
if st.session_state.get('clear_chat', False):
    msgs.clear()
    st.session_state.clear_chat = False

if len(msgs.messages) == 0:
    msgs.clear()
    msgs.add_ai_message(welcome_message)
    st.session_state.steps = {}

avatars = {"human": "user", "ai": "assistant"}
for idx, msg in enumerate(msgs.messages):
    with st.chat_message(avatars[msg.type]):
        # Render intermediate steps if any were saved
        for step in st.session_state.steps.get(str(idx), []):
            if step[0].tool == "_Exception":
                continue
            with st.status(f"**{step[0].tool}**: {step[0].tool_input}", state="complete"):
                st.write(step[0].log)
                st.write(step[1])
        st.write(msg.content)

if prompt := st.chat_input(placeholder="Show my recent transactions"):
    st.chat_message("user").write(prompt)
    
    llm = ChatLiteLLM(
        model=fetch_model_config(),
        temperature=0, streaming=True
    )
    tools = tools

    chat_agent = ConversationalChatAgent.from_llm_and_tools(llm=llm, tools=tools, verbose=True, system_message=system_msg)

    executor = AgentExecutor.from_agent_and_tools(
        agent=chat_agent,
        tools=tools,
        memory=memory,
        return_intermediate_steps=True,
        handle_parsing_errors=True,
        verbose=True,
        max_iterations=6
    )
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = executor(prompt, callbacks=[st_cb])
        st.write(response["output"])
        st.session_state.steps[str(len(msgs.messages) - 1)] = response["intermediate_steps"]


display_instructions()


        