import streamlit as st
import os
import requests
from gTTS import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

# إعدادات الصفحة والتصميم
st.set_page_config(
    page_title="Vido AI Pro - Full Video Generator",
    page_icon="🎬",
    layout="centered"
)

# لمسات تصميمية بالـ CSS لتحسين مظهر الواجهة
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        padding: 12px;
        border-radius: 8px;
        border: none;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    .status-card {
        padding: 15px;
        background-color: #1e293b;
        border-radius: 8px;
        border-right: 5px solid #2563eb;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Vido AI Pro - Ultimate Studio")
st.caption("أنشئ فيديوهات كاملة (MP4) بدمج الصوت، الصور والتأثيرات تلقائياً")

# إنشاء مجلد مؤقت لحفظ الأصول
os.makedirs("temp_assets", exist_ok=True)

# إدخال السكريبت
default_script = """المشهد الأول: رائد فضاء يستكشف كوكباً غريباً مليئاً بالأضواء.
المشهد الثاني: يجد سفينة فضائية قديمة مهجورة بين الجبال.
المشهد الثالث: تضيء السفينة فجأة وتنطلق إلى السماء بسرعة عالية."""

script_input = st.text_area(
    "📜 أدخل السكريبت (اكتب كل مشهد في سطر منفصل):",
    value=default_script,
    height=160
)

if st.button("🚀 بدء إنشاء وتصدير الفيديو الكامل (MP4)"):
    if not script_input.strip():
        st.warning("⚠️ يرجى إدخال السكريبت أولاً!")
    else:
        scenes = [s.strip() for s in script_input.split('\n') if s.strip()]
        total_scenes = len(scenes)
        video_clips = []
        
        # عناصر متابعة الإنجاز والنسبة المئوية
        progress_bar = st.progress(0)
        percentage_text = st.empty()
        status_box = st.empty()
        
        try:
            for index, scene_text in enumerate(scenes):
                # حساب النسبة المئوية التقريبية لكل مشهد
                current_percent = int(((index) / total_scenes) * 85) # 85% لمعالجة المشاهد و 15% للدمج النهائي
                progress_bar.progress(current_percent)
                percentage_text.markdown(f"### ⏳ نسبة الإنجاز: `{current_percent}%`")
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
                
                audio_clip = AudioFileClip(audio_path)
                duration = audio_clip.duration
                
                # 2. توليد الصورة
                prompt_encoded = requests.utils.quote(f"Cinematic 3D render, {scene_text}")
                image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=768&height=768&nologo=true"
                image_path = f"temp_assets/scene_{index}.jpg"
                
                img_data = requests.get(image_url).content
                with open(image_path, 'wb') as handler:
                    handler.write(img_data)
                
                # 3. ربط الصورة بالصوت
                image_clip = ImageClip(image_path).set_duration(duration)
                video_clip = image_clip.set_audio(audio_clip)
                video_clips.append(video_clip)

            # مرحلة الدمج النهائي
            progress_bar.progress(90)
            percentage_text.markdown("### ⏳ نسبة الإنجاز: `90%`")
            status_box.markdown("""
            <div class="status-card">
                <b>🔄 جاري دمج كافة المشاهد وتصدير ملف الفيديو النهائي...</b>
            </div>
            """, unsafe_allow_html=True)
            
            final_video = concatenate_videoclips(video_clips, method="compose")
            output_file = "final_video.mp4"
            final_video.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")
            
            # مكتمل 100%
            progress_bar.progress(100)
            percentage_text.markdown("### ✅ نسبة الإنجاز: `100%`")
            status_box.empty()
            
            st.success("🎉 تم إنشاء الفيديو بنجاح!")
            st.video(output_file)
            
        except Exception as e:
            status_box.empty()
            st.error(f"❌ حدث خطأ أثناء المعالجة: {e}")
