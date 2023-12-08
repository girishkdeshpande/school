import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List


class CourseBase(BaseModel):
    course_name: str = Field(max_length=40)

    class ConfigDict:
        from_attributes = True


class StudentBase(BaseModel):
    student_name: str = Field(max_length=40)
    student_email: EmailStr
    year_enrolled: datetime.date
    course_enrolled: list = []

    class ConfigDict:
        from_attributes = True


class ShowCourse(CourseBase):
    course_id: int


class CourseSchema(CourseBase):
    students: List[StudentBase]


class StudentSchema(StudentBase):
    courses: List[CourseBase]


class TeacherBase(BaseModel):
    teacher_name: str = Field(max_length=40)
    teacher_email: EmailStr
    assign_course: list = []

    class ConfigDict:
        from_attribute = True


class TeacherSchema(TeacherBase):
    courses: List[CourseBase]

