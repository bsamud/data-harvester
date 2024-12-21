from common.logger import log

def safe_convert(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.error(f"Conversion error: {e}")
            return None
    return wrapper
