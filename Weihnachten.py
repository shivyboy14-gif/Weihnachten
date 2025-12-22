import streamlit as st
import requests
import json
from datetime import datetime, date
from streamlit_extras.let_it_rain import rain

# ===== CONFIGURATION =====
GROQ_API_KEY = "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"
PEXELS_API_KEY = "3Y3jiJZ6WAL49N6lPsdlRbRZ6IZBfHZFHP86dr9yZfxFYoxedLLlDKAC"

# ===== CHECK IF CHRISTMAS SEASON =====
def is_christmas_season():
    today = date.today()
    # Show Christmas decorations from Dec 1 to Dec 26
    return today.month == 12 and today.day <= 26

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Dein Lern-Assistent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== CHRISTMAS CSS =====
def get_christmas_css():
    if not is_christmas_season():
        return ""
    
    return """
    <style>
    /* Snowflakes */
    .snowflake {
        position: fixed;
        top: -10px;
        z-index: 9999;
        color: #fff;
        font-size: 1.5em;
        text-shadow: 0 0 5px #fff;
        animation: fall linear forwards;
        pointer-events: none;
    }
    
    @keyframes fall {
        to {
            transform: translateY(100vh) rotate(360deg);
        }
    }
    
    /* Christmas Lights */
    .christmas-lights {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 30px;
        z-index: 9998;
        display: flex;
        justify-content: space-around;
        background: linear-gradient(180deg, #1a472a 0%, transparent 100%);
        padding-top: 5px;
    }
    
    .light {
        width: 15px;
        height: 25px;
        border-radius: 50%;
        animation: glow 1s ease-in-out infinite alternate;
    }
    
    .light:nth-child(4n+1) { background: #ff0000; animation-delay: 0s; }
    .light:nth-child(4n+2) { background: #00ff00; animation-delay: 0.25s; }
    .light:nth-child(4n+3) { background: #ffd700; animation-delay: 0.5s; }
    .light:nth-child(4n+4) { background: #0066ff; animation-delay: 0.75s; }
    
    @keyframes glow {
        from { opacity: 0.4; box-shadow: 0 0 5px currentColor; }
        to { opacity: 1; box-shadow: 0 0 20px currentColor, 0 0 30px currentColor; }
    }
    
    /* Christmas Trees on sides */
    .tree-left, .tree-right {
        position: fixed;
        bottom: 0;
        font-size: 4rem;
        z-index: 9997;
        animation: sway 3s ease-in-out infinite;
    }
    
    .tree-left { left: 20px; }
    .tree-right { right: 20px; }
    
    @keyframes sway {
        0%, 100% { transform: rotate(-2deg); }
        50% { transform: rotate(2deg); }
    }
    
    /* Candy cane border */
    .stApp {
        border-top: 8px solid;
        border-image: repeating-linear-gradient(
            45deg,
            #ff0000,
            #ff0000 10px,
            #ffffff 10px,
            #ffffff 20px
        ) 8;
    }
    
    /* Gift boxes decoration */
    .gifts {
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 2rem;
        z-index: 9997;
        display: flex;
        gap: 10px;
    }
    
    /* Holly decoration */
    .holly {
        position: fixed;
        top: 35px;
        right: 20px;
        font-size: 2rem;
        z-index: 9997;
    }
    
    /* Santa decoration */
    .santa {
        position: fixed;
        top: 35px;
        left: 20px;
        font-size: 2rem;
        z-index: 9997;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Snow ground effect */
    .snow-ground {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 20px;
        background: linear-gradient(180deg, transparent 0%, rgba(255,255,255,0.3) 100%);
        z-index: 9996;
    }
    
    /* Make main content have padding for decorations */
    .main .block-container {
        padding-top: 50px !important;
    }
    </style>
    
    <!-- Christmas Lights -->
    <div class="christmas-lights">
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
        <div class="light"></div>
    </div>
    
    <!-- Trees -->
    <div class="tree-left">🎄</div>
    <div class="tree-right">🎄</div>
    
    <!-- Holly -->
    <div class="holly">🎅</div>
    
    <!-- Santa -->
    <div class="santa">🦌</div>
    
    <!-- Snow ground -->
    <div class="snow-ground"></div>
    
    <!-- Gifts -->
    <div class="gifts">🎁🎁🎁</div>
    
    <!-- Snowflakes JavaScript -->
    <script>
    function createSnowflakes() {
        const snowflakes = ['❄', '❅', '❆', '✻', '✼'];
        
        setInterval(() => {
            const snowflake = document.createElement('div');
            snowflake.className = 'snowflake';
            snowflake.innerHTML = snowflakes[Math.floor(Math.random() * snowflakes.length)];
            snowflake.style.left = Math.random() * 100 + 'vw';
            snowflake.style.animationDuration = (Math.random() * 3 + 4) + 's';
            snowflake.style.fontSize = (Math.random() * 1 + 0.8) + 'em';
            document.body.appendChild(snowflake);
            
            setTimeout(() => snowflake.remove(), 7000);
        }, 200);
    }
    
    // Start snowflakes after page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createSnowflakes);
    } else {
        createSnowflakes();
    }
    </script>
    """

