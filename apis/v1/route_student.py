# File contains apis for Student
import logging
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter
from fastapi.responses import JSONResponse
from typing import List

from schemas.schema import StudentSchema, NewStudent, UpdateStudent
from core.config import get_db, special_str
from db.models.model import Student, CourseStudent

router = APIRouter()
logger = logging.getLogger('school')


# Enroll new student
@router.post("/student")
def new_student(student: NewStudent, db: Session = Depends(get_db)):
    try:
        # Checking for input is not empty
        logger.info("Checking whether student name is None")
        student = student.model_dump()
        if student['student_name'] == "":
            logger.error("Student name is None")
            return JSONResponse({"Message": "All fields except course_enrolled are mandatory", "Status": 400},
                                status_code=status.HTTP_400_BAD_REQUEST)

        # Checking student name for special characters
        logger.info("Student: Checking whether student name has special characters")
        if special_str.search(student['student_name']):
            logger.error("Student name has special characters")
            return JSONResponse({"Message": "Student name field should have characters", "Status": 406},
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)

        # Creating instance for new student
        logger.info("Creating instance of student to add in database")
        add_student = Student(
            student_name=student['student_name'].title(),
            student_email=student['student_email'],
            year_enrolled=student['year_enrolled']
        )

        # Adding new student to database
        logger.info("Adding new student into database")
        db.add(add_student)
        db.commit()
        db.refresh(add_student)

        # Adding courses enrolled by student to database
        logger.info("Adding courses enrolled by new student into database")
        for cors in student['course_enrolled']:
            add_course = CourseStudent(
                student_id=add_student.student_id,
                course_id=cors
            )
            db.add(add_course)
            db.commit()
            db.refresh(add_course)

        logger.info("Student added successfully")
        return JSONResponse({
            "Message": f"Student {student['student_name']} added successfully with courses {student['course_enrolled']}",
            "Status": 200}, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View student by student id
@router.get("/student/{student_id}", response_model=StudentSchema)
def view_student(sid: int, db: Session = Depends(get_db)):
    try:
        # Checking student id exists or not
        logger.info(f"Checking for presence of student id {sid}")
        student = db.query(Student).filter(Student.student_id == sid).first()
        if student:
            logger.info(f"Student id {sid} is present.Returned student details")
            return student
        else:
            logger.error(f"Student id {sid} does not exist")
            return JSONResponse({"Message": f"Student with id {sid} does not exist",
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
@router.delete("/student/{student_id}")
def complete_delete_student(sid: int, db: Session = Depends(get_db)):
    try:
        # Checking for availability of student & deleting if available
        logger.info(f"Checking for presence of student id {sid}")
        student = db.query(Student).filter(Student.student_id == sid).first()
        if student:
            db.delete(student)
            db.commit()
            logger.info(f"Student id {sid} is present. Record deleted")
            return JSONResponse({"Message": f"Student id {sid} deleted successfully", "Status": 200},
                                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Student id {sid} does not exist")
            return JSONResponse({"Message": f"Student id {sid} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Disenroll student from course
@router.delete("/student/{student_id}/{course_id}")
def disenroll_from_course(student_id: int, course_id: int, db: Session = Depends(get_db)):
    try:
        # Checking input is not zero
        logger.info("Checking whether input is zero or not")
        if student_id == 0 or course_id == 0:
            return JSONResponse({"Message": f" {student_id} {course_id} Invalid Inout", "Status": 400},
                                status_code=status.HTTP_400_BAD_REQUEST)
        else:
            # Checking for record with given student id & course id. Deleting if available.
            logger.info(f"Checking for record of student id {student_id} against course id {course_id}")
            course = db.query(CourseStudent).filter((CourseStudent.student_id == student_id),
                                                    (CourseStudent.course_id == course_id)).first()
            if course:
                db.delete(course)
                db.commit()
                logger.info("Record exist.Record deleted")
                return JSONResponse({"Message": f"Student id {student_id} disenrolled from course {course_id}",
                                     "Status": 200}, status_code=status.HTTP_200_OK)
            else:
                logger.error(f"Student id {student_id} not enrolled for course {course_id}")
                return JSONResponse({"Message": f"Student id {student_id} not enrolled for course {course_id}",
                                     "Status": 404}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Change status of student / Soft delete
@router.patch("/student/{student_id}")
def delete_student(sid: int, db: Session = Depends(get_db)):
    try:
        # Checking student id exists or not & changing status if available
        logger.info(f"Checking for presence of student id {sid}")
        student = db.query(Student).filter((Student.student_id == sid), (Student.student_status == "Active")).first()
        if student:
            student.student_status = "Inactive"
            db.add(student)
            db.commit()
            db.refresh(student)
            logger.info(f"Student id {sid} present. Status changed")
            return JSONResponse({"Message": f"Status of student id {sid} changed successfully", "Status": 200},
                                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Student id {sid} not found")
            return JSONResponse({"Message": f"Student id {sid} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Update master record of student
@router.put("/student/{student_id}", response_model=UpdateStudent)
def update_student(student_id: int, update_data: UpdateStudent, db: Session = Depends(get_db)):
    try:
        update_data = update_data.model_dump()
        # Checking for availability of student & updating record if available
        logger.info(f"Checking for presence of student id {student_id}")
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if student:
            student.student_name = update_data['student_name'].title()
            student.student_email = update_data['student_email']
            student.year_enrolled = update_data['year_enrolled']
            db.add(student)
            db.commit()
            db.refresh(student)
            logger.info(f"Student id {student_id} exist. Record updated")
            return JSONResponse({"Message": f"Record of student id {student_id} updated successfully", "Status": 200},
                                status_code=status.HTTP_200_OK)
        else:
            logger.error(f"Student id {student_id} not found")
            return JSONResponse({"Message": f"Student with id {student_id} does not exist", "Status": 404},
                                status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Updating course for student
@router.put("/student/{student_id}/{from_course}/{to_course}", response_model=UpdateStudent)
def course_migrate(student_id: int, from_course: int, to_course: int, db: Session = Depends(get_db)):
    try:
        # Checking for input for zero
        logger.info("Checking whether input is zero or not")
        if student_id == 0 or from_course == 0 or to_course == 0:
            return JSONResponse({"Message": f"{student_id} {from_course} {to_course} Invalid input", "Status": 400},
                                status_code=status.HTTP_400_BAD_REQUEST)
        else:
            # Checking for record of student whether he is enrolled for course from which moving
            logger.info(f"Checking {student_id} against enrolled courses")
            check_course = db.query(CourseStudent).filter((CourseStudent.student_id == student_id),
                                                          (CourseStudent.course_id == from_course)).first()
            if check_course:
                check_course.course_id = to_course
                # Checking whether student is already enrolled for course to which moving
                logger.info(f"Checking student {student_id} already enrolled to course {to_course}")
                move_course = db.query(CourseStudent).filter((CourseStudent.student_id == student_id),
                                                             (CourseStudent.course_id == check_course.course_id)).first()
                if move_course:
                    logger.info(f"Student {student_id} already enrolled to {to_course}")
                    return JSONResponse(content=f"Student {student_id} already enrolled for course {check_course.course_id}")
                else:
                    logger.info(f"Student {student_id} not enrolled to {to_course}")
                    db.add(check_course)
                    db.commit()
                    db.refresh(check_course)
                    logger.info(f"Updating record of student id {student_id}")
                    return JSONResponse(
                        {"Message": f"Student {student_id} successfully moved from course {from_course} to course {to_course}",
                         "Status": 200}, status_code=status.HTTP_200_OK)
            else:
                logger.error(f"Student {student_id} is not enrolled for course {from_course}")
                return JSONResponse({"Message": f"Student {student_id} is not enrolled for course {from_course}", "Status": 404},
                                    status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(e)
        return JSONResponse({"Message": "An unexpected error occurred. Please try again later",
                             "Status": 500}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
