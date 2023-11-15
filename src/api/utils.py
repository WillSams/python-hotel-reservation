import datetime
import inspect
import logging

from settings import API_PORT, DB_URL, ENV, IS_DEBUG

Logger = logging.getLogger()


def api_port():
    return API_PORT


def is_debug() -> bool:
    return IS_DEBUG


def runtime_environment():
    return ENV


def database_host():
    return DB_URL


def get_calling_function_name():
    frame = inspect.currentframe().f_back
    calling_frame = frame.f_back
    return calling_frame.f_code.co_name


def setup_file_logger():
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    log_file = f"logs/{current_date}.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
    )

    start_message = f"🚀 Hotel X - API ready at localhost:{API_PORT}/{ENV}/api"
    Logger.info(start_message)


def log_api_error(module_name, message):
    caller = get_calling_function_name()
    Logger.info(f"{module_name}.{caller} error(s):\n\t{message}")


def logger_exit_message():
    Logger.info("🛑 Hotel X - API stopped!")
