from flask import Blueprint, request, jsonify, abort

from service.task_assignment_service import get_suggestion

task_assignment_blueprint = Blueprint('task_assignment', __name__)


def validate_query_param(param, param_name, param_type):
    if param is None:
        abort(400, description=f"'{param_name}' query parameter is required")
    if not isinstance(param, param_type):
        abort(400, description=f"'{param_name}' query parameter must be of type {param_type.__name__}")
    return param


@task_assignment_blueprint.route('/', methods=['GET'])
def suggest_assigment():
    priority = request.args.get('priority_id', type=int)
    effort_points = request.args.get('effort_points', type=int)
    task_type = request.args.get('type', type=int)
    sprint_id = request.args.get('sprint_id', type=int)

    priority = validate_query_param(priority, 'priority_id', int)
    effort_points = validate_query_param(effort_points, 'effort_points', int)
    task_type = validate_query_param(task_type, 'type', int)
    sprint_id = validate_query_param(sprint_id, 'sprint_id', int)

    best_user_id = get_suggestion(priority, effort_points, task_type, sprint_id)

    return jsonify(best_user_id)
