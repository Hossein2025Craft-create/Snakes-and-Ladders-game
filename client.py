import websocket
import threading
import json

room_id = input("Room ID: ")
player_name = input("Player Name: ")

SERVER = f"ws://127.0.0.1:8000/ws/{room_id}"  # ✅ اصلاح شد

def on_message(ws, message):
    print("\n[SERVER]:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Disconnected")

def on_open(ws):
    print("Connected!")

    def send_loop():
        while True:
            text = input("> ")
            ws.send(text)

    threading.Thread(target=send_loop, daemon=True).start()

ws = websocket.WebSocketApp(
    SERVER,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()