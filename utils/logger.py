import logging
# 设置Logger的默认格式
LOG_FORMAT = "[%(asctime)s][%(levelname)s]: %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)