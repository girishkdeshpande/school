# File contains apis for Course
import logging
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import or_

from schemas.schema import CourseSchema, NewCourse, UpdateCourse
from core.config import get_db, special_str
from db.models.model import Course

router = APIRouter()
logger = logging.getLogger('school')


# Add new course
@router.post("/course")
def add_new_course(course: NewCourse, db: Session = Depends(get_db)):
    try:
        # Checking input for empty, special characters and course name already exists
        logger.info("Checking whether course name is None or having special characters or already exists")
        course = course.model_dump()
        if course['course_name'] == "":
            logger.error("Course name is None")
            return JSONResponse({"Message": "Course name should not be empty", "Status": 400},
                                status_code=status.HTTP_400_BAD_REQUEST)

        elif special_str.search(course['course_name']):
            logger.error("Course name has special characters")
            return JSONResponse({"Message": "Course name should be alphanumeric", "Status": 406},
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)

        elif db.query(Course).filter(Course.course_name.ilike(course['course_name'])):
            logger.error("Course Name already exists")
            return JSONResponse({"Message": "Course Name already exist", "Status": 409},
                                status_code=status.HTTP_409_CONFLICT)

        # Creating instance for new course and adding to database
        logger.info("Creating instance for new course")
        new_course = Course(course_name=course['course_name'].title())
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        logger.info("New Course added into database")
        return JSONResponse({"Message": f"Course {course['course_name']} added successfully", "Status": 200},
                            status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View course by course id
@router.get("/course/{course_id}", response_model=CourseSchema)
def view_course(course_id: int, db: Session = Depends(get_db)):
    try:
        # Checking course id exists or not & reverting if available
        logger.info("Checking course id exists or not")
        course = db.query(Course).filter(Course.course_id == course_id).first()
        if course:
            logger.info(f"{course_id} exists. Returning details")
            return course
        else:
            logger.error(f"Course id {course_id} not found")
            return JSONResponse({"Message": f"Course with id {course_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View all courses
@router.get("/courses", response_model=list[CourseSchema])
def view_all_course(db: Session = Depends(get_db)):
    try:
        # Checking for availability & reverting if available
        logger.info("Checking records exists or not")
        courses = db.query(Course).all()
        if courses:
            logger.info("Records exists. Returned details")
            return courses
        else:
            logger.error("Not single record(s) found")
            return JSONResponse({"Message": "Not single record(s) found", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete course by course id / Hard Delete
@router.delete("/course/{course_id}")
def complete_delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        # Checking availability of course for given course id
        logger.info(f"Checking course id {course_id} exists or not")
        course = db.query(Course).filter(Course.course_id == course_id).first()

        # Deleting record
        if course:
            db.delete(course)
            db.commit()
            logger.info(f"course id {course_id} exists. Record deleted")
            return JSONResponse({"Message": f"Successfully deleted Course {course.course_name}", "Status": 200},
                                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Course with id {course_id} does not exist")
            return JSONResponse({"Message": f"Course with id {course_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete course by course id / Soft Delete
@router.patch("/course/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        # Checking availability of course for given course id
        logger.info(f"Checking course id {course_id} exists or not")
        course = db.query(Course).filter(Course.course_id == course_id).first()

        # Updating record
        if course:
            course.course_status = "Inactive"
            db.add(course)
            db.commit()
            db.refresh(course)
            logger.info(f"Course id {course_id} exists. Status changed")
            return JSONResponse({"Message": f"Status changed successfully for course id {course_id}", "Status": 200},
                                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Course with id {course_id} does not exist")
            return JSONResponse({"Message": f"Course with id {course_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Updating master Course
@router.put("/course/{course_id}", response_model=UpdateCourse)
def update_course(course_id: int, update_data: UpdateCourse, db: Session = Depends(get_db)):
    try:
        update_data = update_data.model_dump()
        # Checking availability of course for given course id
        logger.info(f"Checking course id {course_id} exists or not")
        course = db.query(Course).filter(Course.course_id == course_id).first()

        # Updating record
        if course:
            course.course_name = update_data['course_name'].title()
            db.add(course)
            db.commit()
            db.refresh(course)
            logger.info(f"Course id {course_id} exists. Record updated")
            return JSONResponse({"Message": f"Record of course id {course_id} updated successfully", "Status": 200},
                                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Course id {course_id} does not exist")
            return JSONResponse({"Message": f"Course id {course_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
