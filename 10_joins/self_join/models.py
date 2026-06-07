from sqlalchemy import ForeignKey, String

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)



class Base(DeclarativeBase):
    pass





class BaseModel(Base):

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)






class Employee(BaseModel):

    __tablename__ = "employees"


    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(100))
    department: Mapped[str] = mapped_column(String(100))
    level: Mapped[str] = mapped_column(String(50))


    manager_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id"), nullable=True)

    manager: Mapped[Employee | None] = relationship(
        "Employee", 
        remote_side="Employee.id"
    )


    def __repr__(self) -> str:

        if "manager" in self.__dict__:
            manager_info = self.manager.name if self.manager else "None"
        else:
            manager_info = f"{self.manager_id}" if self.manager_id else "None"

        return f"<Emp Name: '{self.name}' | Role: '{self.role}' | Manager: {manager_info}>"
