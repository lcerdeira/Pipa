from flask import Flask
from extensions.config import init_app, load_modules

def create_app():
  app = Flask(__name__)
  init_app(app)
  load_modules(app)
  return app
