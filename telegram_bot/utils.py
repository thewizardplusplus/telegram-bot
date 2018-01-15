from . import logger

def catch_exceptions(function):
    def wrapper(*args):
        try:
            function(*args)
        except Exception as exception:
            logger.get_logger().exception(exception)

    return wrapper
