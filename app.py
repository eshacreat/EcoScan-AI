from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
# PASTE YOUR API KEY HERE
PAGESPEED_KEY = "AIzaSyDmxKfp9yzf3XUZ6JwIisegZ8qG1MBLtrY" 

# --- AI LOGIC FUNCTION ---
def get_eco_status(score):
    if score >= 90:
        return {"label": "Eco-Guardian", "color": "#2d6a4f", "advice": "Minimal energy waste. Carbon footprint is optimized."}
    elif score >= 50:
        return {"label": "Power Hungry", "color": "#764a12", "advice": "Heavier assets are causing unnecessary server load."}
    else:
        return {"label": "Carbon Heavy", "color": "#9b2226", "advice": "High bloat detected. This site consumes excess electricity."}

# --- THE FRONT PAGE (MAIN HUB) ---
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Eco-Scan AI</title>
        <style>
            body { 
                margin: 0; 
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.4)), 
                            url('https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=1920&q=80');
                background-size: cover;
                background-attachment: fixed;
                display: flex; justify-content: center; align-items: center; height: 100vh;
            }
            .glass-card {
                background: rgba(255, 255, 255, 0.75);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                text-align: center;
                border: 1px solid rgba(255, 255, 255, 0.3);
                width: 400px;
            }
            input {
                padding: 12px; width: 80%; border-radius: 10px; border: 1px solid #ddd;
                margin: 20px 0; outline: none;
            }
            button {
                background: #84a59d; color: white; border: none; padding: 12px 25px;
                border-radius: 10px; cursor: pointer; font-size: 16px; transition: 0.3s;
            }
            button:hover { background: #f5cac3; color: #333; }
        </style>
    </head>
    <body>
        <div class="glass-card">
            <h1 style="color: #555;">Eco-Scan AI 🌿</h1>
            <p style="color: #777;">Enter a URL to analyze its environmental impact</p>
            <form action="/scan" method="post">
                <input type="text" name="url" placeholder="https://example.com" required>
                <br>
                <button type="submit">BEGIN ANALYSIS</button>
            </form>
        </div>
    </body>
    </html>
    '''

# --- THE RESULTS PAGE ---
@app.route('/scan', methods=['POST'])
def scan():
    target_url = request.form.get('url')
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={target_url}&key={PAGESPEED_KEY}"
    
    try:
        response = requests.get(api_url, timeout=60)
        data = response.json()
        score = data['lighthouseResult']['categories']['performance']['score'] * 100
        status = get_eco_status(score)
        
        return f'''
        <body style="margin:0; font-family:sans-serif; background:#f0f4f8; display:flex; justify-content:center; align-items:center; height:100vh;">
            <div style="background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; width: 450px; border-top: 10px solid {status['color']};">
                <h2 style="color: #444;">{target_url}</h2>
                <h1 style="font-size: 48px; color: {status['color']}; margin: 10px 0;">{score:.0f}</h1>
                <h3 style="color: {status['color']};">{status['label']}</h3>
                <p style="color: #666; line-height: 1.6;">{status['advice']}</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                <a href="/" style="text-decoration: none; color: #84a59d; font-weight: bold;">← DISMISS</a>
            </div>
        </body>
        '''
    except Exception as e:
        return f"<h3>Error connecting to server.</h3><p>{e}</p><a href='/'>Back</a>"

if __name__ == '__main__':
    app.run(debug=True)