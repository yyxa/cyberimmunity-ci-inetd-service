import os
import json
import threading
import requests
from flask import jsonify
from uuid import uuid4
import uuid
from confluent_kafka import Consumer, OFFSET_BEGINNING

from .producer import proceed_to_deliver


MODULE_NAME: str = os.getenv("MODULE_NAME")

def run_process(details):
    try:
        service_data = details.get("data", {}).get("run", {})
        if not service_data:
            print("No service data provided in details")
            return

        api_url = f"http://{os.getenv('DEMON_HOST', 'ci-inetd-port_listener')}:{os.getenv('DEMON_PORT', '8003')}/daemons/start"

        response = requests.post(
            api_url,
            json=service_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        if response.status_code == 201:
            result = response.json()
            print(f"Successfully started process: {result}")
            
            details["process_info"] = result
            send_to_executor_entity_sender(details)

        send_log(details)
        return

    except Exception as e:
        error_msg = f"Error in run_process: {str(e)}"
        print(error_msg)
        details["error"] = error_msg
        send_log(details)
        return

def send_log(details):
    new_details = {}
    new_details["data"] = details
    new_details["deliver_to"] = "ci-inetd-log_receiver"
    new_details["operation"] = "log"
    new_details["id"] = uuid4().__str__()
    
    proceed_to_deliver(details)

def send_to_executor_entity_sender(details):
    details["operation"] = "process_info"
    details["deliver_to"] = "ci-inetd-executor_entity_sender"
    details["id"] = uuid4().__str__()
    
    send_log(details)
    proceed_to_deliver(details)
    
def handle_event(id, details_str):
    """ Обработчик входящих в модуль задач. """
    details = json.loads(details_str)

    source: str = details.get("source")
    deliver_to: str = details.get("deliver_to")
    data: str = details.get("data")
    operation: str = details.get("operation")

    print(f"[info] handling event {id}, "
          f"{source}->{deliver_to}: {operation}")

    if operation == "start_app":
        send_log(details)
        run_process(details)
    
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