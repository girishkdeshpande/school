from sqlalchemy.orm import Session

from schemas.schema import CourseBase, CourseSchema
from db.models.model import Course

from fastapi.encoders import jsonable_encoder


def create_new_course(course: CourseBase, db: Session):
    new_course = Course(course_name=course.course_name)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


'''def update_student_id(course_id: int, sid: schema.CourseBase, db: Session):
    data = db.get(model.Course, course_id)
    update_data = sid.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(data, key, value)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data
    data = db.query(model.Course).filter(model.Course.course_id == course_id).first()
    stored_model = schema.ShowCourse(**data)
    update_data = course.model_dump(exclude_unset=True)
    updated_data = stored_model.model_copy(update=update_data)
    data = db.query(model.Course).filter(model.Course.course_id == course_id).first()
    stored_data = schema.CourseCreate.model_dump_json(data)
    db.query(model.Course).update
    stored_data = model.Course[course_id]
    stored_model = schema.CourseBase(**stored_data)
    update_data = course.model_dump(exclude_unset=True)
    updated_sid = stored_model.model_copy(update=update_data)
    model.Course[course_id] = jsonable_encoder(updated_sid)
    return updated_sid'''


def get_course(cid: int, db: Session):
    single_course = db.query(Course).filter(Course.course_id == cid).first()
    return single_course


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    all_courses = db.query(Course).offset(skip).limit(limit).all()
    return all_courses
