# Политики безопасности
policies = (
    # dst daemons
    {"src": "ci-inetd-executor", "dst": "daemons"},
    {"src": "ci-inetd-id_status", "dst": "daemons"},
    {"src": "ci-inetd-port_status", "dst": "daemons"},
    {"src": "ci-inetd-critical_executor", "dst": "daemons"},
    {"src": "ci-inetd-terminator", "dst": "daemons"},
    
    # dst ci-inetd-port_listener
    {"src": "ci-inetd-config_parser", "dst": "ci-inetd-port_listener"}, # , "cmd": "config_from_file"

    # dst ci-inetd-request_forwarder
    {"src": "ci-inetd-port_listener", "dst": "ci-inetd-request_forwarder"},
    
    # dst ci-inetd-config_parser
    {"src": "ci-inetd-port_listener", "dst": "ci-inetd-config_parser"}, # , "cmd": "get_config_from_file"
    {"src": "ci-inetd-request_verifier", "dst": "ci-inetd-config_parser"}, # , "cmd": "get_config_from_file"
    {"src": "ci-inetd-log_analyzer", "dst": "ci-inetd-config_parser"}, # , "cmd": "get_config_from_file"
    {"src": "ci-inetd-status_manager", "dst": "ci-inetd-config_parser"}, # , "cmd": "get_config_from_file"
    
    # dst ci-inetd-request_verifier
    {"src": "ci-inetd-request_forwarder", "dst": "ci-inetd-request_verifier"},
    {"src": "ci-inetd-config_parser", "dst": "ci-inetd-request_verifier"},
    
    # dst ci-inetd-log_analyzer
    {"src": "ci-inetd-config_parser", "dst": "ci-inetd-log_analyzer"},
    {"src": "ci-inetd-log_forwarder", "dst": "ci-inetd-log_analyzer"},

    # dst ci-inetd-permission_executor
    {"src": "ci-inetd-request_verifier", "dst": "ci-inetd-permission_executor"},
    {"src": "ci-inetd-action_manager", "dst": "ci-inetd-permission_executor"},
    {"src": "ci-inetd-status_manager", "dst": "ci-inetd-permission_executor"},
    
    # dst ci-inetd-permission_executor
    {"src": "ci-inetd-request_verifier", "dst": "ci-inetd-permission_executor"},
    {"src": "ci-inetd-action_manager", "dst": "ci-inetd-permission_executor"},
    {"src": "ci-inetd-status_manager", "dst": "ci-inetd-permission_executor"},
    
    # dst ci-inetd-executor
    {"src": "ci-inetd-permission_executor", "dst": "ci-inetd-executor"},
    
    # dst ci-inetd-executor_entity_sender
    {"src": "ci-inetd-executor", "dst": "ci-inetd-executor_entity_sender"},
    
    # dst ci-inetd-action_manager
    {"src": "ci-inetd-config_parser", "dst": "ci-inetd-action_manager"},
    
    # dst ci-inetd-status_manager
    {"src": "ci-inetd-config_parser", "dst": "ci-inetd-status_manager"},
    {"src": "ci-inetd-id_status", "dst": "ci-inetd-status_manager"},
    {"src": "ci-inetd-port_status", "dst": "ci-inetd-status_manager"},
    
    # dst ci-inetd-id_status
    {"src": "ci-inetd-executor_entity_sender", "dst": "ci-inetd-id_status"},
    {"src": "ci-inetd-critical_entity_sender", "dst": "ci-inetd-id_status"},

    # dst ci-inetd-port_status
    {"src": "ci-inetd-request_forwarder", "dst": "ci-inetd-port_status"},
    
    # dst ci-inetd-critical_entity_sender
    {"src": "ci-inetd-critical_executor", "dst": "ci-inetd-critical_entity_sender"},
    
    # dst ci-inetd-critical_executor
    {"src": "ci-inetd-action_manager", "dst": "ci-inetd-critical_executor"},
    
    # dst ci-inetd-permission_terminator
    {"src": "ci-inetd-action_manager", "dst": "ci-inetd-permission_terminator"},
    {"src": "ci-inetd-status_manager", "dst": "ci-inetd-permission_terminator"},
    
    # dst ci-inetd-terminator
    {"src": "ci-inetd-permission_terminator", "dst": "ci-inetd-terminator"},
    
    # dst ci-inetd-log_receiver
    {"src": "ci-inetd-port_listener", "dst": "ci-inetd-log_receiver"},
    {"src": "ci-inetd-request_verifier", "dst": "ci-inetd-log_receiver"},
    {"src": "ci-inetd-executor", "dst": "ci-inetd-log_receiver"},
    {"src": "ci-inetd-action_manager", "dst": "ci-inetd-log_receiver"},
    {"src": "ci-inetd-status_manager", "dst": "ci-inetd-log_receiver"},
    {"src": "ci-inetd-id_status", "dst": "ci-inetd-log_receiver"},
    {"src": "ci-inetd-port_status", "dst": "ci-inetd-log_receiver"},
    {"src": "ci-inetd-critical_executor", "dst": "ci-inetd-log_receiver"},
    {"src": "ci-inetd-terminator", "dst": "ci-inetd-log_receiver"},
    
    # dst ci-inetd-log_forwarder
    {"src": "ci-inetd-log_receiver", "dst": "ci-inetd-log_receiver"},

    # dst ci-inted-log_storage
    {"src": "ci-inetd-log_receiver", "dst": "ci-inted-log_storage"},
    
)
    
def check_operation(id, details) -> bool:
    src: str = details.get("source")
    dst: str = details.get("deliver_to")
    # cmd: str = details.get("operation")

    if not all((src, dst)):
        return False

    print(f"[info] checking policies for event {id}, {src}->{dst}")

    return {"src": src, "dst": dst} in policies
