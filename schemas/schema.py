# File contains all schemas for Student, Course & Teacher

import datetime
from pydantic import BaseModel, Field, EmailStr, ValidationError, field_validator, PositiveInt, model_validator
from pydantic_core import PydanticCustomError
from typing import Optional, List, Union, Any


class NewCourse(BaseModel):
    course_name: str = Field(..., min_length=2)


class ShowCourse(BaseModel):
    course_id: PositiveInt
    course_name: str
    course_status: bool

    class ConfigDict:
        from_attributes = True


class UpdateCourse(BaseModel):
    course_id: PositiveInt = Field(..., gt=0)
    course_name: str = Field(..., min_length=2)


class SingleCourse(BaseModel):
    course_id: PositiveInt


class NewStudent(BaseModel):
    student_name: str = Field(...,min_length=3)
    student_email: EmailStr
    year_enrolled: datetime.date
    course_enrolled: list = []


class ShowStudent(BaseModel):
    student_id: PositiveInt
    student_name: str = Field(...,min_length=3)
    student_email: EmailStr
    year_enrolled: datetime.date

    class ConfigDict:
        from_attributes = True


class UpdateStudent(BaseModel):
    student_id: PositiveInt = Field(..., gt=0)
    student_name: Optional[str] = None
    student_email: Optional[EmailStr] = None
    year_enrolled: Optional[datetime.date] = None


class SingleStudent(BaseModel):
    student_id: PositiveInt = Field(..., gt=0)


class DisenrollStudent(BaseModel):
    student_id: PositiveInt = Field(..., gt=0)
    course_id: PositiveInt = Field(..., gt=0)


class MigrateStudent(BaseModel):
    student_id: PositiveInt = Field(..., gt=0)
    from_course_id: PositiveInt = Field(..., gt=0)
    to_course_id: PositiveInt = Field(..., gt=0)


class NewTeacher(BaseModel):
    teacher_name: str = Field(..., min_length=3)
    teacher_email: EmailStr
    assign_course: list = []


class ShowTeacher(BaseModel):
    teacher_id: PositiveInt
    teacher_name: str = Field(..., min_length=3)
    teacher_email: EmailStr

    class ConfigDict:
        from_attribute = True


class UpdateTeacher(BaseModel):
    teacher_id: PositiveInt = Field(..., gt=0)
    teacher_name: Optional[str] = None
    teacher_email: Optional[EmailStr] = None


class SingleTeacher(BaseModel):
    teacher_id: PositiveInt = Field(..., gt=0)


class DisassignTeacher(BaseModel):
    teacher_id: PositiveInt = Field(..., gt=0)
    course_id: PositiveInt = Field(..., gt=0)


class TeacherSchema(ShowTeacher):
    assigned_courses: List[ShowCourse]


class StudentSchema(ShowStudent):
    courses: List[ShowCourse]


class CourseSchema(ShowCourse):
    students: List[ShowStudent]
    teachers: List[ShowTeacher]
