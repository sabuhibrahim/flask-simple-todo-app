import os


from flask import Flask, render_template, redirect, url_for, request, escape, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)

from sqlalchemy.sql import func
from sqlalchemy import or_, and_
from sqlalchemy.orm import relationship
from main.forms import LoginForm, RegisterForm, TodoForm

this_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

app.config["SECRET_KEY"] = "dGwqIYV9C4cHdFOP2L9DyXKtqtbtUiGQ"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + this_dir + "/todo.db"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

bcrypt = Bcrypt(app)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String)
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_date = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, None, db.ForeignKey("users.id"))
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    complete = db.Column(db.Boolean)
    date_cr = db.Column(db.DateTime(timezone=True), server_default=func.now())
    date_up = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/")
@login_required
def index():
    form = TodoForm()
    todos = Todolist.query.filter_by(user_id=current_user.id)
    return render_template("index.html", form=form, todos=todos)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    messages = []
    if request.method == "POST" and form.validate_on_submit():
        user = Users.query.filter(
            or_(Users.username == form.username.data, Users.email == form.username.data)
        ).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for("index"))
        messages.append("Username/Email or password wrong")
    return render_template("login.html", form=form, messages=messages)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    messages = []
    if request.method == "POST" and form.validate_on_submit():
        error = None
        user = Users.query.filter(
            or_(Users.username == form.username.data, Users.email == form.username.data)
        ).first()
        if user:
            error = True
            messages.append("This username or email already registered")
        if error != True:
            password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            new_user = Users(
                username=form.username.data,
                email=form.email.data,
                password=password,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=form.remember.data)
            return redirect(url_for("index"))
    return render_template("register.html", form=form, messages=messages)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route(
    "/add",
    methods=[
        "POST",
    ],
)
@login_required
def addTodo():
    form = TodoForm()
    if form.validate_on_submit():
        new_todo = Todolist(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            complete=False,
        )
        db.session.add(new_todo)
        db.session.commit()
        return jsonify(
            {
                "message": "OK",
                "id": new_todo.id,
                "title": new_todo.title,
                "description": new_todo.description,
            }
        )
    return jsonify(
        {
            "message": "BAD",
            "errors": form.errors,
        }
    )


@app.route("/update/<int:todo_id>")
@login_required
def update(todo_id):
    todo = Todolist.query.filter_by(id=todo_id).first()
    if todo.user_id == current_user.id:
        db.session.query(Todolist).filter_by(id=todo_id).update({"complete": 1})
        db.session.commit()
        return jsonify({"message": "OK"})
    return jsonify({"message": "BAD"})


@app.route("/delete/<int:todo_id>")
@login_required
def delete(todo_id):
    todo = Todolist.query.filter_by(id=todo_id).first()
    if todo.user_id == current_user.id:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"message": "OK"})
    return jsonify({"message": "BAD"})


@app.route("/search/<string:text>")
@login_required
def search(text):
    user_todos = Todolist.query.filter(
        and_(
            Todolist.user_id == current_user.id,
            or_(
                Todolist.title.like("%" + text + "%"),
                Todolist.description.like("%" + text + "%"),
            ),
        )
    )
    todos = []
    for todo in user_todos:
        todos.append(
            {
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "complete": todo.complete,
            }
        )
    return jsonify(todos)


@app.route("/search/")
@login_required
def searchAll():
    user_todos = Todolist.query.filter(Todolist.user_id == current_user.id)
    todos = []
    for todo in user_todos:
        todos.append(
            {
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "complete": todo.complete,
            }
        )
    return jsonify(todos)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
