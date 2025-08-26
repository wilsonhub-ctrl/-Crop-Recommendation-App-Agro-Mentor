import streamlit as st
import pickle
import pandas as pd
from PIL import Image
import base64
import time
from datetime import datetime
import numpy as np
import os
import requests
global test
test = 'negetive'


# Base64 encoded images
LEAF_ICON = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48cGF0aCBmaWxsPSIjNENBRjUwIiBkPSJNNDgwIDEyOGMwIDEyMC04MCAyNDAtMTYwIDMyMHMtMTYwIDY0LTMyMCA2NEMwIDMyMCA2NCAxNjAgMTkyIDgwczIyNCAwIDI4OCA0NHoiLz48L3N2Zz4="
PLANT_ICON = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48cGF0aCBmaWxsPSIjNENBRjUwIiBkPSJNNjQgOTZINDQ4VjQxNkg2NFY5NloiLz48cGF0aCBmaWxsPSIjODFDNzg0IiBkPSJNMTI4IDE2MEgzODRWMzUySDEyOFYxNjBaIi8+PC9zdmc+"



# Theme configurations
THEMES = {
    "Green Forest": {
        "primary": "#2e7d32",
        "secondary": "#4caf50",
        "background": "linear-gradient(-45deg, #e8f5e9, #c8e6c9, #a5d6a7, #81c784)",
        "text": "#1b5e20"
    },
    "Ocean Blue": {
        "primary": "#1565c0",
        "secondary": "#42a5f5",
        "background": "linear-gradient(-45deg, #e3f2fd, #bbdefb, #90caf9, #64b5f6)",
        "text": "#0d47a1"
    },
    "Sunset Orange": {
        "primary": "#d84315",
        "secondary": "#ff7043",
        "background": "linear-gradient(-45deg, #fbe9e7, #ffccbc, #ffab91, #ff8a65)",
        "text": "#bf360c"
    },
    "Purple Dream": {
        "primary": "#6a1b9a",
        "secondary": "#ab47bc",
        "background": "linear-gradient(-45deg, #f3e5f5, #e1bee7, #ce93d8, #ba68c8)",
        "text": "#4a148c"
    }
}

