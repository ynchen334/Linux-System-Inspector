import unittest
import logging
from unittest.mock import patch, Mock
from collections import Counter
from main import (
    parse_arguments,
    print_result,
    run_check,
    get_exit_code,
)


class TestParseArguments(unittest.TestCase):

    def test_default_arguments(self):
        with patch("sys.argv", ["main.py"]):
            selected_checks, log_level = parse_arguments()

        self.assertEqual(
            [func.__name__ for func in selected_checks],
            ["check_cpu", "check_memory", "check_disk"]
        )
        self.assertEqual(log_level, logging.INFO)

    def test_select_cpu(self):
        with patch("sys.argv", ["main.py", "--check", "cpu"]):
            selected_checks, _ = parse_arguments()

        self.assertEqual(
            [func.__name__ for func in selected_checks],
            ["check_cpu"]
        )

    def test_log_level_case_insensitive(self):
        with patch("sys.argv", ["main.py", "--log-level", "debug"]):
            _, log_level = parse_arguments()

        self.assertEqual(log_level, logging.DEBUG)


class TestPrintResult(unittest.TestCase):

    def test_print_result(self):
        result = {
            "name": "CPU",
            "status": "OK",
            "value": 30.0,
            "message": "CPU usage is normal",
        }

        with patch("builtins.print") as mock_print:
            print_result(result)

        output = "\n".join(
            str(call.args[0]) for call in mock_print.call_args_list
        )

        self.assertIn("CPU: OK", output)
        self.assertIn("CPU Usage: 30.0%", output)
        self.assertIn("CPU usage is normal", output)

    def test_print_result_without_value(self):
        result = {
            "name": "CPU",
            "status": "CRITICAL",
            "value": None,
            "message": "check failed",
        }

        with patch("builtins.print") as mock_print:
            print_result(result)

        output = "\n".join(
            str(call.args[0]) for call in mock_print.call_args_list
        )

        self.assertIn("CPU Usage: N/A", output)


class TestRunCheck(unittest.TestCase):

    def setUp(self):
        self.logger = Mock()

    def test_run_check_success(self):
        fake_result = {
            "name": "CPU",
            "status": "OK",
            "value": 30.0,
            "message": "CPU usage is normal",
        }

        def fake_check():
            return fake_result

        result = run_check(fake_check, self.logger)

        self.assertEqual(result["status"], "OK")
        self.assertEqual(result["value"], 30.0)
        self.logger.info.assert_called()

    def test_run_check_exception(self):
        def fake_check():
            raise RuntimeError("test error")

        result = run_check(fake_check, self.logger)

        self.assertEqual(result["status"], "CRITICAL")
        self.assertIsNone(result["value"])
        self.assertIn("test error", result["message"])
        self.logger.exception.assert_called_once()


class TestGetExitCode(unittest.TestCase):

    def test_all_ok(self):
        self.assertEqual(get_exit_code(Counter({"OK": 3})), 0)

    def test_has_warning(self):
        self.assertEqual(
            get_exit_code(Counter({"OK": 2, "WARNING": 1})),
            1
        )

    def test_has_critical(self):
        self.assertEqual(
            get_exit_code(
                Counter({"OK": 1, "WARNING": 1, "CRITICAL": 1})
            ),
            2
        )

    def test_empty_counts(self):
        self.assertEqual(get_exit_code(Counter()), 0)



class TestMain(unittest.TestCase):

    def test_main_all_ok(self):
        from main import main

        cpu_result = {
            "name": "CPU",
            "status": "OK",
            "value": 30.0,
            "message": "CPU usage is normal",
        }
        memory_result = {
            "name": "Memory",
            "status": "OK",
            "value": 40.0,
            "message": "Memory usage is normal",
        }
        disk_result = {
            "name": "Disk",
            "status": "OK",
            "value": 50.0,
            "message": "Disk usage is normal",
        }

        with patch(
            "main.parse_arguments",
            return_value=(
                [
                    lambda: cpu_result,
                    lambda: memory_result,
                    lambda: disk_result,
                ],
                logging.INFO,
            ),
        ), patch("main.setup_logger") as mock_setup_logger, \
             patch("main.print_result") as mock_print_result, \
             patch("builtins.print") as mock_print:

            mock_logger = Mock()
            mock_setup_logger.return_value = mock_logger

            exit_code = main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(mock_print_result.call_count, 3)
        mock_setup_logger.assert_called_once_with(logging.INFO)

        output = "\n".join(
            str(call.args[0]) for call in mock_print.call_args_list
            if call.args
        )
        self.assertIn("OK: 3", output)
        self.assertIn("WARNING: 0", output)
        self.assertIn("CRITICAL: 0", output)

    def test_main_with_warning(self):
        from main import main

        warning_result = {
            "name": "CPU",
            "status": "WARNING",
            "value": 85.0,
            "message": "CPU usage is high",
        }

        with patch(
            "main.parse_arguments",
            return_value=([lambda: warning_result], logging.INFO),
        ), patch("main.setup_logger", return_value=Mock()), \
             patch("main.print_result"), \
             patch("builtins.print"):

            exit_code = main()

        self.assertEqual(exit_code, 1)

    def test_main_with_critical(self):
        from main import main

        critical_result = {
            "name": "Disk",
            "status": "CRITICAL",
            "value": 97.0,
            "message": "Disk usage is critically high",
        }

        with patch(
            "main.parse_arguments",
            return_value=([lambda: critical_result], logging.INFO),
        ), patch("main.setup_logger", return_value=Mock()), \
             patch("main.print_result"), \
             patch("builtins.print"):

            exit_code = main()

        self.assertEqual(exit_code, 2)


if __name__ == "__main__":
    unittest.main()