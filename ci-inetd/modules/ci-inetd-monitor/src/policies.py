# Политики безопасности
policies = (
    # dst daemons
    {"src": "ci-inetd-Executor", "dst": "daemons"},
    {"src": "ci-inetd-IdStatus", "dst": "daemons"},
    {"src": "ci-inetd-PortStatus", "dst": "daemons"},
    {"src": "ci-inetd-CriticalExecutor", "dst": "daemons"},
    {"src": "ci-inetd-Terminator", "dst": "daemons"},
    
    # dst ci-inetd-PortListener
    {"src": "user", "dst": "ci-inetd-PortListener"},
    {"src": "ci-inetd-ConfigParser", "dst": "ci-inetd-PortListener"},

    # dst ci-inetd-RequestForwarder
    {"src": "ci-inetd-PortListener", "dst": "ci-inetd-RequestForwarder"},

    # dst ci-inetd-ConfigFile
    {"src": "ci-inetd-ConfigParser", "dst": "ci-inetd-ConfigFile"}, # , "cmd": "config_from_file"
    
    # dst ci-inetd-ConfigParser
    {"src": "ci-inetd-ConfigFile", "dst": "ci-inetd-ConfigParser"}, # , "cmd": "get_config_from_file"
    {"src": "ci-inetd-PortListener", "dst": "ci-inetd-ConfigParser"},
    {"src": "ci-inetd-RequestVerifier", "dst": "ci-inetd-ConfigParser"},
    {"src": "ci-inetd-LogAnalyzer", "dst": "ci-inetd-ConfigParser"},
    {"src": "ci-inetd-StatusManager", "dst": "ci-inetd-ConfigParser"},
    
    # dst ci-inetd-RequestVerifier
    {"src": "ci-inetd-RequestForwarder", "dst": "ci-inetd-RequestVerifier"},
    {"src": "ci-inetd-ConfigParser", "dst": "ci-inetd-RequestVerifier"},
    
    # dst ci-inetd-LogAnalyzer
    {"src": "ci-inetd-ConfigParser", "dst": "ci-inetd-LogAnalyzer"},
    {"src": "ci-inetd-LogForwarder", "dst": "ci-inetd-LogAnalyzer"},

    # dst ci-inetd-PermissionExecutor
    {"src": "ci-inetd-RequestVerifier", "dst": "ci-inetd-PermissionExecutor"},
    {"src": "ci-inetd-ActionManager", "dst": "ci-inetd-PermissionExecutor"},
    {"src": "ci-inetd-StatusManager", "dst": "ci-inetd-PermissionExecutor"},
    
    # dst ci-inetd-PermissionExecutor
    {"src": "ci-inetd-RequestVerifier", "dst": "ci-inetd-PermissionExecutor"},
    {"src": "ci-inetd-ActionManager", "dst": "ci-inetd-PermissionExecutor"},
    {"src": "ci-inetd-StatusManager", "dst": "ci-inetd-PermissionExecutor"},
    
    # dst ci-inetd-Executor
    {"src": "ci-inetd-PermissionExecutor", "dst": "ci-inetd-Executor"},
    
    # dst ci-inetd-ExecutorEntitySender
    {"src": "ci-inetd-Executor", "dst": "ci-inetd-ExecutorEntitySender"},
    
    # dst ci-inetd-ActionManager
    {"src": "ci-inetd-ConfigParser", "dst": "ci-inetd-ActionManager"},
    
    # dst ci-inetd-StatusManager
    {"src": "ci-inetd-ConfigParser", "dst": "ci-inetd-StatusManager"},
    {"src": "ci-inetd-IdStatus", "dst": "ci-inetd-StatusManager"},
    {"src": "ci-inetd-PortStatus", "dst": "ci-inetd-StatusManager"},
    
    # dst ci-inetd-IdStatus
    {"src": "ci-inetd-ExecutorEntitySender", "dst": "ci-inetd-IdStatus"},
    {"src": "ci-inetd-CriticalEntitySender", "dst": "ci-inetd-IdStatus"},

    # dst ci-inetd-PortStatus
    {"src": "ci-inetd-RequestForwarder", "dst": "ci-inetd-PortStatus"},
    
    # dst ci-inetd-CriticalEntitySender
    {"src": "ci-inetd-CriticalExecutor", "dst": "ci-inetd-CriticalEntitySender"},
    
    # dst ci-inetd-CriticalExecutor
    {"src": "ci-inetd-ActionManager", "dst": "ci-inetd-CriticalExecutor"},
    
    # dst ci-inetd-PermissionTerminator
    {"src": "ci-inetd-ActionManager", "dst": "ci-inetd-PermissionTerminator"},
    {"src": "ci-inetd-StatusManager", "dst": "ci-inetd-PermissionTerminator"},
    
    # dst ci-inetd-Terminator
    {"src": "ci-inetd-PermissionTerminator", "dst": "ci-inetd-Terminator"},
    
    # dst ci-inetd-LogReceiver
    {"src": "ci-inetd-PortListener", "dst": "ci-inetd-LogReceiver"},
    {"src": "ci-inetd-RequestVerifier", "dst": "ci-inetd-LogReceiver"},
    {"src": "ci-inetd-Executor", "dst": "ci-inetd-LogReceiver"},
    {"src": "ci-inetd-ActionManager", "dst": "ci-inetd-LogReceiver"},
    {"src": "ci-inetd-StatusManager", "dst": "ci-inetd-LogReceiver"},
    {"src": "ci-inetd-IdStatus", "dst": "ci-inetd-LogReceiver"},
    {"src": "ci-inetd-PortStatus", "dst": "ci-inetd-LogReceiver"},
    {"src": "ci-inetd-CriticalExecutor", "dst": "ci-inetd-LogReceiver"},
    {"src": "ci-inetd-Terminator", "dst": "ci-inetd-LogReceiver"},
    
    # dst ci-inetd-LogForwarder
    {"src": "ci-inetd-LogReceiver", "dst": "ci-inetd-LogReceiver"},

    # dst ci-inted-LogStorage
    {"src": "ci-inetd-LogReceiver", "dst": "ci-inted-LogStorage"},
    
)
    
def check_operation(id, details) -> bool:
    src: str = details.get("source")
    dst: str = details.get("deliver_to")
    # cmd: str = details.get("operation")

    if not all((src, dst)):
        return False

    print(f"[info] checking policies for event {id}, {src}->{dst}")

    return {"src": src, "dst": dst} in policies
