# File contains apis for Teacher

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session

from schemas.schema import NewTeacher, TeacherSchema, UpdateTeacher
from core.config import get_db, special_str
from db.models.model import Teacher, CourseTeacher

router = APIRouter()


# Add new teacher
@router.post("/teacher", response_model=NewTeacher)
def new_teacher(teacher: NewTeacher, db: Session = Depends(get_db)):
    try:
        # Checking for input is not empty
        if teacher.teacher_name == "":
            return JSONResponse(content="All fields except assigned_course are mandatory", status_code=status.HTTP_406_NOT_ACCEPTABLE)

        # Checking teacher name for special characters
        if special_str.search(teacher.teacher_name):
            return JSONResponse(content="Name field should have characters", status_code=status.HTTP_406_NOT_ACCEPTABLE)

        # Creating instance for new teacher
        add_teacher = Teacher(
                    teacher_name=teacher.teacher_name.title(),
                    teacher_email=teacher.teacher_email
                    )
        # Adding instance to database
        db.add(add_teacher)
        db.commit()
        db.refresh(add_teacher)

        # Adding courses which teacher teaches
        for course in teacher.assign_course:
            add_course = CourseTeacher(
                teacher_id=add_teacher.teacher_id,
                course_id=course
            )
            db.add(add_course)
            db.commit()
            db.refresh(add_course)

        return JSONResponse(content="Teacher added successfully", status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View teacher details by teacher id
@router.get("/teacher/{teacher_id}", response_model=TeacherSchema)
def view_teacher(teacher_id: int, db: Session = Depends(get_db)):
    try:
        # Checking for teacher exists or not
        single_teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
        if single_teacher:
            return single_teacher
        else:
            return JSONResponse(content=f"Teacher with id {teacher_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View all teacher's details
@router.get("/teachers", response_model=List[TeacherSchema])
def view_all_teachers(db: Session = Depends(get_db)):
    try:
        # Checking for availability of teachers & reverting if available
        all_teacher = db.query(Teacher).all()
        if all_teacher:
            return all_teacher
        else:
            return JSONResponse(content="No records found", status_code=status.HTTP_204_NO_CONTENT)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/teacher/{teacher_id}")
def complete_delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    try:
        # Checking for teacher exists or not
        single_teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
        if single_teacher:
            db.delete(single_teacher)
            db.commit()
            return JSONResponse(content="Teacher deleted successfully", status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content=f"Teacher with id {teacher_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete course against teacher
@router.delete("/teacher/{teacher_id}/{course_id}")
def remove_course(teacher_id: int, course_id: int, db: Session = Depends(get_db)):
    try:
        # Checking input is not zero
        if teacher_id == 0 or course_id == 0:
            return JSONResponse(content="Invalid Inout", status_code=status.HTTP_400_BAD_REQUEST)
        else:
            # Checking for record with given teacher id & course id. Deleting if available.
            course = db.query(CourseTeacher).filter((CourseTeacher.teacher_id == teacher_id), (CourseTeacher.course_id == course_id)).first()
            if course:
                db.delete(course)
                db.commit()
                return JSONResponse(content=f"Teacher with id {teacher_id} disenrolled from course {course_id}", status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(content=f"Teacher with id {teacher_id} not enrolled for course {course_id}", status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/teacher/{teacher_id}")
def delete_teacher(tid: int, db: Session = Depends(get_db)):
    try:
        # Checking for teacher exists & changing status if available
        teacher = db.query(Teacher).filter(Teacher.teacher_id == tid).first()
        if teacher:
            teacher.teacher_status = "Inactive"
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            return JSONResponse(content="Status changed successfully", status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content=f"Teacher with id {tid} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/teacher/{teacher_id}", response_model=UpdateTeacher)
def update_teacher(teacher_id: int, update_data: UpdateTeacher, db: Session = Depends(get_db)):
    try:
        # Checking for teacher exists & updating record if available
        teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
        if teacher:
            teacher.teacher_name = update_data.teacher_name.title()
            teacher.teacher_email = update_data.teacher_email
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            return JSONResponse(content=f"Record of id {teacher_id} updated successfully", status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content=f"Teacher with id {teacher_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    except:
        return JSONResponse(content="Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
