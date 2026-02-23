# models/streamlit.py - COMPLETELY FIXED VERSION
import streamlit as st
import numpy as np
import cv2
import joblib
from tensorflow.keras.models import load_model
import os
import sys

# ==================== FIX 1: CORRECT IMPORT PATHS ====================
# Get absolute path to project root
current_dir = os.path.dirname(os.path.abspath(__file__))  # models folder
project_root = os.path.dirname(current_dir)  # Fyp folder (one level up)

# Add project root to Python path so we can import firebase files
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import Firebase auth with Google Sign-In
try:
    from firebase_auth import login_user, register_user, google_sign_in
    from firebase_config import FIREBASE_CONFIG
    FIREBASE_ENABLED = True
    FIREBASE_CONFIGURED = True
except ImportError as e:
    st.warning(f"⚠️ Firebase not configured: {e}")
    FIREBASE_ENABLED = False
    FIREBASE_CONFIGURED = False
except Exception as e:
    st.warning(f"⚠️ Firebase error: {e}")
    FIREBASE_ENABLED = False
    FIREBASE_CONFIGURED = False

# ==================== FIX 2: CORRECT MODEL PATHS ====================
# Model paths - files are in models/ folder
MODEL_PATH = os.path.join(current_dir, "brain_tumor_cnn.h5")
ENCODER_PATH = os.path.join(current_dir, "label_encoder.pkl")

