from flask import Flask
from src.course import course
from src.home import home

def create_app() -> Flask:
	app = Flask(__name__)
	app.register_blueprint(course)
	app.register_blueprint(home)
	
	return app