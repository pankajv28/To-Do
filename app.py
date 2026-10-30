from todo import add_task, edit_task, delete_task, load_tasks, get_user_projects, archive_task, restore_task
from manage_users import create_user, edit_user, login_user, show_users, delete_user
from flask import Flask, render_template, session, request, redirect, url_for, flash, abort
import sqlite3
from werkzeug.middleware.proxy_fix import ProxyFix
import os

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

app.secret_key = os.environ["FLASK_SECRET_KEY"]

if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY is not set")

#login route
@app.route('/login', methods = ['POST','GET'])
def login():

    if request.method == 'GET':
        return render_template('login.html')
    else: 
        session.clear()
        username = request.form['username']
        password = request.form['password']
        login, name, user, role = login_user(username,password)
        if login:
            session['user_id'] = user
            session['status'] = True
            session['username'] = name
            session['role'] = role
            if role == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('home'))
        else:
            flash ('Incorrect Username or Password.','error')
            return redirect(url_for('login'))

#createuser
@app.route('/users/create_user', methods = ['POST'])
def createuser():
    if request.form['password'] == request.form['confirm_password'] :
        try:
            selected_role = request.form.get("role", "app")
            create_user(request.form['username'],request.form['displayname'],request.form['password'], selected_role)
            flash ('User Created.','success')
        except sqlite3.IntegrityError :
            flash ('Username already exists','error')
        return redirect(url_for('admin', role = selected_role))
    else :
        flash ('Passwords dont match','error')
        return (redirect(url_for('createuser')))

#edit_user_details
@app.route('/users/edit_user', methods = ['POST'])
def edituser():
    if request.form['password'] == request.form['confirm_password'] :
        selected_role = request.form.get("role", "app")
        if edit_user(request.form['username'], request.form['displayname'],request.form['password']):
            flash ('Password Changed','success')
        else :
            flash ('Password not changed.','error')
        return redirect(url_for('admin', role=selected_role))
    else :
        flash ('Passwords dont match','error')
        return (redirect(url_for('editpassword')))

#delete_user
@app.route('/users/delete_user', methods = ['POST'])
def deleteuser():
    if session.get('status', False):
        selected_role = request.form.get("role", "app")
        if request.form['username'] == session['username']:
            flash('Logged in user cant be deleted.','error')
        else:
            delete_user(request.form['username'])
            flash('User Deleted.', 'success')
        return (redirect(url_for('admin', role=selected_role)))
    else :
        session.clear()
        return (redirect(url_for('login')))

#show_users
@app.route('/users', methods = ['GET'])
def admin():
    if session.get('status', False):
        users = show_users()
        selected_role = request.args.get("role", "app")
        return render_template('admin.html', users = users, selected_role = selected_role)
    else :
        session.clear()
        return (redirect(url_for('login')))

#logout
@app.route("/logout")
def logout():
    session.clear()
    flash('User Logged out Successfully','success')
    return (render_template('login.html'))

#add_task
@app.route('/add_task', methods = ['POST'])
def addtask():
    try:
        if session.get('status', False):
            add_task(request.form['title'],request.form['description'],request.form['status'],request.form['project_id'],session['user_id'])
            return (redirect(url_for('home', status_view = request.form.get('return_status', 'done'), project_id = request.form.get('project_id', type=int))))
        else :
            session.clear()
            return (redirect(url_for('login')))
    except ValueError as e:
        flash(str(e),'error')

#edit_task
@app.route('/edit_task', methods = ['POST'])
def edittask():
    if session.get('status', False):
        edit_task(request.form['task_number'],request.form['title'],request.form['description'],request.form['status'])
        return (redirect(url_for('home', status_view = request.form.get('return_status', 'done'), project_id = request.form.get('project_id', type=int))))
    else :
        session.clear()
        return (redirect(url_for('login')))
    
#delete_task
@app.route('/delete', methods = ['POST'])
def deletetask():
    if session.get('status', False):
        delete_task(request.form['task_number'])
        return (redirect(url_for('home', status_view = request.form.get('return_status', 'done'), project_id = request.form.get('project_id', type=int))))
    else :
        session.clear()
        return (redirect(url_for('login')))

#archive_task
@app.route('/archive', methods = ['POST'])
def archivetask():
    if session.get('status', False):
        archive_task(request.form.get('task_number'))
        return (redirect(url_for('home', status_view = request.form.get('return_status', 'done'), project_id = request.form.get('project_id', type=int))))
    else :
        session.clear()
        return (redirect(url_for('login')))

#restore_task
@app.route('/restore', methods = ['POST'])
def restoretask():
    if session.get('status', False):
        restore_task(request.form.get('task_number'))
        return (redirect(url_for('home', status_view = request.form.get('return_status', 'done'), project_id = request.form.get('project_id', type=int))))
    else :
        session.clear()
        return (redirect(url_for('login')))
    
#load_task
@app.route('/', methods = ['GET'])
def home():
    if session.get('status', False):
        user_id = session['user_id']
        projects = get_user_projects(user_id)
        tasks = []
        selected_project_id = None
        selected_status = request.args.get('status_view', 'done')
        if selected_status not in ('done','skipped','archived'):
            selected_status = 'done'
        if projects :
            allowed_project_ids = [row[0] for row in projects]
            project_id = request.args.get("project_id",type= int)
            if project_id in allowed_project_ids:
                selected_project_id = project_id
            else:
                selected_project_id = allowed_project_ids[0]
            tasks = load_tasks(selected_project_id)
        return render_template('index.html', tasks = tasks, username = session.get('username'), projects = projects, selected_project_id = selected_project_id, role = session['role'], selected_status=selected_status)
    else :
        session.clear()
        return (redirect(url_for('login')))

# Create Project    
@app.route('/projects/create')
def create_project():
    if not session.get('status', False):
        return redirect(url_for('login'))
    if session.get('role') != 'super':
        abort(403)
    return render_template(
        'project_placeholder.html',
        page_title='Create project',
        username=session.get('username')
    )

# Manage Project
@app.route('/projects/manage')
def manage_projects():
    if not session.get('status', False):
        return redirect(url_for('login'))
    if session.get('role') != 'super':
        abort(403)
    return render_template(
        'project_placeholder.html',
        page_title='Manage projects',
        username=session.get('username')
    )

if __name__ == '__main__':
    app.run(debug=True, port = 5001)