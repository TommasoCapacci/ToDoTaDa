from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from markupsafe import escape

app = Flask(__name__)
app.config['SECRET_KEY'] = '85943d5610ca03df6877641a021bedfd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import User, Todo
from forms import RegistrationForm, LoginForm


# WEBSITE ROUTES

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # create new user here
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, no_home=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # authenticate user here
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            return render_template('login.html', title='Login unsuccesful! Please try again', form=form, no_home=True)
    return render_template('login.html', title='Login', form=form, no_home=True)

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route('/')
@app.route('/home')
@login_required
def home():
    filter = request.args.get("filter")
    show_completed = request.args.get("show_completed")
    username = ''
    todo_list = []
    try:
        user = User.query.get(int(current_user.get_id()))
        username = user.username
        todo_query = Todo.query.where(Todo.user_id==user.id)
        # filter todos
        if filter:
            todo_query = todo_query.where(Todo.title.like(f'%{filter}%')).order_by(Todo.id.desc())
        else:
            todo_query = todo_query.order_by(Todo.id.desc())
        # show only requested todos
        if show_completed and show_completed == "true":
            todo_list = todo_query.all()
        else:
            todo_list = todo_query.filter_by(completed=False).all()
    except:
        db.create_all()
    return render_template('home.html', title=username+'\'s Todos', todo_list=todo_list, filter=filter, show_completed=show_completed)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return render_template('create.html', title='Create a new Todo')
    else:
        # we get the data by the form, so from the POST request body
        title = escape(request.form.get('title'))
        new_todo = Todo(title=title, user_id=int(current_user.get_id()))
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def edit(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != int(current_user.get_id()):
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('edit.html', title='Edit your Todo', todo=todo)
    else:
        todo.title = request.form.get('title')
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/done/<int:todo_id>', methods=['POST'])
@login_required
def done(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != int(current_user.get_id()):
        return redirect(url_for('home'))
    todo.completed = True
    db.session.commit()
    filter = request.form.get('filter')
    show_completed = request.form.get('show_completed')
    if filter and filter != 'None':
        if show_completed and show_completed != 'None':
            return redirect(url_for('home', filter=filter, show_completed=show_completed))
        else:
            return redirect(url_for('home', filter=filter))
    else:
        if show_completed and show_completed != 'None':
            return redirect(url_for('home', show_completed=show_completed))
        else:
            return redirect(url_for('home'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
@login_required
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != int(current_user.get_id()):
        return redirect(url_for('home'))
    db.session.delete(todo)
    db.session.commit()
    filter = request.form.get('filter')
    show_completed = request.form.get('show_completed')
    if filter and filter != 'None':
        if show_completed and show_completed != 'None':
            return redirect(url_for('home', filter=filter, show_completed=show_completed))
        else:
            return redirect(url_for('home', filter=filter))
    else:
        if show_completed and show_completed != 'None':
            return redirect(url_for('home', show_completed=show_completed))
        else:
            return redirect(url_for('home'))




