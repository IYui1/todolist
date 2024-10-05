from flask import Flask, render_template, redirect, url_for, request, flash
from flask import Flask, abort, render_template, redirect, url_for, flash, request, has_request_context, g
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE IN DB

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    
class Item2(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200),nullable = False)
    
class Item3(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200),nullable = False)
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    
class Task2(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200),nullable = False)
    
class Task3(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200),nullable = False)

class Schedule1(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    monday = db.Column(db.String(200),nullable = False)
    tuesday = db.Column(db.String(200),nullable = False)
    wednesday = db.Column(db.String(200),nullable = False)
    thursday = db.Column(db.String(200),nullable = False)
    friday = db.Column(db.String(200),nullable = False)
    saturday = db.Column(db.String(200),nullable = False)

class Schedule2(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200),nullable = False)
    
class Schedule3(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200),nullable = False)

    
    def is_active(self):
        return True
    
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html',user=current_user)
@app.route("/todolist", methods=["GET", "POST"])
def todolist():
    selected_item_ids = request.form.getlist("item_ids")
    selected_priority_ids = request.form.getlist("priority_ids")
    selected_urgent_ids =request.form.getlist("urgent_ids")
    if request.method == "POST":
        item_name = request.form.get("newItem")
        if item_name:
            new_item = Item(name=item_name)
            db.session.add(new_item)
            db.session.commit()
            flash("Item added to the list!")

        # Menangani penambahan item prioritas
        priority_name = request.form.get("newPriority")
        if priority_name:
            new_priority = Item2(name=priority_name)
            db.session.add(new_priority)
            db.session.commit()
            flash("Priority item added to the list!")
        urgent_name = request.form.get("newUrgent")
        if urgent_name:
            new_urgent = Item3(name = urgent_name)
            db.session.add(new_urgent)
            db.session.commit()
            flash("Urgent item added to the list!")
            
        return redirect(url_for("todolist"))
    all_text = db.session.execute(db.select(Item)).scalars().all()
    items = Item.query.all()
    priority_items = Item2.query.all()
    urgent_items = Item3.query.all()

    return render_template("todo.html", newListItems=items,text = all_text,priority_items = priority_items,urgent_items = urgent_items,selected_item_ids=selected_item_ids, selected_priority_ids=selected_priority_ids, selected_urgent_ids = selected_urgent_ids)
@app.route("/delete",methods = ["POST"])
def delete():
    item_ids = request.form.getlist('item_ids')
    task_ids = request.form.getlist('task_ids')

    # Handle item deletions
    if item_ids:
        for item_id in item_ids:
            item_to_delete = db.session.query(Item).get(item_id)
            if item_to_delete:
                db.session.delete(item_to_delete)
                db.session.commit()  # Commit after deletion
                flash("Item deleted from the list!")
        return redirect(url_for('todolist'))  # Redirect after item deletion

    # Handle task deletions
    if task_ids:
        for task_id in task_ids:
            task_to_delete = db.session.query(Task).get(task_id)
            if task_to_delete:
                db.session.delete(task_to_delete)
                db.session.commit()  # Commit after deletion
                flash("Task deleted from the list!")
        return redirect(url_for('task'))  # Redirect after task deletio

@app.route("/delete_priority", methods=["POST"])
def delete_priority():
    priority_ids = request.form.getlist('priority_ids')
    task_priority_ids = request.form.getlist('task_priority_ids')
    schedule_priority_ids = request.form.getlist("schedule_priority_ids")
    
    if priority_ids:
        for item_id in priority_ids:
            text_delete = db.get_or_404(Item2, item_id)
            db.session.delete(text_delete)   
        db.session.commit()
        return redirect(url_for('todolist'))

    if task_priority_ids:
        for item_id in task_priority_ids:
            text_delete = db.get_or_404(Task2,item_id)
            db.session.delete(text_delete)
        db.session.commit()
        return redirect(url_for('task'))
    
    if schedule_priority_ids:
        for item_id in schedule_priority_ids:
            text_delete = db.get_or_404(Schedule2,item_id)
            db.session.delete(text_delete)
        db.session.commit()
        return redirect(url_for('schedule'))
    
