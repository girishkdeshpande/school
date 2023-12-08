from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from typing import List

from schemas.schema import StudentSchema, StudentBase
from core.config import get_db
from db.repository.student import create_new_student, get_students, get_student


router = APIRouter()


@router.post("/", response_model=StudentBase, status_code=status.HTTP_201_CREATED)
def create_student(stud: StudentBase, db: Session = Depends(get_db)):
    new_student = create_new_student(student=stud, db=db)
    return new_student


@router.get("/student/{student_id}", response_model=StudentSchema, response_model_exclude={"course_enrolled"})
def show_student(sid: int, db: Session = Depends(get_db)):
    student = get_student(sid=sid, db=db)
    if not student:
        raise HTTPException(detail=f"Student with id {sid} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    return student


@router.get("/students", response_model=List[StudentSchema])
def show_all_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_student = get_students(db, skip=skip, limit=limit)
    return all_student

