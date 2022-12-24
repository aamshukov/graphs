#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Logger wrapper """
import os
import logging
from base import Base


class Logger(Base):
    """
    Logger
    """
    LOGGER_NAME = 'uilab.graphs'

    def __init__(self, level=logging.DEBUG, path=None):
        """
        """
        super().__init__()
        self.logger = logging.getLogger(Logger.LOGGER_NAME)
        self.logger.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        if path:
            if not os.path.exists(path):
                os.makedirs(path)
            file_handler = logging.FileHandler(os.path.join(path, f'{Logger.LOGGER_NAME}.log'))
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, msg, *args, **kwargs):
        """
        """
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        """
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        """
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        """
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """
        """
        self.logger.exception(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        """
        self.logger.critical(msg, *args, **kwargs)
