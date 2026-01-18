import streamlit as st
import base64
import yaml
import os

def display_instructions():
    from transaction_db import TransactionDb
    import json
    
    # Markdown with some basic CSS styles for the box
    box_css = """
    <style>
        .db-box {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 10px;
        }
        .user-header {
            font-weight: bold;
            color: #1f77b4;
            margin-bottom: 5px;
        }
        .transaction-item {
            font-size: 12px;
            padding: 5px;
            background-color: #fff;
            border-left: 3px solid #28a745;
            margin: 5px 0;
        }
    </style>
    """
    
    st.sidebar.markdown(box_css, unsafe_allow_html=True)
    st.sidebar.markdown("### 📊 Database Contents")
    
    # Fetch all data from database
    db = TransactionDb()
    cursor = db.conn.cursor()
    
    # Get all users
    cursor.execute("SELECT userId, username, password FROM Users ORDER BY userId")
    users = cursor.fetchall()
    
    # Display each user with their transactions
    for user in users:
        user_id, username, password = user
        
        st.sidebar.markdown(f"""
        <div class='db-box'>
            <div class='user-header'>👤 {username} (ID: {user_id})</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get transactions for this user
        cursor.execute("SELECT reference, recipient, amount FROM Transactions WHERE userId = ? ORDER BY transactionId", (user_id,))
        transactions = cursor.fetchall()
        
        if transactions:
            with st.sidebar.expander(f"💳 Transactions ({len(transactions)})", expanded=False):
                for ref, recipient, amount in transactions:
                    st.markdown(f"""
                    <div class='transaction-item'>
                        <strong>{ref}</strong><br/>
                        To: {recipient}<br/>
                        Amount: ${amount:.2f}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.sidebar.caption("No transactions")
    
    db.close()



# Function to convert image to base64
def get_image_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def display_logo():
    # Convert your image
    image_base64 = get_image_base64("labs-logo.png")

    # URL of the company website
    url = ''

    # HTML for centered image with hyperlink
    html_string = f"""
    <div style="display:flex; justify-content:center;">
        <a href="{url}" target="_blank">
        <img src="data:image/png;base64,{image_base64}" width="150px">
        </a>
    </div>
    """
    # Display the HTML in the sidebar
    st.sidebar.markdown(html_string, unsafe_allow_html=True)

def _load_llm_config():
    with open('llm-config.yaml', 'r') as f:
        yaml_data = yaml.load(f, Loader=yaml.SafeLoader)
    return yaml_data

def fetch_model_config():
    chosen_model_name = os.getenv("model_name")
    llm_config = _load_llm_config()
    for model_config in llm_config.get("models"):
        if chosen_model_name == model_config.get("model_name"):
            return model_config.get("model")
    else:
        return llm_config.get("default_model")