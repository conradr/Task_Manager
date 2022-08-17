from flask import Flask, render_template, request, redirect, url_for
from flask import Blueprint
from repositories import task_repository
from repositories import user_repository
from models.task import Task

tasks_blueprint = Blueprint("tasks", __name__)


@tasks_blueprint.route('/tasks', methods=['GET'])
def tasks():
    tasks_list = task_repository.select_all()
    return render_template('tasks/index.html', all_tasks=tasks_list)


@tasks_blueprint.route('/tasks/new', methods=['GET'])
def new_task():
    users_list = user_repository.select_all()
    return render_template("tasks/new.html", all_users=users_list)


@tasks_blueprint.route('/tasks', methods=['POST'])
def create_task():
    description = request.form['description']
    user_id = request.form['user_id']
    duration = request.form['duration']
    completed = request.form['completed']
    user = user_repository.select(user_id)
    # assumes there's is a matching user
    task = Task(description, user, duration, completed)
    task_repository.save(task)
    # return redirect("/tasks")
    return redirect(url_for('tasks.tasks'))


@tasks_blueprint.route('/tasks/<id>/delete', methods=['POST', 'DELETE'])
def whack_task(id):
    task_repository.delete(id)
    return redirect("/tasks")


@tasks_blueprint.route('/tasks/<id>/update', methods=['GET'])
def make_them_orpans(id):
    task_object = task_repository.select(id)
    users = user_repository.select_all()
    return render_template('/tasks/edit.html', task=task_object, all_users=users)


@tasks_blueprint.route('/tasks/<id>', methods=['GET'])
def show_task(id):
    task_object = task_repository.select(id)
    return render_template("/tasks/show.html", task=task_object)


@tasks_blueprint.route('/tasks/<id>', methods=['POST'])
def save_update_task(id):
    description = request.form['description']
    user_id = request.form['user_id']
    duration = request.form['duration']
    completed = request.form['completed']
    user = user_repository.select(user_id)
    # assumes there's is a matching user
    task = Task(description, user, duration, completed, id)
    task_repository.update(task)
    # return redirect("/tasks")
    return redirect(url_for('tasks.tasks'))
