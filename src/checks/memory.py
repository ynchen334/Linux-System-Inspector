import psutil

def check_memory():
    memory_info = psutil.virtual_memory()

    if memory_info.percent < 80:
        status = "OK"
        memory_message = "Memory usage is normal"
    elif memory_info.percent < 95:
        status = "WARNING"
        memory_message = "Memory usage is high"
    else:
        status = "CRITICAL"
        memory_message = "Memory usage is critically high"

    result = {
        "name": "Memory",
        "status": status,
        "value": memory_info.percent,
        "message": memory_message
    }

    return result
    

if __name__ =="__main__":
    print(check_memory())

