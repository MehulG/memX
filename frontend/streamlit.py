# memX Streamlit Dashboard MVP

import streamlit as st
import secrets
import json
import time
import pandas as pd
from supabase import create_client, Client, ClientOptions

# --- Setup ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_SERVICE_KEY"]

# Initialize temporary client for login/signup
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Auth (signup/login) ---
st.title("🔐 memX Dashboard")
if "session" not in st.session_state:
    st.session_state.session = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

st.sidebar.title("Account")
auth_mode = st.sidebar.radio("Select Mode", ["login", "signup"])
st.session_state.auth_mode = auth_mode

if not st.session_state.session:
    with st.form("Auth"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Submit")
        if submitted:
            try:
                if st.session_state.auth_mode == "login":
                    session = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.session = session
                    st.success(f"Logged in as {email}")
                    time.sleep(1)
                    st.rerun()
                else:
                    session = supabase.auth.sign_up({"email": email, "password": password})
                    st.success(f"Signed up as {email}. Please check your email to confirm.")
                    st.session_state.session = session
                    time.sleep(1)
                    st.rerun()
            except Exception as e:
                st.error("{} failed: {}".format(st.session_state.auth_mode.capitalize(), str(e)))
    st.stop()

access_token = st.session_state.session.session.access_token
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
    options=ClientOptions(headers={"Authorization": f"Bearer {access_token}"})
)

user_id = st.session_state.session.user.id
user_prefix = user_id[:8]  # used to namespace scope keys

# --- API Key Viewer ---
st.header("🔑 Your API Keys")
st.caption(f"🔒 Namespace: `{user_prefix}` (automatically applied to all scopes)")

keys = supabase.table("api_keys").select("*").execute()
if keys.data:
    table_data = [
        {
            "Key": k["key"],
            "Read Scope": ", ".join(k["scopes"].get("read", [])),
            "Write Scope": ", ".join(k["scopes"].get("write", [])),
            "Created At": k["created_at"]
        }
        for k in keys.data
    ]
    df = pd.DataFrame(table_data)
    st.dataframe(df)
else:
    st.info("No keys found.")

# --- API Key Creator ---
st.header("➕ Create New API Key")

with st.form("create_key"):
    key_name = st.text_input("Name")
    read_scope = st.text_input("Read scope (comma-separated)", "agent:*")
    write_scope = st.text_input("Write scope (comma-separated)", "agent:goal")
    submit_key = st.form_submit_button("Create")

    if submit_key:
        api_key = secrets.token_hex(16)
        scopes = {
            "read": [f"{user_prefix}:{s.strip()}" for s in read_scope.split(",")],
            "write": [f"{user_prefix}:{s.strip()}" for s in write_scope.split(",")]
        }
        supabase.rpc("create_api_key", {
            "key_name": key_name,
            "key_value": api_key,
            "scopes": scopes,
            "is_active": True
        }).execute()
        st.success("API Key Created: {}".format(api_key))

# --- Memory Viewer (Optional) ---
# You could add polling here to connect to your FastAPI memX backend
# and display live key-value state or pub/sub logs.
