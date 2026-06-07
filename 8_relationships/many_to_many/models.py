from typing import List
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)





class Base(DeclarativeBase):

    pass


class BaseModel(Base):

    __abstract__ = True     

    id: Mapped[int] = mapped_column(Integer, primary_key=True)





class Student(BaseModel):

    __tablename__ = "students"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    
    enrollments: Mapped[List["Enrollment"]] = relationship(back_populates="student") 

    ## Optional (only for developer ease):
    # courses: Mapped[List["Course"]] = relationship(secondary="enrollments", viewonly=True)





class Course(BaseModel):

    __tablename__ = "courses"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    
    enrollments: Mapped[List["Enrollment"]] = relationship(back_populates="course")

    ## Optional (only for developer ease):
    # students: Mapped[List["Student"]] = relationship(secondary="enrollments", viewonly=True)






## Enrollment is Association(Bridging) model/table
class Enrollment(BaseModel):

    __tablename__ = "enrollments"
    
    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))    
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))        

    student: Mapped["Student"] = relationship(back_populates="enrollments")
    course: Mapped["Course"] = relationship(back_populates="enrollments")

    ## grade is extra field/data
    grade: Mapped[str | None] = mapped_column(String, nullable=True)        

