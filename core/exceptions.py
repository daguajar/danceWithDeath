# -*- encoding: utf-8 -*-

from constants.status import ACTION_NOT_FOUND_STATUS
from constants.status import APPOINTMENT_NOT_FOUND_STATUS
from constants.status import BAD_FORMAT_DATE_STATUS
from constants.status import BAD_FORMAT_EMAIL_STATUS
from constants.status import BAD_FORMAT_ID_STATUS
from constants.status import BROKEN_PIPE_ERROR_STATUS
from constants.status import CANT_CREATE_APPOINTMENT_BEFORE_STATUS
from constants.status import CANT_CREATE_APPOINTMENT_STATUS
from constants.status import CANT_DELETE_APPOINTMENT_BEFORE_STATUS
from constants.status import CANT_DELETE_APPOINTMENT_STATUS
from constants.status import CANT_LIST_APPOINTMENTS_STATUS
from constants.status import CANT_UPDATE_APPOINTMENT_BEFORE_STATUS
from constants.status import CANT_UPDATE_APPOINTMENT_STATUS
from constants.status import DUPLICATE_APPOINTMENT_STATUS
from constants.status import MISSING_ACTION_STATUS
from constants.status import MISSING_DATE_STATUS
from constants.status import MISSING_EMAIL_STATUS
from constants.status import MISSING_ID_STATUS
from constants.status import MISSING_TIME_STATUS
from constants.status import TIME_NOT_A_NUMBER_STATUS
from constants.status import DATE_NOT_IN_RANGE_STATUS
from constants.status import TIME_NOT_IN_RANGE_STATUS
from constants.status import PAST_DATE_STATUS
from constants.status import PAST_TIME_STATUS

from utils.logger import createLog
log = createLog(__name__)


# Top Exception
class DanceWithDeathException(Exception):
    def __init__(self, message, status):
        self.message = message
        self.status = status
        log.error(str(self))
        super()

    def __str__(self):
        return '[{status}] {message}'.format(
            status=self.status,
            message=self.message,
        )


# Action Not Found
class DWDActionNotFoundException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = ACTION_NOT_FOUND_STATUS
        super().__init__(self.message, self.status)


# Appointment Not Found 
class DWDAppointmentNotFoundException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = APPOINTMENT_NOT_FOUND_STATUS
        super().__init__(self.message, self.status)


# Bad Format Date
class DWDBadFormatDateException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = BAD_FORMAT_DATE_STATUS
        super().__init__(self.message, self.status)


# Bad Format Email
class DWDBadFormatEmailException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = BAD_FORMAT_EMAIL_STATUS
        super().__init__(self.message, self.status)


# Bad Format Id
class DWDBadFormatIdException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = BAD_FORMAT_ID_STATUS
        super().__init__(self.message, self.status)


# Can't Create Appontment before now
class DWDCantCreateAppointmentBeforeException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = CANT_CREATE_APPOINTMENT_BEFORE_STATUS
        super().__init__(self.message, self.status)


# Can't Create Appontment by another exception
class DWDCantCreateAppointmentException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = CANT_CREATE_APPOINTMENT_STATUS
        super().__init__(self.message, self.status)


# Can't Delete Appontment before now
class DWDCantDeleteAppointmentBeforeException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = CANT_DELETE_APPOINTMENT_BEFORE_STATUS
        super().__init__(self.message, self.status)


# Can't Delete Appontment by another exception
class DWDCantDeleteAppointmentException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = CANT_DELETE_APPOINTMENT_STATUS
        super().__init__(self.message, self.status)


# Can't List Appontment by another exception
class DWDCantListAppointmentsException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = CANT_LIST_APPOINTMENTS_STATUS
        super().__init__(self.message, self.status)


# Can't Update Appontment before now
class DWDCantUpdateAppointmentBeforeException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = CANT_UPDATE_APPOINTMENT_BEFORE_STATUS
        super().__init__(self.message, self.status)


# Can't Update Appontment by another exception
class DWDCantUpdateAppointmentException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = CANT_UPDATE_APPOINTMENT_STATUS
        super().__init__(self.message, self.status)


# Date Not in range  (Monday - Friday)
class DWDDateNotInRangeException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = DATE_NOT_IN_RANGE_STATUS
        super().__init__(self.message, self.status)


# Duplicate Appontment: exists one for that date and time
class DWDDuplicateAppointmentException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = DUPLICATE_APPOINTMENT_STATUS
        super().__init__(self.message, self.status)


# Missing Action
class DWDMissingActionException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = MISSING_ACTION_STATUS
        super().__init__(self.message, self.status)


# Missing Date
class DWDMissingDateException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = MISSING_DATE_STATUS
        super().__init__(self.message, self.status)


# Missing Email
class DWDMissingEmailException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = MISSING_EMAIL_STATUS
        super().__init__(self.message, self.status)


# Missing Id
class DWDMissingIdException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = MISSING_ID_STATUS
        super().__init__(self.message, self.status)


# Missing Time
class DWDMissingTimeException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = MISSING_TIME_STATUS
        super().__init__(self.message, self.status)


# Time Not a Number
class DWDTimeNotANumberException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = TIME_NOT_A_NUMBER_STATUS
        super().__init__(self.message, self.status)


# Time Not in range (9 - 17)
class DWDTimeNotInRangeException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = TIME_NOT_IN_RANGE_STATUS
        super().__init__(self.message, self.status)


# Date Past 
# (Cam't create, modify or delete appoinments before current day)
class DWDPastDateException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = PAST_DATE_STATUS
        super().__init__(self.message, self.status)


# Time Past 
# (Cam't create, modify or delete appoinments 
# before current time in current day)
class DWDPastTimeException(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = PAST_TIME_STATUS
        super().__init__(self.message, self.status)



# Broken Pipe Error
# Manage Error from DB
class DWDBrokenPipeError(DanceWithDeathException):
    def __init__(self, message):
        self.message = message
        self.status = BROKEN_PIPE_ERROR_STATUS
        super().__init__(self.message, self.status)



