from dataclasses import dataclass
from datetime import date

@dataclass
class Task:
    id: int | None
    title: str
    due_date: date
    completed: bool = False
