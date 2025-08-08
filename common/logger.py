import logging

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] [%(levelname)s] [%(thread)d] [%(filename)s:%(lineno)d] %(message)s")

logger = logging.getLogger("hil")
logger.setLevel(logging.DEBUG)
