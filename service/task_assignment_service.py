from database import db
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sqlalchemy import text


def to_dict(db_object):
    return {c.name: getattr(db_object, c.name) for c in db_object.__table__.columns}


def get_suggestion(priority, effort_points, type):
    new_task = np.array([priority, effort_points, type])
    task_user_association = get_task_user_association()

    final_similarity_scores = []

    for user_id, tasks in task_user_association.items():
        cosine_similarity_scores = calculate_cosine_similarity(new_task, tasks)
        jaccard_similarity_scores = calculate_jaccard_similarity(new_task, tasks)
        combined_similarity_scores = np.mean([cosine_similarity_scores, jaccard_similarity_scores], axis=0)
        final_similarity_score = np.mean(combined_similarity_scores)
        final_similarity_scores.append(final_similarity_score)

    best_user_id = list(task_user_association.keys())[np.argmax(final_similarity_scores)]

    return best_user_id


def get_task_user_association():
    query = text("""
        SELECT assignee_id, ARRAY[priority_id, effort_points, task_type_id] AS task_details
        FROM tasks
        ORDER BY assignee_id
    """)

    res = db.session.execute(query)

    tasks_by_user = {}

    for row in res:
        if row.assignee_id not in tasks_by_user:
            tasks_by_user[row.assignee_id] = []
        tasks_by_user[row.assignee_id].append(row.task_details)

    for assignee_id, tasks in tasks_by_user.items():
        tasks_by_user[assignee_id] = np.array(tasks)
    return tasks_by_user


def calculate_cosine_similarity(new_task, tasks):
    cosine_similarity_scores = cosine_similarity([new_task[:2]], tasks[:, :2])[0]
    return cosine_similarity_scores


def calculate_jaccard_similarity(new_task, tasks):
    jaccard_similarity_scores = []
    for task in tasks:
        intersection = np.intersect1d(new_task[2:], task[2:]).size
        union = np.union1d(new_task[2:], task[2:]).size
        similarity = intersection / union
        jaccard_similarity_scores.append(similarity)

    return jaccard_similarity_scores

