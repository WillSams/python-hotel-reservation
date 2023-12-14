import datetime
import inspect
import logging
from typing import cast

from settings import API_PORT, DB_URL, ENV, IS_DEBUG

Logger = logging.getLogger()


def api_port() -> int:
    return cast(int, API_PORT)


def is_debug() -> bool:
    return cast(bool, IS_DEBUG)


def runtime_environment() -> str:
    return ENV


def database_host() -> str:
    return DB_URL


def get_calling_function_name() -> str:
    frame = inspect.currentframe()

    calling_frame = frame.f_back if frame is not None else None
    return calling_frame.f_code.co_name if calling_frame is not None else ""


def setup_file_logger() -> None:
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    log_file = f"logs/{current_date}.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
    )

    start_message = f"🚀 Hotel X - API ready at localhost:{API_PORT}/{ENV}/api"
    Logger.info(start_message)


def log_api_error(module_name: str, message: str) -> None:
    caller = get_calling_function_name()
    Logger.info(f"{module_name}.{caller} error(s):\n\t{message}")


def logger_exit_message() -> None:
    Logger.info("🛑 Hotel X - API stopped!")