# ===== NORMAL CSS =====
def get_normal_css():
    return """
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main .block-container {
        padding-top: 2rem;
    }
    
    /* Chat styling */
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        gap: 10px;
        align-items: flex-start;
    }
    
    .chat-message.user {
        background: rgba(255,255,255,0.1);
        flex-direction: row-reverse;
    }
    
    .chat-message.ai {
        background: rgba(255,255,255,0.2);
    }
    
    .avatar {
        font-size: 2rem;
    }
    
    .message-content {
        flex: 1;
        color: white;
    }
    
    /* Welcome title */
    .welcome-title {
        text-align: center;
        font-size: 3rem;
        color: #ffd700;
        text-shadow: 0 0 20px rgba(255,215,0,0.5);
        animation: glow 2s ease-in-out infinite alternate;
        margin: 2rem 0;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(255,215,0,0.5); }
        to { text-shadow: 0 0 40px rgba(255,215,0,0.8); }
    }
    
    /* Slide styling */
    .slide-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: #333;
    }
    
    .slide-title {
        color: #667eea;
        border-bottom: 2px solid #764ba2;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 1rem;
        color: white;
    }
    
    .header-container h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .header-container p {
        opacity: 0.9;
        font-size: 1.1rem;
    }
    </style>
    """

# ===== INJECT CSS =====
st.markdown(get_normal_css(), unsafe_allow_html=True)
if is_christmas_season():
    st.markdown(get_christmas_css(), unsafe_allow_html=True)

# ===== SESSION STATE INITIALIZATION =====
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True
    st.session_state.messages = []
    st.session_state.welcome_done = False

