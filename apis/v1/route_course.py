# File contains apis for Course
import logging

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_, or_

from schemas.schema import CourseSchema, NewCourse, UpdateCourse, SingleCourse
from core.config import get_db, special_str
from db.models.model import Course

router = APIRouter()
logger = logging.getLogger('school')


# Add new course
@router.post("/course", response_model=NewCourse)
def add_new_course(data: NewCourse, db: Session = Depends(get_db)):
    try:
        # Checking for special characters
        logger.info("Checking whether having special characters")
        if special_str.search(data.course_name):
            logger.error("Course name has special characters")
            return JSONResponse({"Message": "Course name should be alphanumeric", "Status": 406},
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)

        # Checking course name already exists or not
        logger.info("Checking course already exists or not")
        if db.query(Course).filter(or_(Course.course_name == data.course_name.title(),
                                       Course.course_name == data.course_name.upper())).one_or_none():
            logger.error("Course Name already exists")
            return JSONResponse({"Message": "Course Name already exist", "Status": 409},
                                status_code=status.HTTP_409_CONFLICT)

        # Creating instance for new course and adding to database
        logger.info("Creating instance for new course")
        new_course = Course(course_name=data.course_name.title())
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        logger.info("New Course added into database")
        return JSONResponse({"Message": f"Course {data.course_name} added successfully", "Status": 200},
                            status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View course by course id
@router.get("/course/", response_model=CourseSchema)
def view_course(course_id: int, db: Session = Depends(get_db)):
    try:
        # Checking course id exists or not & reverting if available
        logger.info("Checking course id exists or not")
        course = db.query(Course).filter(and_(Course.course_id == course_id,
                                              Course.course_status == True)).first()
        if course:
            logger.info(f"Course id {course_id} exists. Returning details")
            return course
        else:
            logger.error(f"Course id {course_id} not found")
            return JSONResponse({"Message": f"Course id {course_id} does not exist", "Status": 404},
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
@router.delete("/course")
def complete_delete_course(data: SingleCourse, db: Session = Depends(get_db)):
    try:
        # Checking availability of course for given course id
        logger.info(f"Checking course id {data.course_id} exists or not")
        course = db.query(Course).filter(Course.course_id == data.course_id).first()

        # Deleting record
        if course:
            db.delete(course)
            db.commit()
            logger.info(f"course id {data.course_id} exists. Record deleted")
            return JSONResponse({"Message": f"Successfully deleted Course {course.course_name}", "Status": 200},
                                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Course with id {data.course_id} does not exist")
            return JSONResponse({"Message": f"Course id {data.course_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete course by course id / Soft Delete
@router.patch("/course/")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        # Checking availability of course for given course id
        logger.info(f"Checking course id {course_id} exists or not")
        course = db.query(Course).filter(
            and_(Course.course_id == course_id, Course.course_status == True)).first()

        # Changing status
        if course:
            course.course_status = False
            db.add(course)
            db.commit()
            db.refresh(course)
            logger.info(f"Course id {course_id} exists. Status changed to False")
            return JSONResponse(
                {"Message": f"Status changed successfully for course {course.course_name}", "Status": 200},
                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Course id {course_id} does not exist")
            return JSONResponse({"Message": f"Course with id {course_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later", "Status": 500},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Updating master Course
@router.put("/course")
def update_course(data: UpdateCourse, db: Session = Depends(get_db)):
    try:
        # Checking availability of course for given course id
        logger.info(f"Checking course id {data.course_id} exists or not")
        course = db.query(Course).filter(and_(Course.course_id == data.course_id,
                                              Course.course_status == True)).first()

        # Updating record
        if course:
            logger.info("Checking course already exists or not")
            if db.query(Course).filter(or_(Course.course_name == data.course_name.title(),
                                       Course.course_name == data.course_name.upper())).one_or_none():
                logger.error("Course Name already exists")
                return JSONResponse({"Message": "Course Name already exist", "Status": 409},
                                    status_code=status.HTTP_409_CONFLICT)
            else:
                course.course_name = data.course_name.title()
                db.add(course)
                db.commit()
                db.refresh(course)
                logger.info(f"Course id {data.course_id} exists. Record updated")
                return JSONResponse({"Message": f"Record of course id {data.course_id} updated successfully", "Status": 200},
                                    status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Course id {data.course_id} does not exist")
            return JSONResponse({"Message": f"Course id {data.course_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later", "Status": 500},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
