# -*- encoding: utf-8 -*-

import calendar
import re

from datetime import datetime

from constants.definitions import DATE_FORMAT
from constants.definitions import MAX_DATE
from constants.definitions import MIN_DATE
from constants.definitions import MAX_TIME
from constants.definitions import MIN_TIME

from constants.messages import BAD_FORMAT_DATE_MESSAGE
from constants.messages import BAD_FORMAT_EMAIL_MESSAGE
from constants.messages import BAD_FORMAT_ID_MESSAGE
from constants.messages import TIME_NOT_A_NUMBER_MESSAGE
from constants.messages import TIME_NOT_IN_RANGE_MESSAGE
from constants.messages import PAST_DATE_MESSAGE

from core.exceptions import DWDBadFormatDateException
from core.exceptions import DWDBadFormatEmailException
from core.exceptions import DWDBadFormatIdException
from core.exceptions import DWDTimeNotANumberException
from core.exceptions import DWDTimeNotInRangeException
from core.exceptions import DWDPastDateException


'''
Check if an email is valid
Raise DWDBadFormatEmailException
'''
def check_email(email):
    if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
        raise DWDBadFormatEmailException(
            BAD_FORMAT_EMAIL_MESSAGE.format(
                email=email,
            )
        )
    return True


'''
Check if a key is in dicto and 
if the value is the same
'''
def check_param(key, dicto, value=None):
    return (key in dicto and (value == None or (dicto[key] == value if key in dicto else False)))


'''
Check if date is in correct format then return
Raise DWDBadFormatDateException
'''
def check_date_format_and_return(date_str):
    try:
        date_time = datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        raise DWDBadFormatDateException(
            BAD_FORMAT_DATE_MESSAGE.format(
                date=date_str,
            )
        )

    return date_time.date()


'''
Check if date is in range (Monday - Friday)
'''
def check_date_range(date):
    weekday = date.weekday()
    dayname = calendar.day_name[weekday]
    if weekday not in range(MIN_DATE, MAX_DATE+1):
        return False
    return True


'''
Check if time is a positive number
Raise DWDTimeNotANumberException
'''
def check_time_format(str_time):
    if not check_positive_integer(str_time):
        raise DWDTimeNotANumberException(
            TIME_NOT_A_NUMBER_MESSAGE.format(
                time=str_time,
            )
        )
    return int(str_time)


'''
Check if time is in range (9 - 17)
Raise DWDTimeNotInRangeException
'''
def check_time_range(time):
    if time not in range(MIN_TIME, MAX_TIME+1):
        raise DWDTimeNotInRangeException(
            TIME_NOT_IN_RANGE_MESSAGE.format(
                time=time,
            )
        )
    return True


'''
Check if date is not lower than current day
Raise DWDPastDateException
'''
def check_is_past_date(date):
    now = datetime.now()
    if date < now.date():
        raise DWDPastDateException(
            PAST_DATE_MESSAGE.format(
                date=date.strftime(DATE_FORMAT),
            )
        )
    return True


'''
Check if time is not lower than current time
'''
def check_is_past_time(date, time):
    now = datetime.now()
    date = datetime.combine(date, datetime.min.time()).replace(hour=time)
    if date < now:
        return False
    return True


'''
Check if id is a positive number
Raise DWDBadFormatIdException
'''
def check_id_format(id_str):
    if not check_positive_integer(id_str):
        raise DWDBadFormatIdException(
            BAD_FORMAT_ID_MESSAGE.format(
                id=id_str,
            )
        )
    return int(id_str)


'''
Check if a string is a positive integer
'''
def check_positive_integer(str_integer):
    try:
        if int(str_integer) > 0:
            return True
        else:
            return False
    except ValueError:
        return False






