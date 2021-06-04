from flask import Flask
from .utils import tokenize

app = Flask(__name__)

from app import run
app.run(debug=True)