# ===== WELCOME SCREEN (First Visit Only) =====
if st.session_state.first_visit and not st.session_state.welcome_done:
    
    # Confetti effect
    if is_christmas_season():
        rain(
            emoji="🎄❄️🎁⭐",
            font_size=30,
            falling_speed=5,
            animation_length="infinite",
        )
    
    # Welcome container
    st.markdown("""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 80vh;
            text-align: center;
        ">
    """, unsafe_allow_html=True)
    
    if is_christmas_season():
        st.markdown("""
            <h1 class="welcome-title">🎄 Frohe Weihnachten, Sophia! 🎄</h1>
            <p style="color: white; font-size: 1.5rem; margin: 20px 0;">
                Ein ganz besonderes Geschenk nur für dich! ✨
            </p>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <h1 class="welcome-title">👋 Willkommen, Sophia!</h1>
            <p style="color: white; font-size: 1.5rem; margin: 20px 0;">
                Dein persönlicher Lern-Assistent ist bereit!
            </p>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if is_christmas_season():
            button_text = "🎁 Geschenk öffnen ✨"
        else:
            button_text = "🚀 Los geht's!"
        
        if st.button(button_text, use_container_width=True, type="primary"):
            st.session_state.welcome_done = True
            st.session_state.first_visit = False
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ===== MAIN APPLICATION =====

# Header
st.markdown("""
    <div class="header-container">
        <h1>🎓 Sophias Lern-Assistent</h1>
        <p>Ich helfe dir bei Hausaufgaben und erstelle Präsentationen!</p>
    </div>
""", unsafe_allow_html=True)

# ===== API FUNCTIONS =====
def fetch_pexels_image(query):
    """Fetch image from Pexels API"""
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        response = requests.get(
            f"https://api.pexels.com/v1/search?query={query}&per_page=1",
            headers=headers,
            timeout=10
        )
        data = response.json()
        if data.get("photos"):
            return data["photos"][0]["src"]["medium"]
    except Exception as e:
        st.error(f"Bild-Fehler: {e}")
    return None

def call_groq_api(user_message):
    """Call Groq API for AI response"""
    
    system_prompt = """Du bist ein freundlicher KI-Lernassistent für Sophia, eine Schülerin.

REGELN:
- Antworte IMMER auf Deutsch
- Verwende einfache, schulgerechte Sprache
- Sei ermutigend und geduldig
- Erkläre Schritt für Schritt
- Löse Hausaufgaben nicht komplett - hilf beim Verstehen

PRÄSENTATIONSMODUS:
Wenn nach einer Präsentation gefragt wird, antworte NUR mit validem JSON:
{
  "title": "Titel der Präsentation",
  "slides": [
    {
      "slideTitle": "Folientitel",
      "text": ["Punkt 1", "Punkt 2", "Punkt 3"],
      "imageQuery": "english keywords for image"
    }
  ]
}

REGELN FÜR PRÄSENTATIONEN:
- Erstelle 4-6 Folien
- Kurze, klare Stichpunkte (max 4 pro Folie)
- imageQuery MUSS auf Englisch sein
- Keine Emojis im JSON
- Kein Text außerhalb des JSON

Sei wie ein geduldiger, freundlicher Tutor!"""

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GROQ_API_KEY}"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=30
        )
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Entschuldigung, es gab einen Fehler: {str(e)}"

def render_presentation(json_data):
    """Render presentation slides"""
    st.markdown(f"### 📊 {json_data['title']}")
    
    for i, slide in enumerate(json_data['slides'], 1):
        with st.container():
            st.markdown(f"""
                <div class="slide-container">
                    <h3 class="slide-title">Folie {i}: {slide['slideTitle']}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                for point in slide['text']:
                    st.markdown(f"• {point}")
            
            with col2:
                image_url = fetch_pexels_image(slide['imageQuery'])
                if image_url:
                    st.image(image_url, use_container_width=True)
        
        st.divider()

# ===== CHAT INTERFACE =====

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    if not st.session_state.messages:
        # Initial greeting
        greeting = "Hallo Sophia! 👋 Ich bin dein persönlicher Lern-Assistent. "
        greeting += "Ich kann dir bei **Hausaufgaben** helfen oder **Präsentationen** erstellen. "
        greeting += "Was möchtest du heute lernen?"
        
        st.markdown(f"""
            <div class="chat-message ai">
                <span class="avatar">🤖</span>
                <div class="message-content">{greeting}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Display message history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user">
                    <span class="avatar">👩</span>
                    <div class="message-content">{msg["content"]}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Check if it's a presentation
            if msg.get("is_presentation"):
                st.markdown(f"""
                    <div class="chat-message ai">
                        <span class="avatar">🤖</span>
                        <div class="message-content">Hier ist deine Präsentation:</div>
                    </div>
                """, unsafe_allow_html=True)
                render_presentation(msg["presentation_data"])
            else:
                st.markdown(f"""
                    <div class="chat-message ai">
                        <span class="avatar">🤖</span>
                        <div class="message-content">{msg["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)

# Input area
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Deine Frage",
        placeholder="Schreibe deine Frage hier...",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    send_button = st.button("Senden 📤", use_container_width=True, type="primary")

# Process input
if send_button and user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Get AI response
    with st.spinner("🤔 Ich denke nach..."):
        response = call_groq_api(user_input)
    
    # Check if response is a presentation (JSON)
    try:
        json_data = json.loads(response)
        if "title" in json_data and "slides" in json_data:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "",
                "is_presentation": True,
                "presentation_data": json_data
            })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
    except json.JSONDecodeError:
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
    
    st.rerun()

# ===== SIDEBAR INFO =====
with st.sidebar:
    st.markdown("### 📚 Tipps")
    st.markdown("""
    **Für Hausaufgaben:**
    - Stelle deine Frage
    - Ich erkläre Schritt für Schritt
    
    **Für Präsentationen:**
    - Sage z.B.: *"Erstelle eine Präsentation über Vulkane"*
    - Ich erstelle Folien mit Bildern!
    """)
    
    st.divider()
    
    if st.button("🗑️ Chat löschen"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # Show Christmas status
    if is_christmas_season():
        st.markdown("🎄 **Weihnachtsmodus aktiv!**")
        days_left = 26 - date.today().day
        if days_left > 0:
            st.markdown(f"Noch {days_left} Tage bis Weihnachten vorbei ist!")
    else:
        st.markdown("🎓 **Normaler Modus**")

# ===== FOOTER =====
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.5); font-size: 0.8rem;">
        Mit ❤️ für Sophia gemacht
    </div>
""", unsafe_allow_html=True)