from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime

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






class User(BaseModel):

    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    first_name: Mapped[str | None] = mapped_column(String(100))      
    last_name: Mapped[str | None] = mapped_column(String(100))

    password: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )


    addresses: Mapped[list["Address"]] = relationship("Address", back_populates="user", cascade="all, delete-orphan")


    def __repr__(self) -> str:
        return f"<User id: {self.id} | username: {self.username} | email: {self.email}>"






class Address(BaseModel):

    __tablename__ = 'addresses'

    location: Mapped[str] = mapped_column(String(255), nullable=False)

    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    
    user: Mapped[User | None] = relationship("User", back_populates="addresses")


    def __repr__(self) -> str:
        return f"<Address id: {self.id} | location: {self.location}> | user_id: {self.user_id}"

