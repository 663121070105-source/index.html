from flask import Flask, render_template_string, request, jsonify, session
from roboflow import Roboflow
import os
import random

app = Flask(__name__)
app.secret_key = 'durian_secret_key'

# ใส่ API Key ของคุณที่นี่
ROBOFLOW_API_KEY = "aUQh6GrqTow8tSgITsZK" 
rf = Roboflow(api_key=ROBOFLOW_API_KEY)
project = rf.workspace("new-workspace-7qbtz").project("durian-detection-zb1dk")
model = project.version(3).model

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #E8F5E9 0%, #FFF9C4 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="container">
        <h2>🥭 Durian Smart AI Checker</h2>
        <input type="file" accept="image/*" onchange="analyze(event)">
        <div id="result"></div>
    </div>

    <script>
        async function analyze(event) {
            const file = event.target.files[0];
            const formData = new FormData();
            formData.append('image', file);
            
            document.getElementById('result').innerHTML = "⏳ กำลังวิเคราะห์...";
            
            const res = await fetch('/api/analyze-durian', { method: 'POST', body: formData });
            const data = await res.json();
            
            if(data.success) {
                document.getElementById('result').innerHTML = `<h3>ผลลัพธ์: ${data.status}</h3><p>ความแม่นยำ: ${data.confidence}%</p>`;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/analyze-durian', methods=['POST'])
def analyze_durian():
    file = request.files['image']
    file.save("temp.jpg")
    result = model.predict("temp.jpg", confidence=40).json()
    predictions = result.get('predictions', [])
    
    if not predictions:
        return jsonify({'success': True, 'status': 'ไม่พบทุเรียน', 'confidence': 0})
        
    top = predictions[0]
    return jsonify({'success': True, 'status': top['class'], 'confidence': int(top['confidence']*100)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
