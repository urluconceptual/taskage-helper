from flask import Blueprint, request, jsonify

from service.task_assignment_service import get_suggestion

task_assignment_blueprint = Blueprint('task_assignment', __name__)


@task_assignment_blueprint.route('/', methods=['GET'])
def suggest_assigment():
    priority = request.args.get('priority_id', type=int)
    effort_points = request.args.get('effort_points', type=int)
    task_type = request.args.get('type', type=int)

    best_user_id = get_suggestion(priority, effort_points, task_type)

    return jsonify(best_user_id)
