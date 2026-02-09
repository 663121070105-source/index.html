import streamlit as st
from roboflow import Roboflow
from PIL import Image
import os

ROBOFLOW_API_KEY = "aUQh6GrqTow8tSgITsZK" # ใช้รหัส Private Key ของคุณ
PROJECT_NAME = "durian-detection-zb1dk"
VERSION_NUMBER = 3

st.set_page_config(page_title="Durian Smart AI", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; }
    .status-box { padding: 20px; border-radius: 15px; background-color: white; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🍈 Durian Smart AI Pro")
st.write("ระบบตรวจสอบทุเรียนอัจฉริยะด้วยเทคโนโลยี AI")



col1, col2 = st.columns(2) # ปรับเป็น 2 คอลัมน์
with col1:
    st.metric("ความแม่นยำ (mAP)", "91.8%") # ข้อมูลจาก v3
with col2:
    st.metric("ความถูกต้อง", "92.2%") # ข้อมูลจาก v3

st.divider()


option = st.radio("เลือกวิธีตรวจสอบ:", ("📸 ถ่ายรูปจากกล้อง", "📁 อัปโหลดรูปภาพจากเครื่อง"))

img_file = None
if option == "📸 ถ่ายรูปจากกล้อง":
    img_file = st.camera_input("กดเพื่อถ่ายรูปทุเรียน")
else:
    img_file = st.file_uploader("เลือกไฟล์รูปภาพทุเรียน...", type=["jpg", "jpeg", "png"])


# --- แก้ไขส่วนการประมวลผล (แทนที่ส่วนเดิม) ---
if img_file:
    with st.spinner('AI กำลังวาดกรอบวิเคราะห์ทุเรียน...'):
        image = Image.open(img_file)
        temp_path = "temp_scan.jpg"
        image.save(temp_path)
        
        try:
           
            rf = Roboflow(api_key=ROBOFLOW_API_KEY)
            project = rf.workspace().project(PROJECT_NAME)
            model = project.version(VERSION_NUMBER).model
            
            
            model.predict(temp_path).save("result.jpg")
            
           
            st.image("result.jpg", caption="AI ตรวจพบและแบ่งลูกทุเรียนแล้ว", use_container_width=True)
            
            
            prediction = model.predict(temp_path).json()
            if prediction['predictions']:
                for pred in prediction['predictions']:
                    st.success(f"🎯 ลูกที่พบ: {pred['class']} (มั่นใจ {pred['confidence']:.2%})")
            
        except Exception as e:
            st.error(f"Error: {e}")
   
        if os.path.exists(temp_path):
            os.remove(temp_path)

st.divider()
st.info("💡 คำแนะนำ: ควรตรวจสอบทุเรียนในที่ที่มีแสงสว่างเพียงพอเพื่อให้ AI ทำงานได้แม่นยำที่สุด")



