# 📱 Remote Mouse & Keyboard Control

Ein einfacher, aber mächtiger Python-Server, der dein Smartphone in eine Fernbedienung für deinen PC verwandelt. Steuere Maus und wichtige Tasten bequem über das lokale Netzwerk.

## ✨ Features

*   **🖱️ Touchpad:** Steuere den Mauszeiger deines PCs präzise über ein Touch-Feld auf deinem Smartphone-Display.
*   **👆 Klicks:** Linksklick und Rechtsklick Buttons.
*   **⌨️ Shortcuts:**
    *   **Space:** Praktisch für YouTube/Netflix (Play/Pause).
    *   **Discord Mute:** Globaler Shortcut (`^`), um dich in Discord schnell stummzuschalten.
*   **⚡ Performance:** Optimiert für geringe Latenz im lokalen Netzwerk.
*   **📱 Responsive & App-like:** Fühlt sich auf dem Handy fast wie eine native App an.

## 🛠️ Voraussetzungen

Du benötigst Python installiert auf deinem PC.

Die folgenden Python-Bibliotheken werden benötigt:
*   `Flask` (Webserver)
*   `pyautogui` (Maus-/Tastatursteuerung)

##  🚀 Installation

1.  **Repository klonen** (oder Dateien herunterladen):
    ```bash
    git clone <DEIN-REPO-URL>
    cd Board
    ```

2.  **Abhängigkeiten installieren:**
    Am besten in einer virtuellen Umgebung:
    ```bash
    pip install flask pyautogui
    ```

## 🎮 Benutzung

1.  **Server starten:**
    ```bash
    python server.py
    ```
    *(Stelle sicher, dass du dich im richtigen Verzeichnis befindest)*

2.  **IP-Adresse finden:**
    Das Skript zeigt dir beim Start normalerweise an, unter welcher IP es läuft (z.B. `http://192.168.2.35:5000`).
    Falls nicht, finde deine lokale IP-Adresse heraus (`ipconfig` auf Windows).

3.  **Verbinden:**
    Öffne den Browser auf deinem Smartphone und gib die Adresse ein:
    `http://<IP-DEINES-PCS>:5000`

    💡 **Wichtig:** Dein PC und dein Smartphone müssen im **gleichen WLAN/Netzwerk** sein.

## ⚠️ Sicherheitshinweis

Dieses Tool öffnet einen Server in deinem lokalen Netzwerk, der Kontrolle über Maus und Tastatur erlaubt.
*   Benutze es **nur in vertrauenswürdigen Netzwerken** (dein Zuhause).
*   Benutze es **niemals** in öffentlichen WLANs (Uni, Café, Flughafen).

## 📝 Lizenz

Feel free to use and modify!
