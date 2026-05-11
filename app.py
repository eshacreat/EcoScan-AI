from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# 1. SETUP & CONFIGURATION
load_dotenv() 
app = Flask(__name__) 
PAGESPEED_KEY = os.getenv("PAGESPEED_KEY")

# 2. AI LOGIC FUNCTION
def get_eco_status(score):
    if score >= 85: # Lowered the "Guardian" threshold to be more realistic
        return {
            "label": "Eco-Guardian", 
            "color": "#2d6a4f", 
            "advice": "Excellent optimization! Tiny digital footprint.",
            "impact": "This site is in the top 10% of energy-efficient web design."
        }
    elif score >= 60: # The "Average" zone
        return {
            "label": "Digital Heavyweight", 
            "color": "#764a12", 
            "advice": "Unoptimized images or scripts are draining server power.",
            "impact": "If 1,000 people visit this, it's like driving a car for 2 miles."
        }
    else: # The "Problem" zone
        return {
            "label": "Carbon Critic", 
            "color": "#9b2226", 
            "advice": "Critical bloat. This site requires massive server cooling.",
            "impact": "This site uses as much energy per load as boiling a cup of water."
        }
# 3. THE FRONT PAGE (MAIN HUB)
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Eco-Scan AI</title>
        <style>
            body { 
                margin: 0; font-family: 'Segoe UI', sans-serif;
                display: flex; justify-content: center; align-items: center; 
                height: 100vh; width: 100vw; overflow: hidden;
            }
            body::before {
                content: ""; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
                background: url('https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=1920&q=80');
                background-size: cover; background-position: center;
                filter: blur(3px); z-index: -1; transform: scale(1.07);
            }
            .glass-card {
                background: rgba(255, 255, 255, 0.98); border-radius: 28px;
                padding: 45px; box-shadow: 0 20px 50px rgba(0,0,0,0.2); 
                text-align: center; border: 1px solid rgba(255, 255, 255, 0.5);
                width: 420px; position: relative;
            }
            h1 { color: #2d6a4f; margin-top: 0; }
            input {
                padding: 15px; width: 85%; border-radius: 12px; border: 1px solid #ddd;
                margin: 25px 0 15px 0; outline: none; font-size: 16px;
            }
            button {
                background: #2d6a4f; color: white; border: none; padding: 15px 30px;
                border-radius: 12px; cursor: pointer; font-size: 16px; 
                font-weight: bold; width: 93%; transition: 0.3s;
            }
            button:hover { background: #40916c; transform: translateY(-2px); }
            
            .spinner {
                border: 4px solid rgba(255, 255, 255, 0.3);
                border-top: 4px solid #fff; border-radius: 50%;
                width: 40px; height: 40px; animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
        <script>
            const jokes = [
                "Scanning for digital dust bunnies...",
                "Measuring the weight of your pixels...",
                "Negotiating with the Google Overlords...",
                "Searching for hidden carbon monsters...",
                "Watering the digital trees..."
            ];
            let jokeIndex = 0;
            function rotateJokes() {
                const jokeElement = document.getElementById('loading-joke');
                if (jokeElement) {
                    jokeElement.innerText = jokes[jokeIndex];
                    jokeIndex = (jokeIndex + 1) % jokes.length;
                }
            }
            function showLoading() {
                document.getElementById('main-card').style.display = 'none';
                document.getElementById('loader').style.display = 'block';
                setInterval(rotateJokes, 4000);
            }
        </script>
    </head>
    <body>
        <div id="loader" style="display:none; text-align:center; color:white;">
            <div class="spinner"></div> 
            <h2 id="loading-joke" style="color: white; font-size: 28px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5); min-height: 40px;">
                Analyzing Digital Footprint...
            </h2>
            <p style="color: rgba(255,255,255,0.9); text-shadow: 1px 1px 5px rgba(0,0,0,0.5); font-weight: 500;">
                Google is thinking. This usually takes 30-60 seconds.
            </p>
        </div>
        <div id="main-card" class="glass-card">
            <h1>Eco-Scan AI 🌿</h1>
            <p>Analyze the carbon footprint of any website</p>
            <form action="/scan" method="post" onsubmit="showLoading()">
                <input type="text" name="url" placeholder="https://example.com" required>
                <button type="submit">BEGIN ANALYSIS</button>
            </form>
        </div>
    </body>
    </html>
    '''

# 4. THE RESULTS PAGE
@app.route('/scan', methods=['POST'])
def scan():
    target_url = request.form.get('url').strip()
    
    if not target_url.startswith("http"):
        return f'''
        <style>
            body {{ margin: 0; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; }}
            body::before {{ content: ""; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: url('https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=1920&q=80'); background-size: cover; filter: blur(6px); z-index: -1; transform: scale(1.1); }}
            .error-card {{ background: white; padding: 45px; border-radius: 28px; text-align: center; width: 420px; border-top: 10px solid #f87171; box-shadow: 0 20px 50px rgba(0,0,0,0.2); }}
        </style>
        <body>
            <div class="error-card">
                <h1 style="color: #991b1b;">Link Format Error</h1>
                <p>Please use a full link starting with <b>https://</b></p>
                <a href="/" style="text-decoration: none; color: #f87171; font-weight: bold;">← TRY AGAIN</a>
            </div>
        </body>
        '''

    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={target_url}&key={PAGESPEED_KEY}"
    
    try:
        response = requests.get(api_url, timeout=60)
        data = response.json()
        if 'error' in data:
            raise Exception("Google could not reach this website.")

        score = data['lighthouseResult']['categories']['performance']['score'] * 100
        status = get_eco_status(score)
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ margin: 0; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
                body::before {{ content: ""; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: url('https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=1920&q=80'); background-size: cover; filter: blur(6px); z-index: -1; transform: scale(1.1); }}
                .results-card {{ background: rgba(255, 255, 255, 0.98); border-radius: 28px; padding: 45px; box-shadow: 0 20px 50px rgba(0,0,0,0.2); text-align: center; width: 420px; border-top: 12px solid {status['color']}; }}
                .score-circle {{ font-size: 64px; font-weight: 800; color: {status['color']}; margin: 20px 0; }}
                .ai-recommendation {{ background: #f8f9fa; border-left: 5px solid {status['color']}; padding: 20px; border-radius: 12px; margin-top: 25px; text-align: left; }}
                .back-btn {{ display: inline-block; margin-top: 30px; text-decoration: none; color: #666; font-weight: 600; transition: 0.3s; }}
                .back-btn:hover {{ color: #2d6a4f; }}
            </style>
        </head>
        <body>
            <div class="results-card">
                <h3 style="color: #888; margin-bottom: 0;">ANALYSIS FOR</h3>
                <p style="margin-top: 5px; font-weight: bold;">{target_url}</p>
                <div class="score-circle">{score:.0f}</div>
                <h2 style="color: {status['color']};">{status['label']}</h2>
                <div class="ai-recommendation">
                    <strong style="color: #333;">💡 AI Suggestion:</strong>
                    <p style="margin: 10px 0 0 0; color: #555;">{status['advice']}</p>
                    <p style="margin-top: 10px; font-size: 14px; color: #888;">{status['impact']}</p>
                </div>
                <a href="/" class="back-btn">← RUN ANOTHER SCAN</a>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return f'''
        <style>
            body {{ margin: 0; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; }}
            body::before {{ content: ""; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: url('https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=1920&q=80'); background-size: cover; filter: blur(6px); z-index: -1; transform: scale(1.1); }}
            .error-card {{ background: white; padding: 45px; border-radius: 28px; text-align: center; width: 420px; border-top: 10px solid #fbbf24; box-shadow: 0 20px 50px rgba(0,0,0,0.2); }}
        </style>
        <body>
            <div class="error-card">
                <h1 style="color: #b45309;">Connection Issue</h1>
                <p style="color: #666;">Error: {e}</p>
                <a href="/" style="text-decoration: none; color: #d97706; font-weight: bold;">← BACK TO HOME</a>
            </div>
        </body>
        '''

if __name__ == '__main__':
    app.run(debug=True)
