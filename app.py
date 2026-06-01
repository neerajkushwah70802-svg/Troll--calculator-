from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

roast_templates = [
    "{name}, 2 plus 2 bhi nahi aata? School ja wapis",
    "{name}, calculator bhi bol raha hai 'mujhe uninstall kar do '",
    "{name}, tere se to alexa bhi zyada samajhdaar hai ",
    "{name}, tu youtube pe 'how to use calculator 'search kar ",
    "{name}, tera attendance bhi proxy se lagta hoga ",
    "{name}, tera dimaag airplane ode pe hai kya ?",
    ]

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Troll Calculator v7.0 💥</title>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
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
        input { 
            padding: 12px; 
            font-size: 18px; 
            width: 200px; 
            border: 2px solid #ff4757;
            border-radius: 5px;
            background: #2f3542;
            color: white;
            margin: 5px;
        }
        button { 
            padding: 12px 25px; 
            font-size: 18px; 
            background: #ff4757; 
            color: white; 
            border: none; 
            cursor: pointer; 
            border-radius: 5px;
            transition: 0.3s;
            margin-top: 10px;
        }
        button:hover { 
            background: #ff3838; 
            transform: scale(1.05);
        }
        .result { 
            margin-top: 30px; 
            font-size: 20px; 
            background: #2f3542; 
            padding: 25px; 
            border-radius: 10px; 
            border: 2px solid #57606f;
            position: relative;
            z-index: 10;
        }
        .wrong { 
            color: #ff4757; 
            font-weight: bold;
            animation: shake 0.5s;
        }
        .correct { 
            color: #2ed573; 
            font-weight: bold;
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        .calculating {
            animation: blink 1s infinite;
        }
        @keyframes blink {
            50% { opacity: 0.3; }
        }
        .troll-counter {
            margin-top: 20px;
            font-size: 24px;
            color: #ffa502;
        }
        #canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }
        .label {
            font-size: 16px;
            color: #ffa502;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    <h1>Troll Calculator v7.0 💥🎉</h1>
    <form method="POST" id="calcForm">
        <div class="label">Apna naam dal bhai:</div>
        <input name="username" id="nameInput" placeholder="Naam likh" value="{{ username }}" required autocomplete="off">
        <br>
        <div class="label" style="margin-top:15px;">Calculation dal:</div>
        <input name="exp" id="expInput" placeholder="2+2 dal bhai" value="{{ exp }}" required autocomplete="off">
        <br>
        <button type="submit">Calculate</button>
    </form>
    
    <div id="loading" style="display:none; margin-top:20px;">
        <p class="calculating">Calculating... 99% complete...</p>
    </div>
    
    {% if result %}
    <div class="result" id="resultBox">
        {{ result|safe }}
        <div class="troll-counter"><b>Total trolls: {{ troll_count }}</b></div>
    </div>
    
    {% if is_troll %}
    <audio id="trollSound" autoplay>
        <source src="https://www.myinstants.com/media/sounds/vine-boom.mp3" type="audio/mpeg">
    </audio>
    <script>
        // 1. BOOM Sound
        document.getElementById('trollSound').volume = 1.0;
        document.getElementById('trollSound').play();
        
        // 2. Confetti Blast
        function fireConfetti() {
            var count = 200;
            var defaults = { origin: { y: 0.7 } };
            function fire(particleRatio, opts) {
                confetti(Object.assign({}, defaults, opts, {
                    particleCount: Math.floor(count * particleRatio)
                }));
            }
            fire(0.25, { spread: 26, startVelocity: 55 });
            fire(0.2, { spread: 60 });
            fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8 });
            fire(0.1, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2 });
            fire(0.1, { spread: 120, startVelocity: 45 });
        }
        fireConfetti();
        setTimeout(fireConfetti, 250);
        setTimeout(fireConfetti, 400);
        
        // 3. Voice Roast - AB JO NAAM DAALA WAHI BOLEGA
        const roastText = "{{ roast_text }}";
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(roastText);
            utterance.lang = 'hi-IN';
            utterance.rate = 0.9;
            utterance.pitch = 1.2;
            utterance.volume = 1.0;
            speechSynthesis.speak(utterance);
        }
        
        // 4. Shake Animation
        setTimeout(() => {
            document.getElementById('resultBox').style.animation = 'shake 0.5s';
        }, 100);
    </script>
    {% endif %}
    {% endif %}
    
    <script>
        document.getElementById('calcForm').onsubmit = function() {
            document.getElementById('loading').style.display = 'block';
            return true;
        }
    </script>
</body>
</html>
'''

troll_count = 0

@app.route('/', methods=['GET', 'POST'])
def calculator():
    global troll_count
    result = ""
    exp = ""
    username = ""
    is_troll = False
    roast_text = ""
    
    if request.method == 'POST':
        exp = request.form['exp']
        username = request.form['username'].strip()
        if not username:
            username = "Bhai"  # Agar naam khali chhod diya to
        
        try:
            correct = eval(exp)
            
            if random.random() < 0.5:
                wrong = correct + random.randint(1,25)
                # AB JO NAAM DAALA WAHI USE HOGA
                roast_text = random.choice(roast_templates).format(name=username)
                result = f'''
                <p class="calculating">Calculating... 99% complete...</p>
                <p style="color:#ff4757; font-size:28px;">💥 BOOM! ERROR 💥</p>
                <span class="wrong">Answer: {wrong} HAHAHA</span><br><br>
                <b>Ruk... ye to galat hai!</b><br>
                <span class="correct">Sahi answer: {correct}</span><br><br>
                <b>Calculator:</b> {roast_text}
                '''
                troll_count += 1
                is_troll = True
            else:
                result = f'<span class="correct" style="font-size:28px;">Answer: {correct}</span>'
                
        except:
            roast_text = f"{username}, Kya ulta pulta dal raha hai bhai"
            result = '<span class="wrong">Kya ulta pulta dal raha hai bhai HAHAHA</span>'
            troll_count += 1
            is_troll = True
            
    return render_template_string(HTML, result=result, exp=exp, username=username, troll_count=troll_count, is_troll=is_troll, roast_text=roast_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
