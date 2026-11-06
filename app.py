import streamlit as st
import os
import requests
from gtts import gTTS
from PIL import Image

# إعدادات الصفحة والتصميم العام
st.set_page_config(
    page_title="Vido AI Pro - Ultimate Studio",
    page_icon="🎬",
    layout="centered"
)

# تصميم واجهة مستخدم احترافية وعصرية (Dark Mode)
st.markdown("""
    <style>
    .main {
        background-color: #0b0f19;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: bold;
        padding: 14px;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8 100%, #1e40af 100%);
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

st.title("🎬 Vido AI Pro - Ultimate Studio")
st.caption("الاستوديو الذكي المتكامل لتوليد وصناعة محتوى مرئي وصوتي احترافي بدون علامات مائية")

# إنشاء مجلد مؤقت للأصول والملفات
os.makedirs("temp_assets", exist_ok=True)

# إدخال السكريبت
default_script = """المشهد الأول: رحلة استكشاف مذهلة داخل غابة ساحرة مليئة بالأشجار العملاقة.
المشهد الثاني: البطل يكتشف أثراً قديماً غامضاً ينبض بطاقة سرية لا تصدق.
المشهد الثالث: تبدأ الأثر في الانفتاح كاشفة عن بوابة لعالم مستقبلية مذهلة."""

script_input = st.text_area(
    "📜 أدخل السكريبت الخاص بك (اكتب كل مشهد في سطر مستقل):",
    value=default_script,
    height=180
)

# زر البدء والمعالجة
if st.button("🚀 بدء إنشاء وتوليد مشاهد الاستوديو الاحترافية"):
    if not script_input.strip():
        st.warning("⚠️ يرجى إدخال السكريبت أولاً!")
    else:
        scenes = [s.strip() for s in script_input.split('\n') if s.strip()]
        total_scenes = len(scenes)
        
        progress_bar = st.progress(0)
        percentage_text = st.empty()
        status_box = st.empty()
        
        try:
            for index, scene_text in enumerate(scenes):
                current_percent = int(((index + 1) / total_scenes) * 100)
                progress_bar.progress(current_percent)
                percentage_text.markdown(f"### ⏳ نسبة الإنجاز: `{current_percent}%`")
                
                clean_scene_desc = scene_text.split(":")[-1].strip() if ":" in scene_text else scene_text
                
                status_box.markdown(f"""
                <div class="status-card">
                    <b>🎬 معالجة المشهد ({index + 1} من {total_scenes}):</b><br>
                    <i>"{clean_scene_desc}"</i>
                </div>
                """, unsafe_allow_html=True)
                
                # 1. توليد التعليق الصوتي للمشهد
                audio_path = f"temp_assets/scene_{index}.mp3"
                try:
                    tts = gTTS(text=clean_scene_desc, lang='ar', slow=False)
                    tts.save(audio_path)
                except Exception:
                    pass
                
                # 2. توليد الصورة السينمائية بدون علامة مائية نهائياً عبر معلمة nologo=true
                image_path = f"temp_assets/scene_{index}.jpg"
                image_fetched = False
                
                try:
                    prompt_encoded = requests.utils.quote(f"Cinematic 8k resolution, highly detailed, {clean_scene_desc}")
                    image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=1024&height=576&nologo=true"
                    img_response = requests.get(image_url, timeout=10)
                    if img_response.status_code == 200:
                        with open(image_path, 'wb') as handler:
                            handler.write(img_response.content)
                        img = Image.open(image_path)
                        img = img.resize((1024, 576))
                        img.save(image_path)
                        image_fetched = True
                except Exception:
                    image_fetched = False
                
                if not image_fetched:
                    img = Image.new('RGB', (1024, 576), color=(15, 23, 42))
                    img.save(image_path)

                # عرض النتيجة المتكاملة لكل مشهد
                st.image(image_path, caption=f"المشهد {index + 1}: {clean_scene_desc}", use_container_width=True)
                if os.path.exists(audio_path):
                    st.audio(audio_path)
            
            status_box.empty()
            st.success("🎉 تم إنشاء وتوليد كافة مشاهد الاستوديو بنجاح تام وبدون أي علامات مائية!")
            
        except Exception as e:
            status_box.empty()
            st.error(f"❌ حدث خطأ غير متوقع أثناء المعالجة: {e}")
