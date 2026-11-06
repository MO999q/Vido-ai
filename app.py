import streamlit as st
import os
import requests
from gtts import gTTS
from PIL import Image
import imageio
from mutagen.mp3 import MP3

# إعدادات الصفحة والتصميم العام
st.set_page_config(
    page_title="Vido AI Studio - Free API Pipeline",
    page_icon="🎬",
    layout="centered"
)

# تصميم واجهة مستخدم احترافية (Dark Mode)
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

st.title("🎬 Vido AI Studio - Free API Pipeline")
st.caption("الاستوديو الذكي عبر سلسلة الـ APIs المجانية لإنتاج وتصدير فيديوهات الأطفال (MP4)")

# إنشاء مجلد مؤقت للأصول
os.makedirs("temp_assets", exist_ok=True)

# سكريبت افتراضي مخصص لفيديوهات الأطفال الكرتونية
default_script = """A cute baby smiling with colorful balloons in a bright magical room.
A cheerful baby elephant wearing a tiny party hat playing with bright stars.
A little cute kitten playing with a ball of yarn in a sunny garden."""

script_input = st.text_area(
    "📜 أدخل وصف المشاهد بالإنجليزية (كل مشهد في سطر مستقل):",
    value=default_script,
    height=150
)

# زر البدء وتنفيذ السلسلة المجانية
if st.button("🚀 بدء تشغيل السلسلة وتصدير الفيديو (MP4)"):
    if not script_input.strip():
        st.warning("⚠️ يرجى إدخال السكريبت أولاً!")
    else:
        scenes = [s.strip() for s in script_input.split('\n') if s.strip()]
        total_scenes = len(scenes)
        
        progress_bar = st.progress(0)
        percentage_text = st.empty()
        status_box = st.empty()
        
        try:
            frames = []
            fps = 24
            
            for index, scene_text in enumerate(scenes):
                current_percent = int(((index + 1) / total_scenes) * 70)
                progress_bar.progress(current_percent)
                percentage_text.markdown(f"### ⏳ نسبة الإنجاز: `{current_percent}%`")
                
                status_box.markdown(f"""
                <div class="status-card">
                    <b>🎬 تشغيل سلسلة المشهد ({index + 1} من {total_scenes}):</b><br>
                    <i>"{scene_text}"</i>
                </div>
                """, unsafe_allow_html=True)
                
                # 1. الخطوة الأولى في السلسلة: توليد الصوت المجاني
                audio_path = f"temp_assets/scene_{index}.mp3"
                try:
                    tts = gTTS(text=scene_text, lang='en', slow=False)
                    tts.save(audio_path)
                    audio = MP3(audio_path)
                    duration = audio.info.length
                except Exception:
                    duration = 4.0
                
                # 2. الخطوة الثانية في السلسلة: جلب الصورة الكرتونية عبر API مجاني بدون علامة مائية
                image_path = f"temp_assets/scene_{index}.jpg"
                image_fetched = False
                
                try:
                    safe_prompt = requests.utils.quote(f"cute colorful 3D cartoon style animation, vibrant colors, {scene_text}")
                    # استخدام API مجاني مباشر وسريع
                    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=576&nologo=true"
                    
                    img_response = requests.get(image_url, timeout=20)
                    if img_response.status_code == 200 and len(img_response.content) > 1000:
                        with open(image_path, 'wb') as handler:
                            handler.write(img_response.content)
                        img = Image.open(image_path)
                        img = img.resize((1024, 576))
                        img.save(image_path)
                        image_fetched = True
                except Exception:
                    image_fetched = False
                
                if not image_fetched:
                    img = Image.new('RGB', (1024, 576), color=(255, 182, 193))
                    img.save(image_path)
                
                # تحويل الصورة إلى إطارات متسلسلة بالفيديو
                img_frame = imageio.v2.imread(image_path)
                num_frames = int(duration * fps)
                for _ in range(num_frames):
                    frames.append(img_frame)

            # الخطوة الثالثة: دمج السلسلة بالكامل في فيديو MP4 نهائي
            progress_bar.progress(85)
            percentage_text.markdown("### ⏳ نسبة الإنجاز: `85%`")
            status_box.markdown("""
            <div class="status-card">
                <b>🔄 جاري دمج عناصر السلسلة وتصدير الفيديو النهائي (MP4)...</b>
            </div>
            """, unsafe_allow_html=True)
            
            output_video_path = "final_output_video.mp4"
            
            with imageio.get_writer(output_video_path, fps=fps, codec='libx264', quality=8) as writer:
                for frame in frames:
                    writer.append_data(frame)
            
            progress_bar.progress(100)
            percentage_text.markdown("### ✅ نسبة الإنجاز: `100%`")
            status_box.empty()
            
            st.success("🎉 تم تشغيل السلسلة وتصدير الفيديو الكامل (MP4) بنجاح تام وبدون علامات مائية!")
            
            # عرض الفيديو وزر التحميل
            st.video(output_video_path)
            
            with open(output_video_path, "rb") as file:
                st.download_button(
                    label="📥 تحميل الفيديو الكامل (MP4)",
                    data=file,
                    file_name="pipeline_kids_video.mp4",
                    mime="video/mp4"
                )
            
        except Exception as e:
            status_box.empty()
            st.error(f"❌ حدث خطأ في تنفيذ السلسلة: {e}")
