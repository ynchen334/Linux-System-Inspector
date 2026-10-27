
import unittest
from unittest.mock import patch, Mock
from src.checks.disk import check_disk


class TestCheckDisk(unittest.TestCase):

    def test_disk_normal(self):
        fake_disk = Mock()
        fake_disk.percent = 30.0

        with patch(
            "src.checks.disk.psutil.disk_usage", return_value=fake_disk
        ) as mock_disk_usage:
            result = check_disk()

        mock_disk_usage.assert_called_once_with("/")
        self.assertEqual(result["name"], "Disk")
        self.assertEqual(result["status"], "OK")
        self.assertEqual(result["value"], 30.0)
        self.assertEqual(result["message"], "Disk usage is normal")

    def test_disk_warning(self):
        fake_disk = Mock()
        fake_disk.percent = 85.0

        with patch(
            "src.checks.disk.psutil.disk_usage", return_value=fake_disk
        ):
            result = check_disk()

        self.assertEqual(result["status"], "WARNING")
        self.assertEqual(result["value"], 85.0)
        self.assertEqual(result["message"], "Disk usage is high")

    def test_disk_critical(self):
        fake_disk = Mock()
        fake_disk.percent = 97.0

        with patch(
            "src.checks.disk.psutil.disk_usage", return_value=fake_disk
        ):
            result = check_disk()

        self.assertEqual(result["status"], "CRITICAL")
        self.assertEqual(result["value"], 97.0)
        self.assertEqual(result["message"], "Disk usage is critically high")

    def test_disk_boundary_80(self):
        fake_disk = Mock()
        fake_disk.percent = 80.0

        with patch(
            "src.checks.disk.psutil.disk_usage", return_value=fake_disk
        ):
            result = check_disk()

        self.assertEqual(result["status"], "WARNING")

    def test_disk_boundary_95(self):
        fake_disk = Mock()
        fake_disk.percent = 95.0

        with patch(
            "src.checks.disk.psutil.disk_usage", return_value=fake_disk
        ):
            result = check_disk()

        self.assertEqual(result["status"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()
