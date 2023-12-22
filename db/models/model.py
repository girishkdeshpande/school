# File contains models of master tables & child tables

from core.config import Base
import datetime

from sqlalchemy import String, Integer, Column, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = "course"

    course_id = Column(Integer, autoincrement=True, primary_key=True)
    course_name = Column(String, nullable=False, unique=True)
    course_status = Column(Boolean, nullable=False, default=True)

    students = relationship("Student", secondary="coursestudent", back_populates="courses")
    teachers = relationship("Teacher", secondary="courseteacher", back_populates="assigned_courses")


class Student(Base):
    __tablename__ = "student"

    student_id = Column(Integer, autoincrement=True, primary_key=True)
    student_name = Column(String, nullable=False)
    student_email = Column(String, nullable=False, unique=True)
    year_enrolled = Column(Date, default=datetime.datetime.year)
    student_status = Column(Boolean, nullable=False, default=True)

    courses = relationship("Course", secondary="coursestudent", back_populates="students")


class Teacher(Base):
    __tablename__ = "teacher"

    teacher_id = Column(Integer, autoincrement=True, primary_key=True)
    teacher_name = Column(String, nullable=False)
    teacher_email = Column(String, nullable=False, unique=True)
    teacher_status = Column(Boolean, nullable=False, default=True)

    assigned_courses = relationship("Course", secondary="courseteacher", back_populates="teachers")


class CourseTeacher(Base):
    __tablename__ = "courseteacher"

    teacher_id = Column(Integer, ForeignKey("teacher.teacher_id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("course.course_id"), primary_key=True)


class CourseStudent(Base):
    __tablename__ = "coursestudent"

    student_id = Column(Integer, ForeignKey("student.student_id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("course.course_id"), primary_key=True)
