# -*- encoding: utf-8 -*-

from constants.actions import CREATE
from constants.actions import DELETE
from constants.actions import LIST
from constants.actions import UPDATE

from constants.messages import CREATE_OK_MESSAGE
from constants.messages import DELETE_OK_MESSAGE
from constants.messages import LIST_OK_MESSAGE
from constants.messages import UPDATE_OK_MESSAGE

from constants.messages import ACTION_NOT_FOUND_MESSAGE
from constants.messages import DATE_NOT_IN_RANGE_MESSAGE
from constants.messages import MISSING_ACTION_MESSAGE
from constants.messages import MISSING_DATE_MESSAGE
from constants.messages import MISSING_EMAIL_MESSAGE
from constants.messages import MISSING_ID_MESSAGE
from constants.messages import MISSING_TIME_MESSAGE
from constants.messages import PAST_TIME_MESSAGE

from constants.params import ACTION
from constants.params import DATE
from constants.params import EMAIL
from constants.params import ID
from constants.params import MESSAGE
from constants.params import STATUS
from constants.params import TIME
from constants.params import TIMES

from constants.status import CREATE_OK_STATUS
from constants.status import DELETE_OK_STATUS
from constants.status import GENERIC_EXCEPTION_STATUS
from constants.status import GENERIC_OK_STATUS
from constants.status import LIST_OK_STATUS
from constants.status import UPDATE_OK_STATUS

from core.exceptions import DWDActionNotFoundException
from core.exceptions import DWDDateNotInRangeException
from core.exceptions import DWDMissingActionException
from core.exceptions import DWDMissingDateException
from core.exceptions import DWDMissingEmailException
from core.exceptions import DWDMissingIdException
from core.exceptions import DWDMissingTimeException
from core.exceptions import DWDPastTimeException

from core.methods import create_appointment
from core.methods import delete_appointment
from core.methods import exists_appointment
from core.methods import get_times
from core.methods import update_appointment

from utils.validators import check_param
from utils.validators import check_date_format_and_return
from utils.validators import check_date_range
from utils.validators import check_email
from utils.validators import check_id_format
from utils.validators import check_is_past_date
from utils.validators import check_is_past_time
from utils.validators import check_time_format
from utils.validators import check_time_range


def create_json_from_args(params):
    if not check_param(ACTION, params):
        raise DWDMissingActionException(
            MISSING_ACTION_MESSAGE
        )

    action = params[ACTION]

    if action == LIST:
        # check missing
        if not check_param(DATE, params):
            raise DWDMissingDateException(
                MISSING_DATE_MESSAGE
            )

        # Check Date
        date_str = params[DATE]
        date = check_date_format_and_return(date_str)

        # Get data
        times = get_times(date)
        return {
            DATE: date_str,
            MESSAGE: LIST_OK_MESSAGE,
            STATUS: LIST_OK_STATUS,
            TIMES: times,
        }

    elif action == CREATE:
        # Check missing
        if not check_param(DATE, params):
            raise DWDMissingDateException(
                MISSING_DATE_MESSAGE
            )
        if not check_param(TIME, params):
            raise DWDMissingTimeException(
                MISSING_TIME_MESSAGE
            )
        if not check_param(EMAIL, params):
            raise DWDMissingEmailException(
                MISSING_EMAIL_MESSAGE
            )

        # Check Date
        date_str = params[DATE]
        date = check_date_format_and_return(date_str)
        if not check_date_range(date):
            raise DWDDateNotInRangeException(
                DATE_NOT_IN_RANGE_MESSAGE.format(
                    date=date.strftime(DATE_FORMAT),
                    dayname=dayname,
                )
            )

        check_is_past_date(date)

        # Check Time
        time_str = params[TIME]
        time = check_time_format(time_str)
        check_time_range(time)

        # check_email
        email = params[EMAIL]
        check_email(email)

        times, date_str = create_appointment(date, time, email)
        return {
            DATE: date_str,
            MESSAGE: CREATE_OK_MESSAGE,
            STATUS: CREATE_OK_STATUS,
            TIMES: times,
        }

    elif action == UPDATE:
        # Check missing
        if not check_param(ID, params):
            raise DWDMissingIdException(
                MISSING_ID_MESSAGE
            )
        
        id_str = params[ID]
        id = check_id_format(id_str)
        exists_appointment(id)

        # Check optional values

        # Date
        date = None
        if check_param(DATE, params):
            date_str = params[DATE]
            date = check_date_format_and_return(date_str)
            if not check_date_range(date):
                raise DWDDateNotInRangeException(
                    DATE_NOT_IN_RANGE_MESSAGE.format(
                        date=date.strftime(DATE_FORMAT),
                        dayname=dayname,
                    )
                )
            check_is_past_date(date)
    
        # Time
        time = None
        if check_param(TIME, params):
            time_str = params[TIME]
            time = check_time_format(time_str)
            check_time_range(time)
            if not check_is_past_time(date, time):
                raise DWDPastTimeException(
                    PAST_TIME_MESSAGE.format(
                        date=date.strftime(DATE_FORMAT),
                        time=time,
                    )
                )
        
        # Email
        email = None
        if check_param(EMAIL, params):
            email = params[EMAIL]
            check_email(email)

        times, date_str = update_appointment(id, date, time, email)
        return {
            DATE: date_str,
            MESSAGE: UPDATE_OK_MESSAGE,
            STATUS: UPDATE_OK_STATUS,
            TIMES: times,
        }

    elif action == DELETE:
        # Check missing
        if not check_param(ID, params):
            raise DWDMissingIdException(
                MISSING_ID_MESSAGE
            )
        
        id_str = params[ID]
        id = check_id_format(id_str)
        exists_appointment(id)

        times, date_str = delete_appointment(id)
        return {
            DATE: date_str,
            MESSAGE: DELETE_OK_MESSAGE,
            STATUS: DELETE_OK_STATUS,
            TIMES: times,
        }

    else:
        raise DWDActionNotFoundException(
            ACTION_NOT_FOUND_MESSAGE.format(
                action=action,
            )
        )

    return {'OKI':'DOKI'}


def create_json_from_dwdexception(DWDException):
    return{
        MESSAGE: DWDException.message,
        STATUS: DWDException.status,
    }


def create_json_from_exception(Exception):
    return{
        MESSAGE: str(Exception),
        STATUS: GENERIC_EXCEPTION_STATUS,
    }

