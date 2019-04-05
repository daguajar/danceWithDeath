# -*- encoding: utf-8 -*-
from datetime import datetime
import sys
import traceback

from pymysql.err import OperationalError as pymysqlOperationalError

from sqlalchemy.exc import OperationalError as sqlalchemyOperationalError
from sqlalchemy.sql.expression import and_

from constants.actions import CREATE
from constants.actions import DELETE
from constants.actions import LIST
from constants.actions import UPDATE

from constants.definitions import DATE_FORMAT
from constants.definitions import MAX_TIME
from constants.definitions import MIN_TIME

from constants.messages import APPOINTMENT_NOT_FOUND_MESSAGE
from constants.messages import BROKEN_PIPE_ERROR_MESSAGE
from constants.messages import CANT_CREATE_APPOINTMENT_BEFORE_MESSAGE
from constants.messages import CANT_CREATE_APPOINTMENT_MESSAGE
from constants.messages import CANT_DELETE_APPOINTMENT_BEFORE_MESSAGE
from constants.messages import CANT_DELETE_APPOINTMENT_MESSAGE
from constants.messages import CANT_LIST_APPOINTMENTS_MESSAGE
from constants.messages import CANT_UPDATE_APPOINTMENT_BEFORE_MESSAGE
from constants.messages import CANT_UPDATE_APPOINTMENT_MESSAGE
from constants.messages import DUPLICATE_APPOINTMENT_MESSAGE

from constants.params import ACTION
from constants.params import APPOINTMENT
from constants.params import DATE
from constants.params import EMAIL
from constants.params import ENABLED
from constants.params import ID
from constants.params import MESSAGE
from constants.params import STATUS
from constants.params import TIME

from core.exceptions import DanceWithDeathException
from core.exceptions import DWDAppointmentNotFoundException
from core.exceptions import DWDBrokenPipeError
from core.exceptions import DWDCantCreateAppointmentBeforeException
from core.exceptions import DWDCantCreateAppointmentException
from core.exceptions import DWDCantDeleteAppointmentBeforeException
from core.exceptions import DWDCantDeleteAppointmentException
from core.exceptions import DWDCantListAppointmentsException
from core.exceptions import DWDCantUpdateAppointmentBeforeException
from core.exceptions import DWDCantUpdateAppointmentException
from core.exceptions import DWDDuplicateAppointmentException
from core.exceptions import DWDPastTimeException

from db.models import Action
from db.models import Appointment
from db.models import Log
from db.models import Session

from utils.logger import createLog
from utils.validators import check_date_range
from utils.validators import check_is_past_time


_log = createLog(__name__)


def get_times(date):
    time_dict = {tm: {ENABLED: check_is_past_time(date, tm) if check_date_range(date) else False, APPOINTMENT: None} for tm in range(MIN_TIME, MAX_TIME+1)}

    session = Session()
    now = datetime.now()

    try:
        action = session.query(Action).filter(Action.name == LIST).one()

        appointments = session.query(Appointment).filter(and_(
            Appointment.date == date,
            Appointment.is_deleted == False,
        )).all()

        for appointment in appointments:
            time_dict[appointment.time][APPOINTMENT] = {
                ID: appointment.id,
                DATE: appointment.date.strftime(DATE_FORMAT),
                TIME: appointment.time,
                EMAIL: appointment.email,
            }

        log = Log(now, None, action, None, None, None, date, None, None)

        session.add(log)

        session.commit()

    except pymysqlOperationalError as poe:
        raise DWDBrokenPipeError(
            BROKEN_PIPE_ERROR_MESSAGE
        )
    except sqlalchemyOperationalError as soe:
        raise DWDBrokenPipeError(
            BROKEN_PIPE_ERROR_MESSAGE
        )
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        message = '    '.join(line for line in lines)
        _log.error(message)
        raise DWDCantListAppointmentsException(
            CANT_LIST_APPOINTMENTS_MESSAGE.format(
                date=date.strftime(DATE_FORMAT),
            )
        )

    finally:
        session.close()

    return time_dict


