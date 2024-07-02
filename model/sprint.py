from sqlalchemy import Column, Integer, ForeignKey, DateTime

from database import db


class Sprint(db.Model):
    __tablename__ = 'sprints'

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    start_date = Column('start_date', DateTime)
    end_date = Column('end_date', DateTime)
