import psutil

def check_cpu():
    cpu_usage = psutil.cpu_percent(interval=1)

    if cpu_usage < 80:
        cpu_status = "OK"
        cpu_message = "CPU usage is normal"
    elif cpu_usage < 95:
        cpu_status = "WARNING"
        cpu_message = "CPU usage is high"
    else:
        cpu_status = "CRITICAL"
        cpu_message = "CPU usage is critically high"

    result = {
        "name": "CPU",
        "status": cpu_status,
        "value": cpu_usage,
        "message": cpu_message
    }

    return result

if __name__ =="__main__":
    print(check_cpu())

