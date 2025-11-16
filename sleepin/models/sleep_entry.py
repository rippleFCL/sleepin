from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class SleepEntry(Base):
    __tablename__ = "sleep_entries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    awake_start: Mapped[datetime | None] = mapped_column(default=None)
    sleep_start: Mapped[datetime] = mapped_column(server_default=func.now())
    sleep_end: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)

    def __repr__(self) -> str:
        return f"<SleepEntry(id={self.id}, awake_start={self.awake_start}, sleep_start={self.sleep_start}, sleep_end={self.sleep_end})>"
