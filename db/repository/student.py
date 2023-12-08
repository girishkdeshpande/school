from sqlalchemy.orm import Session

from schemas.schema import StudentBase, StudentSchema
from db.models.model import Student, StudentCourse


def create_new_student(student: StudentBase, db: Session):
    new_student = Student(
                        student_name=student.student_name,
                        student_email=student.student_email,
                        year_enrolled=student.year_enrolled,
                    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    for cors in student.course_enrolled:
        add_course = StudentCourse(
            student_id=new_student.student_id,
            course_id=cors
        )
        db.add(add_course)
        db.commit()
        db.refresh(add_course)

    return student


def get_student(sid: int, db: Session):
    single_student = db.query(Student).filter(Student.student_id == sid).first()
    return single_student


def get_students(db: Session, skip: int = 0, limit: int = 100):
    all_students = db.query(Student).offset(skip).limit(limit).all()
    return all_students
