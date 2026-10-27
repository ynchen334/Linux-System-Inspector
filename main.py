from collections import Counter
import argparse
import logging
from src.checks.cpu import check_cpu
from src.checks.memory import check_memory
from src.checks.disk import check_disk
from src.utils.logger import setup_logger



def parse_arguments():
    parser = argparse.ArgumentParser(description="Check cpu, memory or disk (default:all)")
    parser.add_argument("--check", 
                        nargs="*", 
                        choices=["cpu", "memory", "disk"],
                        default=["cpu", "memory", "disk"]
                        )
    parser.add_argument("--log-level",
                        type = str.upper,
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        default="INFO"
                        )
    args = parser.parse_args()
    if not args.check:
        args.check = ["cpu", "memory", "disk"]
    
    checks = {
    "cpu": check_cpu,
    "memory": check_memory,
    "disk": check_disk,
    }
    selects = [checks[name] for name in args.check]

    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    log_level = level_map[args.log_level.upper()]
    return selects, log_level



def print_result(result):
    value = result.get('value')
    if value is None:
        value = 'N/A'

    print(f"{result.get('name')}: {result.get('status')}")
    if value ==  'N/A':
        print(f"{result.get('name')} Usage: {value}")
    else:
        print(f"{result.get('name')} Usage: {value}%")
    print(f"Message: {result.get('message')}")


def run_check(check_func, logger):
    try:
        logger.info("Checking %s", check_func.__name__)
        result = check_func()
        logger.info("Check result: name=%s, status=%s, value=%s",result.get("name"), result.get("status"), result.get("value"))
        return result
    
    except Exception as e:
        result = {
            "name": check_func.__name__,
            "status": "CRITICAL",
            "value": None,
            "message": f"check failed: {e}"
        }
        logger.exception("Check failed: %s", check_func.__name__)
        return result 


def get_exit_code(status_counts):
    has_critical = status_counts.get("CRITICAL", 0) > 0
    has_warning = status_counts.get("WARNING", 0) > 0
    
    if has_critical:
        return 2
    elif has_warning:
        return 1
    else:
        return 0


def main():
    print("===== Linux System Inspector =====\n")
    selected_checks, log_level = parse_arguments()
    logger = setup_logger(log_level)
    results = [run_check(selected_func, logger) for selected_func in selected_checks]

    for res in results:
        print_result(res)
        print()

    statuses = [res["status"] for res in results]
    status_counts = Counter(statuses)

    print("========== Summary ==========")
    print(f"OK: {status_counts.get('OK', 0)}")
    print(f"WARNING: {status_counts.get('WARNING', 0)}")
    print(f"CRITICAL: {status_counts.get('CRITICAL', 0)}")

    return get_exit_code(status_counts)


if __name__ == "__main__":
    import sys
    sys.exit(main())