from flask import Blueprint, request, jsonify

from model.user import User

task_assignment_blueprint = Blueprint('task_assignment', __name__)


@task_assignment_blueprint.route('/', methods=['GET'])
def suggest_assigment():
    task_id = request.args.get('id')
    users = User.query.all()
    for user in users:
        print(user.username)
    return jsonify(task_id)
