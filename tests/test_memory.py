import unittest
from unittest.mock import patch, Mock
from src.checks.memory import check_memory

class TestCheckMemory(unittest.TestCase):

    def test_memory_normal(self):
        fake_memory = Mock()
        fake_memory.percent = 30.0

        with patch("src.checks.memory.psutil.virtual_memory",
            return_value=fake_memory):
            result = check_memory()
        self.assertEqual(result["status"], "OK")
        self.assertEqual(result["value"], 30.0)

    def test_memory_warning(self):
        fake_memory = Mock()
        fake_memory.percent = 85.0

        with patch("src.checks.memory.psutil.virtual_memory",
            return_value=fake_memory):
            return check_memory()
        self.assertEqual(result["status"], "WARNING")
        self.assertEqual(result["value"], 85.0)

    def test_memory_critical(self):
            fake_memory = Mock()
            fake_memory.percent = 96.0
    
            with patch("src.checks.memory.psutil.virtual_memory",
                return_value=fake_memory):
                return check_memory()
            self.assertEqual(result["status"], "CRITICAL")
            self.assertEqual(result["value"], 96.0)
    


if __name__ == "__main__":
    unittest.main()
