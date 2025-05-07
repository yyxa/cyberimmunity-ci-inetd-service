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

PROCESSES = {}
HOST = '0.0.0.0'
PORT: int = int(os.getenv("MODULE_PORT"))
MODULE_NAME: str = os.getenv("MODULE_NAME")
MAX_WAIT_TIME: int = 30
app = Flask(__name__)
        
@app.route('/daemons/processes', methods=['GET'])
def list_processes():
    """Возвращает список всех активных процессов"""
    return jsonify({
        'processes': PROCESSES,
        'count': len(PROCESSES)
    })

@app.route('/daemons/process/<string:process_id>', methods=['GET'])
def get_process_status(process_id):
    """Проверяет статус процесса по ID"""
    if process_id not in PROCESSES:
        return jsonify({"error": "Process not found"}), 404
    
    return jsonify(PROCESSES[process_id])

@app.route('/daemons/start', methods=['POST'])
def start_process():
    """Запуск процесса"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    service_data = request.get_json()
    process_id = str(uuid4())
    
    required_fields = ['port', 'user', 'program_path']
    for field in required_fields:
        if field not in service_data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    for pid, proc in PROCESSES.items():
        if proc['port'] == service_data['port']:
            return jsonify({
                "error": f"Port {service_data['port']} already in use",
                "process_id": pid
            }), 400
    
    PROCESSES[process_id] = {
        **service_data,
        'id': process_id,
        'start_time': time.time(),
        'status': 'running'
    }
    
    return jsonify({
        "message": "Process registered",
        "process_id": process_id,
        "service": service_data
    }), 201

@app.route('/daemons/stop/<string:process_id>', methods=['POST'])
def stop_process(process_id):
    """Убивает процесс"""
    if process_id not in PROCESSES:
        return jsonify({"error": "Process not found"}), 404
    
    removed_process = PROCESSES.pop(process_id)
    return jsonify({
        "message": "Process removed",
        "process_id": process_id,
        "service": removed_process
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
