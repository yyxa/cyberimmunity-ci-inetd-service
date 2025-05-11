import os
import random
import time
import json
import threading
import multiprocessing

from uuid import uuid4
from flask import Flask, jsonify, abort, request
import requests
from werkzeug.exceptions import HTTPException

PROCESSES = {}
PID_COUNTER = 1000
HOST = '0.0.0.0'
PORT: int = int(os.getenv("MODULE_PORT"))
MODULE_NAME: str = os.getenv("MODULE_NAME")
MAX_WAIT_TIME: int = 30
app = Flask(__name__)
        
def generate_pid():
    global PID_COUNTER
    PID_COUNTER += 1
    return PID_COUNTER

@app.route('/daemons/processes', methods=['GET'])
def list_processes():
    return jsonify({
        'processes': PROCESSES,
        'count': len(PROCESSES)
    })

@app.route('/daemons/process/pid/<int:pid>', methods=['GET'])
def get_process_status(pid):
    if pid not in PROCESSES:
        return jsonify({"error": "Process not found"}), 404
    return jsonify(PROCESSES[pid])

@app.route('/daemons/process/port/<int:port>', methods=['GET'])
def get_process_by_port(port):
    process = next((p for p in PROCESSES.values() if p['port'] == port), None)
    
    if not process:
        return jsonify({"error": f"Process with port {port} not found"}), 404
    
    return jsonify(process)

@app.route('/daemons/start', methods=['POST'])
def start_process():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    
    required = ['port', 'user', 'program_path']
    if any(field not in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400
    
    if any(p['port'] == data['port'] for p in PROCESSES.values()):
        return jsonify({"error": f"Port {data['port']} already in use"}), 400
    
    pid = generate_pid()
    
    PROCESSES[pid] = {
        **data,
        'pid': pid,
        'start_time': time.time(),
        'status': 'running'
    }
    
    return jsonify({
        "message": "Process started",
        "pid": pid,
        "details": data
    }), 201

@app.route('/daemons/stop/<int:pid>', methods=['POST'])
def stop_process(pid):
    if pid not in PROCESSES:
        return jsonify({"error": "Process not found"}), 404
    
    removed = PROCESSES.pop(pid)
    return jsonify({
        "message": "Process stopped",
        "pid": pid,
        "details": removed
    })

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    return jsonify({
        "status": e.code,
        "name": e.name,
    }), e.code

    
def start_web():
    threading.Thread(target=lambda: app.run(
        host=HOST, port=PORT, debug=True, use_reloader=False
    )).start()
