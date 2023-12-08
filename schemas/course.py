from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    #course_id: int
    course_name: str = Field(max_length=40)


class ShowCourse(BaseModel):
    course_id: int
    course_name: str = Field(max_length=40)
