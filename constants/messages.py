# -*- encoding: utf-8 -*-

from constants.actions import ACTIONS
from constants.definitions import NAME

VALID_ACTIONS = [a[NAME] for a in ACTIONS]

# Ok messages
CREATE_OK_MESSAGE = 'Appointment successfully created'
DELETE_OK_MESSAGE = 'Appointment successfully deleted'
LIST_OK_MESSAGE = 'Appointments successfully listed'
UPDATE_OK_MESSAGE = 'Appointment successfully updated'

# Not Ok messages
ACTION_NOT_FOUND_MESSAGE = 'Action \'{action}\' can`t be found. Valid actions are ' + str(VALID_ACTIONS) + '.'
APPOINTMENT_NOT_FOUND_MESSAGE = 'Appointment with id \'{id}\' can`t be found.'
BAD_FORMAT_DATE_MESSAGE = 'Date not in format : \'{date}\''
BAD_FORMAT_EMAIL_MESSAGE = 'Email not in format : \'{email}\''
BAD_FORMAT_ID_MESSAGE = 'Appointment`s id must be a positive number : \'{id}\''
CANT_CREATE_APPOINTMENT_BEFORE_MESSAGE = 'Can`t create appointments before current date and time : \'{date}\', \'{time}\', \'{email}\''
CANT_CREATE_APPOINTMENT_MESSAGE = 'Can`t create appointment by another exception : \'{date}\', \'{time}\', \'{email}\''
CANT_DELETE_APPOINTMENT_BEFORE_MESSAGE = 'Can`t delete appointments before current date and time : \'{appointment}\''
CANT_DELETE_APPOINTMENT_MESSAGE = 'Can`t delete appointment by another exception : \'{id}\''
CANT_LIST_APPOINTMENTS_MESSAGE = 'Can`t list appointments by another exception : \'{date}\''
CANT_UPDATE_APPOINTMENT_BEFORE_MESSAGE = 'Can`t update appointments before current date and time : \'{appointment}\''
CANT_UPDATE_APPOINTMENT_MESSAGE = 'Can`t update appointment by another exception : \'{id}\', \'{date}\', \'{time}\', \'{email}\''
DATE_NOT_IN_RANGE_MESSAGE = 'Date must be between Monday to Friday : \'{date}\' [\'{dayname}\']'
DUPLICATE_APPOINTMENT_MESSAGE = 'Exists an appointment for this date and time : \'{appointment}\''
MISSING_ACTION_MESSAGE = 'Missing Action in request.'
MISSING_DATE_MESSAGE = 'Missing date in request.'
MISSING_EMAIL_MESSAGE = 'Missing email in request.'
MISSING_ID_MESSAGE = 'Missing appointment`s id in request.'
MISSING_TIME_MESSAGE = 'Missing time in request.'
PAST_DATE_MESSAGE = 'Date must be from today to the future : \'{date}\''
PAST_TIME_MESSAGE = 'Time must be from now to the future : \'{date}\', \'{time}\''
TIME_NOT_A_NUMBER_MESSAGE = 'Time must be a number between 9 to 17 : \'{time}\''
TIME_NOT_IN_RANGE_MESSAGE = 'Time must be between 9 to 17 : \'{time}\''
BROKEN_PIPE_ERROR_MESSAGE = "Broken Pipe Error"
