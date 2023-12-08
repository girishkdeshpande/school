from db.base_class import Base

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..models.student import Student


class Course(Base):
    course_id = Column(Integer, autoincrement=True, primary_key=True)
    course_name = Column(String, nullable=False, unique=True)

    students = relationship("Student", back_populates="courses")