def create_appointment(date, time, email):
    try:
        session = Session()

        if not check_is_past_time(date, time):
            raise DWDCantCreateAppointmentBeforeException(
                CANT_CREATE_APPOINTMENT_BEFORE_MESSAGE.format(
                date=date.strftime(DATE_FORMAT),
                time=time,
                email=email,
                )
            )

        previous_appointment = session.query(Appointment).filter(and_(
            Appointment.date == date,
            Appointment.time == time,
            Appointment.is_deleted == False,
        )).one_or_none()

        if previous_appointment is not None:
            raise DWDDuplicateAppointmentException(
                DUPLICATE_APPOINTMENT_MESSAGE.format(
                    appointment=previous_appointment,
                )
            )

        now = datetime.now()

        action = session.query(Action).filter(Action.name == CREATE).one()

        appointment = Appointment(date, time, email)

        log = Log(now, appointment, action, None, None, None, date, time, email)

        session.add(appointment)
        session.add(log)

        session.commit()

    except DanceWithDeathException as dwde:
        raise dwde

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        message = '    '.join(line for line in lines)
        _log.error(message)
        raise DWDCantCreateAppointmentException(
            CANT_CREATE_APPOINTMENT_MESSAGE.format(
                date=date.strftime(DATE_FORMAT),
                time=time,
                email=email,
            )
        )

    finally:
        session.close()

    return get_times(date), date.strftime(DATE_FORMAT)


def update_appointment(id, new_date, new_time, new_email):
    try:
        session = Session()
        now = datetime.now()

        action = session.query(Action).filter(Action.name == UPDATE).one()

        appointment = session.query(Appointment).filter(Appointment.id == id).one()

        old_date = appointment.date
        old_time = appointment.time
        old_email = appointment.email

        if not check_is_past_time(old_date, old_time):
            raise DWDCantUpdateAppointmentBeforeException(
                CANT_UPDATE_APPOINTMENT_BEFORE_MESSAGE.format(
                    appointment=appointment,
                )
            )

        if new_date is None:
            new_date = old_date

        if new_time is None:
            new_time = old_time

        if new_email is None:
            new_email = old_email

        previous_appointment = session.query(Appointment).filter(and_(
            Appointment.date == new_date,
            Appointment.time == new_time,
            Appointment.is_deleted == False,
        )).one_or_none()

        if previous_appointment is not None and previous_appointment != appointment:
            raise DWDDuplicateAppointmentException(
                DUPLICATE_APPOINTMENT_MESSAGE.format(
                    appointment=previous_appointment,
                )
            )

        log = Log(now, appointment, action, old_date, old_time, old_email, new_date, new_time, new_email)

        appointment.date = new_date
        appointment.time = new_time
        appointment.email = new_email

        session.add(log)

        session.commit()

    except DanceWithDeathException as dwde:
        raise dwde

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        message = '    '.join(line for line in lines)
        _log.error(message)
        
        raise DWDCantUpdateAppointmentException(
            CANT_UPDATE_APPOINTMENT_MESSAGE.format(
                id=id,
                date=new_date.strftime(DATE_FORMAT),
                time=time,
                email=email,
            )
        )

    finally:
        session.close()

    return get_times(new_date), new_date.strftime(DATE_FORMAT)


def delete_appointment(id):
    try:
        session = Session()
        now = datetime.now()

        action = session.query(Action).filter(Action.name == DELETE).one()

        appointment = session.query(Appointment).filter(Appointment.id == id).one()

        date = appointment.date
        time = appointment.time

        if not check_is_past_time(date, time):
            raise DWDCantDeleteAppointmentBeforeException(
                CANT_DELETE_APPOINTMENT_BEFORE_MESSAGE.format(
                    appointment=appointment,
                )
            )

        log = Log(now, appointment, action, appointment.date, appointment.time, appointment.email)

        appointment.is_deleted = True

        session.add(log)

        session.commit()

    except DanceWithDeathException as dwde:
        raise dwde

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        message = '    '.join(line for line in lines)
        _log.error(message)
        
        raise DWDCantDeleteAppointmentException(
            CANT_DELETE_APPOINTMENT_MESSAGE.format(
                id=id,
            )
        )

    finally:
        session.close()

    return get_times(date), date.strftime(DATE_FORMAT)


def exists_appointment(id):
    exists = True
    session = Session()

    appointment = session.query(Appointment).filter(Appointment.id == id).one_or_none()
    if appointment is None or appointment.is_deleted:
        exists = False

    session.close()

    if not exists:
        raise DWDAppointmentNotFoundException(
            APPOINTMENT_NOT_FOUND_MESSAGE.format(
                id=id,
            )
        )

    return True
