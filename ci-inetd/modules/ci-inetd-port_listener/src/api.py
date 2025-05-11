import os
import random
import time
import json
import threading
import multiprocessing

from uuid import uuid4
from flask import Flask, jsonify, abort
import requests
from werkzeug.exceptions import HTTPException


_requests_queue: multiprocessing.Queue = None
_response_queue: multiprocessing.Queue = None
CONFIG = None

HOST = '0.0.0.0'
PORT: int = int(os.getenv("MODULE_PORT"))
MODULE_NAME: str = os.getenv("MODULE_NAME")
MAX_WAIT_TIME: int = 30
app = Flask(__name__)

def send_config_request():
    details = {
        "operation": "get_config_from_file",
        "deliver_to": "ci-inetd-config_parser",
        "source": MODULE_NAME,
        "id": str(uuid4())
    }
    
    details_log = details.copy()
    send_to_logs(details_log)
    
    try:
        _requests_queue.put(details)
        print(f"{MODULE_NAME} sent config request: {details}")
    except Exception as e:
        print(f"Error sending config request: {e}")
        
def load_config(data):
    global CONFIG
    
    if data:
        try:
            CONFIG = json.loads(data)
            print("Config loaded successfully")
        except json.JSONDecodeError:
            print("Error parsing config JSON")
            CONFIG = None
    else:
        print("Failed to load config")
        
def send_to_forwarder(details):
    if not details:
        abort(400)

    details["deliver_to"] = "ci-inetd-request_forwarder"
    details["source"] = MODULE_NAME
    details["id"] = uuid4().__str__()

    details_log = details.copy()
    send_to_logs(details_log)
    
    try:
        _requests_queue.put(details)
        print(f"{MODULE_NAME} update event: {details}")
    except Exception as e:
        print("[COM-MOBILE_DEBUG] malformed request", e)
        abort(400)
        
def send_to_logs(details):
    new_details = {}
    new_details["data"] = details
    new_details["deliver_to"] = "ci-inetd-log_receiver"
    new_details["source"] = MODULE_NAME
    new_details["operation"] = "log"
    new_details["id"] = uuid4().__str__()

    try:
        _requests_queue.put(new_details)
        print(f"{MODULE_NAME} update event: {new_details}")
    except Exception as e:
        print("[COM-MOBILE_DEBUG] malformed request", e)
        abort(400)
        
def wait_response():
    start_time = time.time()
    while 1:
        if time.time() - start_time > MAX_WAIT_TIME:
            break

        try:
            response = _response_queue.get(timeout=MAX_WAIT_TIME)
        except Exception as e:
            print("timeout...", e)
            continue
        
        # if not isinstance(response, dict):
        #     print("not a dict...")
        #     continue

        data = response.get('data')
        if not data:
            print("something strange...")
            continue

        print("response", response)
        return data

    print("OUT OF TIME...")

    return None

@app.route('/ci-inetd/start/<int:port>', methods=['POST'])
def start_process(port):
    details_to_send = {
        "operation": "port_request",
        "data": {
            "port": port
        }
    }
    
    details_log = details_to_send.copy()
    send_to_logs(details_log)
    
    if not CONFIG:
        return jsonify({"error": "Config not loaded"}), 500
    
    services = CONFIG.get('services', {})
    port_exists = any(service.get('port') == port for service in services.values())
    
    if not port_exists:
        return jsonify({"error": f"Port {port} not found in config"}), 404
    
    send_to_forwarder(details_to_send)
    # data = wait_response()
    # return jsonify(data)
    return {}

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    return jsonify({
        "status": e.code,
        "name": e.name,
    }), e.code

    
def start_web(requests_queue, response_queue):
    global _requests_queue
    global _response_queue

    _requests_queue = requests_queue
    _response_queue = response_queue

    # send_config_request()
    
    threading.Thread(target=lambda: app.run(
        host=HOST, port=PORT, debug=True, use_reloader=False
    )).start()
