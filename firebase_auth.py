# # firebase_auth.py (in project root)
# import streamlit as st
# import pyrebase
# from firebase_config import FIREBASE_CONFIG

# # Initialize Firebase
# firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
# auth = firebase.auth()
# db = firebase.database()

# def login_user(email, password):
#     """Login with email/password"""
#     try:
#         user = auth.sign_in_with_email_and_password(email, password)
#         return user
#     except Exception as e:
#         error_msg = str(e)
#         if "INVALID_LOGIN_CREDENTIALS" in error_msg:
#             st.error("❌ Invalid email or password")
#         else:
#             st.error(f"Login failed: {error_msg}")
#         return None

# def register_user(email, password, username):
#     """Register new user"""
#     try:
#         # Create user
#         user = auth.create_user_with_email_and_password(email, password)
        
#         # Store user info
#         user_data = {
#             "username": username,
#             "email": email,
#             "created_at": {".sv": "timestamp"},
#             "role": "user"
#         }
        
#         # Save to database
#         db.child("users").child(user['localId']).set(user_data)
        
#         return user
#     except Exception as e:
#         error_msg = str(e)
#         if "EMAIL_EXISTS" in error_msg:
#             st.error("❌ Email already registered")
#         else:
#             st.error(f"Registration failed: {error_msg}")
#         return None
    

    # firebase_auth.py (in project root)
import app as st
import pyrebase
from firebase_config import FIREBASE_CONFIG

# Initialize Firebase
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = firebase.auth()
db = firebase.database()

def login_user(email, password):
    """Login with email/password"""
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        error_msg = str(e)
        if "INVALID_LOGIN_CREDENTIALS" in error_msg:
            st.error("❌ Invalid email or password")
        else:
            st.error(f"Login failed: {error_msg}")
        return None

def register_user(email, password, username):
    """Register new user"""
    try:
        # Create user
        user = auth.create_user_with_email_and_password(email, password)
        
        # Store user info
        user_data = {
            "username": username,
            "email": email,
            "created_at": {".sv": "timestamp"},
            "role": "user"
        }
        
        # Save to database
        db.child("users").child(user['localId']).set(user_data)
        
        return user
    except Exception as e:
        error_msg = str(e)
        if "EMAIL_EXISTS" in error_msg:
            st.error("❌ Email already registered")
        else:
            st.error(f"Registration failed: {error_msg}")
        return None

