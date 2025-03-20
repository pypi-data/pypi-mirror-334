import sys
import logging
import coloredlogs


class xlogger(): ##TODO: xlog
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    def __init__(self,
                 name="default",
                 level=None,
                 format='[%(asctime)s][%(name)s][%(levelname)s]:%(message)s'):

        self.__sh = None
        self.__fh = None

        self.logger = logging.getLogger(name)
        if level is not None:
            self.logger.setLevel(level)

        self.formatter = None
        self.color_format = None
        self.setStreamFormat(format)

        for i in self.logger.handlers:
            if isinstance(i, logging.StreamHandler):
                self.__sh = i
            elif isinstance(i, logging.FileHandler):
                self.__fh = i

    @property
    def level(self):
        return self.logger.level

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def log(self, level, msg):
        self.logger.log(level, msg)

    def setLevel(self, level):
        # 10 20 30 40 50
        # logging.DEBUG, logging.INFO, logging.WARNING
        self.logger.setLevel(level)

    def setStreamFormat(self, format):
        self.formatter = logging.Formatter(format)
        self.color_format = coloredlogs.ColoredFormatter(format) \
            if sys.getwindowsversion().major >= 10 \
            else self.formatter

    def setStreamhandler(self, level=None):
        if self.__sh is not None:
            self.logger.removeHandler(self.__sh)

        self.__sh = logging.StreamHandler()
        self.__sh.setFormatter(self.color_format)

        if level:
            self.__sh.setLevel(level)

        self.logger.addHandler(self.__sh)

    def setFilehandler(self, filename, level=None):
        if self.__fh is not None:
            self.logger.removeHandler(self.__fh)

        if filename is not None:
            from logging.handlers import RotatingFileHandler
            self.__fh = logging.FileHandler(filename)
            # self.__fh = RotatingFileHandler(filename, mode='a', maxBytes=10*1024,
            #                      backupCount=100, encoding=None, delay=0)
            self.__fh.setFormatter(self.formatter)
            if level:
                self.__fh.setLevel(level)
            self.logger.addHandler(self.__fh)

    def shutdown(self):
        logging.shutdown()
