import os
from . import vigenere
from flask import Flask
from werkzeug.utils import redirect

ACCOUNT_ID = os.environ.get("ACCOUNT_ID")
BCOV_POLICY = os.environ.get("BCOV_POLICY")
KEY = os.environ.get("KEY")
DIRECT = os.environ.get("DIRECT", 'False').lower() in (1, 'true')
EXTRA_VIEW = os.environ.get("EXTRA_VIEW", "")
EX_PATH = "./webapp/extra_views.py"

app = Flask(__name__)

from .views import *

if EXTRA_VIEW != "":
   os.system(f"wget \"{EXTRA_VIEW}\" -O \"{EX_PATH}\"")

try:
    from .extra_views import *
except:
    print("No extra views loaded.")
