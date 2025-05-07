import os
import json
import threading

from uuid import uuid4
import uuid
from confluent_kafka import Consumer, OFFSET_BEGINNING

from .producer import proceed_to_deliver


MODULE_NAME: str = os.getenv("MODULE_NAME")
CONFIG = None

def send_log(details):
    new_details = {}
    new_details["data"] = details
    new_details["deliver_to"] = "ci-inetd-log_receiver"
    new_details["operation"] = "log"
    new_details["id"] = uuid4().__str__()
        
    proceed_to_deliver(new_details)

def send_to_permission_executor(details):
    details["operation"] = "start_app"
    details["deliver_to"] = "ci-inetd-permission_executor"
    details["id"] = uuid4().__str__()
    
    send_log(details)
    proceed_to_deliver(details)

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
    
def handle_event(id, details_str):
    """ Обработчик входящих в модуль задач. """
    details = json.loads(details_str)

    source: str = details.get("source")
    deliver_to: str = details.get("deliver_to")
    data: str = details.get("data")
    operation: str = details.get("operation")

    print(f"[info] handling event {id}, "
          f"{source}->{deliver_to}: {operation}")

    if operation == "config_from_file":
        send_log(details)
        load_config(data)
    elif operation == "verify_request":
        send_log(details)
        
        if not CONFIG:
            return
        
        services = CONFIG.get('services', {})
        # port_exists = any(service.get('port') == details["port"] for service in services.values())
        
        for service_name, service_config in services.items():
            if service_config.get('port') == details["port"]:
                
                details["data"]["run"] = services[service_name]
                send_to_permission_executor(details)
                break
        
        # if port_exists:
        #     send_to_permission_executor(details)

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