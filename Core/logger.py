import logging


FORMATTER = '%(asctime)s - %(name)s - %(levelname)s - [%(module)s] - %(message)s'
LOGNAME = 'emca_debug.log'


def InitLogSystem():
    """
    Init the log system
    :return:
    """
    # set up logger system
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(LOGNAME, mode='w')
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(FORMATTER)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
