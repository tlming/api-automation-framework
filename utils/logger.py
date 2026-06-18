import logging
import sys


def setup_logger(level='INFO'):
    """配置logging。"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        stream=sys.stdout,
    )