import logging
from importlib import reload
import os
import inspect
from appdirs import user_data_dir

from gw_certificate.common.debug import debug_print
from gw_certificate.common.utils import current_timestamp


def db_utils():
    """
    Use databricks dbutils from an external package
    for example: to use dbutils.fs.head() - use db_utils().fs.head()
    """
    for frame in inspect.getouterframes(inspect.currentframe()):
        global_names = set(frame.frame.f_globals)
        # Use multiple functions to reduce risk of mismatch
        if all(v in global_names for v in ["dbutils"]):
            return frame.frame.f_globals["dbutils"]()
    raise EnvironmentError("Unable to detect dbutils function")

def initialize_logger(working_directory=None):
    """
    initializes the logger to print to log and to logfile, which by default is named by the current timestamp (ms)
    when calling the function.
    :param working_directory: working directory to save logfile (in case running locally)
    :type working_directory: str
    :return: logger fileHandler filename
    """
    logging.shutdown()
    reload(logging)
    logger = logging.getLogger()
    for handler in logger.handlers:
        try:
            # extract current filename from log
            filename = handler.baseFilename.split('\\')[-1].split('.')[0]
            debug_print(f'Logger already initialized! passing logfile {filename}')
            return filename
        except Exception:
            pass
    logger_filename = int(current_timestamp())
    if working_directory is None:
        working_directory = os.path.join(user_data_dir(), 'wiliot', 'deployment_tools')
    if not os.path.exists(working_directory):
        os.makedirs(working_directory)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s | %(levelname)s | %(message)s',
                        handlers=[
                            logging.FileHandler(f'{working_directory}/{logger_filename}.log', 'a'),
                            # logging.handlers.RotatingFileHandler
                            logging.StreamHandler()
                        ])
    # filter stream to show info and up
    logging.getLogger().handlers[0].setLevel(logging.DEBUG)
    logging.getLogger().handlers[1].setLevel(logging.INFO)
    debug_print(f'logger initialized at {logger_filename}', center=True)
    debug_print(f'logfile located at {working_directory}/{logger_filename}.log')
    logging.getLogger().setLevel(logging.DEBUG)
    return logger_filename
