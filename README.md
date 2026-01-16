# 📱 mobile-pc-remote

A lightweight but powerful Python server that turns your smartphone into a fully featured remote control for your PC with **live screen sharing**. Control your mouse, keyboard, and media playback comfortably from your local network.

## ✨ Features

*   **� Live Screen Sharing:** View your PC's screen directly on your phone in real-time.
*   **🖱️ Smart Touchpad:** 
    *   Responsive mouse control with low latency.
    *   **Tap-to-Click:** Tap once for a left click.
    *   **Auto Monitor Switch:** Automatically captures the monitor where your cursor is located.
    *   **Fullscreen Mode:** Immersive control overlay.
*   **🎮 Controls:**
    *   Left and Right clicks.
    *   **Discord Mute:** Dedicated button for quick mute (`^` key).
*   **⚡ Performance:** Optimized `mss` screen capture for high frame rates and low lag.
*   **📱 App-like Experience:** Responsive web interface that works on any smartphone browser.

## 🛠️ Requirements

*   Python 3.x installed on your PC.
*   A smartphone connected to the same Wi-Fi/Local Network.

## 🚀 Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/SevReiden/mobile-pc-remote.git
    cd mobile-pc-remote
    ```

2.  **Install Dependencies:**
    ```bash
    pip install flask pyautogui mss pillow
    ```

## 🎮 Usage

1.  **Start the Server:**
    ```bash
    python server.py
    ```

2.  **Connect:**
    *   The script logs the IP address (e.g., `http://192.168.x.x:5000`).
    *   Open this address in your smartphone's web browser.

3.  **Enjoy:**
    *   Use the grey area as a trackpad.
    *   Tap the **"📺 Bildschirm An/Aus"** button to toggle the live screen view.

## ⚠️ Security Note

This tool exposes a control server on your local network.
*   **ONLY** use this in trusted networks (Home Wi-Fi).
*   **NEVER** use this in public networks (Universities, Cafés, Airports) without extra security layers (VPN/Tunnel).

## 📝 License

Feel free to use and modify for your personal projects!
