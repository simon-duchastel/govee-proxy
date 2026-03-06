from flask import Flask, request, jsonify
import socket
import json

app = Flask(__name__)

# --- HARDCODED SETTINGS ---
GOVEE_IP = "192.168.1.87"
GOVEE_UDP_PORT = 4003
# --------------------------

def send_udp(payload):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    sock.sendto(bytes(json.dumps(payload), "utf-8"), (GOVEE_IP, GOVEE_UDP_PORT))
    try:
        data, _ = sock.recvfrom(1024)
        return json.loads(data.decode())
    except socket.timeout:
        return None
    finally:
        sock.close()

@app.route('/toggle', methods=['POST'])
def toggle_govee():
    # 1. Ask the device for its current status
    status_query = {"msg": {"cmd": "devStatus", "data": {}}}
    response = send_udp(status_query)
    
    if not response:
        return jsonify({"error": "Device not responding"}), 500

    # 2. Check if it's currently ON (1) or OFF (0)
    current_state = response['msg']['data']['onOff']
    new_state = 0 if current_state == 1 else 1
    
    # 3. Send the toggle command
    toggle_cmd = {"msg": {"cmd": "turn", "data": {"value": new_state}}}
    send_udp(toggle_cmd)
    
    state_text = "OFF" if new_state == 0 else "ON"
    return jsonify({"status": "Success", "switched_to": state_text}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
