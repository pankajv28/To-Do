from todo import add_task, edit_task, delete_task, load_tasks
from manage_users import create_user, edit_password, login_user, show_users, delete_user
from flask import Flask, render_template, session, request, redirect, url_for, flash
import sqlite3
from werkzeug.middleware.proxy_fix import ProxyFix
import os

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

#app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.secret_key = '6f0e57a4138b5269a46e63d716b84156145d7a2433187a98f6e22d0ca49a1783'

#login route
@app.route('/login', methods = ['POST','GET'])
def login():

    if request.method == 'GET':
        return render_template('login.html')
    else: 
        session.clear()
        username = request.form['username']
        password = request.form['password']
        login, user, group = login_user(username,password)
        if login:
            session['user_id'] = user
            session['status'] = True
            session['username'] = username
            if group == 'admin':
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
            selected_group = request.form.get("group", "normal")
            create_user(request.form['username'],request.form['password'], selected_group)
            flash ('User Created.','success')
        except sqlite3.IntegrityError :
            flash ('Username already exists','error')
        return redirect(url_for('admin', group = selected_group))
    else :
        flash ('Passwords dont match','error')
        return (redirect(url_for('createuser')))

#edit_forgot_password
@app.route('/users/edit_password', methods = ['POST'])
def editpassword():
    if request.form['password'] == request.form['confirm_password'] :
        selected_group = request.form.get("group", "normal")
        if edit_password(request.form['username'],request.form['password']):
            flash ('Password Changed','success')
        else :
            flash ('Password not changed.','error')
        return redirect(url_for('admin', group=selected_group))
    else :
        flash ('Passwords dont match','error')
        return (redirect(url_for('editpassword')))

#delete_user
@app.route('/users/delete_user', methods = ['POST'])
def deleteuser():
    if session.get('status', False):
        selected_group = request.form.get("group", "normal")
        if request.form['username'] == session['username']:
            flash('Logged in user cant be deleted.','error')
        else:
            delete_user(request.form['username'])
            flash('User Deleted.', 'success')
        return (redirect(url_for('admin',group=selected_group)))
    else :
        session.clear()
        return (redirect(url_for('login')))

#show_users
@app.route('/users', methods = ['GET'])
def admin():
    if session.get('status', False):
        users = show_users()
        selected_group = request.args.get("group", "normal")
        return render_template('admin.html', users = users, selected_group = selected_group)
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
            add_task(request.form['title'],request.form['description'],request.form['status'],session['user_id'])
            return (redirect(url_for('home')))
        else :
            session.clear()
            return (redirect(url_for('login')))
    except ValueError as e:
        flash(str(e),'error')

#edit_task
@app.route('/edit_task', methods = ['POST'])
def edittask():
    if session.get('status', False):
        edit_task(request.form['task_number'],request.form['title'],request.form['description'],request.form['status'],session['user_id'])
        return (redirect(url_for('home')))
    else :
        session.clear()
        return (redirect(url_for('login')))
    
#delete_task
@app.route('/delete', methods = ['POST'])
def deletetask():
    if session.get('status', False):
        delete_task(request.form['task_number'],session['user_id'])
        return (redirect(url_for('home')))
    else :
        session.clear()
        return (redirect(url_for('login')))
    
#load_task
@app.route('/', methods = ['GET'])
def home():
    if session.get('status', False):
        tasks = load_tasks(session['user_id'])
        return render_template('index.html', tasks = tasks, username = session.get('username'))
    else :
        session.clear()
        return (redirect(url_for('login')))

if __name__ == '__main__':
    app.run(debug=True, port = 5001)