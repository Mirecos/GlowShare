import sys
#avoid __pycache__ folders when developing
sys.dont_write_bytecode = True

import os
import time

from src.classes.LocalClient import LocalClient

from src.utils import clear

clear()
local_client = LocalClient(os.getcwd(), "data", "data_remote")

while True:
    try:
        local_client.handle_input()
    except KeyboardInterrupt:
        sys.exit(0)
