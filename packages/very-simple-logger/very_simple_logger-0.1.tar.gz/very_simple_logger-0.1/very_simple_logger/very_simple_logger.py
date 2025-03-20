# -*- coding: utf-8 -*-
"""
Created on Fri March 14 18:28:36 2025

@author: Javier S. Zurdo
@module: Create a simple logger with a standard format.
"""

#%% ------------ Libraries -----------------
# ------------------------------------------
import logging

#%% ------------ Classes -------------------
# ------------------------------------------
class Very_Simple_Logger:
    def __init__(self, logger_name:str, log_file:str):
        self.logger_name = logger_name
        self.log_file = log_file
        self.logger = self.logger_create(self.logger_name, self.log_file)

    def logger_create(self, logger_name:str, log_file:str)->logging.Logger:
        # logging.info()
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        # Console handler with level = debug
        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(logging.DEBUG)
        # Set formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        # Set formatter to console handler
        consolehandler.setFormatter(formatter)
        # Set a file handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        # Set consolehandler to logger
        logger.addHandler(consolehandler)
        return logger

    def logger_delete(self):
        for h in self.logger.handlers:
            self.logger.removeHandler(h)
            h.flush()
            h.close()
