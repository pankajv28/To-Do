import json
from flask import Flask, render_template, redirect, url_for, request
from todo import add_task, find_task, delete_task, save_tasks, load_tasks

app = Flask(__name__)

@app.route('/')
def home():
    tasks = load_tasks()
    return render_template('index.html',tasks=tasks)

@app.route('/tasks/add',methods = ['POST'])
def add_task_route():
    tasks = load_tasks()
    title = request.form.get("title")    
    description = request.form.get("description")
    status = request.form.get("status")
    add_task(tasks,title,description, status)
    save_tasks(tasks)
    return redirect(url_for('home'))

@app.route('/tasks/edit',methods = ['POST'])
def edit_task_route():
    tasks = load_tasks()
    current_status = request.form.get('current_status')
    number = request.form.get('number', type=int)

    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    new_status = request.form.get('status')

    task = find_task(tasks, current_status, number)

    task['title'] = title
    task['description'] = description
    task['status'] = new_status

    save_tasks(tasks)

    return redirect(url_for('home'))

@app.route('/tasks/delete',methods = ['POST'])
def delete_task_route():
    tasks = load_tasks()
    current_status = request.form.get('current_status')
    number = request.form.get('number', type=int)
    delete_task(tasks,current_status,number)
    save_tasks(tasks)

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)