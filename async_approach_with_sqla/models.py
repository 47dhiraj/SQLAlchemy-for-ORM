from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, JSON, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base






class BaseModel(Base):

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())






class User(BaseModel):

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    password: Mapped[str] = mapped_column(String(255), nullable=False) 
    
    dob: Mapped[date | None] = mapped_column(Date, nullable=True)
    address: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username!r})>"
