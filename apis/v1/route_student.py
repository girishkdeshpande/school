# File contains apis for Student
import logging
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
from fastapi import Depends, status, APIRouter
from fastapi.responses import JSONResponse
from typing import List

from schemas.schema import StudentSchema, NewStudent, UpdateStudent, ShowStudent, SingleStudent, DisenrollStudent, MigrateStudent
from core.config import get_db, special_str
from db.models.model import Student, CourseStudent, Course

router = APIRouter()
logger = logging.getLogger('school')


# Enroll new student
@router.post("/student")
def new_student(data: NewStudent, db: Session = Depends(get_db)):
    try:
        # Checking student name for special characters
        logger.info("Checking whether student name has special characters")
        if special_str.search(data.student_name):
            logger.error("Student name has special characters")
            return JSONResponse({"Message": "Student name field should have characters", "Status": 406},
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)

        # Checking student for unique email
        logger.info("Checking for unique email address")
        if db.query(Student).filter(Student.student_email == data.student_email).first():
            logger.error(f"Email {data.student_email} already exists")
            return JSONResponse({"Message": f"Email address {data.student_email} already exists", "Status": 406},
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)

        # Creating instance for new student
        logger.info("Creating instance of student to add in database")
        add_student = Student(
            student_name=data.student_name.title(),
            student_email=data.student_email,
            year_enrolled=data.year_enrolled
        )

        # Adding new student to database
        logger.info("Adding new student into database")
        db.add(add_student)
        db.commit()
        db.refresh(add_student)

        # Adding courses enrolled by student to database
        logger.info("Adding courses enrolled by new student into database")
        for cors in data.course_enrolled:
            if db.query(Course).filter(Course.course_id == cors).first():
                add_course = CourseStudent(student_id=add_student.student_id,
                                           course_id=cors)
                db.add(add_course)
                db.commit()
                db.refresh(add_course)
            else:
                return JSONResponse({"Message": f"Course {cors} not found", "Status": 404},
                                    status_code=status.HTTP_404_NOT_FOUND)

        logger.info("Student added successfully")
        return JSONResponse({
            "Message": f"Student {data.student_name} added successfully with courses {data.course_enrolled}",
            "Status": 200}, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View student by student id
@router.get("/student/", response_model=StudentSchema)
def view_student(student_id: int, db: Session = Depends(get_db)):
    try:
        # Checking student id exists or not
        logger.info(f"Checking for presence of student id {student_id}")
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if student:
            logger.info(f"Student id {student_id} is present.Returned student details")
            return student
        else:
            logger.error(f"Student id {student_id} does not exist")
            return JSONResponse({"Message": f"Student with id {student_id} does not exist",
                                 "Status": 404}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View all student's details
@router.get("/students", response_model=List[StudentSchema])
def view_all_students(db: Session = Depends(get_db)):
    try:
        # Checking student records exists or not
        logger.info("Checking whether database is empty or not")
        all_student = db.query(Student).all()
        if all_student:
            logger.info("Database is not empty. Records returned")
            return all_student
        else:
            logger.info("Database is not having any records")
            return JSONResponse({"Message": "Not a single record(s) found", "Status": 204},
                                status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete Student record by student id / Hard Delete
@router.delete("/student")
def complete_delete_student(data: SingleStudent, db: Session = Depends(get_db)):
    try:
        # Checking for availability of student & deleting if available
        logger.info(f"Checking for presence of student id {data.student_id}")
        student = db.query(Student).filter(Student.student_id == data.student_id).first()
        if student:
            db.delete(student)
            db.commit()
            logger.info(f"Student id {data.student_id} is present. Record deleted")
            return JSONResponse({"Message": f"Student id {data.student_id} deleted successfully", "Status": 200},
                                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Student id {data.student_id} does not exist")
            return JSONResponse({"Message": f"Student id {data.student_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Disenroll student from course
@router.delete("/student")
def disenroll_from_course(data: DisenrollStudent, db: Session = Depends(get_db)):
    try:
        # Checking for record with given student id & course id. Deleting if available.
        logger.info(f"Checking for record of student id {data.student_id} against course id {data.course_id}")
        course = db.query(CourseStudent).filter(and_(CourseStudent.student_id == data.student_id,
                                                     CourseStudent.course_id == data.course_id)).first()
        if course:
            db.delete(course)
            db.commit()
            logger.info("Record exist.Record deleted")
            return JSONResponse(
                {"Message": f"Student id {data.student_id} disenrolled from course {data.course_id}",
                 "Status": 200}, status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Student id {data.student_id} not enrolled for course {data.course_id}")
            return JSONResponse(
                {"Message": f"Student id {data.student_id} not enrolled for course {data.course_id}",
                 "Status": 404}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Change status of student / Soft delete
@router.patch("/student/")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    try:
        # Checking student id exists or not & changing status if available
        logger.info(f"Checking for presence of student id {student_id}")
        student = db.query(Student).filter(and_(Student.student_id == student_id,
                                                Student.student_status == True)).first()
        if student:
            student.student_status = False
            db.add(student)
            db.commit()
            db.refresh(student)
            logger.info(f"Student id {student_id} present. Status changed")
            return JSONResponse({"Message": f"Status of student id {student_id} changed successfully", "Status": 200},
                                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Student id {student_id} not found")
            return JSONResponse({"Message": f"Student id {student_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Update master record of student
@router.put("/student")
def update_student(data: UpdateStudent, db: Session = Depends(get_db)):
    try:
        # Checking for availability of student & updating record if available
        logger.info(f"Checking for presence of student id {data.student_id}")
        student = db.query(Student).filter(Student.student_id == data.student_id).first()
        if student:
            # Checking for special characters
            if special_str.search(data.student_name):
                logger.error("Student name has special characters")
                return JSONResponse({"Message": "Student name field should have characters", "Status": 406},
                                    status_code=status.HTTP_406_NOT_ACCEPTABLE)

            # Checking input is not empty
            elif data.student_name == "":
                student.student_name = student.student_name
            else:
                student.student_name = data.student_name.title()

            # Checking student for unique email
            logger.info("Checking for unique email address")
            if db.query(Student).filter(Student.student_email == data.student_email).first():
                logger.error(f"Email {data.student_email} already exists")
                return JSONResponse({"Message": f"Email address {data.student_email} already exists", "Status": 406},
                                    status_code=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                student.student_email = data.student_email

            db.add(student)
            db.commit()
            db.refresh(student)
            logger.info(f"Student id {data.student_id} exist. Record updated")
            return JSONResponse({"Message": f"Record of student id {data.student_id} updated successfully", "Status": 200},
                                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Student id {data.student_id} not found")
            return JSONResponse({"Message": f"Student with id {data.student_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Updating course for student
@router.put("/student", response_model=MigrateStudent)
def course_migrate(data: MigrateStudent, db: Session = Depends(get_db)):
    try:
        # Checking for record of student whether he is enrolled for course from which moving
        logger.info(f"Checking {data.student_id} against enrolled courses")
        check_course = db.query(CourseStudent).filter(and_(CourseStudent.student_id == data.student_id,
                                                      CourseStudent.course_id == data.from_course_id)).first()
        if check_course:
            check_course.course_id = data.to_course_id
            # Checking whether student is already enrolled for course to which moving
            logger.info(f"Checking student {data.student_id} already enrolled to course {data.to_course_id}")
            move_course = db.query(CourseStudent).filter(and_(CourseStudent.student_id == data.student_id,
                                                         CourseStudent.course_id == check_course.course_id)).first()
            if move_course:
                logger.info(f"Student {data.student_id} already enrolled to {data.to_course_id}")
                return JSONResponse(
                    content=f"Student {data.student_id} already enrolled for course {check_course.course_id}")
            else:
                logger.info(f"Student {data.student_id} not enrolled to {data.to_course_id}")
                db.add(check_course)
                db.commit()
                db.refresh(check_course)
                logger.info(f"Updating record of student id {data.student_id}")
                return JSONResponse({"Message": f"Student {data.student_id} successfully moved from course {data.from_course_id} to course {data.to_course_id}",
                                    "Status": 200}, status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Student {data.student_id} is not enrolled for course {data.from_course_id}")
            return JSONResponse({"Message": f"Student {data.student_id} is not enrolled for course {data.from_course_id}",
                                 "Status": 404}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
