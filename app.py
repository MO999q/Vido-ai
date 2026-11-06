import streamlit as st
import os
import requests
from gTTS import gTTS
from PIL import Image

st.set_page_config(
    page_title="Vido AI Studio - Fast & Stable",
    page_icon="🎬",
    layout="centered"
)

st.markdown("""
    <style>
    .main { background-color: #0b0f19; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: bold;
        padding: 14px;
        border-radius: 10px;
        border: none;
        font-size: 16px;
    }
    .status-card {
        padding: 16px;
        background-color: #1e293b;
        border-radius: 10px;
        border-right: 6px solid #2563eb;
        margin-bottom: 15px;
        color: #f8fafc;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Vido AI Studio - Stable Edition")
st.caption("الاستوديو الذكي السريع لتوليد الصور والتعليق الصوتي للمشاهد بدون أخطاء تثبيت")

os.makedirs("temp_assets", exist_ok=True)

default_script = """المشهد الأول: رحلة استكشاف مذهلة داخل غابة ساحرة مليئة بالأضواء.
المشهد الثاني: البطل يكتشف أثراً قديماً غامضاً ينبض بطاقة سرية.
المشهد الثالث: تنطلق اللقطة نحو السماء الواسعة وسط نجوم الفضاء الساطعة."""

script_input = st.text_area(
    "📜 أدخل السكريبت (كل مشهد في سطر مستقل):",
    value=default_script,
    height=150
)

if st.button("🚀 بدء توليد المشاهد والصوتيات فوراً"):
    if not script_input.strip():
        st.warning("⚠️ يرجى إدخال السكريبت أولاً!")
    else:
        scenes = [s.strip() for s in script_input.split('\n') if s.strip()]
        total_scenes = len(scenes)
        
        progress_bar = st.progress(0)
        status_box = st.empty()
        
        try:
            for index, scene_text in enumerate(scenes):
                progress_bar.progress(int(((index + 1) / total_scenes) * 100))
                status_box.markdown(f"""
                <div class="status-card">
                    <b>🎬 معالجة المشهد ({index + 1} من {total_scenes}):</b><br>
                    <i>"{scene_text}"</i>
                </div>
                """, unsafe_allow_html=True)
                
                # 1. توليد الصوت
                audio_path = f"temp_assets/scene_{index}.mp3"
                tts = gTTS(text=scene_text, lang='ar', slow=False)
                tts.save(audio_path)
                
                # 2. توليد الصورة السينمائية
                prompt_encoded = requests.utils.quote(f"Cinematic 8k resolution, {scene_text}")
                image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=1024&height=576&nologo=true"
                image_path = f"temp_assets/scene_{index}.jpg"
                
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    with open(image_path, 'wb') as handler:
                        handler.write(img_response.content)
                    
                    img = Image.open(image_path)
                    img = img.resize((1024, 576))
                    img.save(image_path)
                
                # عرض النتيجة لكل مشهد مباشرة (صورة + صوت) لضمان الاستقرار التام وسرعة العرض
                st.image(image_path, caption=f"المشهد {index + 1}")
                st.audio(audio_path)
            
            status_box.empty()
            st.success("🎉 تم توليد كافة مشاهد الاستوديو بنجاح وبدون أي أخطاء تثبيت!")
            
        except Exception as e:
            status_box.empty()
            st.error(f"❌ حدث خطأ: {e}")
