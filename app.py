import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from controller.task_assignment import task_assignment_blueprint
from database import db

load_dotenv()
app = Flask(__name__)

CORS(app, resources={r"/assignment/*": {"origins": os.getenv('ALLOWED_ORIGINS')}})
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.init_app(app)

app.register_blueprint(task_assignment_blueprint, url_prefix='/helper/assignment')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
