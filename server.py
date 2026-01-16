from flask import Flask, request, Response
import pyautogui
import mss
import io
from PIL import Image, ImageDraw

# Sicherheitsfeature: Fail-Safe deaktivieren, falls gewünscht (Vorsicht!)
# pyautogui.FAILSAFE = False

# WICHTIG: Standard-Pause deaktivieren für flüssigere Bewegung
pyautogui.PAUSE = 0

app = Flask(__name__)

def gen_frames():
    # MSS muss im gleichen Thread initialisiert werden (Thread-Safe Fix)
    with mss.mss() as sct:
        while True:
            # Mausposition holen
            mouse_x, mouse_y = pyautogui.position()

            # Automatisch den Monitor finden, auf dem die Maus ist
            monitor = sct.monitors[1] # Fallback auf Primary
            for m in sct.monitors[1:]:
                # Prüfen ob Maus innerhalb der Monitor-Grenzen liegt
                if (m["left"] <= mouse_x < m["left"] + m["width"]) and \
                   (m["top"] <= mouse_y < m["top"] + m["height"]):
                    monitor = m
                    break
            
            sct_img = sct.grab(monitor)
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
            # Performance: Bild skalieren (z.B. 60%)
            scale = 0.6
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size)

            # Mauszeiger einzeichnen (relativ zum aktuellen Monitor)
            cursor_x = int((mouse_x - monitor["left"]) * scale)
            cursor_y = int((mouse_y - monitor["top"]) * scale)
            
            draw = ImageDraw.Draw(img)
            r = 5 # Radius Mauspunkt
            draw.ellipse((cursor_x-r, cursor_y-r, cursor_x+r, cursor_y+r), fill="red", outline="white")

            # In Bytes konvertieren
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=45)
            img_byte_arr = img_byte_arr.getvalue()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_byte_arr + b'\r\n')

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
            body { 
                font-family: -apple-system, system-ui, sans-serif; 
                background-color: #1a1a1a; 
                color: white; 
                display: flex; 
                flex-direction: column; 
                /* Dynamische Höhe für Mobile */
                min-height: 100dvh; 
                margin: 0; 
                /* Scrollen erlauben */
                overflow-y: auto;
                padding-bottom: 20px;
            }
            h1 { text-align: center; font-weight: 300; margin: 10px 0; font-size: 1.2rem; }
            
            .grid { 
                display: grid; 
                grid-template-columns: repeat(3, 1fr); 
                gap: 8px; 
                padding: 0 10px; 
                margin-bottom: 10px;
                flex-shrink: 0;
            }
            
            button { 
                background: #333; color: white; border: none; padding: 15px 5px; font-size: 0.9rem; border-radius: 12px; 
                box-shadow: 0 4px 0 #000; transition: all 0.1s; -webkit-tap-highlight-color: transparent;
                touch-action: manipulation;
                font-weight: bold;
            }
            button:active { transform: translateY(4px); box-shadow: 0 0 0 #000; background: #444; }
            
            .primary { background: #007bff; box-shadow: 0 4px 0 #0056b3; }
            .primary:active { background: #0069d9; box-shadow: 0 0 0 #000; }
            
            .media { background: #28a745; box-shadow: 0 4px 0 #1e7e34; }
            .media:active { background: #218838; box-shadow: 0 0 0 #000; }
            
            .toggle-btn { background: #6f42c1; box-shadow: 0 4px 0 #5a32a3; margin: 0 10px 10px 10px; }
            .toggle-btn:active { background: #5a32a3; box-shadow: 0 0 0 #000; }

            #touchpad-container {
                /* Höhe des Touchpads */
                height: 40vh; 
                width: 90%;
                align-self: center;
                background: #2a2a2a; /* Standard: Grau */
                margin: 10px 0;
                border-radius: 16px;
                border: 2px dashed #444;
                position: relative;
                touch-action: none;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #666;
                overflow: hidden;
                flex-shrink: 0;
            }
            
            /* Wenn Screen-View aktiv ist -> Fullscreen Overlay */
            #touchpad-container.screen-mode {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                margin: 0;
                border-radius: 0;
                border: none;
                z-index: 1000;
                background: #000;
            }

            #stream-img {
                width: 100%;
                height: 100%;
                object-fit: contain;
                pointer-events: none;
                user-select: none;
                display: none;
            }

            /* Schließen-Button (nur im Screen-Mode sichtbar) */
            #close-btn {
                position: absolute;
                top: 20px;
                right: 20px;
                width: 50px;
                height: 50px;
                background: rgba(255, 0, 0, 0.7);
                color: white;
                border-radius: 50%;
                display: none; /* Standard: unsichtbar */
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                font-weight: bold;
                border: 2px solid white;
                z-index: 1001;
                cursor: pointer;
            }

            .label-text { pointer-events: none; }
        </style>
    </head>
    <body>
        <h1>Ultimate Remote</h1>
        
        <button class="toggle-btn" onclick="toggleView()">📺 Bildschirm An/Aus</button>
        
        <div id="touchpad-container">
            <span id="touchpad-label" class="label-text">Touchpad</span>
            <img id="stream-img" src="" alt="Live Stream">
            <div id="close-btn" onclick="toggleView()">X</div>
        </div>

        <div class="grid">
            <button class="primary" onclick="fetch('/click')">L-Klick</button>
            <button class="primary" onclick="fetch('/right_click')">R-Klick</button>
            <button class="media" onclick="fetch('/zirkumflex')">Discord Mute</button>
        </div>
        
        <div class="grid">
             <button onclick="fetch('/space')">Space</button>
             <button onclick="fetch('/enter')">Enter</button>
             <button onclick="fetch('/backspace')">⌫</button>
        </div>

        <script>
            let streamActive = false;
            
            function toggleView() {
                streamActive = !streamActive;
                const container = document.getElementById('touchpad-container');
                const img = document.getElementById('stream-img');
                const label = document.getElementById('touchpad-label');
                const closeBtn = document.getElementById('close-btn');
                
                if (streamActive) {
                    // Modus: Bildschirm (Fullscreen)
                    container.classList.add('screen-mode');
                    label.style.display = 'none';
                    img.style.display = 'block';
                    closeBtn.style.display = 'flex'; // X-Button zeigen
                    img.src = "/video_feed";
                } else {
                    // Modus: Touchpad (Normal)
                    container.classList.remove('screen-mode');
                    label.style.display = 'block';
                    img.style.display = 'none';
                    closeBtn.style.display = 'none';
                    img.src = ""; // Stream stoppen
                }
            }

            // --- Touchpad Logic ---
            const touchpad = document.getElementById('touchpad-container');
            let lastX = 0;
            let lastY = 0;
            let isTracking = false;
            
            // Puffer für flüssigere Bewegung
            let moveBufferX = 0;
            let moveBufferY = 0;
            let isBusy = false; 
            
            // Sendet gesammelte Bewegung alle 30ms (ca. 30 FPS)
            setInterval(() => {
                if ((moveBufferX !== 0 || moveBufferY !== 0) && !isBusy) {
                    isBusy = true;
                    // Werte kopieren und Puffer sofort leeren
                    const sendX = Math.round(moveBufferX);
                    const sendY = Math.round(moveBufferY);
                    moveBufferX = 0;
                    moveBufferY = 0;

                    // Nur senden wenn wirklich Bewegung da war (nach Rundung)
                    if (sendX === 0 && sendY === 0) {
                        isBusy = false;
                        return;
                    }

                    fetch(`/move?x=${sendX}&y=${sendY}`, { method: 'POST' })
                        .then(() => {
                            // Erfolg
                        })
                        .catch(err => {
                            console.error(err);
                        })
                        .finally(() => { 
                            isBusy = false; 
                        });
                }
            }, 30);

            // Für Tap-Detection
            let startX = 0;
            let startY = 0;
            let startTime = 0;
            let hasMoved = false;

            touchpad.addEventListener('touchstart', (e) => {
                isTracking = true;
                const t = e.touches[0];
                lastX = t.clientX;
                lastY = t.clientY;
                
                // Startwerte für Tap-Erkennung
                startX = t.clientX;
                startY = t.clientY;
                startTime = new Date().getTime();
                hasMoved = false;
            });

            touchpad.addEventListener('touchend', (e) => {
                isTracking = false;
                
                // Prüfen ob es ein Tap war (kurz und wenig Bewegung)
                const endTime = new Date().getTime();
                const duration = endTime - startTime;
                
                // Wenn nicht bewegt (oder nur minimal zittert) und kurz gedrückt -> Klick
                if (!hasMoved && duration < 250) {
                    fetch('/click');
                    // Visuelles Feedback
                    touchpad.style.backgroundColor = '#444'; 
                    setTimeout(() => {
                        // Farbe zurücksetzen je nach Modus
                        if (!streamActive) touchpad.style.backgroundColor = '#2a2a2a';
                        else touchpad.style.backgroundColor = '#000';
                    }, 100);
                }
            });

            touchpad.addEventListener('touchmove', (e) => {
                if (!isTracking) return;
                
                // Verhindert Scrollen/Zoom Verhalten
                if (e.cancelable) e.preventDefault();

                const currentX = e.touches[0].clientX;
                const currentY = e.touches[0].clientY;
                
                const deltaX = currentX - lastX;
                const deltaY = currentY - lastY;
                
                // Prüfen ob signifikante Bewegung für "Drag" vs "Tap"
                // Schwelle von 5px, damit minimales Wackeln nicht als Move zählt
                if (Math.abs(currentX - startX) > 5 || Math.abs(currentY - startY) > 5) {
                    hasMoved = true;
                }
                
                // Bewegung in den Puffer addieren statt sofort zu senden
                moveBufferX += deltaX;
                moveBufferY += deltaY;
                
                lastX = currentX;
                lastY = currentY;
            }, { passive: false });
            
            document.addEventListener('touchmove', function(event) {
                if (event.scale !== 1) { event.preventDefault(); }
            }, { passive: false });
        </script>
    </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/click')
def mouse_click():
    pyautogui.click()
    return "OK", 200

@app.route('/right_click')
def mouse_right_click():
    pyautogui.rightClick()
    return "OK", 200

@app.route('/scroll_click')
def mouse_scroll_click():
    pyautogui.middleClick()
    return "OK", 200

@app.route('/move', methods=['POST'])
def move_mouse():
    x = request.args.get('x', default=0, type=int)
    y = request.args.get('y', default=0, type=int)
    multiplier = 3.5 
    pyautogui.moveRel(x * multiplier, y * multiplier)
    return "OK", 200

@app.route('/space')
def press_space():
    pyautogui.press('space')
    return "OK", 200

@app.route('/enter')
def press_enter():
    pyautogui.press('enter')
    return "OK", 200

@app.route('/backspace')
def press_backspace():
    pyautogui.press('backspace')
    return "OK", 200

@app.route('/zirkumflex')
def press_caret():
    pyautogui.write('^') 
    return "OK", 200

if __name__ == '__main__':
    # Listen auf allen Interfaces
    app.run(host='0.0.0.0', port=5000)