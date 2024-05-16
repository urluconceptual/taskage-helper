from flask import Flask
from sqlalchemy import text
from controller.task_assignment import task_assignment_blueprint
from database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/taskage'
db.init_app(app)

app.register_blueprint(task_assignment_blueprint, url_prefix='/assignment')

if __name__ == '__main__':
    app.run()