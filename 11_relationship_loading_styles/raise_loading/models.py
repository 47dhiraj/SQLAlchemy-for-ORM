from sqlalchemy import ForeignKey, Integer, String, Text, create_engine

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

    id: Mapped[int] = mapped_column(primary_key=True)




class User(BaseModel):

    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String(50))

    sensitive_information: Mapped[list["SensitiveInformation"]] = relationship(
        "SensitiveInformation", 
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="raise"                    
    )

    def __repr__(self) -> str:
        return f'<User {self.name}>'





class SensitiveInformation(BaseModel):

    __tablename__ = 'sensitive_informations'

    content: Mapped[str | None] = mapped_column(Text)
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    
    user: Mapped["User"] = relationship("User", back_populates="sensitive_information")

    def __repr__(self) -> str:
        return f'<SensitiveInformation id={self.id}>'
