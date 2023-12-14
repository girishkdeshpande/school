from sqlalchemy.orm import Session
from sqlalchemy import update

from schemas.schema import NewTeacher
from db.models.model import Teacher, CourseTeacher


def create_new_teacher(teacher: NewTeacher, db: Session):
    new_teacher = Teacher(
                teacher_name=teacher.teacher_name,
                teacher_email=teacher.teacher_email
                )
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    for cors in teacher.assign_course:
        add_course = CourseTeacher(
            teacher_id=new_teacher.teacher_id,
            course_id=cors
        )
        db.add(add_course)
        db.commit()
        db.refresh(add_course)

    return new_teacher


def get_teacher(tid: int, db: Session):
    single_teacher = db.query(Teacher).filter(Teacher.teacher_id == tid).first()
    return single_teacher


def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    all_teachers = db.query(Teacher).offset(skip).limit(limit).all()
    return all_teachers


def delete_teacher(tid: int, db: Session):
    single_teacher = db.query(Teacher).filter(Teacher.teacher_id == tid).first()
    return single_teacher
