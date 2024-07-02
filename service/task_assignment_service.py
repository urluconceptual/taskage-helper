import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import text

from database import db


def get_suggestion(priority, effort_points, task_type, sprint_id):
    new_task = [priority, effort_points, task_type]
    past_tasks = get_past_tasks()
    team_capacity = get_team_capacity(sprint_id)

    normalized_new_task, normalized_past_tasks = normalize_data(new_task, past_tasks)
    task_user_association = get_task_user_association(normalized_past_tasks)

    final_similarity_scores = calculate_similarity_scores(normalized_new_task, task_user_association, team_capacity,
                                                          effort_points)

    best_user_id = list(task_user_association.keys())[np.argmax(final_similarity_scores)]

    return best_user_id


def calculate_similarity_scores(normalized_new_task, task_user_association, team_capacity, effort_points):
    return [
        calculate_user_similarity_score(normalized_new_task, tasks, team_capacity.get(user_id, 0), effort_points)
        for user_id, tasks in task_user_association.items()
    ]


def calculate_user_similarity_score(normalized_new_task, tasks, user_capacity, task_effort_points):
    cosine_similarity_scores = calculate_cosine_similarity(np.array(normalized_new_task[:2]), tasks[:, :2])
    jaccard_similarity_scores = calculate_jaccard_similarity(np.array(normalized_new_task[2:]), tasks[:, 2:])
    combined_similarity_scores = np.mean([cosine_similarity_scores, jaccard_similarity_scores], axis=0)
    mean_similarity = np.mean(combined_similarity_scores)

    # Adjust the similarity score based on user capacity
    capacity_adjustment = 1 if user_capacity >= task_effort_points else user_capacity / task_effort_points
    final_score = mean_similarity * capacity_adjustment

    return final_score


def get_past_tasks():
    query = text("""
        SELECT assignee_id, ARRAY[priority_id, effort_points, task_type_id] AS task_details
        FROM tasks
        ORDER BY assignee_id
    """)
    return db.session.execute(query).fetchall()


def normalize_data(new_task, past_tasks):
    scaler = MinMaxScaler()
    all_tasks = [new_task[:2]] + [task.task_details[:2] for task in past_tasks]
    scaler.fit(all_tasks)

    normalized_new_task = transform_data(scaler, new_task)
    normalized_past_tasks = [(user_id, transform_data(scaler, task)) for user_id, task in past_tasks]

    return [normalized_new_task, normalized_past_tasks]


def transform_data(scaler, task):
    normalized_new_task_values = scaler.transform([task[:2]])[0]
    normalized_new_task = [normalized_new_task_values[0], normalized_new_task_values[1], task[2]]
    return normalized_new_task


def get_task_user_association(normalized_past_tasks):
    tasks_by_user = {}
    for assignee_id, task_details in normalized_past_tasks:
        if assignee_id not in tasks_by_user:
            tasks_by_user[assignee_id] = []
        tasks_by_user[assignee_id].append(task_details)
    for assignee_id, tasks in tasks_by_user.items():
        tasks_by_user[assignee_id] = np.array(tasks)
    return tasks_by_user


def calculate_cosine_similarity(new_task, tasks):
    cosine_similarity_scores = cosine_similarity([new_task], tasks)[0]
    return np.array(cosine_similarity_scores)


def calculate_jaccard_similarity(new_task, tasks):
    jaccard_similarity_scores = [
        calculate_single_jaccard_similarity(new_task, task)
        for task in tasks
    ]
    return jaccard_similarity_scores


def calculate_single_jaccard_similarity(new_task, task):
    intersection = np.intersect1d(new_task, task).size
    union = np.union1d(new_task, task).size
    return intersection / union


def get_team_capacity(sprint_id):
    query = text("""
        SELECT t.assignee_id, SUM(t.effort_points) AS total_effort
        FROM tasks t
        WHERE t.sprint_id = :sprint_id
        GROUP BY t.assignee_id
    """)
    result = db.session.execute(query, {'sprint_id': sprint_id}).fetchall()

    capacity = {row['assignee_id']: row['total_effort'] for row in result}
    return capacity
