from db.base_class import Base

from sqlalchemy import Column, String, Integer


class Teacher(Base):
    teacher_id = Column(Integer, autoincrement=True, primary_key=True)
    teacher_name = Column(String, nullable=False)
    teacher_email = Column(String, nullable=False, unique=True)
