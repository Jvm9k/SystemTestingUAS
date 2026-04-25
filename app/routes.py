from flask import Flask, request, jsonify
from datetime import date
from app.service import TaskService
from app.repository import TaskRepository

app = Flask(__name__)
service = TaskService(TaskRepository())

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({
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
    }), 200

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    try:
        task = service.create_task(data["title"], date.fromisoformat(data["due_date"]))
        return jsonify({"id": task.id, "title": task.title, "due_date": task.due_date.isoformat(), "completed": task.completed}), 201
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400

@app.route("/tasks/<int:task_id>/toggle", methods=["PATCH"])
def toggle_task(task_id):
    try:
        task = service.toggle_complete(task_id)
        return jsonify({"id": task.id, "completed": task.completed})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    tasks = service.list_all_tasks()
    return jsonify([{
        "id": task.id,
        "title": task.title,
        "due_date": task.due_date.isoformat(),
        "completed": task.completed
    } for task in tasks]), 200

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    try:
        task = service.get_task_by_id(task_id)
        return jsonify({
            "id": task.id,
            "title": task.title,
            "due_date": task.due_date.isoformat(),
            "completed": task.completed
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        service.delete_task(task_id)
        return jsonify({"message": "Task deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
