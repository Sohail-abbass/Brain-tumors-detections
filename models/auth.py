import app as st
from firebase_auth import login_user, register_user

def show_login_page():
    st.markdown('<h1 class="auth-title">Welcome back!</h1>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">Sign in to your credentials to access your account</p>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.form_submit_button("Login"):
                if email and password:
                    user = login_user(email, password)
                    if user:
                        st.session_state['user'] = user
                        st.session_state['authenticated'] = True
                        st.session_state['user_id'] = user['localId']
                        st.success("Login successful!")
                        st.rerun()
                else:
                    st.error("Please enter email and password")

def show_register_page():
    st.markdown('<h1 class="auth-title">Get Started Now</h1>', unsafe_allow_html=True)
    
    with st.form("register_form"):
        name = st.text_input("Name")
        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.form_submit_button("Register"):
            if not name or not email or not password:
                st.error("All fields are required!")
            elif password != confirm_password:
                st.error("Passwords don't match!")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                user = register_user(email, password, name)
                if user:
                    st.success("Registration successful! Please login.")
                    st.session_state['show_login'] = True