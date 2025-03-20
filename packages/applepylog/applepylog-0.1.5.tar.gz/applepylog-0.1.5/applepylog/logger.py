import sys
from datetime import datetime
from .writer import LogLevel, Writer
from typing import TextIO, Self, List

class Logger:
    writers: List[Writer]
    logger_name: str
    parent: Self

    def __init__(self, logger_name: str, *, initial_log_level: LogLevel = LogLevel.WARN,
                 initial_writer: TextIO = sys.stdout, parent: Self = None):
        self.logger_name = logger_name
        self.writers = [Writer(initial_writer, "Main", initial_log_level)]
        self.parent = parent

    def add_writer(self, writer: TextIO, writer_name: str, log_level: LogLevel):
        self.writers.append(Writer(writer, writer_name, log_level))

    def __get_full_name(self) -> str:
        if self.parent is None:
            return self.logger_name
        else:
            return f"{(self.parent.__get_full_name())}.{self.logger_name}"

    def __build_basic_message(self, message: str, log_level: LogLevel) -> str:
        return f"{datetime.now()} {log_level.name} {self.__get_full_name()}, {message}\n"

    def __log_message(self, message: str, log_lvl: LogLevel):
        out_msg = self.__build_basic_message(message, log_lvl)
        for writer in self.writers:
            if writer.log_level.value >= log_lvl.value:
                writer.writer.write(out_msg)

    def info(self, message: str):
        self.__log_message(message, LogLevel.INFO)

    def warn(self, message: str):
        self.__log_message(message, LogLevel.WARN)

    def debug(self, message: str):
        self.__log_message(message, LogLevel.DEBUG)

    def error(self, message: str):
        self.__log_message(message, LogLevel.ERROR)
