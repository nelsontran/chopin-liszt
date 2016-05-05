#!/usr/bin/env python3

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "{{ INSTALL_DIR }}/")

# virtual environment
activate_this = "{{ VENV_DIR }}/bin/activate_this.py"
exec(open(activate_this).read(), dict(__file__=activate_this))

# get application object
from app import app as application
application.secret_key = "{{ SECRET_KEY }}"
