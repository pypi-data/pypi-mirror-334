from datetime import date, datetime, timedelta
from . import common, logger
import uuid

def addPayment(sepa: str, row: list) -> list:
    """
    Return a new payment

    Parameters
    ----------
    sepa: str
        the SEPA format
    row: list
        the current CSV row

    Returns
    -------
    list
    """
    match sepa:
        case sepa if sepa.startswith('pain.001'):
            return addCredit(sepa, row)
        case sepa if sepa.startswith('pain.008'):
            return addDebit(sepa, row)
        case _:
            logger.print_log("SEPA format not supported!", 'error')
            exit()


def addCredit(sepa: str, row: list) -> list:
    """
    Return a new credit payment

    Parameters
    ----------
    sepa: str
        the SEPA format
    row: list
        the current CSV row

    Returns
    -------
    list
    """
    match sepa:
        case sepa if sepa.startswith('pain.001.001.03'):
            _return = {
                'name': row['name'],
                'IBAN': row['iban'],
                'amount': common.convert_to_cents(row['amount']), # in cents
                'execution_date': date.today() + timedelta(days=2),
                'description': row['description'],
                'endtoend_id': common.generate_endtoend(),
                'lines': [
                    row['address1'],
                    row['address2']
                ],
            }

            if 'bic' in row and row['bic']:
                _return['BIC'] = row['bic']

            return _return
        case sepa if sepa.startswith('pain.001.001.09'):
            _return = {
                'name': row['name'],
                'IBAN': row['iban'],
                'amount': common.convert_to_cents(row['amount']), # in cents
                'execution_date': date.today() + timedelta(days=2),
                'description': row['description'],
                'endtoend_id': common.generate_endtoend(),
                'address': {
                    'street_name': row['street_name'],
                    'building_number': row['building_number'],
                    'postcode': row['postcode'],
                    'town': row['town'],
                    'country': row['country'],
                }
            }

            if 'bic' in row and row['bic']:
                _return['BIC'] = row['bic']
            if 'department' in row and row['department']:
                _return['address']['department'] = row['department']
            if 'subdepartment' in row and row['subdepartment']:
                _return['address']['subdepartment'] = row['subdepartment']
            if 'country_subdivision' in row and row['country_subdivision']:
                _return['address']['country_subdivision'] = row['country_subdivision']

            return _return
        case _:
            logger.print_log("SEPA format not supported!", 'error')
            exit()  


def addDebit(sepa: str, row: list) -> list:
    """
    Return a new debit payment

    Parameters
    ----------
    sepa: str
        the SEPA format
    row: list
        the current CSV row

    Returns
    -------
    list
    """
    match sepa:
        case sepa if sepa.startswith('pain.008.001.02'):
            _return = {
                'name': row['name'],
                'IBAN': row['iban'],
                #'BIC': row['bic'], # IBAN Only
                'amount': common.convert_to_cents(row['amount']), # in cents
                'collection_date': datetime.strptime(row['collection_date'], '%Y-%m-%d').date(),
                'type': 'RCUR', # FRST|RCUR|OOFF|FNAL
                'mandate_id': row['mandate_id'],
                'mandate_date': datetime.strptime(row['mandate_date'], '%Y-%m-%d').date(),
                'description': row['description'],
                'endtoend_id': common.generate_endtoend(),
                'lines': [
                    row['address1'],
                    row['address2']
                ],
            }

            if 'bic' in row and row['bic']:
                _return['BIC'] = row['bic']

            return _return
        case sepa if sepa.startswith('pain.008.001.08'):
            _return = {
                'name': row['name'],
                'IBAN': row['iban'],
                #'BIC': row['bic'], # IBAN Only
                'amount': common.convert_to_cents(row['amount']), # in cents
                'collection_date': datetime.strptime(row['collection_date'], '%Y-%m-%d').date(),
                'type': 'RCUR', # FRST|RCUR|OOFF|FNAL
                'mandate_id': row['mandate_id'],
                'mandate_date': datetime.strptime(row['mandate_date'], '%Y-%m-%d').date(),
                'description': row['description'],
                'endtoend_id': common.generate_endtoend(),
                'address': {
                    'street_name': row['street_name'],
                    'building_number': row['building_number'],
                    'postcode': row['postcode'],
                    'town': row['town'],
                    'country': row['country'],
                }
            }

            if 'bic' in row and row['bic']:
                _return['BIC'] = row['bic']
            if 'department' in row and row['department']:
                _return['address']['department'] = row['department']
            if 'subdepartment' in row and row['subdepartment']:
                _return['address']['subdepartment'] = row['subdepartment']
            if 'country_subdivision' in row and row['country_subdivision']:
                _return['address']['country_subdivision'] = row['country_subdivision']

            return _return
        case _:
            logger.print_log("SEPA format not supported!", 'error')
            exit()
