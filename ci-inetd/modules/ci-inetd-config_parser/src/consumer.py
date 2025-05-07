import os
import json
import threading

from uuid import uuid4
import uuid
from confluent_kafka import Consumer, OFFSET_BEGINNING

from .producer import proceed_to_deliver


MODULE_NAME: str = os.getenv("MODULE_NAME")

def parse_conf_to_json(conf_file_path):
    config = {"services": {}, "logging": {}}
    section = None

    with open(conf_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith(';'):
                continue

            if line.startswith('['):
                section = line[1:-1].lower()
                continue

            if section == "services":
                parts = line.split(maxsplit=4)
                if len(parts) >= 4:
                    service, port, user, program_path, *args = parts
                    args = args[0] if args else ""
                    config["services"][service] = {
                        "port": int(port),
                        "user": user,
                        "program_path": program_path,
                        "arguments": args
                    }

            elif section == "logging" and "=" in line:
                key, value = map(str.strip, line.split("=", 1))
                config["logging"][key] = value

    return json.dumps(config, indent=2)

def prepare_config(details):
    conf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../default.conf'))
    if not os.path.exists(conf_path):
        raise FileNotFoundError(f"Config file not found at: {conf_path}")
    
    details["data"] = parse_conf_to_json(conf_path)
    return details

def send_to_port_listener(details):
    details["operation"] = "config_from_file"
    details["deliver_to"] = "ci-inetd-port_listener"
    details["id"] = uuid4().__str__()
    
    proceed_to_deliver(details)

def send_to_request_verifier(details):
    details["operation"] = "config_from_file"
    details["deliver_to"] = "ci-inetd-request_verifier"
    details["id"] = uuid4().__str__()
    
    proceed_to_deliver(details)
    
def send_to_log_analyzer(details):
    details["operation"] = "config_from_file"
    details["deliver_to"] = "ci-inetd-log_analyzer"
    details["id"] = uuid4().__str__()
    
    proceed_to_deliver(details)
    
def send_to_status_manager(details):
    details["operation"] = "config_from_file"
    details["deliver_to"] = "ci-inetd-status_manager"
    details["id"] = uuid4().__str__()
    
    proceed_to_deliver(details)

def init_log():
    details = prepare_config({})
    
    send_to_log_analyzer(details)
    send_to_port_listener(details)
    send_to_request_verifier(details)
    send_to_status_manager(details)
    
def handle_event(id, details_str):
    details = json.loads(details_str)

    source: str = details.get("source")
    deliver_to: str = details.get("deliver_to")
    data: str = details.get("data")
    operation: str = details.get("operation")

    print(f"[info] handling event {id}, "
          f"{source}->{deliver_to}: {operation}")
    
    return

def consumer_job(args, config):
    init_log()
    
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