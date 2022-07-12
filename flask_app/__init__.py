from flask import Flask
app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()
import os
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
port = os.getenv('PORT')
