from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from typing import List

from schemas.schema import TeacherBase, TeacherSchema
from db.session import get_db
from db.repository.teacher import create_new_teacher, get_teacher
from db.models.model import Teacher

router = APIRouter()


@router.post("/", response_model=TeacherBase, status_code=status.HTTP_201_CREATED)
def create_teacher(tcher: TeacherBase, db: Session = Depends(get_db)):
    add_teacher = create_new_teacher(teacher=tcher, db=db)
    return add_teacher


@router.get("/teacher/{teacher_id}", response_model=TeacherSchema)
def show_teacher(tid: int, db: Session = Depends(get_db)):
    single_teacher = get_teacher(tid=tid, db=db)
    if not single_teacher:
        raise HTTPException(detail=f"Student with id {tid} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    return single_teacher


@router.get("/teachers", response_model=List[TeacherSchema])
def show_all_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_teacher = get_teachers(db, skip=skip, limit=limit)
    return all_teacher
