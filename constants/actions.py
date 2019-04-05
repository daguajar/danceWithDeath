# -*- encoding: utf-8 -*-
from constants.definitions import DESCRIPTION
from constants.definitions import NAME

# Actions
CREATE = 'create'
DELETE = 'delete'
LIST = 'list'
UPDATE = 'update'

# List of all possible actions
ACTIONS = []

# Added actions

# Create Appointment
A_CREATE = {
    NAME: CREATE,
    DESCRIPTION : 'Create an Appointment',
}

ACTIONS.append(A_CREATE)

# Update Appointment
A_UPDATE = {
    NAME: UPDATE,
    DESCRIPTION : 'Update an Appointment',
}

ACTIONS.append(A_UPDATE)

# Delete Appointment
A_DELETE = {
    NAME: DELETE,
    DESCRIPTION : 'Delete an Appointment',
}

ACTIONS.append(A_DELETE)

# List Appointments
A_LIST = {
    NAME: LIST,
    DESCRIPTION : 'List Appointments for a date',
}

ACTIONS.append(A_LIST)