@app.route("/delete_urgent", methods=["POST"])
def delete_urgent():
    urgent_ids = request.form.getlist('Urgent_ids')
    task_urgent_ids = request.form.getlist('task_Urgent_ids')
    schedule_urgent_ids = request.form.getlist("schedule_urgent_ids")
    
    if urgent_ids:
        for item_id in urgent_ids:
            text_delete = db.get_or_404(Item3, item_id)
            db.session.delete(text_delete)
        db.session.commit()
        return redirect(url_for('todolist'))
    
    if task_urgent_ids:
        for item_id in task_urgent_ids:
            text_delete = db.get_or_404(Task3, item_id)
            db.session.delete(text_delete)
        db.session.commit()
        return redirect(url_for('task'))
    
    if schedule_urgent_ids:
        for item_id in schedule_urgent_ids:
            text_delete = db.get_or_404(Schedule3,item_id)
            db.session.delete(text_delete)
        db.session.commit()
        return redirect(url_for('schedule'))
    
@app.route('/task',methods=["GET", "POST"])
def task():
    selected_task_ids = request.form.getlist("task_ids")
    selected_task_priority_ids = request.form.getlist("task_priority_ids")
    selected_task_urgent_ids =request.form.getlist("task_urgent_ids")
    if request.method == "POST":
        item_name = request.form.get("newTask")
        if item_name:
            new_item = Task(name=item_name)
            db.session.add(new_item)
            db.session.commit()
            flash("Item added to the list!")

        # Menangani penambahan item prioritas
        priority_name = request.form.get("newTaskPriority")
        if priority_name:
            new_priority = Task2(name=priority_name)
            db.session.add(new_priority)
            db.session.commit()
            flash("Priority item added to the list!")
        urgent_name = request.form.get("newTaskUrgent")
        if urgent_name:
            new_urgent = Task3(name = urgent_name)
            db.session.add(new_urgent)
            db.session.commit()
            flash("Urgent item added to the list!")
            
        return redirect(url_for("task"))
    all_text = db.session.execute(db.select(Item)).scalars().all()
    task = Task.query.all()
    priority_task = Task2.query.all()
    urgent_task = Task3.query.all()
    return render_template("task.html", newListItems=task,text = all_text,priority_items = priority_task,urgent_items = urgent_task,selected_task_ids=selected_task_ids, selected_task_priority_ids=selected_task_priority_ids, selected_task_urgent_ids = selected_task_urgent_ids)
@app.route('/schedule',methods=["GET", "POST"])
def schedule():
    selected_schedule_ids = request.form.getlist("schedule_ids")
    selected_schedule_priority_ids = request.form.getlist("schedule_priority_ids")
    selected_schedule_urgent_ids =request.form.getlist("schedule_urgent_ids")
    if request.method == "POST":
        schedule_data = request.form.get('scheduleData')
        if schedule_data:
            data = json.loads(schedule_data)
            for entry in data:
                new_schedule = Schedule1(
                    monday=entry[0],
                    tuesday=entry[1],
                    wednesday=entry[2],
                    thursday=entry[3],
                    friday=entry[4],
                    saturday=entry[5]
                )
                db.session.add(new_schedule)
            db.session.commit()
            return redirect(url_for('schedule'))
        
        # Menangani penambahan item prioritas
        schedule_priority_name = request.form.get("newPrioritySchedule")
        if schedule_priority_name:
            new_priority = Schedule2(name=schedule_priority_name)
            db.session.add(new_priority)
            db.session.commit()
            flash("Priority item added to the list!")
        schedule_urgent_name = request.form.get("newUrgentSchedule")
        if schedule_urgent_name:
            new_urgent = Schedule3(name = schedule_urgent_name)
            db.session.add(new_urgent)
            db.session.commit()
            flash("Urgent item added to the list!")
            
        return redirect(url_for("schedule"))
    schedule = Schedule1.query.all()
    priority_schedule = Schedule2.query.all()
    urgent_schedule = Schedule3.query.all()
    return render_template("Schedule.html",selected_schedule_ids =selected_schedule_ids,selected_schedule_priority_ids=selected_schedule_priority_ids,
                           selected_schedule_urgent_ids = selected_schedule_urgent_ids,newListSchedule=schedule,priority_items = priority_schedule,urgent_items = urgent_schedule)



@app.route("/analytics")
def analytics():
    return render_template("analytics.html")
@app.route("/calender")
def calender():
    return render_template("calender.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your email and password.')

    return render_template("login.html", form=form)
@app.route('/register', methods = ["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template("register.html",form = form,current_user = current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True,port=5012)