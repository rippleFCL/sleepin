from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class SleepCounter(Base):
    __tablename__ = "sleep_counter"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    counter_value: Mapped[int]

    def __repr__(self) -> str:
        return f"<SleepCounter(id={self.id}, name={self.name}, counter_value={self.counter_value})>"
