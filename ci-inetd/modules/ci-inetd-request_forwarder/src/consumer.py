import os
import json
import threading

from uuid import uuid4
import uuid
from confluent_kafka import Consumer, OFFSET_BEGINNING

from .producer import proceed_to_deliver


MODULE_NAME: str = os.getenv("MODULE_NAME")

def send_to_request_verifier(details):
    details["operation"] = "verify_request"
    details["deliver_to"] = "ci-inetd-request_verifier"
    details["id"] = uuid4().__str__()
    
    proceed_to_deliver(details)

def send_to_port_status(details):
    details["operation"] = "new_port"
    details["deliver_to"] = "ci-inetd-port_status"
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

    if operation == "port_request":
        port_details = details.copy()
        send_to_port_status(port_details)
        
        verify_details = details.copy()
        send_to_request_verifier(verify_details)

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