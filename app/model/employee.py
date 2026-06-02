from datetime import date
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import db

class Employee(db.Model):
    """Database model representing an Employee record in the 'employees' table."""
    __tablename__ = "employees"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    date_joined: Mapped[date] = mapped_column(Date, nullable=False)

    def to_dict(self) -> dict:
        """Serialize database model to a dictionary format."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "date_joined": self.date_joined.isoformat() if isinstance(self.date_joined, date) else self.date_joined
        }

    def __repr__(self) -> str:
        return f"<Employee id={self.id} name='{self.name}' email='{self.email}'>"
