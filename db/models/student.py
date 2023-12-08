import datetime
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import relationship

from db.base_class import Base


class Student(Base):
    student_id = Column(Integer, autoincrement=True, primary_key=True)
    student_name = Column(String, nullable=False)
    student_email = Column(String, nullable=False, unique=True)
    year_enrolled = Column(Date, default=datetime.datetime.year)

    courses = relationship("Course", back_populates="students")