def apply_theme(theme_name):
    theme = THEMES[theme_name]
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        
        * {{
            font-family: 'Poppins', sans-serif;
        }}
        
        .main {{
            padding: 2rem;
            animation: fadeIn 1s ease-in;
        }}
        
        .stApp {{
            background: {theme['background']};
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }}
        
        .sidebar .sidebar-content {{
            background: rgba(255, 255, 255, 0.95);
        }}
        
        .title {{
            color: {theme['primary']};
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
        }}
        
        .card {{
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            transition: transform 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
        }}
        
        .weather-card {{
            text-align: center;
            padding: 1rem;
        }}
        
        .price-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .price-table th {{
            background: {theme['primary']};
            color: white;
            padding: 1rem;
        }}
        
        .price-table td {{
            padding: 0.8rem;
            border-bottom: 1px solid #eee;
        }}
        
        .trend-up {{
            color: #4caf50;
        }}
        
        .trend-down {{
            color: #f44336;
        }}
        </style>
    """, unsafe_allow_html=True)

# Page Configuration
st.set_page_config(
    page_title="Sustainable Agriculture Predictor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with more animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        padding: 2rem;
        animation: fadeIn 1s ease-in;
    }
    
    .title {
        background: linear-gradient(45deg, #2e7d32, #1b5e20);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 2rem;
        animation: slideDown 1s ease-out;
        position: relative;
    }
    
    .title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #2e7d32, transparent);
        animation: shimmer 2s infinite;
    }
    
    .subtitle {
        color: #1b5e20;
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 2rem;
        animation: fadeIn 1.5s ease-in;
    }
    
    .card {
        background: rgba(241, 248, 233, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(76, 175, 80, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.2),
            transparent
        );
        transition: 0.5s;
    }
    
    .card:hover::before {
        left: 100%;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        border-color: rgba(76, 175, 80, 0.3);
    }
    
    .feature-card {
        background: linear-gradient(135deg, #4CAF50, #2E7D32);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        transform: rotate(45deg);
        animation: shimmerRotate 10s infinite linear;
    }
    
    .feature-card:hover {
        transform: scale(1.02) translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }
    
    .contact-form {
        max-width: 600px;
        margin: 0 auto;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .contact-form::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #2e7d32, #1b5e20);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 60%);
        transform: rotate(45deg);
        transition: 0.5s;
    }
    
    .stButton > button:hover::after {
        transform: rotate(225deg);
    }
    
    .success-msg {
        padding: 1rem;
        background: #E8F5E9;
        border-left: 4px solid #2E7D32;
        border-radius: 4px;
        margin: 1rem 0;
        animation: slideIn 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .success-msg::after {
        content: '✓';
        position: absolute;
        right: 1rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        color: #2E7D32;
        animation: scaleIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideDown {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-50%) scaleX(0.5); opacity: 0; }
        50% { transform: translateX(-50%) scaleX(1); opacity: 1; }
        100% { transform: translateX(-50%) scaleX(0.5); opacity: 0; }
    }
    
    @keyframes shimmerRotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes scaleIn {
        from { transform: translateY(-50%) scale(0); }
        to { transform: translateY(-50%) scale(1); }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .floating-icon {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Enhanced Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1b5e20 0%, #2e7d32 100%);
        position: relative;
        overflow: hidden;
    }
    
    .css-1d391kg::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('data:image/svg+xml;base64,${LEAF_ICON}') no-repeat center center;
        opacity: 0.1;
        animation: float 6s ease-in-out infinite;
    }
    
    .css-1d391kg .stRadio > label {
        color: white !important;
        position: relative;
        z-index: 1;
    }
    
    /* Input field styling */
    .stTextInput > div > div {
        border-radius: 10px;
        border: 1px solid rgba(76, 175, 80, 0.2);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div:focus-within {
        border-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced animated background
def add_bg_from_url():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(-45deg, #e8f5e9, #c8e6c9, #a5d6a7, #81c784);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Animated background
def add_bg_from_url():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(-45deg, #e8f5e9, #c8e6c9, #a5d6a7, #81c784);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Loading animation
def loading_animation():
    with st.spinner('Loading...'):
        time.sleep(1)


# ai assistant
def assistant():
    import streamlit as st
    from langchain_community.llms import Ollama

    # Initialize model
    llm = Ollama(model='llama3.2:1b')

    # List of agriculture-related keywords

    AGRI_KEYWORDS = [
    "crop", "plant", "seed", "seedling", "germination", "sapling", "plantation", "transplanting", "plant density", "crop variety", "hybrid seeds", "genetically modified", "biofortification",
    "farming", "organic farming", "precision farming", "sustainable farming", "mixed farming", "mono-cropping", "crop rotation", "intercropping", "contour farming", "tillage", "no-till farming", "mulching", "cover cropping",
    "soil", "soil health", "soil testing", "soil fertility", "soil erosion", "soil structure", "soil pH", "salinity", "compost", "manure", "vermicompost", "biochar", "green manure", "irrigation", "drip irrigation", "sprinkler system", "canal irrigation", "rainwater harvesting", "waterlogging", "water table",
    "pest", "insect", "mite", "weed", "fungus", "bacteria", "viral disease", "crop disease", "blight", "rust", "wilt", "fungicide", "pesticide", "insecticide", "bio-pesticide", "pest management", "IPM",
    "fertilizer", "biofertilizer", "NPK", "micronutrients", "macronutrients", "urea", "potash", "phosphate", "foliar spray", "fertigation", "nutrient deficiency",
    "tractor", "plough", "harvester", "seed drill", "thresher", "agri-drone", "farm machinery", "automated irrigation", "sensor", "IoT in farming", "remote sensing", "agri app", "weather sensor", "soil sensor",
    "harvest", "harvesting", "crop yield", "storage", "cold storage", "warehouse", "supply chain", "post-harvest loss", "transportation", "grading", "packaging", "value addition",
    "farmer", "farm income", "subsidy", "crop insurance", "MSP", "market price", "mandi", "agri-loan", "kisan credit", "eNAM", "agri-policy", "farm bill",
    "livestock", "poultry", "dairy", "goat farming", "cattle", "buffalo", "fodder", "grazing", "animal feed", "veterinary", "milking", "silage",
    "horticulture", "floriculture", "sericulture", "apiculture", "aquaculture", "agroforestry", "greenhouse", "polyhouse", "nursery", "plant tissue culture", "hydroponics", "aeroponics"
    ]

# Chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    st.title("🌱 Agriculture Assistant")

    # User input
    user_input = st.text_input("Ask something related to agriculture:", key="input")

    def is_agriculture_related(text):
        text = text.lower()
        return any(word in text for word in AGRI_KEYWORDS)

    if user_input:
        if is_agriculture_related(user_input):
            # Add user input
            st.session_state.history.append(("You", user_input))
            # Build context
            context = "\n".join([f"{u}: {m}" for u, m in st.session_state.history])
            # Get response
            response = llm.invoke(context)
            st.session_state.history.append(("AgriBot", response))
        else:
         response = "❌ Please ask questions related to agriculture only."
         st.session_state.history.append(("AgriBot", response))

# Display history
    for speaker, msg in st.session_state.history:
        st.markdown(f"**{speaker}**: {msg}")


# Home Page with enhanced features

def home():
    st.markdown("<h1 class='title'>🌱 Agro Mentor</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Empowering farmers with AI-driven insights</p>", unsafe_allow_html=True)
    
    # Animated statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class='feature-card'>
                <h3>🎯 99%</h3>
                <p>Prediction Accuracy</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class='feature-card'>
                <h3>🌍 1000+</h3>
                <p>Farmers Helped</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class='feature-card'>
                <h3>🌿 50+</h3>
                <p>Sustainable Practices</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Main content
    st.markdown(
        """
        <div class='card'>
            <h2>Welcome to Smart Agriculture! 🚀</h2>
            <p>Use our AI-powered platform to:</p>
            <ul>
                <li>Predict optimal crops for your land</li>
                <li>Get personalized sustainability recommendations</li>
                <li>Access expert agricultural tips</li>
                <li>Connect with our community</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# Enhanced Model Prediction Page
