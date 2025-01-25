import os
import json
import threading

from uuid import uuid4
import uuid
from confluent_kafka import Consumer, OFFSET_BEGINNING

from .producer import proceed_to_deliver


MODULE_NAME: str = os.getenv("MODULE_NAME")

def parse_conf_to_json(conf_file_path):
    config = {}
    section = None

    with open(conf_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            
            # Пропуск пустых строк и комментариев
            if not line or line.startswith(';'):
                continue

            # Определение секции
            section_match = re.match(r'\[(.+?)\]', line)
            if section_match:
                section = section_match.group(1)
                config[section] = {}
                continue

            # Парсинг параметров в секциях
            if section and '=' in line:
                key, value = map(str.strip, line.split('=', 1))
                config[section][key] = value

            # Парсинг сервисов в секции "services"
            elif section == 'services':
                parts = re.split(r'\s+', line, maxsplit=5)
                if len(parts) >= 5:
                    service, port, wait_flag, user, program_path, args = (
                        parts[0], parts[1], parts[2], parts[3], parts[4], parts[5] if len(parts) == 6 else ""
                    )
                    config[section][service] = {
                        'port': int(port),
                        'wait_flag': wait_flag,
                        'user': user,
                        'program_path': program_path,
                        'arguments': args
                    }

    return json.dumps(config, indent=4, ensure_ascii=False)

def prepare_config(details):
    conf_path = "../default.conf"
    details["data"] = parse_conf_to_json(conf_path)
    send_to_config_parser(details)

def send_to_config_parser(details):
    details["operation"] = "config_from_file"
    details["deliver_to"] = "ci-inetd-ConfigParser"
    proceed_to_deliver(str(uuid.uuid4()), details)

def handle_event(id, details_str):
    details = json.loads(details_str)

    source: str = details.get("source")
    deliver_to: str = details.get("deliver_to")
    data: str = details.get("data")
    operation: str = details.get("operation")

    print(f"[info] handling event {id}, "
          f"{source}->{deliver_to}: {operation}")

    if operation == "get_config_from_file":
        return prepare_config(details)

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