from sqlalchemy import Column, Integer, String, ForeignKey
from database import db


class User(db.Model):
    __tablename__ = 'app_users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    first_name = Column('first_name', String, nullable=False)
    last_name = Column('last_name', String, nullable=False)
    password = Column(String, nullable=False)
    auth_role = Column('auth_role', String, nullable=False)
    job_title_id = Column(Integer, ForeignKey('job_titles.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))
