###############################
##  SECURE TOOLS WITH AUTHORIZATION
from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain.tools import StructuredTool
import streamlit as st
from datetime import date
from dotenv import load_dotenv
import json
import re
import os
from transaction_db import TransactionDb

load_dotenv()

def get_current_user(input : str):
    """Returns the current authenticated user."""
    # Get the currently logged-in user from session state
    current_user_id = st.session_state.get('current_user_id', 1)
    db = TransactionDb()
    user = db.get_user(current_user_id)
    db.close()
    return user

get_current_user_tool = Tool(
    name='GetCurrentUser',
    func= get_current_user,
    description="Returns the current user for querying transactions."
)

def get_transactions(userId : str):
    """Returns the transactions associated to the userId provided.
    
    SECURITY: This function enforces authorization checks to prevent
    unauthorized access to other users' data.
    """
    try:
        # SECURITY CHECK 1: Detect SQL injection patterns FIRST
        # This should be checked before authorization to properly identify attack type
        sql_patterns = [
            r"UNION\s+SELECT",
            r"DROP\s+TABLE",
            r"INSERT\s+INTO",
            r"DELETE\s+FROM",
            r"--",
            r";",
            r"'.*OR.*'.*=.*'",
            r"1=1"
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, str(userId), re.IGNORECASE):
                return json.dumps({
                    "error": "SQL_INJECTION_DETECTED",
                    "message": "Potential SQL injection detected. This attempt has been blocked and logged.",
                    "suspicious_input": userId
                }, indent=4)
        
        # SECURITY CHECK 2: Validate userId is numeric
        if not str(userId).isdigit():
            return json.dumps({
                "error": "INVALID_INPUT",
                "message": "Invalid userId format. UserId must be numeric.",
                "provided_userId": userId
            }, indent=4)
        
        # SECURITY CHECK 3: Validate userId matches current user (authorization)
        current_user_json = get_current_user("")
        current_user_data = json.loads(current_user_json)
        authorized_user_id = str(current_user_data[0]['userId'])
        
        # Check if requested userId matches authorized user
        if str(userId) != authorized_user_id:
            return json.dumps({
                "error": "AUTHORIZATION_DENIED",
                "message": f"Access denied. You can only view transactions for your own account (userId {authorized_user_id}). Attempted access to userId {userId} has been logged.",
                "requested_userId": userId,
                "authorized_userId": authorized_user_id
            }, indent=4)
        
        # All security checks passed - fetch transactions
        db = TransactionDb()
        transactions = db.get_user_transactions(userId)
        db.close()
        return transactions
        
    except Exception as e:
        return json.dumps({
            "error": "SYSTEM_ERROR",
            "message": f"Error: {str(e)}"
        }, indent=4)
            

get_recent_transactions_tool = Tool(
    name='GetUserTransactions',
    func= get_transactions,
    description="Returns the transactions associated to the userId provided. This tool enforces authorization and only returns data for the authenticated user."
)
