# Task Management System

A simple yet comprehensive task management REST API built with Flask, demonstrating modern software development practices including automated testing and continuous integration.

## Features

- **Create Tasks**: Add new tasks with title and due date
- **View Tasks**: List all tasks or retrieve individual task details
- **Toggle Completion**: Mark tasks as complete or incomplete
- **Delete Tasks**: Remove tasks from the system
- **Input Validation**: Comprehensive validation of task data
- **Error Handling**: Meaningful error responses for invalid operations

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── model.py           # Data models
│   ├── repository.py      # Data persistence layer (SQLite)
│   ├── service.py         # Business logic layer
│   └── routes.py          # Flask API endpoints
├── tests/
│   ├── __init__.py
│   ├── test_service.py    # Unit tests (15+ test cases)
│   └── test_routes.py     # Integration tests (10+ test cases)
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI/CD pipeline
├── requirements.txt       # Python dependencies
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.12+
- pip (Python package manager)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SystemTestingUAS.git
cd SystemTestingUAS
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Important: Activate Virtual Environment First

Before running the app, activate the virtual environment:

**On Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### Quick Start (Recommended)
Once the virtual environment is activated:
```bash
python run.py
```

### Alternative Methods

**Method 1** (Using environment variable):
```bash
set FLASK_APP=app.routes
flask run
```

**Method 2** (Using Flask CLI):
```bash
flask --app app.routes run
```

The API will be available at `http://localhost:5000`

**To stop the server**: Press `Ctrl+C` in the terminal

**To deactivate virtual environment**: Type `deactivate` in your terminal

### Testing the API

You can test the API endpoints using:
- Browser: `http://localhost:5000` (GET requests only)
- cURL: `curl http://localhost:5000/tasks`
- Postman: Import the endpoints and test
- Python: Use the `requests` library

Start with the welcome page at `http://localhost:5000` to see all available endpoints.

## API Endpoints

### Welcome Endpoint
**GET** `/`
```json
Response (200):
{
  "message": "Welcome to Task Management System API",
  "version": "1.0.0",
  "endpoints": {
    "GET /": "This welcome message",
    "GET /tasks": "List all tasks",
    "POST /tasks": "Create a new task",
    "GET /tasks/{id}": "Get a specific task",
    "PATCH /tasks/{id}/toggle": "Toggle task completion",
    "DELETE /tasks/{id}": "Delete a task"
  }
}
```

### Create Task
**POST** `/tasks`
```json
Request:
{
  "title": "Buy groceries",
  "due_date": "2025-12-31"
}

Response (201):
{
  "id": 1,
  "title": "Buy groceries",
  "due_date": "2025-12-31",
  "completed": false
}
```

### List All Tasks
**GET** `/tasks`
```json
Response (200):
[
  {
    "id": 1,
    "title": "Buy groceries",
    "due_date": "2025-12-31",
    "completed": false
  },
  ...
]
```

### Get Single Task
**GET** `/tasks/{id}`
```json
Response (200):
{
  "id": 1,
  "title": "Buy groceries",
  "due_date": "2025-12-31",
  "completed": false
}
```

### Toggle Task Completion
**PATCH** `/tasks/{id}/toggle`
```json
Response (200):
{
  "id": 1,
  "completed": true
}
```

### Delete Task
**DELETE** `/tasks/{id}`
```json
Response (200):
{
  "message": "Task deleted"
}
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Tests with Coverage Report
```bash
pytest --cov=app --cov-report=term-missing --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/test_service.py
pytest tests/test_routes.py
```

### Run Tests with Verbose Output
```bash
pytest -v
```

## Testing Strategy

### Unit Tests (15+ test cases)
Located in `tests/test_service.py`, these tests focus on business logic validation:
- Valid task creation with various inputs
- Input validation (empty title, long title, past dates)
- Task completion toggling
- Task retrieval and deletion
- Edge cases and boundary conditions

**Test Coverage**:
- Title validation (empty, whitespace, length limits)
- Due date validation (past dates, today, future)
- Task state transitions
- Task retrieval scenarios
- Task deletion scenarios

### Integration Tests (10+ test cases)
Located in `tests/test_routes.py`, these tests validate API endpoint behavior:
- Task creation via HTTP endpoints
- Task listing and retrieval
- Error handling with appropriate HTTP status codes
- Complete workflow scenarios (create → read → update → delete)
- Endpoint integration with database

**Test Coverage**:
- POST /tasks (success and failures)
- GET /tasks (empty and with data)
- GET /tasks/{id} (existing and non-existent)
- PATCH /tasks/{id}/toggle (success and failures)
- DELETE /tasks/{id} (success and failures)

### Test Execution Flow
1. **Unit Tests**: Validate business logic in isolation using mocks
2. **Integration Tests**: Validate full request/response cycle with in-memory database
3. **Coverage Analysis**: Verify code coverage meets minimum threshold (60%)

## Continuous Integration (GitHub Actions)

The project uses GitHub Actions for automated testing on every push and pull request.

### CI Pipeline (`​.github/workflows/ci.yml`)

The workflow performs the following steps:

1. **Checkout Code**: Clone the repository
2. **Setup Python**: Install Python 3.12
3. **Install Dependencies**: Install packages from requirements.txt
4. **Run Tests**: Execute pytest with coverage reporting
5. **Generate Coverage Report**: Create coverage.xml for analysis

**Trigger Events**:
- Push to main branch
- Pull requests to main branch

**Outputs**:
- Test execution results
- Coverage metrics (60%+ target)
- Artifacts (coverage.xml)

### Viewing CI Status
- Go to the "Actions" tab on GitHub
- Click on a workflow run to see detailed logs
- Coverage reports are available as artifacts

## Test Coverage Goals

| Metric | Target | Current |
|--------|--------|---------|
| Overall Coverage | 60%+ | ~75% |
| model.py | 100% | 100% |
| service.py | 90%+ | 95% |
| repository.py | 80%+ | 85% |
| routes.py | 85%+ | 90% |

## Development Best Practices Applied

1. **Testable Code Architecture**: Clear separation of concerns (model, repository, service, routes)
2. **Comprehensive Testing**: Unit and integration tests with high coverage
3. **Input Validation**: Robust validation at service layer
4. **Error Handling**: Consistent error responses with meaningful messages
5. **CI/CD Integration**: Automated testing on every commit
6. **Database Abstraction**: Repository pattern for data access
7. **Mock Usage**: Proper use of mocks in unit tests for isolation
8. **Documentation**: Clear README and inline code documentation

## Validation Rules

### Task Creation
- **Title**: Must be 1-100 characters (trimmed)
- **Due Date**: Cannot be in the past (must be today or later)
- **Whitespace**: Titles are trimmed before storage

### Task Operations
- **Get/Toggle/Delete**: Task must exist (404 if not found)
- **Toggle**: Switches between complete and incomplete states

## Dependencies

- **Flask 3.0.0**: Web framework for building REST API
- **pytest 7.4.3**: Testing framework
- **pytest-cov 4.1.0**: Coverage plugin for pytest

## Database

Uses SQLite for data persistence:
- File-based database: `task.db`
- Automatic table creation on first run
- Simple in-memory database for testing

## Future Enhancements

- User authentication and authorization
- Due date reminders/notifications
- Task categories/tags
- Priority levels
- Task search and filtering
- Batch operations
- API rate limiting
- Database migrations

## License

This project is open source and available under the MIT License.

## Author

Developed as a course project for System Testing and CI/CD integration.