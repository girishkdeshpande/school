from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from schemas.schema import CourseBase, ShowCourse, CourseSchema
from db.session import get_db
from db.repository.course import create_new_course, get_courses, get_course
from db.models.model import Course

router = APIRouter()


# Add new course
@router.post("/course", response_model=CourseBase)
def add_course(course: CourseBase, db: Session = Depends(get_db)):
    cors = Course(course_name=course.course_name)
    db.add(cors)
    db.commit()
    db.refresh(cors)
    return cors


'''@router.post("/student/{student_id}/courses", response_model=CourseBase)
def create_course(sid: int, course: CourseBase, db: Session = Depends(get_db)):
    return create_new_course(course=course, db=db)'''


@router.get("/course/{course_id}", response_model=CourseSchema)
def show_course(course_id: int, db: Session = Depends(get_db)):
    course = get_course(db=db, cid=course_id)
    if not course:
        raise HTTPException(detail=f"Course with id {course_id} does not exist", status_code=status.HTTP_404_NOT_FOUND)
    return course


@router.get("/courses", response_model=list[CourseSchema])
def show_all_course(skip: int = 0, limit:int = 100, db: Session = Depends(get_db)):
    courses = get_courses(db, skip=skip, limit=limit)
    return courses
