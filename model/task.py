from sqlalchemy import Column, Integer, String, ForeignKey
from database import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status_id = Column(Integer)
    priority_id = Column(Integer)
    effort_points = Column(Integer)
    estimation = Column(Integer)
    progress = Column(Integer)
    task_type_id = Column(Integer)
    sprint_id = Column(Integer, ForeignKey('sprints.id'))
    assignee_id = Column(Integer, ForeignKey('users.id'))
