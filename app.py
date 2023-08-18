# Imports
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

# App Configurations
app = Flask(__name__)

app.debug = True

app.config['SECRET_KEY'] = '1Hav3AS3cr3t'

