from sqlalchemy.orm import Session

from schemas.schema import TeacherBase
from db.models.model import Teacher, TeacherCourse


def create_new_teacher(teacher: TeacherBase, db: Session):
    new_teacher = Teacher(
                teacher_name=teacher.teacher_name,
                teacher_email=teacher.teacher_email
                )
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    for cors in teacher.assign_course:
        cors_assigned = TeacherCourse(
                        teacher_id=new_teacher.teacher_id,
                        course_id=cors
                    )
        db.add(cors_assigned)
        db.commit()
        db.refresh(cors_assigned)

    return new_teacher


def get_teacher(tid: int, db: Session):
    single_teacher = db.query(Teacher).filter(Teacher.teacher_id == tid).first()
    return single_teacher


def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    all_teachers = db.query(Teacher).offset(skip).limit(limit).all()
    return all_teachers
