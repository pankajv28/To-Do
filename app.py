from flask import Flask, render_template, redirect, url_for, request, session, flash
from todo import init_db,add_task, delete_task, edit_task, load_tasks
import sqlite3
from functools import wraps
from werkzeug.security import check_password_hash

app = Flask(__name__)
init_db()

app.config['SECRET_KEY'] = 'dcdbc6f807eda88c51ab0646db1f8cf01a0e4134f1a153f1be9139c8910b20f8'

def login_required(function):
    @wraps(function)
    def wrapper(*args,**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return function (*args,**kwargs)
    return wrapper

@app.route('/login',methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","").strip()

        connection = sqlite3.connect('tasks.db')

        try:
            cursor = connection.cursor()
            cursor.execute(
                'SELECT id, password_hash from users where username = ?',
                (username,)
            )
            user = cursor.fetchone()
        finally:
            connection.close()
        
        if user and check_password_hash(user[1],password):
            session.clear()
            session['user_id']=user[0]
            session['username']=username

            return redirect(url_for('home'))

        flash('Invalid Username or Password.')

    return render_template('login.html')

@app.route('/logout',methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))
    
@app.route('/')
@login_required
def home():
    tasks = load_tasks(session['user_id'])
    return render_template('index.html',tasks=tasks)

@app.route('/tasks/add',methods = ['POST'])
@login_required
def add_task_route():
    title = request.form.get("title")    
    description = request.form.get("description")
    status = request.form.get("status")

    add_task(session['user_id'], title, description, status)
    return redirect(url_for('home'))

@app.route('/tasks/edit',methods = ['POST'])
@login_required
def edit_task_route():
    number = request.form.get('number', type=int)
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    new_status = request.form.get('status')

    edit_task(session['user_id'], number, title, description, new_status )
    return redirect(url_for('home'))

@app.route('/tasks/delete',methods = ['POST'])
@login_required
def delete_task_route():
    number = request.form.get('number', type=int)

    delete_task(session['user_id'], number)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)