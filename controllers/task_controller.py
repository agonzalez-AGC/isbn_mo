from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from services.task_service import TaskService

task_blueprint = Blueprint('tasks', __name__)

@task_blueprint.route('/tasks', methods=['POST'])
def create_task():

    data = request.form
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    TaskService.create_task(name, description)
    return redirect(url_for('tasks.index'))

@task_blueprint.route('/')
def index():
    return render_template('index.html')

@task_blueprint.route('/edit/<int:id>', methods=['GET'])
def edit_task(id):
    task = TaskService.get_task_by_id(id)
    if not task:
        return "Task not found", 404
    return render_template('edit_task.html', task=task)

@task_blueprint.route('/edit/<int:id>', methods=['POST'])
def update_task(id):
    task = TaskService.get_task_by_id(id)
    if not task:
        return "Task not found", 404

    # Actualizar los campos del formulario
    TaskService.update_task(id, request.form['name'], request.form['description'])

    return redirect(url_for('tasks.index'))