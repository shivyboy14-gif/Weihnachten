import streamlit as st
import requests
import json
import io
from datetime import datetime, date

# PPTX Imports - VEREINFACHT!
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ===== CONFIGURATION =====
GROQ_API_KEY = "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"
PEXELS_API_KEY = "3Y3jiJZ6WAL49N6lPsdlRbRZ6IZBfHZFHP86dr9yZfxFYoxedLLlDKAC"

# ===== CHECK IF CHRISTMAS SEASON =====
def is_christmas_season():
    today = date.today()
    return today.month == 12 and today.day <= 26

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Deine Lern-Assistent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CSS =====
def get_css():
    christmas_css = ""
    if is_christmas_season():
        christmas_css = """
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
            to { transform: translateY(100vh) rotate(360deg); }
        }
        
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
        
        .tree-left, .tree-right {
            position: fixed;
            bottom: 0;
            font-size: 3rem;
            z-index: 9997;
            animation: sway 3s ease-in-out infinite;
        }
        
        .tree-left { left: 10px; }
        .tree-right { right: 10px; }
        
        @keyframes sway {
            0%, 100% { transform: rotate(-2deg); }
            50% { transform: rotate(2deg); }
        }
        
        .main .block-container { padding-top: 40px !important; }
        """
    
    return f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }}
    
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }}
    
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    .chat-message {{
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        gap: 10px;
        align-items: flex-start;
    }}
    
    .chat-message.user {{
        background: rgba(255,255,255,0.1);
        flex-direction: row-reverse;
    }}
    
    .chat-message.ai {{
        background: rgba(255,255,255,0.2);
    }}
    
    .avatar {{ font-size: 2rem; }}
    .message-content {{ flex: 1; color: white; line-height: 1.6; }}
    
    .welcome-title {{
        text-align: center;
        font-size: 3rem;
        color: #ffd700;
        text-shadow: 0 0 20px rgba(255,215,0,0.5);
        animation: title-glow 2s ease-in-out infinite alternate;
        margin: 2rem 0;
    }}
    
    @keyframes title-glow {{
        from {{ text-shadow: 0 0 20px rgba(255,215,0,0.5); }}
        to {{ text-shadow: 0 0 40px rgba(255,215,0,0.8); }}
    }}
    
    .slide-preview {{
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: #333;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    
    .slide-preview h4 {{
        color: #667eea;
        margin-bottom: 10px;
        border-bottom: 2px solid #764ba2;
        padding-bottom: 5px;
    }}
    
    .download-section {{
        background: linear-gradient(135deg, #11998e, #38ef7d);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }}
    
    .header-container {{
        text-align: center;
        padding: 1rem;
        color: white;
    }}
    
    .header-container h1 {{
        font-size: 2.2rem;
        margin-bottom: 0.3rem;
    }}
    
    .header-container p {{
        opacity: 0.9;
        font-size: 1rem;
    }}
    
    {christmas_css}
    </style>
    """

def get_christmas_html():
    if not is_christmas_season():
        return ""
    
    return """
    <div class="christmas-lights">
        <div class="light"></div><div class="light"></div><div class="light"></div>
        <div class="light"></div><div class="light"></div><div class="light"></div>
        <div class="light"></div><div class="light"></div><div class="light"></div>
        <div class="light"></div><div class="light"></div><div class="light"></div>
    </div>
    <div class="tree-left">🎄</div>
    <div class="tree-right">🎄</div>
    
    <script>
    function createSnowflakes() {
        const snowflakes = ['❄', '❅', '❆'];
        setInterval(() => {
            const sf = document.createElement('div');
            sf.className = 'snowflake';
            sf.innerHTML = snowflakes[Math.floor(Math.random() * snowflakes.length)];
            sf.style.left = Math.random() * 100 + 'vw';
            sf.style.animationDuration = (Math.random() * 3 + 4) + 's';
            document.body.appendChild(sf);
            setTimeout(() => sf.remove(), 7000);
        }, 300);
    }
    createSnowflakes();
    </script>
    """

# ===== INJECT CSS =====
st.markdown(get_css(), unsafe_allow_html=True)
st.markdown(get_christmas_html(), unsafe_allow_html=True)

# ===== SESSION STATE INITIALIZATION =====
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.welcome_done = False
    st.session_state.all_chats = {}
    st.session_state.current_chat_id = None
    st.session_state.current_pptx = None
    st.session_state.current_pptx_name = None

# ===== HELPER FUNCTIONS =====
def generate_chat_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_chat_title(messages):
    for msg in messages:
        if msg["role"] == "user":
            title = msg["content"][:40]
            if len(msg["content"]) > 40:
                title += "..."
            return title
    return "Neuer Chat"

def create_new_chat():
    chat_id = generate_chat_id()
    st.session_state.all_chats[chat_id] = {
        "title": "Neuer Chat",
        "messages": [],
        "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "pptx_data": None,
        "pptx_name": None
    }
    st.session_state.current_chat_id = chat_id
    st.session_state.current_pptx = None
    st.session_state.current_pptx_name = None
    return chat_id

# ===== API FUNCTIONS =====
def fetch_pexels_image(query):
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        response = requests.get(
            f"https://api.pexels.com/v1/search?query={query}&per_page=1",
            headers=headers,
            timeout=10
        )
        data = response.json()
        if data.get("photos"):
            image_url = data["photos"][0]["src"]["large"]
            img_response = requests.get(image_url, timeout=10)
            return img_response.content, image_url
    except Exception:
        pass
    return None, None

def call_groq_api(messages_history):
    system_prompt = """Du bist ein freundlicher KI-Lernassistent für Sophia.

REGELN:
- Antworte IMMER auf Deutsch
- Verwende einfache, schulgerechte Sprache
- Sei ermutigend und geduldig
- Erkläre Schritt für Schritt
- Löse Hausaufgaben

PRÄSENTATIONSMODUS:
Wenn nach einer Präsentation gefragt wird, antworte NUR mit validem JSON:
{
  "title": "Titel der Präsentation",
  "slides": [
    {
      "slideTitle": "Folientitel",
      "text": ["Punkt 1", "Punkt 2", "Punkt 3", "Punkt 4"],
      "imageQuery": "english keywords for image"
    }
  ]
}

WICHTIG FÜR PRÄSENTATIONEN:
- Erstelle 5-10 Folien, hängt an den Thema
- Erste Folie = Titelfolie (nur Titel, text kann leer sein)
- Letzte Folie = "Vielen Dank!" oder "Fragen?"
- 3-5 kurze Stichpunkte pro Folie
- imageQuery MUSS auf Englisch sein (2-4 Wörter)
- Keine Emojis im JSON
- Kein Text außerhalb des JSON"""

    api_messages = [{"role": "system", "content": system_prompt}]
    
    for msg in messages_history:
        if msg["role"] in ["user", "assistant"]:
            content = msg.get("content", "")
            if msg.get("is_presentation"):
                content = "Ich habe eine Präsentation erstellt."
            if content:
                api_messages.append({"role": msg["role"], "content": content})

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GROQ_API_KEY}"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": api_messages,
                "temperature": 0.7,
                "max_tokens": 2500
            },
            timeout=30
        )
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Entschuldigung, es gab einen Fehler: {str(e)}"

# ===== POWERPOINT CREATION - OHNE RgbColor! =====
def set_shape_color(shape, r, g, b):
    """Setzt die Füllfarbe einer Form ohne RgbColor"""
    shape.fill.solid()
    shape.fill.fore_color.theme_color = None
    fill = shape.fill._xPr
    solidFill = fill.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill')
    if solidFill is not None:
        srgbClr = solidFill.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
        if srgbClr is not None:
            srgbClr.set('val', f'{r:02X}{g:02X}{b:02X}')

def create_powerpoint(json_data, progress_bar=None):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    total_slides = len(json_data['slides'])
    
    for idx, slide_data in enumerate(json_data['slides']):
        if progress_bar:
            progress_bar.progress((idx + 1) / total_slides, f"Erstelle Folie {idx + 1} von {total_slides}...")
        
        # Benutze ein Layout mit Hintergrund
        slide_layout = prs.slide_layouts[6]  # Blank
        slide = prs.slides.add_slide(slide_layout)
        
        is_title_slide = idx == 0 or not slide_data.get('text') or len(slide_data['text']) == 0
        
        if is_title_slide:
            # TITELFOLIE
            title_box = slide.shapes.add_textbox(
                Inches(0.5), Inches(2.5), Inches(12.333), Inches(2)
            )
            title_frame = title_box.text_frame
            title_frame.word_wrap = True
            title_para = title_frame.paragraphs[0]
            title_para.text = slide_data['slideTitle']
            title_para.font.size = Pt(54)
            title_para.font.bold = True
            title_para.alignment = PP_ALIGN.CENTER
            
            subtitle_box = slide.shapes.add_textbox(
                Inches(2), Inches(4.5), Inches(9.333), Inches(0.8)
            )
            sub_frame = subtitle_box.text_frame
            sub_para = sub_frame.paragraphs[0]
            sub_para.text = json_data.get('title', '')
            sub_para.font.size = Pt(24)
            sub_para.alignment = PP_ALIGN.CENTER
            
        else:
            # INHALTSFOLIE
            title_box = slide.shapes.add_textbox(
                Inches(0.5), Inches(0.3), Inches(12.333), Inches(1)
            )
            title_frame = title_box.text_frame
            title_para = title_frame.paragraphs[0]
            title_para.text = slide_data['slideTitle']
            title_para.font.size = Pt(36)
            title_para.font.bold = True
            
            # Text content
            text_box = slide.shapes.add_textbox(
                Inches(0.5), Inches(1.5), Inches(6), Inches(5.5)
            )
            text_frame = text_box.text_frame
            text_frame.word_wrap = True
            
            for i, point in enumerate(slide_data.get('text', [])):
                if i == 0:
                    para = text_frame.paragraphs[0]
                else:
                    para = text_frame.add_paragraph()
                
                para.text = f"• {point}"
                para.font.size = Pt(22)
                para.space_after = Pt(18)
            
            # Bild hinzufügen
            if slide_data.get('imageQuery'):
                img_bytes, _ = fetch_pexels_image(slide_data['imageQuery'])
                if img_bytes:
                    try:
                        image_stream = io.BytesIO(img_bytes)
                        slide.shapes.add_picture(
                            image_stream,
                            Inches(7), Inches(1.5), Inches(5.8), Inches(5)
                        )
                    except Exception:
                        pass
    
    pptx_bytes = io.BytesIO()
    prs.save(pptx_bytes)
    pptx_bytes.seek(0)
    
    return pptx_bytes.getvalue()

def render_presentation_preview(json_data):
    st.markdown(f"### 📊 Vorschau: {json_data['title']}")
    
    cols = st.columns(2)
    for i, slide in enumerate(json_data['slides']):
        with cols[i % 2]:
            text_html = ''.join(f"<li>{point}</li>" for point in slide.get('text', []))
            st.markdown(f"""
                <div class="slide-preview">
                    <h4>📄 Folie {i + 1}: {slide['slideTitle']}</h4>
                    <ul>{text_html}</ul>
                    <small style="color:#888;">🖼️ Bild: {slide.get('imageQuery', 'Kein Bild')}</small>
                </div>
            """, unsafe_allow_html=True)

# ===== WELCOME SCREEN =====
if not st.session_state.welcome_done:
    st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:80vh;text-align:center;">
    """, unsafe_allow_html=True)
    
    if is_christmas_season():
        st.markdown("""
            <h1 class="welcome-title">🎄 Frohe Weihnachten, Sophia! 🎄</h1>
            <p style="color:white;font-size:1.5rem;margin:20px 0;">Ein ganz besonderes Geschenk  für dich!</p>
        """, unsafe_allow_html=True)
        btn_text = "🎁 Geschenk öffnen ✨"
    else:
        st.markdown("""
            <h1 class="welcome-title">👋 Willkommen, Sophia!</h1>
            <p style="color:white;font-size:1.5rem;margin:20px 0;">Dein persönlicher Lern-Assistent ist bereit!</p>
        """, unsafe_allow_html=True)
        btn_text = "🚀 Los geht's!"
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(btn_text, use_container_width=True, type="primary"):
            st.session_state.welcome_done = True
            create_new_chat()
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ===== SIDEBAR - CHAT HISTORY =====
with st.sidebar:
    st.markdown("## 💬 Chats")
    
    if st.button("➕ Neuer Chat", use_container_width=True, type="primary"):
        create_new_chat()
        st.rerun()
    
    st.markdown("---")
    
    sorted_chats = sorted(
        st.session_state.all_chats.items(),
        key=lambda x: x[0],
        reverse=True
    )
    
    for chat_id, chat_data in sorted_chats:
        is_active = chat_id == st.session_state.current_chat_id
        col1, col2 = st.columns([4, 1])
        
        with col1:
            title = chat_data.get("title", "Neuer Chat")
            btn_label = f"{'📍 ' if is_active else '💭 '}{title}"
            
            if st.button(btn_label, key=f"chat_{chat_id}", use_container_width=True):
                st.session_state.current_chat_id = chat_id
                st.session_state.current_pptx = chat_data.get("pptx_data")
                st.session_state.current_pptx_name = chat_data.get("pptx_name")
                st.rerun()
        
        with col2:
            if st.button("🗑️", key=f"del_{chat_id}"):
                del st.session_state.all_chats[chat_id]
                if chat_id == st.session_state.current_chat_id:
                    if st.session_state.all_chats:
                        st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[0]
                    else:
                        create_new_chat()
                st.rerun()
    
    if not st.session_state.all_chats:
        st.markdown("*Keine Chats vorhanden*")
        create_new_chat()

# ===== MAIN APP =====
if st.session_state.current_chat_id is None or st.session_state.current_chat_id not in st.session_state.all_chats:
    create_new_chat()

current_chat = st.session_state.all_chats[st.session_state.current_chat_id]

# Header
st.markdown("""
    <div class="header-container">
        <h1>🎓 Sophias Lern-Assistent</h1>
        <p>Ich helfe dir bei Hausaufgaben und erstelle PowerPoint-Präsentationen!</p>
    </div>
""", unsafe_allow_html=True)

# Chat messages
chat_container = st.container()

with chat_container:
    messages = current_chat.get("messages", [])
    
    if not messages:
        st.markdown("""
            <div class="chat-message ai">
                <span class="avatar">🤖</span>
                <div class="message-content">
                    Hallo Sophia! 👋 Ich bin dein persönlicher Lern-Assistent.<br><br>
                    <b>Was ich kann:</b><br>
                    📚 Bei Hausaufgaben helfen<br>
                    📊 <b>PowerPoint-Präsentationen erstellen</b> (zum Download!)<br><br>
                    Sag einfach z.B.: <i>"Erstelle eine Präsentation über das Sonnensystem"</i>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    for msg in messages:
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user">
                    <span class="avatar">👩</span>
                    <div class="message-content">{msg["content"]}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            if msg.get("is_presentation"):
                st.markdown("""
                    <div class="chat-message ai">
                        <span class="avatar">🤖</span>
                        <div class="message-content">
                            ✅ Deine Präsentation ist fertig! Hier ist eine Vorschau:
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                render_presentation_preview(msg["presentation_data"])
            else:
                st.markdown(f"""
                    <div class="chat-message ai">
                        <span class="avatar">🤖</span>
                        <div class="message-content">{msg["content"]}</div>
                    </div>
                """, unsafe_allow_html=True)

# Download button
if st.session_state.current_pptx:
    st.markdown("""
        <div class="download-section">
            <h3 style="color:white;margin-bottom:10px;">📥 Deine PowerPoint ist bereit!</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="⬇️ PowerPoint herunterladen (.pptx)",
            data=st.session_state.current_pptx,
            file_name=st.session_state.current_pptx_name,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True,
            type="primary"
        )

# Input area
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Nachricht",
        placeholder="Schreibe deine Nachricht hier...",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    send_button = st.button("📤", use_container_width=True, type="primary")

# Process input
if send_button and user_input:
    current_chat["messages"].append({"role": "user", "content": user_input})
    
    if len(current_chat["messages"]) == 1:
        current_chat["title"] = get_chat_title(current_chat["messages"])
    
    st.session_state.current_pptx = None
    st.session_state.current_pptx_name = None
    
    with st.spinner("🤔 Ich denke nach..."):
        response = call_groq_api(current_chat["messages"])
    
    try:
        json_data = json.loads(response)
        if "title" in json_data and "slides" in json_data:
            current_chat["messages"].append({
                "role": "assistant",
                "content": "",
                "is_presentation": True,
                "presentation_data": json_data
            })
            
            st.info("🎨 Erstelle PowerPoint mit Bildern...")
            progress_bar = st.progress(0, "Starte...")
            
            pptx_bytes = create_powerpoint(json_data, progress_bar)
            
            clean_title = json_data['title'].replace(" ", "_").replace("/", "-")[:50]
            filename = f"{clean_title}.pptx"
            
            st.session_state.current_pptx = pptx_bytes
            st.session_state.current_pptx_name = filename
            
            current_chat["pptx_data"] = pptx_bytes
            current_chat["pptx_name"] = filename
            
            progress_bar.progress(100, "✅ Fertig!")
        else:
            current_chat["messages"].append({"role": "assistant", "content": response})
    except json.JSONDecodeError:
        current_chat["messages"].append({"role": "assistant", "content": response})
    
    st.rerun()

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align:center;color:rgba(255,255,255,0.5);font-size:0.8rem;">
       Shiva :)
    </div>
""", unsafe_allow_html=True)
