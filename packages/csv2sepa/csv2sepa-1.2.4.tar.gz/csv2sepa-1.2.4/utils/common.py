from datetime import datetime
import configparser
import importlib
import os

def check_python_installation() -> None:
    """
    Check if all needed Python libraries are installed and available

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    libraries = [
        'argparse',
        'colorama',
        'configparser',
        'csv',
        'inquirer',
        'os',
        'sepapy',
        'sys',
        'time'
    ]
    for lib in libraries:
        try:
            importlib.import_module(lib)
        except ImportError:
            print(lib +' is not installed.')

    if not os.path.exists('out'):
        os.makedirs('out')


def generate_endtoend() -> str:
    """
    Helper to generate an unique endtoend id

    Parameters
    ----------
    None

    Returns
    -------
    str
        an unique endtoend id
    """
    _config = get_config()
    _name = _config.get('name', 'csv2sepa')

    return (''.join(s[0] for s in _name.split())+'-'+ get_2digit_year() + get_quantieme() +'-'+ str(uuid.uuid4())).upper()[:35]


def get_csv_files() -> list[str]:
    """
    Return a list of files with a .csv extension

    Parameters
    ----------
    None

    Returns
    -------
    list[str]
    """
    return [f for f in os.listdir('./csv/') if f.endswith('.csv')]


def get_sepa_operation(sepa: str, instrument: str) -> str:
    """
    Return the operation for the SEPA format

    Parameters
    ----------
    sepa: str
        the SEPA format

    Returns
    -------
    str
        the 3 letters for the SEPA format (SCT for SEPA Credit Transfer|SDD for SEPA Direct Debit)
    """
    match sepa:
        case sepa if sepa.startswith('pain.001'):
            return 'sct'
        case sepa if sepa.startswith('pain.008') and instrument == 'B2B':
            return 'b2b'
        case sepa if sepa.startswith('pain.008') and instrument == 'B2C':
            return 'sdd'
        case _:
            exit()


def get_csv2json_config():
    """
    Return the configuration from the csv2sepa.ini file

    Parameters
    ----------
    None

    Returns
    -------
    list[str]
    """
    _config = configparser.ConfigParser()
    _config.read('csv2sepa.ini')
    return _config['csv2sepa']


def get_2digit_year() -> int:
    """
    Return the current year with two-digits

    Parameters
    ----------
    None

    Returns
    -------
    int
    """
    return datetime.now().strftime('%y')


def get_quantieme() -> int:
    """
    Return the current day number into the current year

    Parameters
    ----------
    None

    Returns
    -------
    int
    """
    return "{:03d}".format(datetime(year=datetime.now().year,month=datetime.now().month, day=datetime.now().day).timetuple().tm_yday)


def get_gprhdr(sepa: str) -> list:
    """
    Return the GrpHdr informations

    Parameters
    ----------
    sepa: str
        the SEPA format

    Returns
    -------
    list
    """
    _config = get_csv2json_config()
    _generateMsgId = _config.get('generate_msg_id', True)
    
    if _generateMsgId:
        _sepaOperationCode = get_sepa_operation(sepa, _config.get('instrument', 'B2C'))
        _generatedMsgId = _config.get('msg_id', None) +'-'+ _sepaOperationCode +'-'+ get_2digit_year() + get_quantieme() +'-001'
    else:
        _generatedMsgId = _config.get('msg_id', None)
    
    return {
        "msg_id": _generatedMsgId.upper(),
        "name": _config.get('name'),
        "IBAN": _config.get('iban'),
        "BIC": _config.get('bic', 'NOTPROVIDED'),
        "batch": _config.getboolean('batch'),
        "creditor_id": _config.get('ics', None),
        "currency": _config.get('currency', 'EUR'),
        "instrument": _config.get('instrument', 'B2C'),
        "address": {
            # The address and all of its fields are mandatory from November, 20th 2025
            "department": _config.get('addr_department', None),
            "subdepartment": _config.get('addr_subdepartment', None),
            "street_name": _config.get('addr_street_name'),
            "building_number": _config.get('addr_building_number'),
            "postcode": _config.get('addr_postcode'),
            "town": _config.get('addr_town'),
            "country": _config.get('addr_country'),
            "country_subdivision": _config.get('addr_country_subdivision', None),
        },
    }

def convert_to_cents(amount: float) -> int:
    """
    Helper to decimal currency string into integers (cents).

    Parameters
    ----------
    amount: float
        The amount in currency with full stop decimal separator

    Returns
    -------
    int
        The amount in cents
    """
    int_string = '{:.2f}'.format(float(amount))
    int_string = int_string.replace('.', '')
    int_string = int_string.lstrip('00')
    
    return int(int_string)