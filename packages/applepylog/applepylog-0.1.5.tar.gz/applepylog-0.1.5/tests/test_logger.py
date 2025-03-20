import os
import sys

import pytest
from applepylog import Logger, LogLevel
from io import StringIO
from typing import TextIO


class TestLogger:
    writer: TextIO

    @pytest.fixture(autouse=True)
    def setup_writer(self):
        self.writer = StringIO()
        yield
        self.writer = StringIO()
        if os.path.exists("./test.txt"):
            os.remove("./test.txt")

    def test_info_logger_with_same_level(self):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.INFO, initial_writer=self.writer)
        _logger.info("test message")
        self.writer.seek(0)
        assert "INFO Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_warn_logger_with_same_level(self):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.WARN, initial_writer=self.writer)
        _logger.warn("test message")
        self.writer.seek(0)
        assert "WARN Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_debug_logger_with_same_level(self):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.DEBUG, initial_writer=self.writer)
        _logger.debug("test message")
        self.writer.seek(0)
        assert "DEBUG Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_error_logger_with_same_level(self):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.ERROR, initial_writer=self.writer)
        _logger.error("test message")
        self.writer.seek(0)
        assert "ERROR Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_default_level_info_logger(self):
        _logger = Logger("Test Logger", initial_writer=self.writer)
        _logger.info("test message")
        self.writer.seek(0)
        assert "INFO Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_default_level_warn_logger(self):
        _logger = Logger("Test Logger", initial_writer=self.writer)
        _logger.warn("test message")
        self.writer.seek(0)
        assert "WARN Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_default_level_debug_logger(self):
        _logger = Logger("Test Logger", initial_writer=self.writer)
        _logger.debug("test message")
        self.writer.seek(0)
        assert "" == self.writer.read()

    def test_default_level_error_logger(self):
        _logger = Logger("Test Logger", initial_writer=self.writer)
        _logger.error("test message")
        self.writer.seek(0)
        assert "ERROR Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_error_level_info_logger(self):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.ERROR, initial_writer=self.writer)
        _logger.info("test message")
        self.writer.seek(0)
        assert "" == self.writer.read()

    def test_error_level_warn_logger(self):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.ERROR, initial_writer=self.writer)
        _logger.warn("test message")
        self.writer.seek(0)
        assert "" == self.writer.read()

    def test_error_level_debug_logger(self):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.ERROR, initial_writer=self.writer)
        _logger.debug("test message")
        self.writer.seek(0)
        assert "" == self.writer.read()

    def test_error_level_error_logger(self):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.ERROR, initial_writer=self.writer)
        _logger.error("test message")
        self.writer.seek(0)
        assert "ERROR Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_debug_level_info_logger(self):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.DEBUG, initial_writer=self.writer)
        _logger.info("test message")
        self.writer.seek(0)
        assert "INFO Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_debug_level_warn_logger(self):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.DEBUG, initial_writer=self.writer)
        _logger.warn("test message")
        self.writer.seek(0)
        assert "WARN Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_debug_level_error_logger(self):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.DEBUG, initial_writer=self.writer)
        _logger.error("test message")
        self.writer.seek(0)
        assert "ERROR Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_debug_level_debug_logger(self):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.DEBUG, initial_writer=self.writer)
        _logger.debug("test message")
        self.writer.seek(0)
        assert "DEBUG Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_stdout_info_level_info_logger(self, capsys):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.INFO, initial_writer=sys.stdout)
        _logger.info("test message")
        logged = capsys.readouterr()
        assert "INFO Test Logger, test message\n" == logged.out[27:]  # ignoring timestamp

    def test_multi_writers_info_logger(self, capsys):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.INFO, initial_writer=sys.stdout)
        _logger.add_writer(self.writer, "Alt Writer", LogLevel.INFO)
        _logger.info("test message")
        self.writer.seek(0)
        logged = capsys.readouterr()
        assert "INFO Test Logger, test message\n" == logged.out[27:]  # ignoring timestamp
        assert "INFO Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_write_file_info_level_info_logger(self):
        file = open("./test.txt", "w+")
        _logger = Logger("Test Logger", initial_log_level=LogLevel.INFO, initial_writer=file)
        _logger.info("test message")
        file.seek(0)
        assert "INFO Test Logger, test message\n" == file.read()[27:]  # ignoring timestamp
        file.close()

    def test_multi_write_file_info_level_logger(self):
        file = open("./test.txt", "w+")
        _logger = Logger("Test Logger", initial_log_level=LogLevel.INFO, initial_writer=file)
        _logger.info("test message")
        _logger.info("other test message")
        file.seek(0)
        assert ("INFO Test Logger, test message INFO Test Logger, other test message " ==
                ' '.join([line[27:] for line in file.read().split('\n')]))  # ignoring timestamps
        file.close()

    def test_different_log_level_writers(self, capsys):
        _logger = Logger("Test Logger", initial_log_level=LogLevel.ERROR, initial_writer=sys.stdout)
        _logger.add_writer(self.writer, "Alt Writer", LogLevel.INFO)
        _logger.info("test message")
        self.writer.seek(0)
        logged = capsys.readouterr()
        assert "" == logged.out  # ignoring timestamp
        assert "INFO Test Logger, test message\n" == self.writer.read()[27:]  # ignoring timestamp

    def test_hierarchical_logger_name(self):
        _logger1 = Logger("Test1")
        _logger2 = Logger("Test2", initial_writer=self.writer, parent=_logger1)
        _logger2.info("Test")
        self.writer.seek(0)
        assert "INFO Test1.Test2, Test\n" == self.writer.read()[27:]  # ignoring timestamp
