# File contains all schemas for Student, Course & Teacher

import datetime
from pydantic import BaseModel, Field, EmailStr, ValidationError, field_validator
from typing import Optional, List, Union


class NewCourse(BaseModel):
    course_name: str = Field(min_length=2)


class ShowCourse(BaseModel):
    course_id: int
    course_name: str
    course_status: bool

    class ConfigDict:
        from_attributes = True


class UpdateCourse(BaseModel):
    course_id: int = Field(gt=0)
    course_name: str = Field(min_length=2)
    '''@field_validator('course_name')
    def length_gt_2(cls, course_length):
        if course_length == "":
            raise ValueError("empty field")
        return course_length'''


class SingleCourse(BaseModel):
    course_id: int = Field(gt=0)


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


class UpdateStudent(BaseModel):
    student_id: int = Field(gt=0)
    student_name: Optional[str] = None
    student_email: Optional[EmailStr] = None
    year_enrolled: Optional[datetime.date] = None


class SingleStudent(BaseModel):
    student_id: int = Field(gt=0)


class DisenrollStudent(BaseModel):
    student_id: int = Field(gt=0)
    course_id: int = Field(gt=0)


class MigrateStudent(BaseModel):
    student_id: int = Field(gt=0)
    from_course_id: int = Field(gt=0)
    to_course_id: int = Field(gt=0)


class NewTeacher(BaseModel):
    teacher_name: str = Field(min_length=3)
    teacher_email: EmailStr
    assign_course: list = []


class ShowTeacher(BaseModel):
    teacher_id: int
    teacher_name: str = Field(min_length=3)
    teacher_email: EmailStr

    class ConfigDict:
        from_attribute = True


class UpdateTeacher(BaseModel):
    teacher_id: int = Field(gt=0)
    teacher_name: Optional[str] = None
    teacher_email: Optional[EmailStr] = None


class SingleTeacher(BaseModel):
    teacher_id: int = Field(gt=0)


class DisassignTeacher(BaseModel):
    teacher_id: int = Field(gt=0)
    course_id: int = Field(gt=0)


class TeacherSchema(ShowTeacher):
    assigned_courses: List[ShowCourse]


class StudentSchema(ShowStudent):
    courses: List[ShowCourse]


class CourseSchema(ShowCourse):
    students: List[ShowStudent]
    teachers: List[ShowTeacher]








