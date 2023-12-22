# File contains apis for Teacher
import logging
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
from schemas.schema import NewTeacher, TeacherSchema, UpdateTeacher, SingleTeacher, DisassignTeacher
from core.config import get_db, special_str
from db.models.model import Teacher, CourseTeacher

router = APIRouter()
logger = logging.getLogger('school')


# Add new teacher
@router.post("/teacher")
def new_teacher(teacher: NewTeacher, db: Session = Depends(get_db)):
    try:
        # Checking teacher name for special characters
        logger.info("Checking whether teacher name has special characters")
        if special_str.search(teacher.teacher_name):
            return JSONResponse({"Message": "Teacher name field should have characters", "Status": 406},
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)

        # Checking teacher for unique email
        logger.info("Checking for unique email address")
        if db.query(Teacher).filter(Teacher.teacher_email == teacher.teacher_email).first():
            logger.error(f"Email id already exists")
            return JSONResponse({"Message": f"Email {teacher.teacher_email} already exists", "Status": 406},
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)

        # Creating instance for new teacher
        logger.info("Creating instance of teacher to add in database")
        add_teacher = Teacher(
            teacher_name=teacher.teacher_name.title(),
            teacher_email=teacher.teacher_email
            )
        # Adding instance to database
        logger.info("Adding new teacher into database")
        db.add(add_teacher)
        db.commit()
        db.refresh(add_teacher)

        # Adding courses which teacher teaches
        logger.info("Adding courses assigned to new teacher into database")
        for course in teacher.assign_course:
            add_course = CourseTeacher(
                teacher_id=add_teacher.teacher_id,
                course_id=course
            )
            db.add(add_course)
            db.commit()
            db.refresh(add_course)

        logger.info(f"Teacher {teacher.teacher_name} added successfully with course(s) {teacher.assign_course}")
        return JSONResponse({"Message": f"Teacher {teacher.teacher_name} added successfully for courses {teacher.assign_course}",
                            "Status": 200}, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later", "Status": 500},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View teacher details by teacher id
@router.get("/teacher", response_model=TeacherSchema)
def view_teacher(data: SingleTeacher, db: Session = Depends(get_db)):
    try:
        # Checking for teacher exists or not
        logger.info(f"Checking for presence of teacher id {data.teacher_id}")
        single_teacher = db.query(Teacher).filter(Teacher.teacher_id == data.teacher_id).first()
        if single_teacher:
            logger.info(f"Teacher id {data.teacher_id} is present.Returned teacher details")
            return single_teacher
        else:
            logger.error(f"Teacher id {data.teacher_id} does not exist")
            return JSONResponse({"Message": f"Teacher id {data.teacher_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": f"An unexpected error {e} occurred. Please try again later", "Status": 500},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View all teacher's details
@router.get("/teachers", response_model=List[TeacherSchema])
def view_all_teachers(db: Session = Depends(get_db)):
    try:
        # Checking for availability of teachers & reverting if available
        logger.info("Checking whether database is empty or not")
        all_teacher = db.query(Teacher).all()
        if all_teacher:
            logger.info("Database is not empty. Records returned")
            return all_teacher
        else:
            logger.info("Database is not having any records")
            return JSONResponse({"Message": "Not a single record(s) found", "Status": 204},
                                status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later", "Status": 500},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete teacher / Hard Delete
@router.delete("/teacher")
def complete_delete_teacher(data: SingleTeacher, db: Session = Depends(get_db)):
    try:
        # Checking for teacher exists or not
        logger.info(f"Checking for presence of teacher id {data.teacher_id}")
        single_teacher = db.query(Teacher).filter(Teacher.teacher_id == data.teacher_id).first()
        if single_teacher:
            db.delete(single_teacher)
            db.commit()
            logger.info(f"Teacher id {data.teacher_id} is present. Record deleted")
            return JSONResponse({"Message": f"Teacher id {data.teacher_id} deleted successfully", "Status": 200},
                                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Teacher id {data.teacher_id} does not exist")
            return JSONResponse({"Message": f"Teacher id {data.teacher_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later", "Status": 500},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Disassign teacher from course
@router.delete("/teacher")
def disassign_teacher(data: DisassignTeacher, db: Session = Depends(get_db)):
    try:
        # Checking for record with given teacher id & course id. Deleting if available.
        logger.info(f"Checking for record of student id {data.teacher_id} against course id {data.course_id}")
        course = db.query(CourseTeacher).filter(and_(CourseTeacher.teacher_id == data.teacher_id,
                                                CourseTeacher.course_id == data.course_id)).first()
        if course:
            db.delete(course)
            db.commit()
            logger.info("Record exist.Record deleted")
            return JSONResponse({"Message": f"Teacher id {data.teacher_id} disassigned from course {data.course_id}",
                                 "Status": 200}, status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Teacher id {data.teacher_id} not assigned for course {data.course_id}")
            return JSONResponse({"Message": f"Teacher with id {data.teacher_id} not assigned for course {data.course_id}",
                                 "Status": 404}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later", "Status": 500},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Change status of teacher
@router.patch("/teacher")
def delete_teacher(data: SingleTeacher, db: Session = Depends(get_db)):
    try:
        # Checking for teacher exists & changing status if exists
        logger.info(f"Checking for presence of teacher id {data.teacher_id}")
        teacher = db.query(Teacher).filter(and_(Teacher.teacher_id == data.teacher_id,
                                           Teacher.teacher_status == True)).first()
        if teacher:
            teacher.teacher_status = False
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            logger.info(f"Teacher id {data.teacher_id} present. Status changed")
            return JSONResponse({"Message": f"Status of teacher id {data.teacher_id} changed successfully", "Status": 200},
                                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Teacher id {data.teacher_id} not found")
            return JSONResponse({"Message": f"Teacher with id {data.teacher_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later", "Status": 500},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Update master record of teacher
@router.put("/teacher", response_model=UpdateTeacher)
def update_teacher(data: UpdateTeacher, db: Session = Depends(get_db)):
    try:
        if data.teacher_name == "":
            return JSONResponse({"Message": "All fields are mandatory", "Status": 406},
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)

        # Checking for teacher exists & updating record if available
        logger.info(f"Checking for presence of teacher id {data.teacher_id}")
        teacher = db.query(Teacher).filter(Teacher.teacher_id == data.teacher_id).first()
        if teacher:
            teacher.teacher_name = data.teacher_name.title()
            teacher.teacher_email = data.teacher_email
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            logger.info(f"Teacher id {data.teacher_id} exist. Record updated")
            return JSONResponse({"Message": f"Record of teacher id {data.teacher_id} updated successfully", "Status": 200},
                                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Teacher id {data.teacher_id} not found")
            return JSONResponse({"Message": f"Teacher id {data.teacher_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later", "Status": 500},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
