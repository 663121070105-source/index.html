import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(layout="wide", page_title="Durian Smart AI")


html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Durian Smart AI</title>
    <style>
        /* CSS: ส่วนตกแต่งความสวยงาม */
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            /* ตรงนี้คือจุดที่เคย Error (0%) ตอนนี้ปลอดภัยแล้วเพราะอยู่ในเครื่องหมายคำพูด */
            background: linear-gradient(135deg, #E8F5E9 0%, #FFF9C4 100%); 
            min-height: 100vh; 
            padding: 20px; 
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container { 
            width: 100%;
            max-width: 600px; 
            background: rgba(255, 255, 255, 0.95); 
            padding: 40px; 
            border-radius: 25px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.15); 
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        h1 { 
            color: #2E7D32; 
            margin-bottom: 5px; 
            font-size: 2.5rem;
        }
        
        p.subtitle {
            color: #827717;
            margin-bottom: 30px;
            font-size: 1.1rem;
        }

        .emoji-header { 
            font-size: 80px; 
            margin-bottom: 10px; 
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
            40% {transform: translateY(-20px);}
            60% {transform: translateY(-10px);}
        }

        .scan-area {
            background: #F1F8E9;
            border: 2px dashed #AED581;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 25px;
            transition: all 0.3s;
        }

        .scan-area:hover {
            background: #DCEDC8;
            border-color: #7CB342;
        }

        .btn { 
            background: linear-gradient(45deg, #43A047, #66BB6A); 
            color: white; 
            border: none; 
            padding: 18px 40px; 
            font-size: 20px; 
            border-radius: 50px; 
            cursor: pointer; 
            box-shadow: 0 5px 15px rgba(67, 160, 71, 0.4);
            transition: transform 0.2s, box-shadow 0.2s;
            font-weight: bold;
            width: 100%;
        }

        .btn:active { 
            transform: scale(0.98); 
        }

        #result {
            margin-top: 20px;
            display: none;
            animation: fadeIn 0.5s;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .status-box {
            padding: 20px;
            border-radius: 15px;
            color: white;
            margin-top: 15px;
        }
        .status-ripe { background: linear-gradient(135deg, #FDD835, #FBC02D); color: #333; }
        .status-raw { background: linear-gradient(135deg, #66BB6A, #43A047); }
    </style>
</head>
<body>

    <div class="container">
        <div class="emoji-header">🥭</div>
        <h1>Durian Check AI</h1>
        <p class="subtitle">ระบบตรวจสอบความสุกทุเรียนด้วย AI</p>
        
        <div class="scan-area" id="previewArea">
            <div style="font-size: 40px; color: #ccc;">📷</div>
            <p style="color: #888;">แตะปุ่มด้านล่างเพื่อสแกน</p>
        </div>

        <button class="btn" onclick="processScan()">เริ่มวิเคราะห์</button>

        <div id="result">
            </div>
    </div>

    <script>
        function processScan() {
            const preview = document.getElementById('previewArea');
            const resultDiv = document.getElementById('result');
            const btn = document.querySelector('.btn');
            
            // จำลองการโหลด
            preview.innerHTML = '<div style="font-size: 40px;">🔄</div><p>กำลังวิเคราะห์ภาพ...</p>';
            btn.disabled = true;
            btn.style.opacity = '0.7';
            btn.innerText = 'กำลังประมวลผล...';
            resultDiv.style.display = 'none';

            setTimeout(() => {
                // สุ่มผลลัพธ์ (จำลอง AI)
                const isRipe = Math.random() > 0.5;
                const percentage = Math.floor(Math.random() * 20) + 80;
                
                let htmlContent = '';
                
                if(isRipe) {
                    htmlContent = `
                        <div class="status-box status-ripe">
                            <h2>😋 ทุเรียนสุกพอดี</h2>
                            <p style="font-size: 1.2rem;">ความสุก: <strong>${percentage}%</strong></p>
                            <p>เนื้อนุ่ม กลิ่นหอม พร้อมรับประทาน</p>
                        </div>
                    `;
                } else {
                    htmlContent = `
                        <div class="status-box status-raw">
                            <h2>🟢 ทุเรียนยังดิบ</h2>
                            <p style="font-size: 1.2rem;">ความสุก: <strong>${percentage - 40}%</strong></p>
                            <p>ควรบ่มต่ออีก 2-3 วัน</p>
                        </div>
                    `;
                }

                resultDiv.innerHTML = htmlContent;
                resultDiv.style.display = 'block';
                
                // คืนค่าปุ่ม
                preview.innerHTML = '<div style="font-size: 40px;">✅</div><p>วิเคราะห์เสร็จสิ้น</p>';
                btn.disabled = false;
                btn.style.opacity = '1';
                btn.innerText = 'เริ่มวิเคราะห์ใหม่';
                
            }, 2000); // รอ 2 วินาที
        }
    </script>

</body>
</html>
""" 

components.html(html_code, height=850, scrolling=True)
