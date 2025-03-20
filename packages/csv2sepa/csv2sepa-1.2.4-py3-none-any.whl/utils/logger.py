from colorama import Back, Fore, Style
import logging
import os
import sys

def start_logging(logfile: str) -> None:
    """
    Configure et initie le système de log.

    Parameters
    ----------
    logfile : str
        path of the log file

    Returns
    -------
    None
    """
    logging.basicConfig(filename=(logfile), filemode='w', encoding='utf-8', format='%(levelname)s: %(message)s', level=logging.INFO)

def print_log(msg, tlog) -> None:
    """
    Affiche le message à l'écran et l'ajoute au fichier de log

    Parameters
    ----------
    msg: str
        the mmessage to display and to log
    tlog: str
        success|info|warning|error

    Returns
    -------
    None
    """
    if tlog == 'info':
        logging.info(msg)
        print(msg)
    elif tlog == 'success':
        logging.info(msg)
        print(Back.GREEN+ msg +Style.RESET_ALL)
    elif tlog == 'warning':
        logging.warning(msg)
        print(Back.YELLOW+ msg +Style.RESET_ALL)
    elif tlog == 'error':
        logging.error(msg)
        print(Back.RED+Fore.WHITE+ msg +Style.RESET_ALL)
        sys.exit()
    else:
        logging.error(msg)
        print(msg)