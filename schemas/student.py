import datetime
from pydantic import BaseModel, Field, EmailStr


class StudentCreate(BaseModel):
    student_name: str = Field(max_length=40)
    student_email: EmailStr
    year_enrolled: datetime.date
    #courses: list = []


class ShowStudent(BaseModel):
    student_id: int
    student_name: str
    student_email: EmailStr
    year_enrolled: datetime.date

    class ConfigDict:
        from_attributes = True
