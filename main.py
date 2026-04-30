import streamlit as st

users = {
    "admin": "123",
    "abc": "abc123",
    "xyz": "xyz123"
}

# Page configuration
st.set_page_config(page_title="Login Page", layout="centered", initial_sidebar_state="collapsed")

# Center the content using columns
col1, col2, col3 = st.columns([1, 2, 1])  # center column is wider

with col2:  # place everything in the center column
    st.image("logo.png", width=400)
    st.markdown('<h1 style="font-size: 42px;">Supervisor Login</h1>', unsafe_allow_html=True, text_alignment="center")

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", placeholder="Enter your password", type="password")

        col11, col12 = st.columns([1, 3])
        login1 = col11.form_submit_button("Login")

        if login1:
            if not username or not password:
                st.warning("⚠️ Please fill in both username and password.")
            elif username in users and users[username] == password:
                st.session_state.logged_in = True
                st.switch_page("pages/VacNoti.py")
                
            else:
                st.error("❌ Invalid username or password.")
        
            