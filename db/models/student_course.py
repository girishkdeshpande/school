from sqlalchemy import Integer, Column, ForeignKey
from db.base_class import Base


class StudentCourse(Base):
    index = Column(Integer, primary_key=True)
    stud_id = Column(Integer, ForeignKey("student.student_id"))
    cors_id = Column(Integer, ForeignKey("course.course_id"))
