# File contains apis for Course

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from schemas.schema import CourseSchema, NewCourse, UpdateCourse
from core.config import get_db, special_str
from db.models.model import Course

router = APIRouter()


# Add new course
@router.post("/course")
def add_new_course(course: NewCourse, db: Session = Depends(get_db)):
    try:
        # Checking input for empty, special characters and course name already exists
        if course.course_name == "":
            return JSONResponse(content="Course name should not be empty", status_code=status.HTTP_400_BAD_REQUEST)

        elif special_str.search(course.course_name):
            return JSONResponse(content="Course name should be alphanumeric",
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)

        elif db.query(Course).filter(
                Course.course_name == course.course_name.title() or Course.course_name == course.course_name.upper()).first():
            return JSONResponse(content="Course Name already exist", status_code=status.HTTP_409_CONFLICT)
        else:
            # Creating instance for new course and adding to database
            new_course = Course(course_name=course.course_name.title())
            db.add(new_course)
            db.commit()
            db.refresh(new_course)
            return JSONResponse(content="Course added successfully", status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content="Failed to add new course", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View course by course id
@router.get("/course/{course_id}", response_model=CourseSchema)
def view_course(course_id: int, db: Session = Depends(get_db)):
    try:
        # Checking for availability of course id & reverting if available
        course = db.query(Course).filter(Course.course_id == course_id).first()
        if course:
            return course
        else:
            return JSONResponse(content=f"Course with id {course_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View all courses
@router.get("/courses", response_model=list[CourseSchema])
def view_all_course(db: Session = Depends(get_db)):
    try:
        # Checking for availability & reverting if available
        courses = db.query(Course).all()
        if courses:
            return courses
        else:
            return JSONResponse(content="Course table is empty", status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete course by course id / Hard Delete
@router.delete("/course/{course_id}")
def complete_delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        # Checking availability of course for given course id
        course = db.query(Course).filter(Course.course_id == course_id).first()

        # Deleting record
        if course:
            db.delete(course)
            db.commit()
            return JSONResponse(content=f"Successfully deleted Course {course.course_name}", status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content=f"Course with id {course_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete course by course id / Soft Delete
@router.patch("/course/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        # Checking availability of course for given course id
        course = db.query(Course).filter(Course.course_id == course_id).first()

        # Updating record
        if course:
            course.course_status = "Inactive"
            db.add(course)
            db.commit()
            db.refresh(course)
            return JSONResponse(content=f"Status changed successfully for {course_id}", status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content=f"Course with id {course_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Updating records of Course
@router.put("/course/{course_id}", response_model=UpdateCourse)
def update_course(course_id: int, update_data: UpdateCourse, db: Session = Depends(get_db)):
    try:
        # Checking availability of course for given course id
        course = db.query(Course).filter(Course.course_id == course_id).first()

        # Updating record
        if course:
            course.course_name = update_data.course_name.title()
            db.add(course)
            db.commit()
            db.refresh(course)
            return JSONResponse(content=f"Record of id {course_id} updated successfully", status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content=f"Course with id {course_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
