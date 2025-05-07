import os
import json
import threading
from datetime import datetime
from uuid import uuid4
import uuid
from confluent_kafka import Consumer, OFFSET_BEGINNING

from .producer import proceed_to_deliver


MODULE_NAME: str = os.getenv("MODULE_NAME")


def write_to_log_storage(details):
    try:
        log_data = details.get("data")
        if not log_data:
            print("No data to log")
            return
        
        log_filename = "today.log"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "data": log_data
        }
        log_line = json.dumps(log_entry, ensure_ascii=False)
        
        with open(log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(log_line + "\n")
            
        print(f"Successfully logged to {log_filename}")
        
    except Exception as e:
        print(f"Error writing to log: {e}")

def send_to_log_forwarder(details):
    details["operation"] = "log_for_analyzing"
    details["deliver_to"] = "ci-inetd-log_forwarder"
    details["id"] = uuid4().__str__()
    proceed_to_deliver(details)


def handle_event(id, details_str):
    details = json.loads(details_str)

    source: str = details.get("source")
    deliver_to: str = details.get("deliver_to")
    data: str = details.get("data")
    operation: str = details.get("operation")

    print(f"[info] handling event {id}, "
          f"{source}->{deliver_to}: {operation}")

    if operation == "log":
        write_to_log_storage(details)
        send_to_log_forwarder(details)
    
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