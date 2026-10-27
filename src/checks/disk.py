import psutil

def check_disk():
    disk_info = psutil.disk_usage('/')

    if disk_info.percent < 80:
        status = "OK"
        disk_message = "Disk usage is normal"
    elif disk_info.percent < 95:
        status = "WARNING"
        disk_message = "Disk usage is high"
    else:
        status = "CRITICAL"
        disk_message = "Disk usage is critically high"

    result = {
        "name": "Disk",
        "status": status,
        "value": disk_info.percent,
        "message": disk_message
    }

    return result
    

if __name__ =="__main__":
    print(check_disk())