# Page configuration
st.set_page_config(
    page_title="Brain Tumor Detection",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
# if 'authenticated' not in st.session_state:
#     st.session_state.authenticated = False
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = True
    st.session_state.username = "Guest User"
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'login_tab' not in st.session_state:
    st.session_state.login_tab = 'login'  # Default to login tab

# ==================== CUSTOM CSS ====================
def inject_auth_css():
    st.markdown("""
    <style>
    /* Main container - CENTERED */
    .main-container {
        display: flex;
        justify-content: center;
        align-items: center;
        # min-height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Auth container - WHITE BOX */
    .auth-container {
        width: 100%;
        # max-width: 450px;
        padding: 2.5rem;
        # background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin: 0 auto;
    }
    
    /* Toggle container - CENTERED TOP */
    .toggle-container {
        display: flex;
        background: #f8f9fa;
        border-radius: 12px;
        padding: 5px;
        margin: 0 auto 2rem auto;
        width: fit-content;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .toggle-btn {
        padding: 10px 30px;
        border: none;
        border-radius: 8px;
        background: transparent;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s;
        color: #666;
    }
    
    .toggle-btn.active {
        background: white;
        color: #4285f4;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Titles */
    .auth-title {
        font-size: 28px;
        font-weight: 700;
        color: #1a1a1a !important;
        margin-bottom: 0.5rem;
        text-align: left;
    }
    
    .auth-subtitle {
        font-size: 14px;
        color: #666 !important;
        text-align: left;
        margin-bottom: 2rem;
        line-height: 1.5;
    }
    
    /* Form styling - FIXED TEXT COLOR */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        padding: 0.75rem 1rem;
        font-size: 14px;
        transition: all 0.3s;
        background: #f8f9fa;
        color: #1a1a1a !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #999 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4285f4;
        box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.1);
        background: white;
        color: #1a1a1a !important;
    }
    
    /* Label styling */
    .form-label {
        font-size: 12px;
        font-weight: 600;
        color: #333 !important;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 0.75rem;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s;
        border: none;
        margin-top: 1rem;
    }
    
    .primary-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    .primary-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(102, 126, 234, 0.3);
    }
    
    .secondary-btn {
        background: white !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
    }
    
    .secondary-btn:hover {
        background: #f8f9fa !important;
        border-color: #ccc !important;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
    
    /* Links */
    .auth-link {
        text-align: center;
        margin-top: 2rem;
        font-size: 14px;
        color: #666 !important;
    }
    
    .auth-link span {
        color: #4285f4 !important;
        cursor: pointer;
        font-weight: 600;
        text-decoration: none;
    }
    
    .auth-link span:hover {
        text-decoration: underline;
    }
    
    /* Forgot password */
    .forgot-password {
        text-align: right;
        margin-top: 0.5rem;
        font-size: 12px;
    }
    
    .forgot-password a {
        color: #4285f4 !important;
        text-decoration: none;
    }
    
    .forgot-password a:hover {
        text-decoration: underline;
    }
    
    /* Divider */
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.5rem 0;
        color: #666 !important;
        font-size: 12px;
    }
    
    .divider::before,
    .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .divider::before {
        margin-right: 1rem;
    }
    
    .divider::after {
        margin-left: 1rem;
    }
    
    /* Main app styling - FIX TEXT COLORS */
    .main-app h1, .main-app h2, .main-app h3, .main-app p, .main-app div, .main-app span {
        color: #1a1a1a !important;
    }
    
    .main-app .stAlert {
        color: #1a1a1a !important;
    }
    
    /* Fix progress bar text */
    .stProgress > div > div > div > div {
        color: #1a1a1a !important;
    }
    
    /* Fix metric text */
    .stMetric {
        color: #1a1a1a !important;
    }
    
    /* Fix expander text */
    .streamlit-expanderHeader {
        color: #1a1a1a !important;
    }
    
    /* Google button icon */
    .google-icon {
        width: 18px;
        height: 18px;
        margin-right: 10px;
        vertical-align: middle;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== TOGGLE COMPONENT ====================
def show_toggle():
    """Show centered toggle buttons for login/register"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        toggle_html = f"""
        <div class="toggle-container">
            <button class="toggle-btn {'active' if st.session_state.login_tab == 'login' else ''}" 
                    onclick="window.streamlitTabs.setTab('login')">Login</button>
            <button class="toggle-btn {'active' if st.session_state.login_tab == 'register' else ''}" 
                    onclick="window.streamlitTabs.setTab('register')">Register</button>
        </div>
        """
        st.markdown(toggle_html, unsafe_allow_html=True)

# ==================== AUTH PAGES ====================
def show_login_page():
    """Display login page"""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="auth-title">Welcome back!</h1>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">Sign in to your credentials to access your account</p>', unsafe_allow_html=True)
    
    # Form
    with st.form("login_form", clear_on_submit=False):
        # Email field
        st.markdown('<label class="form-label">Email address</label>', unsafe_allow_html=True)
        email = st.text_input(" ", label_visibility="collapsed", placeholder="Enter your email", key="login_email")
        
        # Password field with forgot password
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown('<label class="form-label">Password</label>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="forgot-password"><a href="#">Forgot?</a></div>', unsafe_allow_html=True)
        
        password = st.text_input(" ", type="password", label_visibility="collapsed", 
                                placeholder="Enter your password", key="login_password")
        
        # Login button
        submit = st.form_submit_button("Login", use_container_width=True)
        if submit:
            st.markdown('<style>.stButton > button {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; color: white !important;}</style>', unsafe_allow_html=True)
        
        if submit:
            if not email or not password:
                st.error("Email and password are required!")
            else:
                if FIREBASE_ENABLED:
                    user = login_user(email, password)
                    if user:
                        st.session_state['authenticated'] = True
                        st.session_state['user'] = user
                        st.session_state['user_id'] = user.get('localId')
                        st.session_state['username'] = user.get('displayName', email.split('@')[0])
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password!")
                else:
                    # Demo mode
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = email.split('@')[0] if '@' in email else "User"
                    st.success("✅ Demo login successful!")
                    st.rerun()
    
    # Login link
    st.markdown('<div class="auth-link">Don\'t have an account? <span onclick="window.streamlitTabs.setTab(\'register\')">Sign up</span></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_register_page():
    """Display registration page with Google Sign-In"""
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="auth-title">Get Started Now</h1>', unsafe_allow_html=True)
    
    # Form
    with st.form("register_form", clear_on_submit=False):
        # Name field
        st.markdown('<label class="form-label">Name</label>', unsafe_allow_html=True)
        name = st.text_input(" ", label_visibility="collapsed", placeholder="Enter your full name", key="reg_name")
        
        # Email field
        st.markdown('<label class="form-label">Email address</label>', unsafe_allow_html=True)
        email = st.text_input(" ", label_visibility="collapsed", placeholder="Enter your email", key="reg_email")
        
        # Password field
        st.markdown('<label class="form-label">Password</label>', unsafe_allow_html=True)
        password = st.text_input(" ", type="password", label_visibility="collapsed", 
                                placeholder="Create a password", key="reg_password")
        
        # Confirm password field
        st.markdown('<label class="form-label">Confirm Password</label>', unsafe_allow_html=True)
        confirm_password = st.text_input(" ", type="password", label_visibility="collapsed", 
                                        placeholder="Confirm your password", key="reg_confirm")
        
        # Register button
        submit = st.form_submit_button("Register", use_container_width=True)
        if submit:
            st.markdown('<style>.stButton > button {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; color: white !important;}</style>', unsafe_allow_html=True)
        
        if submit:
            # Validation
            if not name or not email or not password or not confirm_password:
                st.error("❌ All fields are required!")
            elif password != confirm_password:
                st.error("❌ Passwords do not match!")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters long!")
            elif "@" not in email or "." not in email:
                st.error("❌ Please enter a valid email address!")
            else:
                if FIREBASE_ENABLED:
                    user = register_user(email, password, name)
                    if user:
                        st.success("✅ Registration successful! Please login.")
                        st.session_state['login_tab'] = 'login'
                        st.rerun()
                    else:
                        st.error("❌ Registration failed. Email might already exist.")
                else:
                    # Demo mode
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = name
                    st.success("✅ Demo registration successful!")
                    st.rerun()
    
    # Google Sign-In button for Register page
    st.markdown('<div class="divider">or continue with</div>', unsafe_allow_html=True)
    
    # Create custom Google button
    google_html = """
    <div style="text-align: center;">
        <button onclick="window.streamlitGoogleSignIn()" style="
            width: 100%;
            background: white;
            color: #333;
            border: 1px solid #ddd;
            padding: 12px 24px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            transition: all 0.3s;
            margin: 0;
        ">
            <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" 
                 width="18" height="18" class="google-icon">
            Sign up with Google
        </button>
    </div>
    """
    
    st.markdown(google_html, unsafe_allow_html=True)
    
    # Handle Google Sign-In
    if st.button(" ", key="google_register_hidden", help="Google Sign-In"):
        pass  # This is just to capture the button click
    
    # Check if Google button was clicked
    if st.session_state.get('google_register_hidden', False):
        if FIREBASE_CONFIGURED:
            with st.spinner("Signing in with Google..."):
                try:
                    user = google_sign_in()
                    if user:
                        st.session_state['authenticated'] = True
                        st.session_state['user'] = user
                        st.session_state['user_id'] = user.get('localId') or user.get('uid')
                        st.session_state['username'] = user.get('displayName', 'Google User')
                        st.success("✅ Google Sign-In successful!")
                        st.rerun()
                    else:
                        st.error("❌ Google Sign-In failed. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error during Google Sign-In: {str(e)}")
        else:
            st.info("🔧 Google OAuth requires Firebase configuration. Running in demo mode.")
            st.session_state['authenticated'] = True
            st.session_state['username'] = "Google User"
            st.success("✅ Demo Google Sign-In successful!")
            st.rerun()
    
    # Login link
    st.markdown('<div class="auth-link">Already have an account? <span onclick="window.streamlitTabs.setTab(\'login\')">Sign in</span></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== MAIN APP (Brain Tumor Detection) ====================
def show_brain_tumor_app():
    """Main brain tumor detection app after login"""
    # Load models
    with st.spinner("🔄 Loading AI models..."):
        model, encoder, class_labels = load_models()
    
    if model is None or encoder is None:
        st.error("❌ Failed to load AI models. Please check model files.")
        return
    
    # Sidebar with user info and logout
    with st.sidebar:
        st.title(f"👤 Welcome, {st.session_state.get('username', 'User')}!")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            st.session_state['authenticated'] = False
            st.session_state['user'] = None
            st.session_state['username'] = None
            st.rerun()
        
        st.markdown("---")
        st.info("**How to use:**")
        st.write("1. Upload a brain MRI image")
        st.write("2. Wait for AI analysis")
        st.write("3. View results")
        st.write("4. Consult a doctor")
    
    # Main content
    st.title("🧠 Brain Tumor Detection App")
    st.markdown('<div class="main-app">', unsafe_allow_html=True)
    st.write("Upload a **brain MRI image** to detect the tumor type.")
    
    uploaded_file = st.file_uploader(
        "Choose a brain MRI image...", 
        type=["jpg", "jpeg", "png"],
        help="Please upload a proper brain MRI scan in JPG, JPEG or PNG format"
    )
    
    # Show warning if no file is uploaded
    if uploaded_file is None:
        st.warning("⚠️ Please upload a brain MRI image to get a prediction.")
        st.info("""
        **What to upload:**
        - Brain MRI scan images
        - Axial, coronal, or sagittal views
        - Grayscale medical images
        
        **Supported formats:** JPG, JPEG, PNG
        """)
    else:
        try:
            # Validate file size
            file_size = len(uploaded_file.getvalue())
            if file_size < 1024:
                st.error("❌ File is too small. Please upload a proper MRI image.")
                return
            elif file_size > 10 * 1024 * 1024:
                st.error("❌ File is too large. Maximum size is 10MB.")
                return
            
            # Read and validate image
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            
            if len(file_bytes) == 0:
                st.error("❌ Cannot read file. The file might be corrupted.")
                return
            
            # Try to decode image
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            if img is None:
                st.error("❌ Cannot decode image. Please upload a valid image file.")
                return
            
            # Check if image is MRI
            st.subheader("🔍 Validating MRI Scan...")
            with st.spinner("Analyzing image characteristics..."):
                is_mri, mri_reason = is_mri_image(img)
                
                if not is_mri:
                    st.error(f"❌ **NOT A VALID BRAIN MRI SCAN**")
                    st.error(f"**Reason:** {mri_reason}")
                    
                    # Show image analysis
                    st.subheader("📊 Image Analysis")
                    analysis = analyze_image_characteristics(img)
                    
                    for key, value in analysis.items():
                        st.write(f"**{key}:** {value}")
                    
                    st.warning("**This doesn't look like a brain MRI scan.**")
                    
                    # Show the uploaded image
                    st.subheader("📤 Uploaded Image (For Reference)")
                    try:
                        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        st.image(img_rgb, caption="Your uploaded image", use_column_width=True)
                    except:
                        st.image(img, caption="Your uploaded image", use_column_width=True)
                    
                    return
                else:
                    st.success(f"✅ **VALID BRAIN MRI SCAN DETECTED**")
                    st.info(f"**Validation result:** {mri_reason}")
            
            # Show uploaded image preview
            st.subheader("📤 Uploaded MRI Scan")
            col1, col2 = st.columns(2)
            
            with col1:
                # Show original image
                try:
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    st.image(img_rgb, caption="Original MRI Scan", use_column_width=True)
                except:
                    st.image(img, caption="Original MRI Scan", use_column_width=True)
            
            with col2:
                # Show grayscale preview
                if len(img.shape) == 3:
                    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                else:
                    gray_img = img
                st.image(gray_img, caption="Grayscale View", use_column_width=True, clamp=True)
            
            # Preprocess image for model
            st.subheader("🔍 Processing MRI Image...")
            with st.spinner("Preprocessing MRI scan for tumor analysis..."):
                if len(img.shape) == 3:
                    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                else:
                    gray_img = img
                
                img_resized = cv2.resize(gray_img, (224, 224))
                img_normalized = img_resized.astype("float32") / 255.0
                img_expanded = np.expand_dims(img_normalized, axis=-1)
                img_batch = np.expand_dims(img_expanded, axis=0)
            
            # Make prediction
            st.subheader("🧠 Analyzing for Brain Tumors...")
            with st.spinner("Analyzing MRI scan for tumor detection..."):
                try:
                    preds = model.predict(img_batch, verbose=0)
                    predicted_class = np.argmax(preds, axis=1)[0]
                    confidence = np.max(preds)
                    
                    # Show results
                    st.subheader("📋 Diagnosis Results")
                    
                    col_result1, col_result2 = st.columns([1, 2])
                    
                    with col_result1:
                        st.metric(label="Prediction", value=class_labels[predicted_class])
                    
                    with col_result2:
                        confidence_percent = confidence * 100
                        st.write(f"**Confidence:** {confidence:.2%}")
                        
                        # Create a container for the progress bar
                        progress_container = st.container()
                        
                        with progress_container:
                            # Progress bar labels
                            col_labels = st.columns(3)
                            with col_labels[0]:
                                st.markdown("<div style='text-align: left; font-size: 12px; color: #666;'>0%</div>", unsafe_allow_html=True)
                            with col_labels[1]:
                                st.markdown("<div style='text-align: center; font-size: 12px; color: #666;'>50%</div>", unsafe_allow_html=True)
                            with col_labels[2]:
                                st.markdown("<div style='text-align: right; font-size: 12px; color: #666;'>100%</div>", unsafe_allow_html=True)
                            
                            # Custom progress bar using st.progress with custom styling
                            st.markdown(f"""
                            <div style="
                                background: white; 
                                border: 1px solid #e0e0e0; 
                                border-radius: 10px; 
                                padding: 2px; 
                                margin-bottom: 5px;
                                box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
                            ">
                                <div style="
                                    background: #4CAF50; 
                                    height: 24px; 
                                    border-radius: 8px; 
                                    width: {confidence_percent}%;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    color: #ff0000 !important;
                                    font-weight: bold;
                                    font-size: 13px;
                                    transition: width 0.5s ease;
                                ">
                                    {confidence_percent:.1f}%
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("<div style='text-align: center; font-size: 11px; color: #888; margin-top: 5px;'>AI Confidence Level</div>", unsafe_allow_html=True)
                    
                    # Detailed probabilities
                    with st.expander("📈 Detailed Probabilities"):
                        for i, (label, prob) in enumerate(zip(class_labels, preds[0])):
                            st.write(f"**{label}:** {prob:.2%}")
                    
                    # Interpretation
                    st.subheader("💡 Interpretation")
                    if class_labels[predicted_class] == "notumor":
                        st.success("✅ No tumor detected in the MRI scan.")
                        st.info("This is a healthy brain MRI. However, always consult with a medical professional for accurate diagnosis.")
                    else:
                        st.warning(f"⚠️ Potential **{class_labels[predicted_class]}** detected.")
                        st.error("**Important:** This is an AI prediction. Please consult with a qualified neurologist or radiologist for proper medical diagnosis and treatment.")
                    
                except Exception as e:
                    st.error(f"❌ Error during prediction: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== MRI VALIDATION FUNCTIONS ====================
def is_mri_image(img):
    """
    Validate if the uploaded image is a brain MRI scan.
    Returns (is_mri: bool, reason: str)
    """
    try:
        # Check 1: Image dimensions
        height, width = img.shape[:2]
        
        # MRI scans typically have square-ish dimensions
        aspect_ratio = width / height
        if aspect_ratio < 0.5 or aspect_ratio > 2.0:
            return False, f"Image aspect ratio ({aspect_ratio:.2f}) doesn't match typical MRI scans"
        
        # Check 2: Image is grayscale (MRI scans are typically grayscale)
        if len(img.shape) == 3:  # Color image
            # Convert to grayscale for analysis
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray_img = img
        
        # Check 3: Check for MRI-like intensity distribution
        mean_intensity = np.mean(gray_img)
        
        # MRI scans typically have moderate intensity values
        if mean_intensity < 30 or mean_intensity > 220:
            return False, f"Image intensity (mean={mean_intensity:.1f}) doesn't match MRI characteristics"
        
        # Check 4: Check for brain-like structures using edge detection
        edges = cv2.Canny(gray_img, 50, 150)
        edge_density = np.sum(edges > 0) / (height * width)
        
        # MRI brain scans have moderate edge density
        if edge_density < 0.01 or edge_density > 0.3:
            return False, f"Edge density ({edge_density:.3f}) doesn't match brain MRI patterns"
        
        return True, "Image appears to be a valid brain MRI scan"
        
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def analyze_image_characteristics(img):
    """Provide detailed analysis of uploaded image"""
    analysis = {}
    
    if len(img.shape) == 3:
        analysis["Color Channels"] = f"{img.shape[2]} (Color image)"
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        analysis["Color Channels"] = "1 (Grayscale)"
        gray_img = img
    
    height, width = gray_img.shape[:2]
    analysis["Dimensions"] = f"{width} x {height} pixels"
    analysis["Aspect Ratio"] = f"{width/height:.2f}"
    analysis["Mean Intensity"] = f"{np.mean(gray_img):.1f}"
    analysis["Intensity Std"] = f"{np.std(gray_img):.1f}"
    
    # Edge density
    edges = cv2.Canny(gray_img, 50, 150)
    edge_density = np.sum(edges > 0) / (height * width)
    analysis["Edge Density"] = f"{edge_density:.3f}"
    
    return analysis

@st.cache_resource
def load_models():
    try:
        if not os.path.exists(MODEL_PATH):
            st.error(f"❌ Model file not found at: {MODEL_PATH}")
            return None, None, None
        if not os.path.exists(ENCODER_PATH):
            st.error(f"❌ Encoder file not found at: {ENCODER_PATH}")
            return None, None, None
            
        model = load_model(MODEL_PATH)
        encoder = joblib.load(ENCODER_PATH)
        class_labels = list(encoder.classes_)
        
        return model, encoder, class_labels
    except Exception as e:
        st.error(f"❌ Error loading models: {str(e)}")
        return None, None, None

# ==================== MAIN FUNCTION ====================
def main():
    """Main function"""
    # Inject CSS
    inject_auth_css()
    
    # Add JavaScript for tab switching
    st.markdown("""
    <script>
    // Store tab functions in window object
    window.streamlitTabs = {
        setTab: function(tabName) {
            // Update session state via Streamlit
            const data = {tab: tabName};
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: data}, '*');
        }
    };
    
    window.streamlitGoogleSignIn = function() {
        // Trigger Google Sign-In
        const data = {action: 'google_signin'};
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: data}, '*');
    };
    </script>
    """, unsafe_allow_html=True)
    
    # Check for JavaScript messages
    if 'js_message' not in st.session_state:
        st.session_state.js_message = None
    
    # Check authentication
    if not st.session_state.authenticated:
        # Main centered container
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # Centered auth container
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Show centered toggle
            show_toggle()
            
            # Show appropriate form based on tab
            if st.session_state.login_tab == 'login':
                show_login_page()
            else:
                show_register_page()
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close main container
        
        # Tab switching logic
        if st.button("Switch to Register", key="switch_to_register"):
            st.session_state.login_tab = 'register'
            st.rerun()
        
        if st.button("Switch to Login", key="switch_to_login"):
            st.session_state.login_tab = 'login'
            st.rerun()
        
        # Handle Google Sign-In
        if st.session_state.get('google_register_hidden', False):
            if FIREBASE_CONFIGURED:
                with st.spinner("Signing in with Google..."):
                    try:
                        user = google_sign_in()
                        if user:
                            st.session_state['authenticated'] = True
                            st.session_state['user'] = user
                            st.session_state['user_id'] = user.get('localId') or user.get('uid')
                            st.session_state['username'] = user.get('displayName', 'Google User')
                            st.success("✅ Google Sign-In successful!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Google Sign-In error: {str(e)}")
            else:
                st.session_state['authenticated'] = True
                st.session_state['username'] = "Google User"
                st.rerun()
        
    else:
        # Show main app
        show_brain_tumor_app()
    
    # Footer with disclaimer
    st.markdown("---")
    st.caption("""
    **⚠️ IMPORTANT MEDICAL DISCLAIMER:** 
    This AI tool is for **educational and research purposes only**. 
    It is **NOT** a substitute for professional medical advice, diagnosis, or treatment.
    Always consult with a medical professional.
    """)

if __name__ == "__main__":
    main()