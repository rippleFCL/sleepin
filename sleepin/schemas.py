from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SleepEntryCreate(BaseModel):
    sleep_counter_value: int = Field(..., ge=0, description="Current sleep counter value in minutes")
    sleep_end: Optional[datetime] = Field(None, description="Time of sleep ending (defaults to now)")


class SleepIntervalData(BaseModel):
    interval_start: datetime
    interval_end: datetime
    duration_total: int
    duration_awake: int
    duration_asleep: int
