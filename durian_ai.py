from flask import Flask, render_template_string, request, jsonify, session
from roboflow import Roboflow
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'durian_secret_key'

# --- 1. ตั้งค่า Roboflow (อ้างอิงจากรูปโปรเจกต์ของคุณ) ---
# หา API Key ได้ที่: Roboflow > Settings > Workspace > Private API Key
ROBOFLOW_API_KEY = "aUQh6GrqTow8tSgITsZK" 
rf = Roboflow(api_key=ROBOFLOW_API_KEY)
project = rf.workspace("new-workspace-7qbtz").project("durian-detection-zb1dk")
model = project.version(3).model

# --- 2. ข้อมูลจำลองสำหรับระบบ Admin ---
user_data = {}
DEVICES = [
    {'id': 'D-001', 'name': 'Sensor A1', 'location': 'โกดัง 1', 'status': 'online', 'lastUpdate': 'เมื่อสักครู่'}
]
ADMIN_CREDENTIALS = [{'email': 'admin@durianai.com', 'password': 'admin123'}]

# --- 3. HTML Template (ส่วนหน้าตาเว็บ) ---
# ผมใช้ Template เดิมที่คุณส่งมา แต่จะมีการปรับ JavaScript ให้เรียก API จริง
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>Durian Smart AI</title>
    <style>
        /* (ใส่ CSS เดิมของคุณที่นี่) */
        body { font-family: 'Kanit', sans-serif; background: #f0f2f5; }
        .panel { display: none; }
        .panel.active { display: block; }
    </style>
</head>
<body>
    <div id="userPanel" class="panel active">
        <h2>📷 วิเคราะห์คุณภาพทุเรียน</h2>
        <div id="previewArea">
             <button onclick="document.getElementById('fileInput').click()">เลือกรูปภาพทุเรียน</button>
        </div>
        <input type="file" id="fileInput" hidden accept="image/*" onchange="handleImage(event)">
    </div>

    <script>
        // แก้ไขฟังก์ชันวิเคราะห์ภาพให้เรียกใช้ API จริง
        async function analyzeImage(imageData) {
            const preview = document.getElementById('previewArea');
            preview.innerHTML = "<p>🔄 กำลังวิเคราะห์ด้วย AI จริงจาก Roboflow...</p>";

            // แปลงภาพเป็น Blob เพื่อส่งไปที่ Server
            const blob = await (await fetch(imageData)).blob();
            const formData = new FormData();
            formData.append('image', blob);

            try {
                const response = await fetch('/api/analyze-durian', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                if (data.success) {
                    // แสดงผลลัพธ์ที่ได้จาก Model จริง
                    preview.innerHTML = `
                        <div class="result">
                            <h3>ผลการวิเคราะห์: ${data.status}</h3>
                            <p>ความมั่นใจ: ${data.confidence}%</p>
                        </div>
                    `;
                }
            } catch (e) {
                preview.innerHTML = "<p>❌ เกิดข้อผิดพลาดในการเชื่อมต่อ</p>";
            }
        }

        function handleImage(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => analyzeImage(e.target.result);
                reader.readAsDataURL(file);
            }
        }
    </script>
</body>
</html>
'''

# --- 4. API Routes ---
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/analyze-durian', methods=['POST'])
def analyze_durian():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image'})
    
    file = request.files['image']
    temp_path = "temp.jpg"
    file.save(temp_path)

    try:
        # เรียกใช้ Model จาก Roboflow
        result = model.predict(temp_path, confidence=40).json()
        predictions = result.get('predictions', [])

        if not predictions:
            return jsonify({'success': True, 'status': 'ไม่พบทุเรียน', 'confidence': 0})

        top = predictions[0] # ตัวที่แม่นยำที่สุด
        return jsonify({
            'success': True,
            'status': top['class'],
            'confidence': int(top['confidence'] * 100)
        })
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
