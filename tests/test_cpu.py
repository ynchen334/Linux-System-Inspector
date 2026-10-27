import unittest
from unittest.mock import patch
from src.checks.cpu import check_cpu

class TestCheckCPU(unittest.TestCase):

    def test_cpu_normal(self):
        with patch("src.checks.cpu.psutil.cpu_percent", return_value=30.0):
            result = check_cpu()
        self.assertEqual(result["status"], "OK")

    def test_cpu_warning(self):
        with patch("src.checks.cpu.psutil.cpu_percent", return_value=90):
            result = check_cpu()
        self.assertEqual(result["status"], "WARNING")

    def test_cpu_critical(self):
        with patch("src.checks.cpu.psutil.cpu_percent", return_value=99):
            result = check_cpu()
        self.assertEqual(result["status"], "CRITICAL")
        

if __name__ == "__main__":
    unittest.main()