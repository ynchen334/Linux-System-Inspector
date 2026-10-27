# Linux System Inspector

A lightweight Linux system inspection tool written in Python. It checks CPU, memory, and disk usage, records logs, and reports system health status.

## Features

- **CPU Monitoring**: Check CPU usage.
- **Memory Monitoring**: Check memory usage.
- **Disk Monitoring**: Check disk usage.
- **Status Classification**: Report `OK`, `WARNING`, or `CRITICAL`.
- **Logging**: Record inspection results and errors.
- **Command-Line Options**: Select checks and configure log levels.
- **Unit Tests**: Test individual checkers and application logic.

## Requirements

- Python 3
- Linux
- psutil

## Installation

Clone the repository:

```bash
git clone https://github.com/ynchen334/linux-system-inspector.git
cd linux-system-inspector
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install psutil
```

## Usage

Run all checks:

```bash
python3 main.py
```

Check CPU only:

```bash
python3 main.py --check cpu
```

Check memory and disk:

```bash
python3 main.py --check memory disk
```

Set the log level:

```bash
python3 main.py --log-level DEBUG
```

## Status Levels

| Status | Meaning |
|---|---|
| `OK` | Resource usage is normal |
| `WARNING` | Resource usage is high |
| `CRITICAL` | Resource usage is critically high or a check failed |

The program returns different exit codes:

- `0`: All checks passed without warnings or critical issues.
- `1`: At least one warning occurred.
- `2`: At least one critical issue occurred.

## Running Tests

```bash
python3 -m unittest discover -s tests -v
```

## Project Structure

```text
linux-system-inspector/
├── main.py
├── src/
│   ├── checks/
│   │   ├── cpu.py
│   │   ├── memory.py
│   │   └── disk.py
│   └── utils/
│       └── logger.py
└── tests/
    ├── test_cpu.py
    ├── test_memory.py
    ├── test_disk.py
    └── test_main.py
```

## Learning Goals

This project is part of my learning journey in Python, Linux system administration, testing, and cloud-native technologies.

## Future Improvements

- Add more system health checks.
- Improve test coverage.
- Containerize the application with Docker.
- Explore integration with monitoring tools.

## License

This project is for learning and educational purposes.
