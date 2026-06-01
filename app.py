from flask import Flask, render_template_string
import random

app = Flask(__name__)

roast_templates = [
    "{name}, 2 plus 2 bhi nahi aata? School me kya ghass katne jata tha? 🤡",
    "{name}, calculator bhi bol raha hai 'bhai rehne de' 😭",
    "{name}, tere se to Alexa bhi zyada samajhdaar hai 🤖",
    "{name}, tu youtube pe how to use calculator search karta hoga 💀",
    "{name}, tera attendance bhi proxy se lagta hoga 📝",
    "{name}, tera dimaag airplane mode pe hai kya? ✈️"
]

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Troll Calculator v7.0 💀</title>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.2/dist/confetti.browser.min.js"></script>
    <style>
        body {
            font-family: Arial;
            background: #1a1a1a;
            color: white;
            text-align: center;
            padding: 50px;
            overflow-x: hidden;
        }
        h1 {
            color: #ff4757;
            animation: glow 2s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 10px #ff4757; }
            to { text-shadow: 0 0 20px #ff4757, 0 0 30px #ff4757; }
        }
        input, button {
            padding: 12px;
            margin: 10px;
            border-radius: 8px;
            border: none;
            font-size: 16px;
        }
        button {
            background: #ff4757;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover { transform: scale(1.05); }
        .sound-btn {
            background: #2ed573;
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 9999;
        }
        #result {
            margin-top: 30px;
            font-size: 24px;
            font-weight: bold;
            min-height: 60px;
        }
    </style>
</head>
<body>
    <button id="enableSound" class="sound-btn">🔊 Sound On Karo</button>
    
    <h1>💀 TROLL CALCULATOR v7.0 💀</h1>
    <p>Duniya ka sabse imaandaar calculator</p>
    
    <input type="text" id="name" placeholder="Apna naam daal bhai">
    <br>
    <input type="text" id="question" placeholder="2+2 ya kuch bhi puch" value="2+2">
    <br>
    <button onclick="troll()">Hisab Laga</button>
    
    <div id="result"></div>

    <script>
        let soundEnabled = false;
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        document.getElementById('enableSound').onclick = async () => {
            if (audioContext.state === 'suspended') {
                await audioContext.resume();
            }
            soundEnabled = true;
            document.getElementById('enableSound').innerHTML = '✅ Sound On Hai';
            document.getElementById('enableSound').style.background = '#00b894';
            playSound('startup');
        };

        function playSound(type) {
            if (!soundEnabled) return;
            const osc = audioContext.createOscillator();
            const gain = audioContext.createGain();
            osc.connect(gain);
            gain.connect(audioContext.destination);
            
            if (type === 'boom') {
                osc.frequency.value = 60;
                gain.gain.setValueAtTime(0.3, audioContext.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
                osc.start();
                osc.stop(audioContext.currentTime + 0.5);
            } else if (type === 'startup') {
                osc.frequency.setValueAtTime(400, audioContext.currentTime);
                osc.frequency.exponentialRampToValueAtTime(800, audioContext.currentTime + 0.3);
                gain.gain.setValueAtTime(0.2, audioContext.currentTime);
                osc.start();
                osc.stop(audioContext.currentTime + 0.3);
            }
        }

        function speak(text) {
            if (!soundEnabled) return;
            speechSynthesis.cancel();
            const msg = new SpeechSynthesisUtterance(text);
            msg.lang = 'hi-IN';
            msg.rate = 0.9;
            speechSynthesis.speak(msg);
        }

        async function troll() {
            const name = document.getElementById('name').value || 'Bhai';
            const resultDiv = document.getElementById('result');
            
            resultDiv.innerHTML = 'Hisab lag raha hai...';
            
            const roasts = {{ roasts | tojson }};
            const roast = roasts[Math.floor(Math.random() * roasts.length)].replace('{name}', name);
            
            setTimeout(() => {
                playSound('boom');
                resultDiv.innerHTML = `💥 ${roast} 💥`;
                resultDiv.style.color = '#ff4757';
                
                confetti({ particleCount: 150, spread: 100, origin: { y: 0.6 } });
                speak(roast);
            }, 1000);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML, roasts=roast_templates)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
