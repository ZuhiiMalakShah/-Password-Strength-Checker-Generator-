import streamlit as st
import hashlib
import json
import secrets
import string

PASSWORD_FILE = "passwords.json"

# Function to load stored passwords from the JSON file
def load_passwords():
    try:
        with open(PASSWORD_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save passwords to the JSON file
def save_passwords(passwords):
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file, indent=4)

# Function to hash the password for storage (using SHA256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to generate a strong random password
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

# Function to check password strength with custom scoring weights
def check_password_strength(password):
    # Password strength criteria
    length = len(password) >= 8
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    score = sum([length, has_upper, has_lower, has_digit, has_special])
    
    if score == 5:
        return "Strong"
    elif score >= 3:
        return "Medium"
    else:
        return "Weak"

# Function to store passwords
def store_password(site, username, password):
    passwords = load_passwords()
    passwords[site] = {"username": username, "password": hash_password(password)}
    save_passwords(passwords)
    return f"Password for {site} saved successfully!"

# Function to retrieve passwords
def retrieve_password(site):
    passwords = load_passwords()
    if site in passwords:
        return passwords[site]
    else:
        return "No password found for this site."

# Streamlit UI setup
st.set_page_config(page_title="Password Manager", page_icon="🔐", layout="wide")

# Dark theme CSS styles
st.markdown(
    """
    <style>
        body {background-color: #121212; color: white;}
        .stApp {background-color: #121212; color: white;}
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            padding: 12px;
            background-color: #6200EE;
            color: white;
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #3700B3;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #6200EE;
            background-color: #333;
            color: white;
        }
        .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
            border-color: #BB86FC;
        }
        .stSidebar {
            background-color: #333;
            color: white;
            padding: 10px;
        }
        .stSidebar .stRadio > label {
            color: white;
            font-weight: bold;
        }
        .stMarkdown {
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔐 Password Manager & Strength Checker")

menu = ["Generate Password", "Check Password Strength", "Store Password", "Retrieve Password"]
choice = st.sidebar.radio("Select an option", menu)

st.markdown("---")

# Option 1: Generate Password
if choice == "Generate Password":
    st.subheader("🔑 Generate a Secure Password")
    length = st.slider("Select password length", min_value=4, max_value=50, value=12)
    if st.button("Generate", help="Click to generate a random secure password"):
        st.success(f"Generated Password: {generate_password(length)}")

# Option 2: Check Password Strength
elif choice == "Check Password Strength":
    st.subheader("🛡️ Check Password Strength")
    password = st.text_input("Enter password", type="password")
    if st.button("Check", help="Click to analyze the strength of the password"):
        st.info(f"Password Strength: {check_password_strength(password)}")

# Option 3: Store Password
elif choice == "Store Password":
    st.subheader("💾 Store a Password")
    site = st.text_input("Enter site name")
    username = st.text_input("Enter username")
    password = st.text_input("Enter password", type="password")
    if st.button("Save", help="Click to securely store this password"):
        st.success(store_password(site, username, password))

# Option 4: Retrieve Password
elif choice == "Retrieve Password":
    st.subheader("🔍 Retrieve Stored Password")
    site = st.text_input("Enter site name")
    if st.button("Retrieve", help="Click to fetch stored credentials"):
        data = retrieve_password(site)
        if isinstance(data, dict):
            st.info(f"Username: {data['username']}\n\n*Password Hash:* {data['password']}")
        else:
            st.warning(data)

# Footer section with "Created by Zuhii Shah"
st.markdown(
    """
    <hr style="border:1px solid #6200EE;">
    <div style="text-align: center; color: white; font-size: 16px;">
        👩‍💻 Created by <strong>Zuhii Shah</strong> 🔐💡
    </div>
    """, unsafe_allow_html=True
)