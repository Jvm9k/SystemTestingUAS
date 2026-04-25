## Features

- **Create Tasks**: Add new tasks with title and due date
- **View Tasks**: List all tasks or retrieve individual task details
- **Toggle Completion**: Mark tasks as complete or incomplete
- **Delete Tasks**: Remove tasks from the system
- **Input Validation**: Comprehensive validation of task data
- **Error Handling**: Meaningful error responses for invalid operations

## Installation & Setup

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
    "due_date": "2026-12-31",
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
  "due_date": "2026-12-31",
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