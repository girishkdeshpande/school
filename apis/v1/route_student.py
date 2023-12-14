# File contains apis for Student

from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter
from fastapi.responses import JSONResponse
from typing import List

from schemas.schema import StudentSchema, NewStudent, UpdateStudent
from core.config import get_db, special_str
from db.models.model import Student, CourseStudent, Course

router = APIRouter()


# Enroll new student
@router.post("/student", response_model=NewStudent)
def new_student(student: NewStudent, db: Session = Depends(get_db)):
    try:
        # Checking for input is not empty
        if student.student_name == "":
            return JSONResponse(content="All fields except course_enrolled are mandatory",
                                status_code=status.HTTP_400_BAD_REQUEST)

        # Checking student name for special characters
        if special_str.search(student.student_name):
            return JSONResponse(content="Student name field should have characters",
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)

        # Creating instance for new student
        add_student = Student(
            student_name=student.student_name.title(),
            student_email=student.student_email,
            year_enrolled=student.year_enrolled
        )
        # Adding new student to database
        db.add(add_student)
        db.commit()
        db.refresh(add_student)

        # Adding courses enrolled by student to database
        for cors in student.course_enrolled:
            add_course = CourseStudent(
                student_id=add_student.student_id,
                course_id=cors
            )
            db.add(add_course)
            db.commit()
            db.refresh(add_course)

            return JSONResponse(content="Student added successfully", status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View student by student id
@router.get("/student/{student_id}", response_model=StudentSchema)
def show_student(sid: int, db: Session = Depends(get_db)):
    try:
        # Checking for student exists or not
        student = db.query(Student).filter(Student.student_id == sid).first()
        if student:
            return student
        else:
            return JSONResponse(content=f"Student with id {sid} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View all student's details
@router.get("/students", response_model=List[StudentSchema])
def show_all_students(db: Session = Depends(get_db)):
    try:
        # Checking for availability of student & reverting if available
        all_student = db.query(Student).all()
        if all_student:
            return all_student
        else:
            return JSONResponse(content="No records found", status_code=status.HTTP_204_NO_CONTENT)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/student/{student_id}")
def complete_delete_student(sid: int, db: Session = Depends(get_db)):
    try:
        # Checking for availability of student & deleting if available
        student = db.query(Student).filter(Student.student_id == sid).first()
        if student:
            db.delete(student)
            db.commit()
            return JSONResponse(content="Student deleted successfully", status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content=f"Student with id {sid} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete course against student
@router.delete("/student/{student_id}/{course_id}")
def remove_course(student_id: int, course_id: int, db: Session = Depends(get_db)):
    try:
        # Checking input is not zero
        if student_id == 0 or course_id == 0:
            return JSONResponse(content="Invalid Inout", status_code=status.HTTP_400_BAD_REQUEST)
        else:
            # Checking for record with given student id & course id. Deleting if available.
            course = db.query(CourseStudent).filter((CourseStudent.student_id == student_id),
                                                    (CourseStudent.course_id == course_id)).first()
            if course:
                db.delete(course)
                db.commit()
                return JSONResponse(content=f"Student with id {student_id} disenrolled from course {course_id}",
                                    status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(content=f"Student with id {student_id} not enrolled for course {course_id}",
                                    status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/student/{student_id}")
def delete_student(sid: int, db: Session = Depends(get_db)):
    try:
        # Checking for availability of student & changing status if available
        student = db.query(Student).filter(Student.student_id == sid).first()
        if student:
            student.student_status = "Inactive"
            db.add(student)
            db.commit()
            db.refresh(student)
            return JSONResponse(content="Status changed successfully", status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content=f"Student with id {sid} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/student/{student_id}", response_model=UpdateStudent)
def update_student(student_id: int, update_data: UpdateStudent, db: Session = Depends(get_db)):
    try:
        # Checking for availability of student & updating record if available
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if student:
            student.student_name = update_data.student_name.title()
            student.student_email = update_data.student_email
            student.year_enrolled = update_data.year_enrolled
            db.add(student)
            db.commit()
            db.refresh(student)
            return JSONResponse(content=f"Record of id {student_id} updated successfully",
                                status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content=f"Student with id {student_id} does not exist",
                                status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Updating course for student
@router.put("/student/{student_id}/{from_course}/{to_course}", response_model=UpdateStudent)
def course_migrate(student_id: int, from_course: int, to_course: int, db: Session = Depends(get_db)):
    try:
        # Checking for input for zero
        if student_id == 0 or from_course == 0 or to_course == 0:
            return JSONResponse(content="All fields are mandatory", status_code=status.HTTP_400_BAD_REQUEST)
        else:
            # Checking for record of student whether he is enrolled for course from which moving
            check_course = db.query(CourseStudent).filter((CourseStudent.student_id == student_id),
                                                          (CourseStudent.course_id == from_course)).first()
            if check_course:
                check_course.course_id = to_course
                # Checking whether student is already enrolled for course to which moving
                move_course = db.query(CourseStudent).filter((CourseStudent.student_id == student_id),
                                                             (CourseStudent.course_id == check_course.course_id)).first()
                if move_course:
                    return JSONResponse(content=f"Student {student_id} already enrolled for course {check_course.course_id}")
                else:
                    db.add(check_course)
                    db.commit()
                    db.refresh(check_course)
                    return JSONResponse(
                        content=f"Student {student_id} successfully moved from course {from_course} to course {to_course}",
                        status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(content=f"Student {student_id} is not enrolled for course {from_course}",
                                    status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
