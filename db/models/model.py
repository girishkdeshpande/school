from core.config import Base
import datetime

from typing import List
from sqlalchemy import String, Integer, Column, ForeignKey, Date
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = "course"

    course_id = Column(Integer, autoincrement=True, primary_key=True)
    course_name = Column(String, nullable=False, unique=True)

    students = relationship("Student", secondary="studentcourse", back_populates="courses")


class Student(Base):
    __tablename__ = "student"

    student_id = Column(Integer, autoincrement=True, primary_key=True)
    student_name = Column(String, nullable=False)
    student_email = Column(String, nullable=False, unique=True)
    year_enrolled = Column(Date, default=datetime.datetime.year)

    courses = relationship("Course", secondary="studentcourse", back_populates="students")


class StudentCourse(Base):
    __tablename__ = "studentcourse"

    student_id = Column(Integer, ForeignKey("student.student_id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("course.course_id"), primary_key=True)


class Teacher(Base):
    __tablename__ = "teacher"

    teacher_id = Column(Integer, autoincrement=True, primary_key=True)
    teacher_name = Column(String, nullable=False)
    teacher_email = Column(String, nullable=False, unique=True)


class TeacherCourse(Base):
    __tablename__ = "teachercourse"

    teacher_id = Column(Integer, ForeignKey("teacher.teacher_id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("course.course_id"), primary_key=True)
