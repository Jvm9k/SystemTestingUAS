import sqlite3
from app.model import Task
from datetime import date

class TaskRepository:
    def __init__(self, db_path="task.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )""")

    def save(self, task: Task) -> Task:
        cur = self.conn.execute(
            "INSERT INTO tasks (title, due_date, completed) VALUES (?, ?, ?)",
            (task.title, task.due_date.isoformat(), int(task.completed))
        )
        task.id = cur.lastrowid
        return task

    def get_by_id(self, task_id: int) -> Task | None:
        row = self.conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if row:
            id_, title, due_date_str, completed = row
            return Task(id_, title, date.fromisoformat(due_date_str), bool(completed))
        return None

    def list_all(self):
        rows = self.conn.execute("SELECT * FROM tasks").fetchall()
        return [Task(r[0], r[1], date.fromisoformat(r[2]), bool(r[3])) for r in rows]

    def update(self, task: Task):
        self.conn.execute(
            "UPDATE tasks SET title=?, due_date=?, completed=? WHERE id=?",
            (task.title, task.due_date.isoformat(), int(task.completed), task.id)
        )

    def delete(self, task_id: int):
        self.conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
