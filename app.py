from flask import Flask, render_template, redirect, url_for, request
from todo import init_db,add_task, delete_task, edit_task, load_tasks

app = Flask(__name__)
init_db()

@app.route('/')
def home():
    tasks = load_tasks()
    print("Tasks received by Flask:", tasks)
    return render_template('index.html',tasks=tasks)

@app.route('/tasks/add',methods = ['POST'])
def add_task_route():
    title = request.form.get("title")    
    description = request.form.get("description")
    status = request.form.get("status")

    add_task(title, description, status)
    return redirect(url_for('home'))

@app.route('/tasks/edit',methods = ['POST'])
def edit_task_route():
    number = request.form.get('number', type=int)
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    new_status = request.form.get('status')

    edit_task(number, title, description, new_status )
    return redirect(url_for('home'))

@app.route('/tasks/delete',methods = ['POST'])
def delete_task_route():
    number = request.form.get('number', type=int)

    delete_task(number)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)