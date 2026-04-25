from datetime import date
from app.model import Task

class TaskService:
    def __init__(self, repository):
        self.repo = repository

    def create_task(self, title: str, due_date: date) -> Task:
        stripped_title = title.strip() if title else ""
        if not stripped_title or len(stripped_title) > 100:
            raise ValueError("Title must be 1-100 characters")
        if due_date < date.today():
            raise ValueError("Due date cannot be in the past")
        task = Task(id=None, title=stripped_title, due_date=due_date)
        return self.repo.save(task)

    def toggle_complete(self, task_id: int) -> Task:
        task = self.repo.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found")
        task.completed = not task.completed
        self.repo.update(task)
        return task

    def list_all_tasks(self) -> list:
        return self.repo.list_all()

    def get_task_by_id(self, task_id: int) -> Task:
        task = self.repo.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found")
        return task

    def delete_task(self, task_id: int) -> None:
        task = self.repo.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found")
        self.repo.delete(task_id)
