import logging

import colorlog


class BoggerDevManger:
    Logger = logging.Logger

    @staticmethod
    def get_logger(name: str, level=logging.DEBUG) -> logging.Logger:
        logger = logging.getLogger(name)

        if not logger.handlers:
            logger.setLevel(level)
            formatter_str = '%(levelname)s:     | %(name)s | %(message)s - %(asctime)s'
            formatter_color = {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red'
            }
            formatter = colorlog.ColoredFormatter(
                formatter_str,
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors=formatter_color
            )
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

class BoggerDevLogger:
    def __init__(self, params):
        self.logger = BoggerDevManger.get_logger(params)