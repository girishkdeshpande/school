# File contains all schemas for Student, Course & Teacher

import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Union


class NewCourse(BaseModel):
    course_name: str = Field(min_length=2)


class ShowCourse(BaseModel):
    course_id: int
    course_name: str

    class ConfigDict:
        from_attributes = True


class NewStudent(BaseModel):
    student_name: str = Field(min_length=3)
    student_email: EmailStr
    year_enrolled: datetime.date
    course_enrolled: list = []


class ShowStudent(BaseModel):
    student_id: int
    student_name: str
    student_email: EmailStr
    year_enrolled: datetime.date

    class ConfigDict:
        from_attributes = True


class NewTeacher(BaseModel):
    teacher_name: str = Field(min_length=3)
    teacher_email: EmailStr
    assign_course: list = []


class ShowTeacher(BaseModel):
    teacher_id: int
    teacher_name: str = Field(max_length=40)
    teacher_email: EmailStr

    class ConfigDict:
        from_attribute = True


class TeacherSchema(ShowTeacher):
    assigned_courses: List[ShowCourse]


class CourseSchema(ShowCourse):
    students: List[ShowStudent]
    teachers: List[ShowTeacher]


class StudentSchema(ShowStudent):
    courses: List[ShowCourse]


class UpdateTeacher(BaseModel):
    teacher_name: Optional[str] = None
    teacher_email: Optional[EmailStr] = None


class UpdateStudent(BaseModel):
    student_name: Optional[str] = None
    student_email: Optional[EmailStr] = None
    year_enrolled: Optional[datetime.date] = None


class UpdateCourse(BaseModel):
    course_name: Optional[str] = None


