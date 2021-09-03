import os
from . import vigenere
from flask import Flask
from werkzeug.utils import redirect

ACCOUNT_ID = os.environ.get("ACCOUNT_ID")
BCOV_POLICY = os.environ.get("BCOV_POLICY")
KEY = os.environ.get("KEY")
DIRECT = os.environ.get("DIRECT", 'False').lower() in (1, 'true')

app = Flask(__name__)

from .views import *
