import pytest
from datetime import date, timedelta
from unittest.mock import Mock
from app.service import TaskService
from app.model import Task

@pytest.fixture
def repo_mock():
    return Mock()

@pytest.fixture
def service(repo_mock):
    return TaskService(repo_mock)

def test_create_task_with_valid_data(service, repo_mock):
    tomorrow = date.today() + timedelta(days=1)
    repo_mock.save.return_value = Task(1, "Buy milk", tomorrow)
    task = service.create_task("Buy milk", tomorrow)
    assert task.title == "Buy milk"
    assert not task.completed
    repo_mock.save.assert_called_once()

def test_create_task_empty_title(service):
    with pytest.raises(ValueError, match="Title must be"):
        service.create_task("   ", date.today() + timedelta(days=1))

def test_create_task_whitespace_title(service):
    with pytest.raises(ValueError):
        service.create_task("\t\n", date.today() + timedelta(days=1))

def test_create_task_title_too_long(service):
    with pytest.raises(ValueError):
        service.create_task("a"*101, date.today() + timedelta(days=1))

def test_create_task_past_due_date(service):
    yesterday = date.today() - timedelta(days=1)
    with pytest.raises(ValueError, match="Due date"):
        service.create_task("Valid", yesterday)

def test_create_task_today_due_date(service, repo_mock):
    today = date.today()
    repo_mock.save.return_value = Task(1, "Today", today)
    task = service.create_task("Today", today)
    assert task.due_date == today

def test_toggle_complete_success(service, repo_mock):
    task_before = Task(1, "Test", date.today(), False)
    repo_mock.get_by_id.return_value = task_before
    updated = service.toggle_complete(1)
    assert updated.completed is True
    repo_mock.update.assert_called_once()

def test_toggle_complete_task_not_found(service, repo_mock):
    repo_mock.get_by_id.return_value = None
    with pytest.raises(ValueError):
        service.toggle_complete(999)

def test_toggle_complete_twice(service, repo_mock):
    task_before = Task(1, "Test", date.today(), False)
    repo_mock.get_by_id.return_value = task_before
    service.toggle_complete(1)
    assert task_before.completed is True
    service.toggle_complete(1)
    assert task_before.completed is False

def test_create_task_with_valid_whitespace(service, repo_mock):
    tomorrow = date.today() + timedelta(days=1)
    repo_mock.save.return_value = Task(1, "Trimmed", tomorrow)
    task = service.create_task("  Trimmed  ", tomorrow)
    assert task.title == "Trimmed"

def test_list_all_tasks(service, repo_mock):
    tasks = [Task(1, "Task 1", date.today(), False), Task(2, "Task 2", date.today(), True)]
    repo_mock.list_all.return_value = tasks
    result = service.list_all_tasks()
    assert len(result) == 2
    assert result[0].title == "Task 1"
    repo_mock.list_all.assert_called_once()

def test_get_task_by_id_found(service, repo_mock):
    task = Task(1, "Found", date.today(), False)
    repo_mock.get_by_id.return_value = task
    result = service.get_task_by_id(1)
    assert result.title == "Found"
    repo_mock.get_by_id.assert_called_once_with(1)

def test_get_task_by_id_not_found(service, repo_mock):
    repo_mock.get_by_id.return_value = None
    with pytest.raises(ValueError, match="Task not found"):
        service.get_task_by_id(999)

def test_delete_task_success(service, repo_mock):
    task = Task(1, "Delete me", date.today(), False)
    repo_mock.get_by_id.return_value = task
    service.delete_task(1)
    repo_mock.delete.assert_called_once_with(1)

def test_delete_task_not_found(service, repo_mock):
    repo_mock.get_by_id.return_value = None
    with pytest.raises(ValueError, match="Task not found"):
        service.delete_task(999)

def test_create_task_with_exact_100_chars(service, repo_mock):
    tomorrow = date.today() + timedelta(days=1)
    title_100 = "a" * 100
    repo_mock.save.return_value = Task(1, title_100, tomorrow)
    task = service.create_task(title_100, tomorrow)
    assert len(task.title) == 100
    repo_mock.save.assert_called_once()

def test_toggle_complete_preserves_other_fields(service, repo_mock):
    task = Task(1, "Important", date.today() + timedelta(days=5), False)
    repo_mock.get_by_id.return_value = task
    service.toggle_complete(1)
    assert task.title == "Important"
    assert task.id == 1