def google_sign_in():
    """
    Google Sign-In using Pyrebase
    Returns authenticated user info
    """
    try:
        # Get Google provider
        provider = pyrebase.auth.GoogleAuthProvider()
        
        # IMPORTANT: For Streamlit, we need to handle OAuth redirect
        # Pyrebase doesn't have built-in popup support for Streamlit
        # We'll use a manual OAuth flow
        
        # Show Google Sign-In button with OAuth URL
        google_client_id = FIREBASE_CONFIG.get("googleClientId", "")
        
        if not google_client_id:
            st.warning("⚠️ Google OAuth not configured in Firebase. Please add googleClientId to FIREBASE_CONFIG.")
            return None
        
        # Create OAuth URL
        redirect_uri = "http://localhost:8501"  # Streamlit default
        oauth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={google_client_id}&redirect_uri={redirect_uri}&response_type=code&scope=email%20profile&access_type=offline&prompt=consent"
        
        # Display Google Sign-In button
        st.markdown(f"""
        <div style="text-align: center;">
            <a href="{oauth_url}" target="_blank">
                <button style="
                    background-color: white;
                    color: #333;
                    border: 1px solid #ddd;
                    padding: 12px 24px;
                    border-radius: 8px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 12px;
                    font-weight: 600;
                    width: 100%;
                    font-size: 14px;
                    transition: all 0.3s;
                " onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)';" 
                onmouseout="this.style.boxShadow='none';">
                    <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="20" height="20">
                    Sign up with Google
                </button>
            </a>
            <p style="font-size: 12px; color: #666; margin-top: 10px;">
                Click the button to sign in with Google in a new tab
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check for OAuth callback
        query_params = st.experimental_get_query_params()
        
        if 'code' in query_params:
            authorization_code = query_params['code'][0]
            
            # Exchange authorization code for Google ID token
            import requests
            
            # Get tokens
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                'code': authorization_code,
                'client_id': google_client_id,
                'client_secret': FIREBASE_CONFIG.get("googleClientSecret", ""),
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            }
            
            response = requests.post(token_url, data=token_data)
            token_json = response.json()
            
            if 'id_token' in token_json:
                # Sign in to Firebase with Google credential
                try:
                    # Use Firebase REST API to sign in with Google
                    api_key = FIREBASE_CONFIG["apiKey"]
                    firebase_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={api_key}"
                    
                    payload = {
                        'postBody': f"id_token={token_json['id_token']}&providerId=google.com",
                        'requestUri': redirect_uri,
                        'returnIdpCredential': True,
                        'returnSecureToken': True
                    }
                    
                    firebase_response = requests.post(firebase_url, json=payload)
                    firebase_data = firebase_response.json()
                    
                    if 'idToken' in firebase_data:
                        # Create user object similar to Pyrebase
                        user = {
                            'idToken': firebase_data['idToken'],
                            'refreshToken': firebase_data.get('refreshToken', ''),
                            'localId': firebase_data.get('localId', ''),
                            'email': firebase_data.get('email', ''),
                            'displayName': firebase_data.get('displayName', ''),
                            'photoUrl': firebase_data.get('photoUrl', ''),
                            'providerId': 'google.com'
                        }
                        
                        # Check if user exists in database, if not create entry
                        user_id = user['localId']
                        user_ref = db.child("users").child(user_id).get()
                        
                        if not user_ref.val():
                            # Create new user entry
                            user_data = {
                                "username": user.get('displayName', user['email'].split('@')[0]),
                                "email": user['email'],
                                "created_at": {".sv": "timestamp"},
                                "role": "user",
                                "provider": "google",
                                "photo_url": user.get('photoUrl', '')
                            }
                            db.child("users").child(user_id).set(user_data)
                        
                        st.success("✅ Google Sign-In successful!")
                        return user
                
                except Exception as firebase_error:
                    st.error(f"Firebase sign-in error: {firebase_error}")
                    return None
        
        # Alternative: Manual token input for development
        with st.expander("🔧 Development Mode: Enter Google Token Manually"):
            st.info("For development/testing, you can manually paste a Google ID token")
            id_token_input = st.text_input("Google ID Token", type="password")
            
            if st.button("Sign in with Token"):
                if id_token_input:
                    try:
                        # Sign in with the token directly
                        credential = auth.sign_in_with_idp(id_token=id_token_input, provider="google.com")
                        
                        # Create/update user in database
                        user_id = credential['localId']
                        user_ref = db.child("users").child(user_id).get()
                        
                        if not user_ref.val():
                            user_data = {
                                "username": credential.get('displayName', credential['email'].split('@')[0]),
                                "email": credential['email'],
                                "created_at": {".sv": "timestamp"},
                                "role": "user",
                                "provider": "google",
                                "photo_url": credential.get('photoUrl', '')
                            }
                            db.child("users").child(user_id).set(user_data)
                        
                        st.success("✅ Google Sign-In successful!")
                        return credential
                    except Exception as token_error:
                        st.error(f"Token sign-in error: {token_error}")
        
        return None
        
    except Exception as e:
        st.error(f"Google Sign-In error: {str(e)}")
        return None

def sign_in_with_google_redirect():
    """
    Alternative method for Google Sign-In using redirect (for deployed apps)
    """
    try:
        # Create OAuth redirect URL
        redirect_url = auth.create_oauth_redirect_url("http://localhost:8501", "google.com")
        
        # Show redirect button
        st.markdown(f"""
        <div style="text-align: center;">
            <a href="{redirect_url}">
                <button style="
                    background-color: #4285F4;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 8px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 12px;
                    font-weight: 600;
                    width: 100%;
                    font-size: 14px;
                    transition: all 0.3s;
                ">
                    <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="20" height="20">
                    Continue with Google
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Check for redirect result
        try:
            result = auth.get_redirect_result()
            if result and result.user:
                user = result.user
                
                # Create/update user in database
                user_data = {
                    "username": user.display_name if user.display_name else user.email.split('@')[0],
                    "email": user.email,
                    "created_at": {".sv": "timestamp"},
                    "role": "user",
                    "provider": "google",
                    "photo_url": user.photo_url
                }
                
                db.child("users").child(user.uid).set(user_data)
                
                return {
                    'localId': user.uid,
                    'email': user.email,
                    'displayName': user.display_name,
                    'photoUrl': user.photo_url
                }
        except:
            pass  # No redirect result yet
        
        return None
        
    except Exception as e:
        st.error(f"Google redirect error: {str(e)}")
        return None

# Helper function for getting current user
def get_current_user():
    """Get current authenticated user"""
    try:
        # Check session state first
        if 'user' in st.session_state and st.session_state.user:
            return st.session_state.user
        
        # Try to get from Firebase (if token is still valid)
        # Note: Pyrebase doesn't have a built-in method for this
        # You'd need to store and check the token manually
        
        return None
    except:
        return None

# Helper function for logout
def logout_user():
    """Logout current user"""
    try:
        auth.current_user = None
        # Clear session state
        if 'user' in st.session_state:
            del st.session_state.user
        if 'user_id' in st.session_state:
            del st.session_state.user_id
        if 'username' in st.session_state:
            del st.session_state.username
        return True
    except:
        return False