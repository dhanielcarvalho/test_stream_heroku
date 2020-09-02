import logging


class Logger(object):

    def __init__(self, name='logger', level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        sh = logging.StreamHandler()
        self.logger.addHandler(sh)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        sh.setFormatter(formatter)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
