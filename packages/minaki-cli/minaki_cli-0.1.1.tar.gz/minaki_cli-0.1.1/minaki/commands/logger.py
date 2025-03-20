import datetime

def log_command(command):
    """Log executed commands to a file."""
    log_file = "/tmp/minaki_command.log"
    with open(log_file, "a") as f:
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{timestamp} {command}\n")