def model_prediction():
    loaded_model = pickle.load(open('model.pkl', 'rb'))
    st.subheader(" Find out the most suitable crop to grow in your farm 👨‍🌾")
    N = st.number_input("Nitrogen(In Ppm)", 1,150) 
    P = st.number_input("Phosporus(In Ppm)", 5,150)
    K = st.number_input("Potassium(In Ppm)", 0,200)
    temp = st.number_input("Temperature",0.0,60.0)
    humidity = st.number_input("Humidity in %", 10.0,100.0)
    ph = st.number_input("Ph", 0.0,7.0)
    rainfall = st.number_input("Rainfall in mm",0.0,300.0)

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1,-1)

    if st.button('Predict'):
        prediction = loaded_model.predict(single_pred)
        st.write(f"{prediction.item().title()} are recommended by the A.I for your farm.")

# Enhanced Agricultural Tips Page
def agricultural_tips():
    st.markdown("<h2 class='title'>🌿 Agricultural Tips</h2>", unsafe_allow_html=True)
    
    tips = [
        {
            "title": "Crop Rotation 🔄",
            "content": "Implement crop rotation to maintain soil health and reduce pest problems.",
            "icon": "🌱"
        },
        {
            "title": "Water Conservation 💧",
            "content": "Use drip irrigation and mulching to conserve water and maintain soil moisture.",
            "icon": "💧"
        },
        {
            "title": "Natural Pest Control 🐞",
            "content": "Encourage beneficial insects and use companion planting for natural pest management.",
            "icon": "🐞"
        },
        {
            "title": "Soil Health 🌍",
            "content": "Regular soil testing and organic matter addition improves soil fertility.",
            "icon": "🌍"
        }
    ]
    
    for tip in tips:
        st.markdown(
            f"""
            <div class='card'>
                <h3>{tip['icon']} {tip['title']}</h3>
                <p>{tip['content']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Enhanced Contact Page
def contact():
    st.markdown("<h2 class='title'>📧 Contact Us</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <style>
            .contact-container {
                max-width: 800px;
                margin: 0 auto;
                padding: 2rem;
            }
            .contact-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
                margin-bottom: 2rem;
            }
            .contact-info {
                background: rgba(255, 255, 255, 0.95);
                padding: 1.5rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .contact-item {
                display: flex;
                align-items: center;
                margin-bottom: 1rem;
                padding: 0.5rem;
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            .contact-item:hover {
                background: rgba(76, 175, 80, 0.1);
            }
            .contact-icon {
                font-size: 1.5rem;
                margin-right: 1rem;
                color: #2e7d32;
            }
            .social-links {
                display: flex;
                gap: 1rem;
                margin-top: 1rem;
            }
            .social-link {
                font-size: 1.5rem;
                color: #2e7d32;
                text-decoration: none;
                transition: all 0.3s ease;
            }
            .social-link:hover {
                transform: translateY(-3px);
                color: #1b5e20;
            }
        </style>
        <div class="contact-container">
            <div class="contact-grid">
                <div class="contact-info">
                    <h3>Get in Touch</h3>
                    <div class="contact-item">
                        <div class="contact-icon">👨‍💻</div>
                        <div>
                            <strong>Developer</strong><br>
                            Mega Byte Minds
                        </div>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon">🏢</div>
                        <div>
                            <strong>Organization</strong><br>
                            Mega Byte Minds Solutions
                        </div>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon">📧</div>
                        <div>
                            <strong>Email</strong><br>
                            megabyteminds@gmail.com
                        </div>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon">🌐</div>
                        <div>
                            <strong>Website</strong><br>
                            www.megabyteminds.com
                        </div>
                    </div>
                    <div class="social-links">
                        <a href="https://github.com/thenameisnavi" class="social-link">📱</a>
                        <a href="https://www.linkedin.com/in/naveengouda-m-khandeppagoudra-b6b4b1289?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BqS%2FTqPPOTneEm7Q3adLL2g%3D%3D" class="social-link">💼</a>
                        <a href="https://x.com/thenameisnavi20" class="social-link">🐦</a>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def weather():
    # 🔑 Insert your OpenWeatherMap API key here
    API_KEY = "d205ac5eb45aab4018694fff2f428a95"  
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    
    city = st.text_input("Enter city name", "Bengaluru")

    if st.button("Get Weather"):
        if city:
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }
            response = requests.get(BASE_URL, params=params)

            if response.status_code == 200:
                data = response.json()
                weather = data["weather"][0]["description"].title()
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]

                st.subheader(f"📍 Weather in {city.title()}")
                st.metric("🌡️ Temperature", f"{temp} °C")
                st.write(f"☁️ Condition: {weather}")
                st.write(f"💧 Humidity: {humidity}%")
                st.write(f"🌬️ Wind Speed: {wind_speed} m/s")
            else:
                st.error("City not found or API error. Please try again.")
        else:
            st.warning("Please enter a city name.")





def market_prices_page():
    import random
    crop_prices = {
        "Bangalore": {
            "Rice": (2800, 4300),  # Approximate price range for 2024
            "Wheat": (2400, 3800),
            "Maize": (2000, 3300),
            "Cotton": (3800, 5300),
            "Tomato": (1500, 2800),
            "Onion": (2200, 4400),
        },
        "Mumbai": {
            "Rice": (3000, 4600),
            "Wheat": (2500, 4000),
            "Maize": (2000, 3400),
            "Cotton": (3500, 5200),
            "Tomato": (1300, 2900),
            "Onion": (2000, 4200),
        },
        "Delhi": {
            "Rice": (3200, 5100),
            "Wheat": (2700, 4200),
            "Maize": (2100, 3600),
            "Cotton": (3500, 5200),
            "Tomato": (1600, 3100),
            "Onion": (2300, 4700),
        },
        "Chennai": {
            "Rice": (2500, 4000),
            "Wheat": (2300, 3700),
            "Maize": (2000, 3400),
            "Cotton": (3400, 5100),
            "Tomato": (1200, 2500),
            "Onion": (2000, 3800),
        },
        "Kolkata": {
            "Rice": (2800, 4300),
            "Wheat": (2600, 4100),
            "Maize": (1900, 3200),
            "Cotton": (3400, 5100),
            "Tomato": (1400, 2700),
            "Onion": (2100, 4400),
        },
        "Hyderabad": {
            "Rice": (2900, 4500),
            "Wheat": (2400, 3800),
            "Maize": (2000, 3300),
            "Cotton": (3600, 5300),
            "Tomato": (1400, 2800),
            "Onion": (2200, 4400),
        },
        "Ahmedabad": {
            "Rice": (2600, 4200),
            "Wheat": (2300, 3700),
            "Maize": (1900, 3300),
            "Cotton": (3400, 5000),
            "Tomato": (1300, 2500),
            "Onion": (2000, 4200),
        },
        "Lucknow": {
            "Rice": (3000, 4600),
            "Wheat": (2400, 3900),
            "Maize": (2000, 3400),
            "Cotton": (3400, 5100),
            "Tomato": (1500, 2700),
            "Onion": (2100, 4500),
        },
        "Pune": {
            "Rice": (2800, 4300),
            "Wheat": (2300, 3700),
            "Maize": (2000, 3200),
            "Cotton": (3500, 5200),
            "Tomato": (1300, 2600),
            "Onion": (2000, 4200),
        },
        "Jaipur": {
            "Rice": (3000, 4700),
            "Wheat": (2500, 4100),
            "Maize": (2000, 3300),
            "Cotton": (3500, 5300),
            "Tomato": (1400, 2700),
            "Onion": (2100, 4400),
        },
    }

    st.title("Crop Price Finder")

    # Select city and crop from dropdowns
    city = st.selectbox("Select City", list(crop_prices.keys()))
    crop = st.selectbox("Select Crop", list(crop_prices[city].keys()))



    def generate_price(min_price, max_price):
        return round(random.uniform(min_price, max_price), 2)

    # Function to generate random price between min and max
    if st.button("Get Price"):
        min_price, max_price = crop_prices[city][crop]
        price = generate_price(min_price, max_price)
        st.write(f"Price for {crop} in {city}: ₹{price} per quintal.")


def descussion():
    CSV_FILE = "discussion.csv"
    admin_log = 'negetive'

# Load the discussion posts from the CSV file
    def load_posts():
        if os.path.exists(CSV_FILE):
            return pd.read_csv(CSV_FILE)
        else:
            return pd.DataFrame(columns=["User", "Message"])

    # Save a new post to the CSV file
    def save_post(user, message):
        user = user.lower()
        message = message.lower()
        df = load_posts()
        new_post = pd.DataFrame([{"User": user, "Message": message}])
        df = pd.concat([df, new_post], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

        
        messages = [
        'what can i grow now',
        'my ph is 7.0',
        'how to test soil',
        'what is crop rotation',
        'how to increase yield',
        'how to treat leaf spots',
        'which crop needs less water',
        'how to store grains',
        'what is the mandi price of onion',
        'how to get subsidy',
        'my crop is not growing well',
        'suggest winter crops',
        'what is best time to sow paddy',
        'can i use cow dung as fertilizer',
        'how to contact local officer',
        'how to control weeds',
        'suggest crops for sandy soil',
        'what is organic farming',
        'what is NPK',
        'how to compost at home',
        'can i grow vegetables in pots',
        'how many days to grow tomato',
        'how to prevent crop diseases',
        'what is mulching',
        'which crop grows fast',
        'how to increase soil fertility',
        'suggest summer crops',
        'how to detect plant disease',
        'how to use neem oil',
        'what is green manure'
        ]

        response = [
        'please share your location and soil pH',
        'best crops are wheat, barley, and cabbage',
        'use a soil testing kit or visit nearby agri lab',
        'growing different crops in sequence to maintain soil health',
        'use quality seeds, proper irrigation, and balanced fertilizer',
        'use copper-based fungicide and remove affected leaves',
        'millets, mustard, and pulses need less water',
        'dry properly and store in airtight containers with neem leaves',
        'onion price is ₹20/kg in your area',
        'visit your agriculture office or apply through PM-KISAN portal',
        'please share crop type, symptoms, and photo if possible',
        'you can grow wheat, peas, carrots, and garlic',
        'June to July is ideal for sowing paddy in most regions',
        'yes, mix with soil and compost before applying',
        'visit krishi seva kendra or call toll-free 1800-180-1551',
        'use mulching, hand removal, or herbicides to control weeds',
        'you can grow groundnut, watermelon, and bajra in sandy soil',
        'organic farming avoids chemicals and uses natural compost and bio-fertilizers',
        'NPK stands for Nitrogen, Phosphorus, and Potassium — key nutrients for plant growth',
        'collect kitchen waste, dry leaves, and cow dung in a compost bin for 45–60 days',
        'yes, use large containers with good drainage and sunlight',
        'tomato takes 60–80 days to mature after transplanting',
        'use crop rotation, resistant seeds, and regular monitoring to prevent diseases',
        'mulching is covering soil with straw or plastic to retain moisture and control weeds',
        'radish, spinach, and fenugreek grow fast — ready in 30–40 days',
        'add compost, rotate crops, and avoid chemical overuse to improve fertility',
        'suggested crops for summer: brinjal, okra, sunflower, and cucumber',
        'upload an image of the affected plant to get disease diagnosis',
        'mix 5 ml neem oil in 1 liter of water and spray weekly on plants',
        'green manure is growing plants like sunhemp to plow back into soil for fertility'
        ]


        for i in range(0,len(messages)):
            if messages[i] == message:
                new_post = pd.DataFrame([{"User": 'bot', "Message": response[i]}])
                df = pd.concat([df, new_post], ignore_index=True)
                df.to_csv(CSV_FILE, index=False)

# Delete a specific post by index
    def delete_post(index):
        df = load_posts()
        df = df.drop(index).reset_index(drop=True)
        df.to_csv(CSV_FILE, index=False)
        st.success("🗑️ Message deleted.")
        st.rerun()

    # Title for the discussion app
    st.title("💬 Discussion ")

    # Form to add a new message
    st.subheader("Post a New Message")
    user = st.text_input("Your Name")
    message = st.text_area("Message")

    if st.button("Submit"):
        st.write(message)
        if user and message:
            save_post(user, message)
            st.success("✅ Message posted successfully!")
            st.rerun()
    else:
        st.warning("⚠️ Please enter both name and message.")

# Display all the messages
    st.subheader("Discussion Messages")

    df = load_posts()

    if df.empty:
        st.info("ℹ️ No messages yet. Be the first to post!")
    else:
        for i, row in df.iterrows():
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"**{row['User']}**: {row['Message']}")
            with col2:
                if st.button("❌", key=f"delete_{i}"):
                    delete_post(i)
                    
                  


    st.markdown("Get answers to common questions farmers and agri-enthusiasts often ask.")

    # FAQ Data: (You can expand or load from a file/database if needed)
    faqs = [
        {
            "question": "What is organic farming?",
            "answer": "Organic farming is a method of farming that uses natural inputs like compost, green manure, and biological pest control. It avoids synthetic fertilizers and pesticides."
        },
        {
            "question": "Which crop is best to grow in dry land areas?",
            "answer": "Millets, pulses (like chickpeas), and sorghum are suitable for dry land areas as they require less water and are drought-resistant."
        },
        {
            "question": "How can I improve soil fertility naturally?",
            "answer": "Use crop rotation, organic compost, green manure, and nitrogen-fixing plants like legumes to improve soil fertility naturally."
        },
        {
            "question": "What is drip irrigation?",
            "answer": "Drip irrigation delivers water directly to the root zone of plants, minimizing water wastage and maximizing efficiency."
        },
        {
            "question": "How can I protect crops from pests without chemicals?",
            "answer": "You can use neem oil, introduce beneficial insects like ladybugs, and practice crop rotation and intercropping."
        }
    ]

# Display each FAQ with expand/collapse
    for faq in faqs:
        with st.expander(faq["question"]):
            st.write(faq["answer"])



def navigation():
    st.sidebar.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: var(--primary-color); font-size: 1.5rem;">🌿 Agro Mentor</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Theme Selection
    st.sidebar.markdown("<div class='theme-selector'>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='menu-title'>🎨 Choose Theme</p>", unsafe_allow_html=True)
    theme = st.sidebar.selectbox("Theme", list(THEMES.keys()), label_visibility="collapsed")
    apply_theme(theme)
    
    # Main Navigation
    menu_items = {
        "🏠 Home": home,
        "🔮 Crop Recomender": model_prediction,
        "🌡️ Weather": weather,
        "💰 Market Prices": market_prices_page,
        "🌱 Agricultural Tips": agricultural_tips,
        "🤖 AI Assistat":assistant,
        "💬 Discussion":descussion,
        "📧 Contact": contact
        
    }
    
    st.sidebar.markdown("<div class='sidebar-menu'>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='menu-title'>📱 Navigation</p>", unsafe_allow_html=True)
    selected = st.sidebar.radio("", list(menu_items.keys()), label_visibility="collapsed")
    
    # Call the selected function
    menu_items[selected]()

if __name__ == "__main__":
    navigation()
        
    
