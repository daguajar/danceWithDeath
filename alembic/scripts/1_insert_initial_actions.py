# -*- encoding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../..')))

from constants.actions import ACTIONS
from constants.actions import DESCRIPTION
from constants.actions import NAME
from db.models import *

# Se crea sesión
session = Session()

# Create Actions to Insert
for a_def in ACTIONS:
    action = Action(a_def[NAME], a_def[DESCRIPTION])
    session.add(action)

# Commit to DB
session.commit()

# Close Session
session.close()
