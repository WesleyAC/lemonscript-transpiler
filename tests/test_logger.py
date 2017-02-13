import os
import sys
import subprocess
from pytest import raises

parent_dir = os.path.dirname(os.path.realpath(__file__)) + "/../"
sys.path.append(parent_dir) # a bit of a hack, but it makes the import the same
from objects.logger import Logger

def get_file_path(path):
    return os.path.dirname(os.path.realpath(__file__)) + "/" + path

class TestLoggerMethods:

    def get_log_output(self, loglevel_srting, message, loglevel=None):
        command = [get_file_path("files/logger/mock_logger.py"), loglevel_srting, message]
        if loglevel != None:
            command.append(str(loglevel))
        return subprocess.check_output(command).decode("utf-8")

    def test_default_loglevel(self):
        with raises(subprocess.CalledProcessError):
            assert "test_passed" in self.get_log_output("error", "test_passed")
        
        assert "test_passed" in self.get_log_output("warn", "test_passed")
        assert "test_passed" in self.get_log_output("info", "test_passed")
        assert not "test_failed" in self.get_log_output("debug", "test_failed")

    def test_all_loglevel(self):
        with raises(subprocess.CalledProcessError):
            assert "test_passed" in self.get_log_output("error", "test_passed", 4)
        
        assert "test_passed" in self.get_log_output("warn", "test_passed", 4)
        assert "test_passed" in self.get_log_output("info", "test_passed", 4)
        assert "test_passed" in self.get_log_output("debug", "test_passed", 4)

    def test_none_loglevel(self):
        with raises(subprocess.CalledProcessError):
            assert not "test_failed" in self.get_log_output("error", "test_failed", -1)
        
        assert not "test_failed" in self.get_log_output("warn", "test_failed", -1)
        assert not "test_failed" in self.get_log_output("info", "test_failed", -1)
        assert not "test_failed" in self.get_log_output("debug", "test_failed", -1)

    def test_log_type_all(self):
        with raises(subprocess.CalledProcessError):
            assert "ERROR" in self.get_log_output("error", "test", 4)
        
        assert "WARN" in self.get_log_output("warn", "test", 4)
        assert "INFO" in self.get_log_output("info", "test", 4)
        assert "DEBUG" in self.get_log_output("debug", "test", 4)

    def test_log_non_strings(self):
        Logger.info(1)
        Logger.info(-1)
        Logger.info(0.3)
        Logger.info(["a", "b", "c"])
        Logger.info([1, 2, 3])
        Logger.info({"test": 1, "asdf": "arst"})
        Logger.info(Logger)
        Logger.info(Logger.error)
