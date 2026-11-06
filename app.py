import streamlit as st
import os
import requests
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
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

st.title("🎬 Vido AI Pro - Ultimate Video Studio")
st.caption("الاستوديو الذكي لدمج وصناعة فيديو كامل ومتصل (MP4) بجودة احترافية")

# إنشاء مجلد مؤقت للأصول والملفات
os.makedirs("temp_assets", exist_ok=True)

# سكريبت افتراضي مخصص لفيديوهات الأطفال الكرتونية الجذابة
default_script = """A cute baby smiling with colorful balloons in a magical bright playroom, 3D Disney Pixar style, vibrant colors.
A cheerful baby elephant wearing a tiny party hat playing with bright stars, 3D animated style, high quality."""

script_input = st.text_area(
    "📜 أدخل وصف المشاهد بالإنجليزية (كل مشهد في سطر مستقل لضمان دمجها في فيديو واحد):",
    value=default_script,
    height=160
)

# زر البدء والمعالجة وتصدير الفيديو الكامل
if st.button("🚀 بدء دمج وتصدير الفيديو الكامل (MP4)"):
    if not script_input.strip():
        st.warning("⚠️ يرجى إدخال السكريبت أولاً!")
    else:
        scenes = [s.strip() for s in script_input.split('\n') if s.strip()]
        total_scenes = len(scenes)
        video_clips = []
        
        progress_bar = st.progress(0)
        percentage_text = st.empty()
        status_box = st.empty()
        
        try:
            for index, scene_text in enumerate(scenes):
                # حساب النسبة المئوية التقريبية أثناء المعالجة (حتى 80% للمشاهد)
                current_percent = int(((index) / total_scenes) * 80)
                progress_bar.progress(current_percent)
                percentage_text.markdown(f"### ⏳ نسبة الإنجاز: `{current_percent}%`")
                
                status_box.markdown(f"""
                <div class="status-card">
                    <b>🎬 معالجة وتجهيز المشهد ({index + 1} من {total_scenes}):</b><br>
                    <i>"{scene_text}"</i>
                </div>
                """, unsafe_allow_html=True)
                
                # 1. توليد التعليق الصوتي للمشهد
                audio_path = f"temp_assets/scene_{index}.mp3"
                try:
                    tts = gTTS(text=scene_text, lang='en', slow=False)
                    tts.save(audio_path)
                except Exception:
                    pass
                
                audio_clip = AudioFileClip(audio_path)
                duration = audio_clip.duration
                
                # 2. توليد الصورة الكرتونية بدقة عالية بدون علامات مائية (nologo=true)
                image_path = f"temp_assets/scene_{index}.jpg"
                image_fetched = False
                
                try:
                    prompt_encoded = requests.utils.quote(f"3D animated style, vibrant colors, cinematic lighting, cute and friendly, {scene_text}")
                    image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=1024&height=576&nologo=true"
                    img_response = requests.get(image_url, timeout=15)
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
                    img = Image.new('RGB', (1024, 576), color=(30, 41, 59))
                    img.save(image_path)
                
                # 3. ربط الصورة بالصوت لمدة المشهد وإضافتها لقائمة المقاطع
                image_clip = ImageClip(image_path).set_duration(duration)
                video_clip = image_clip.set_audio(audio_clip)
                video_clips.append(video_clip)

            # مرحلة دمج كافة المقاطع في ملف فيديو نهائي واحد ومتصل
            progress_bar.progress(85)
            percentage_text.markdown("### ⏳ نسبة الإنجاز: `85%`")
            status_box.markdown("""
            <div class="status-card">
                <b>🔄 جاري دمج كافة المشاهد في فيديو كامل ومتصل وتصدير ملف (MP4)...</b>
            </div>
            """, unsafe_allow_html=True)
            
            final_video = concatenate_videoclips(video_clips, method="compose")
            output_file = "final_output_video.mp4"
            final_video.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")
            
            # اكتمال العملية بنجاح 100%
            progress_bar.progress(100)
            percentage_text.markdown("### ✅ نسبة الإنجاز: `100%`")
            status_box.empty()
            
            st.success("🎉 تم إنشاء وتصدير الفيديو الكامل والمتصل بنجاح تام وبدون علامات مائية!")
            st.video(output_file)
            
        except Exception as e:
            status_box.empty()
            st.error(f"❌ حدث خطأ أثناء دمج وتصدير الفيديو: {e}")
