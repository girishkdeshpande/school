from pydantic import BaseModel, Field, EmailStr


class TeacherCreate(BaseModel):
    #teacher_id: int
    teacher_name: str = Field(max_length=40)
    teacher_email: EmailStr


class ShowTeacher(BaseModel):
    teacher_id: int
    teacher_name: str
    teacher_email: EmailStr

    class ConfigDict:
        from_attribute = True
