from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import List

from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.sleep_entry import SleepEntry
from models.sleep_counter import SleepCounter
from schemas import SleepEntryCreate, SleepIntervalData


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run migrations on startup
    import os

    alembic_ini_path = os.path.join(os.path.dirname(__file__), "alembic.ini")
    alembic_cfg = Config(alembic_ini_path)
    # Set the script location directory to where we run alembic commands from
    alembic_cfg.set_main_option("script_location", os.path.join(os.path.dirname(__file__), "alembic"))
    command.upgrade(alembic_cfg, "head")
    yield


app = FastAPI(title="Sleepin API", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Welcome to Sleepin API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/sleep", status_code=200)
async def log_sleep(sleep_data: SleepEntryCreate, db: Session = Depends(get_db)):
    """
    Log a new sleep entry when you wake up.
    Tracks counter value in separate table and detects when counter resets to calculate actual sleep duration.
    Automatically calculates wake period from the previous sleep entry.
    """
    sleep_end = sleep_data.sleep_end or datetime.now()
    counter_value = sleep_data.sleep_counter_value

    # Get or create the counter entry by name
    counter = db.query(SleepCounter).filter(SleepCounter.name == "sleep-counter").first()
    current_counter_value = counter.counter_value if counter else 0
    if counter_value < current_counter_value:
        current_counter_value = 0

    if counter_value != 0:
        sleep_length = counter_value - current_counter_value
        previous_sleep_entry = db.query(SleepEntry).order_by(SleepEntry.sleep_end.desc()).first()
        sleep_start = sleep_end - timedelta(minutes=sleep_length)
        if previous_sleep_entry:
            awake_start = previous_sleep_entry.sleep_end
        else:
            awake_start = None
        new_entry = SleepEntry(
            awake_start=awake_start,
            sleep_start=sleep_start,
            sleep_end=sleep_end,
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

    if not counter:
        counter = SleepCounter(name="sleep-counter", counter_value=counter_value)
        db.add(counter)
        db.commit()
        db.refresh(counter)
    else:
        counter.counter_value = counter_value
        db.commit()


    return {"message": "Sleep entry logged successfully"}


@app.get("/sleep/interval", response_model=List[SleepIntervalData])
async def get_sleep_intervals(db: Session = Depends(get_db)):
    """
    Get sleep intervals for the current user.
    """
    sleep_entries = db.query(SleepEntry).all()
    entries = []
    for entry in sleep_entries:
        duration_awake = int((entry.sleep_start -entry.awake_start).total_seconds() // 60) if entry.awake_start else 0
        duration_asleep = int((entry.sleep_end - entry.sleep_start).total_seconds() // 60)
        duration_total = duration_awake + duration_asleep
        interval_start = entry.awake_start if entry.awake_start else entry.sleep_start
        entries.append(
            SleepIntervalData(
                interval_start=interval_start,
                interval_end=entry.sleep_end,
                duration_total=duration_total,
                duration_awake=duration_awake,
                duration_asleep=duration_asleep,
            )
        )
    return entries
