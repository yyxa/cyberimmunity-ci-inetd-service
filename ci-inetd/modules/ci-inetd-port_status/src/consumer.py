import os
import json
import threading
import requests
from uuid import uuid4
import uuid
from confluent_kafka import Consumer, OFFSET_BEGINNING

from .producer import proceed_to_deliver
import time

DAEMONS_SERVICE_URL = f"http://daemons-service:8002"

MODULE_NAME: str = os.getenv("MODULE_NAME")
PORTS = {}

def send_to_status_manager(details):
    details["operation"] = "ports_status"
    details["deliver_to"] = "ci-inetd-status_manager"
    details["id"] = uuid4().__str__()
    
    details_log = details.copy()
    send_log(details_log)
    proceed_to_deliver(details)

def send_log(details):
    new_details = {}
    new_details["data"] = details
    new_details["deliver_to"] = "ci-inetd-log_receiver"
    new_details["operation"] = "log"
    new_details["id"] = uuid4().__str__()
        
    proceed_to_deliver(new_details)
    
def add_new_port(details):
    port = details["data"]["port"]
    if port not in PORTS:
        PORTS[port] = {
            "port": port,
            "status": "unknown",
            "last_checked": None
        }
        print(f"Added new port {port} to monitoring")
    else:
        print(f"Port {port} already exists in monitoring")

def check_ports():
    results = {}
    
    for port in list(PORTS.keys()):
        try:
            response = requests.get(
                f"{DAEMONS_SERVICE_URL}/daemons/process/port/{port}",
                timeout=3
            )
            
            if response.status_code == 200:
                status_data = response.json()
                PORTS[port] = status_data
                results[port] = {
                    "status": status_data.get("status", "unknown"),
                    "service": status_data
                }
            else:
                results[port] = {
                    "status": "not_found",
                    "error": response.json().get("error", "Unknown error")
                }

        except requests.exceptions.RequestException as e:
            results[port] = {
                "status": "unreachable",
                "error": str(e)
            }
            PORTS[port]["status"] = "unreachable"
        
        PORTS[port]["last_checked"] = time.time()
    
    details = {}
    details["data"] = results
    
    send_to_status_manager(details)

def periodic_check():
    while True:
        time.sleep(60)
        check_ports()
        
def handle_event(id, details_str):
    details = json.loads(details_str)

    source: str = details.get("source")
    deliver_to: str = details.get("deliver_to")
    data: str = details.get("data")
    operation: str = details.get("operation")

    print(f"[info] handling event {id}, "
          f"{source}->{deliver_to}: {operation}")

    if operation == "new_port":
        details_log = details.copy()
        details_port = details.copy()
        send_log(details_log)
        add_new_port(details_port)
    
    return


def consumer_job(args, config):
    consumer = Consumer(config)

    def reset_offset(verifier_consumer, partitions):
        if not args.reset:
            return

        for p in partitions:
            p.offset = OFFSET_BEGINNING
        verifier_consumer.assign(partitions)

    topic = MODULE_NAME
    consumer.subscribe([topic], on_assign=reset_offset)

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                pass
            elif msg.error():
                print(f"[error] {msg.error()}")
            else:
                try:
                    id = msg.key().decode('utf-8')
                    details_str = msg.value().decode('utf-8')
                    handle_event(id, details_str)
                except Exception as e:
                    print(f"[error] Malformed event received from " \
                          f"topic {topic}: {msg.value()}. {e}")
    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()

def start_consumer(args, config):
    print(f'{MODULE_NAME}_consumer started')
    threading.Thread(target=lambda: consumer_job(args, config)).start()
    threading.Thread(target=periodic_check, daemon=True).start()