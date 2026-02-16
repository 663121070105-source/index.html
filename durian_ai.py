from flask import Flask, render_template_string, request, jsonify, session
from roboflow import Roboflow
import os
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'durian_secret_key'

# --- 1. ตั้งค่า Roboflow (ใส่ API KEY ของคุณที่นี่) ---
ROBOFLOW_API_KEY = "aUQh6GrqTow8tSgITsZK" 
rf = Roboflow(api_key=ROBOFLOW_API_KEY)
project = rf.workspace("new-workspace-7qbtz").project("durian-detection-zb1dk")
model = project.version(3).model

# ข้อมูลจำลองสำหรับระบบ Admin
user_data = {}
DEVICES = [
    {'id': 'DEVICE-001', 'name': 'เซนเซอร์ทุเรียน 1', 'location': 'โกดัง A', 'status': 'online', 'lastUpdate': 'เมื่อสักครู่'}
]
ADMIN_CREDENTIALS = [{'email': 'admin@durianai.com', 'password': 'admin123'}]

# --- 2. HTML Template (เวอร์ชันเต็มรูปแบบ) ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Durian Smart AI - ระบบตรวจจับทุเรียน</title>
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root { --primary-color: #4CAF50; --secondary-color: #8BC34A; --accent-color: #FFEB3B; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Kanit', sans-serif; }
        body { background: linear-gradient(135deg, #E8F5E9 0%, #FFF9C4 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; background: white; padding: 20px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .mode-switch { display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; }
        .mode-btn { padding: 10px 25px; border: none; border-radius: 50px; cursor: pointer; background: white; font-weight: 600; transition: 0.3s; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        .mode-btn.active { background: var(--primary-color); color: white; }
        .panel { display: none; background: white; padding: 30px; border-radius: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); animation: fadeIn 0.5s ease; }
        .panel.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .upload-area { border: 3px dashed #C8E6C9; padding: 40px; border-radius: 20px; text-align: center; cursor: pointer; transition: 0.3s; }
        .upload-area:hover { border-color: var(--primary-color); background: #F1F8E9; }
        .result-card { margin-top: 30px; padding: 20px; border-radius: 20px; background: #f9f9f9; border-left: 10px solid var(--primary-color); }
        .status-badge { display: inline-block; padding: 8px 20px; border-radius: 50px; font-weight: bold; margin-bottom: 10px; }
        .chart-container { height: 200px; display: flex; align-items: flex-end; gap: 10px; margin-top: 20px; padding: 10px; border-bottom: 2px solid #ddd; }
        .chart-bar { flex: 1; background: var(--secondary-color); border-radius: 5px 5px 0 0; position: relative; transition: 0.5s; }
        .chart-label { position: absolute; bottom: -25px; left: 50%; transform: translateX(-50%); font-size: 10px; white-space: nowrap; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🥭 Durian Smart AI</h1>
            <p>ระบบวิเคราะห์ความสุกและบริหารจัดการโกดัง</p>
        </div>

        <div class="mode-switch">
            <button class="mode-btn active" onclick="switchMode('user')">👤 ผู้ใช้งาน</button>
            <button class="mode-btn" onclick="switchMode('admin')">🔐 ผู้ดูแล</button>
        </div>

        <div id="userPanel" class="panel active">
            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <div style="font-size: 50px;">📸</div>
                <h3>คลิกเพื่ออัพโหลดรูปทุเรียน</h3>
                <p>รองรับไฟล์ JPG, PNG</p>
            </div>
            <input type="file" id="fileInput" hidden accept="image/*" onchange="handleImage(event)">
            <div id="previewArea"></div>
        </div>

        <div id="adminPanel" class="panel">
            <h2>📈 Dashboard ค่าก๊าซในโกดัง</h2>
            <div class="chart-container" id="gasChart">
                </div>
            <div style="margin-top: 40px;">
                <h3>📡 รายชื่อเซนเซอร์</h3>
                <div id="deviceList"></div>
            </div>
        </div>
    </div>

    <script>
        function switchMode(mode) {
            document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(mode + 'Panel').classList.add('active');
            event.target.classList.add('active');
            if(mode === 'admin') loadAdminData();
        }

        async function handleImage(event) {
            const file = event.target.files[0];
            if(!file) return;

            const preview = document.getElementById('previewArea');
            preview.innerHTML = "<div class='result-card'>🔄 กำลังวิเคราะห์ด้วย Roboflow AI...</div>";

            const formData = new FormData();
            formData.append('image', file);

            try {
                const response = await fetch('/api/analyze-durian', { method: 'POST', body: formData });
                const data = await response.json();

                if (data.success) {
                    preview.innerHTML = `
                        <div class="result-card">
                            <div class="status-badge" style="background: #E8F5E9; color: #2E7D32;">✨ ผลการวิเคราะห์</div>
                            <h2>สถานะ: ${data.status}</h2>
                            <p>ระดับความมั่นใจ: ${data.confidence}%</p>
                            <hr style="margin: 15px 0; border: 0; border-top: 1px solid #ddd;">
                            <p>🍃 ค่าก๊าซ Ethylene โดยประมาณ: ${data.ethylene} ppm</p>
                        </div>
                    `;
                }
            } catch (err) { preview.innerHTML = "❌ เกิดข้อผิดพลาด"; }
        }

        function loadAdminData() {
            const chart = document.getElementById('gasChart');
            chart.innerHTML = '';
            for(let i=0; i<8; i++) {
                const h = Math.random() * 150 + 20;
                chart.innerHTML += `<div class="chart-bar" style="height: ${h}px;"><span class="chart-label">${i*3}:00</span></div>`;
            }
        }
    </script>
</body>
</html>
'''

# --- 3. API Routes ---
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/analyze-durian', methods=['POST'])
def analyze_durian():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image uploaded'})
    
    file = request.files['image']
    temp_path = "temp_capture.jpg"
    file.save(temp_path)

    try:
        # เรียกใช้ Roboflow AI จริงๆ
        result = model.predict(temp_path, confidence=40).json()
        predictions = result.get('predictions', [])

        if not predictions:
            return jsonify({'success': True, 'status': 'ไม่พบทุเรียน', 'confidence': 0, 'ethylene': 0})

        top = predictions[0]
        ethylene_sim = round(10 + random.random() * 50, 1) # จำลองค่าก๊าซควบคู่

        return jsonify({
            'success': True,
            'status': top['class'],
            'confidence': int(top['confidence'] * 100),
            'ethylene': ethylene_sim
        })
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
