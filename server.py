from flask import Flask, request
import pyautogui

# Sicherheitsfeature: Fail-Safe deaktivieren, falls gewünscht (Vorsicht!)
# pyautogui.FAILSAFE = False

# WICHTIG: Standard-Pause deaktivieren für flüssigere Bewegung
pyautogui.PAUSE = 0

app = Flask(__name__)

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
                height: 100vh; 
                margin: 0; 
                overflow: hidden;
            }
            h1 { text-align: center; font-weight: 300; margin: 20px 0; font-size: 1.5rem; }
            .grid { 
                display: grid; 
                grid-template-columns: repeat(3, 1fr); 
                gap: 10px; 
                padding: 10px; 
            }
            button { 
                background: #333; color: white; border: none; padding: 15px; font-size: 1rem; border-radius: 12px; 
                box-shadow: 0 4px 0 #000; transition: all 0.1s; -webkit-tap-highlight-color: transparent;
                touch-action: manipulation;
            }
            button:active { transform: translateY(4px); box-shadow: 0 0 0 #000; background: #444; }
            .primary { background: #007bff; box-shadow: 0 4px 0 #0056b3; }
            .primary:active { background: #0069d9; box-shadow: 0 0 0 #000; }
            
            #touchpad-container {
                /* Kleinere, feste Größe statt flex: 1 */
                height: 50vh; 
                width: 90%;
                align-self: center;
                
                background: #2a2a2a;
                margin: 20px 0;
                border-radius: 16px;
                border: 2px dashed #444;
                position: relative;
                touch-action: none; /* Wichtig: Verhindert Scrollen */
                display: flex;
                align-items: center;
                justify-content: center;
                color: #666;
            }
        </style>
    </head>
    <body>
        <h1>Fernsteuerung</h1>
        
        <div id="touchpad-container">
            Touchpad
        </div>

        <div class="grid">
            <button class="primary" onclick="fetch('/click')">L-Klick</button>
            <button class="primary" onclick="fetch('/right_click')">R-Klick</button>
            <button class="primary" onclick="fetch('/zirkumflex')">Discord Mute</button>
        </div>

        <script>
            const touchpad = document.getElementById('touchpad-container');
            let lastX = 0;
            let lastY = 0;
            let isTracking = false;
            let isBusy = false; // Flag um Request-Stau zu verhindern

            touchpad.addEventListener('touchstart', (e) => {
                isTracking = true;
                lastX = e.touches[0].clientX;
                lastY = e.touches[0].clientY;
            });

            touchpad.addEventListener('touchend', () => {
                isTracking = false;
            });

            touchpad.addEventListener('touchmove', (e) => {
                if (!isTracking) return;
                
                const currentX = e.touches[0].clientX;
                const currentY = e.touches[0].clientY;
                
                const deltaX = currentX - lastX;
                const deltaY = currentY - lastY;
                
                lastX = currentX;
                lastY = currentY;

                // Optimierung: Nur senden, wenn signifikante Bewegung UND kein Request offen
                if ((Math.abs(deltaX) > 0 || Math.abs(deltaY) > 0) && !isBusy) {
                    isBusy = true;
                    // _linear=true entfernt Mausbeschleunigung bei pyautogui (falls möglich), hier einfach direct call
                    fetch(`/move?x=${Math.round(deltaX)}&y=${Math.round(deltaY)}`, { method: 'POST' })
                        .finally(() => {
                            isBusy = false;
                        });
                }
            });
            
            document.addEventListener('touchmove', function(event) {
                if (event.scale !== 1) { event.preventDefault(); }
            }, { passive: false });
        </script>
    </body>
    </html>
    """

@app.route('/click')
def mouse_click():
    pyautogui.click()
    return "OK", 200

@app.route('/right_click')
def mouse_right_click():
    pyautogui.rightClick()
    return "OK", 200

@app.route('/move', methods=['POST'])
def move_mouse():
    x = request.args.get('x', default=0, type=int)
    y = request.args.get('y', default=0, type=int)
    
    # Empfindlichkeit
    multiplier = 2.0 
    
    # _pause=False Parameter ist intern, aber PAUSE=0 global hilft schon viel.
    # Wir bewegen relativ zur aktuellen Position.
    pyautogui.moveRel(x * multiplier, y * multiplier)
    
    return "OK", 200

@app.route('/space')
def press_space():
    pyautogui.press('space')
    return "OK", 200

@app.route('/zirkumflex')
def press_caret():
    pyautogui.write('^') 
    return "OK", 200

if __name__ == '__main__':
    # Listen auf allen Interfaces
    app.run(host='0.0.0.0', port=5000)