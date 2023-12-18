# This file contains collection of api routers which later included in main file

from fastapi import APIRouter

from apis.v1 import route_student, route_course, route_teacher


api_router = APIRouter()
api_router.include_router(route_student.router, prefix="", tags=["students"])
api_router.include_router(route_course.router, prefix="", tags=["courses"])
api_router.include_router(route_teacher.router, prefix="", tags=["teachers"])


