from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request, session
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
# from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, Boolean
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
# Import your forms from the forms.py
from forms import TicketForm, RegisterForm, LoginForm, CommentForm, ShoppingForm, CheckForm

import os


app = Flask(__name__)
app.config['SECRET_KEY'] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
ckeditor = CKEditor(app)
Bootstrap5(app)

# TODO: Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///concert.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class Order(db.Model):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True)
    phone: Mapped[str] = mapped_column(String(250))
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    ticket: Mapped[int] = mapped_column(Integer, nullable=True)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    school: Mapped[bool] = mapped_column(Boolean, default=False)
    bag: Mapped[int] = mapped_column(Integer, nullable=True)
    folder: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_s: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_m: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_l: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_xl: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_xxl: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_3xl: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_4xl: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_c_s: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_c_m: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_c_l: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_c_xl: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_c_3xl: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_c_4xl: Mapped[int] = mapped_column(Integer, nullable=True)
    total_cost: Mapped[int] = mapped_column(Integer, nullable=True)
    author_id = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="parent_post")


# TODO: Create a User table for all your registered users.
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    posts = relationship("Order", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    author_id = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    post_id = mapped_column(Integer, db.ForeignKey("order.id"))
    parent_post = relationship("Order", back_populates="comments")


with app.app_context():
    db.create_all()


# TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        register_email = form.email.data
        if User.query.filter_by(email=register_email) and not current_user:
            flash("This email has been registered. Please logged in.")
            return redirect(url_for("login"))
        else:
            pass_hash = generate_password_hash(form.password.data, method="pbkdf2", salt_length=8)
            new_user = User(
                email=register_email,
                name=form.name.data,
                password=pass_hash
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("home"))
    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)


# TODO: Retrieve a user from the database based on their email. 
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(session.pop('original_page',  url_for("home")))
        # 如果有儲存上一頁的紀錄，就會回到登入前的頁面，不然就回home
        else:
            flash("No match user or wrong password.")
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    flash("Successfully logout")
    return redirect(url_for('home'))


@app.route('/')
def home():
    result = db.session.execute(db.select(Order))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts,
                           logged_in=current_user.is_authenticated,
                           user_id=current_user.id if current_user.is_authenticated else None)


# TODO: Allow logged-in users to comment on post
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = db.get_or_404(Order, post_id)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            session['original_page'] = request.referrer  #將原始訪問的頁面（即評論頁面）保存下來
            flash("You have to login or register to comment.")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=form.comment.data,
            author_id=current_user.id,
            post_id=post_id,
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))
    result = db.session.execute(db.select(Comment))
    comments = result.scalars().all()
    return render_template("post.html",
                           post=requested_post,
                           form=form,
                           all_comments=comments,
                           logged_in=current_user.is_authenticated,)


def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(401)
        if current_user.id != 1:
            return abort(403)
        return func(*args, **kwargs)
    return wrapper


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-order", methods=["GET", "POST"])
def add_new_post():
    form = TicketForm()
    if form.validate_on_submit():
        if form.school.data:
            cost = form.ticket.data * 350
        else:
            cost = form.ticket.data * 500
        session['ticket_form_data'] = {
            'name': form.name.data,
            'ticket': form.ticket.data,
            'phone': form.phone.data,
            'school': form.school.data,
            'email': form.email.data,
            'ticket_cost': cost
        }
        if form.submit.data:
            return redirect(url_for("check_order"))
        elif form.shopping.data:
            return redirect(url_for("shopping"))
    return render_template("ticket.html", form=form)


@app.route("/shopping", methods=["POST", "GET"])
def shopping():
    shopping_form = ShoppingForm()
    if shopping_form.validate_on_submit():
        cost = (shopping_form.bag.data*300 + shopping_form.folder.data*130
                + shopping_form.cloth_a_s.data*200
                + shopping_form.cloth_a_m.data*200
                + shopping_form.cloth_a_l.data*200
                + shopping_form.cloth_a_xl.data*200
                + shopping_form.cloth_a_xxl.data*200
                + shopping_form.cloth_a_3xl.data*200
                + shopping_form.cloth_a_4xl.data*200
                + shopping_form.cloth_c_s.data*200
                + shopping_form.cloth_c_m.data*200
                + shopping_form.cloth_c_l.data*200
                + shopping_form.cloth_c_xl.data*200
                + shopping_form.cloth_c_3xl.data*200
                + shopping_form.cloth_c_4xl.data*200
                )
        session['shopping_form_data'] = {
            'bag': shopping_form.bag.data,
            'folder': shopping_form.folder.data,
            "cloth_a_s": shopping_form.cloth_a_s.data,
            "cloth_a_m": shopping_form.cloth_a_m.data,
            "cloth_a_l": shopping_form.cloth_a_l.data,
            "cloth_a_xl": shopping_form.cloth_a_xl.data,
            "cloth_a_xxl": shopping_form.cloth_a_xxl.data,
            "cloth_a_3xl": shopping_form.cloth_a_3xl.data,
            "cloth_a_4xl": shopping_form.cloth_a_4xl.data,
            "cloth_c_s": shopping_form.cloth_c_s.data,
            "cloth_c_m": shopping_form.cloth_c_m.data,
            "cloth_c_l": shopping_form.cloth_c_l.data,
            "cloth_c_xl": shopping_form.cloth_c_xl.data,
            "cloth_c_3xl": shopping_form.cloth_c_3xl.data,
            "cloth_c_4xl": shopping_form.cloth_c_4xl.data,
            'shopping_cost': cost
        }
        return redirect(url_for("check_order"))
    return render_template("shopping.html", form=shopping_form)


# 查詢訂單功能
@app.route("/check_order", methods=["GET", "POST"])
def check_order():
    form = CheckForm()
    if "shopping_form_data" in session:
        cost = session['shopping_form_data']["shopping_cost"] + session['ticket_form_data']["ticket_cost"]
        new_order = Order(
            name=session['ticket_form_data']['name'],
            ticket=session['ticket_form_data']['ticket'],
            date=date.today().strftime("%B %d, %Y"),
            phone=session['ticket_form_data']['phone'],
            school=session['ticket_form_data']['school'],
            email=session['ticket_form_data']['email'],
            bag=session['shopping_form_data']['bag'],
            folder=session['shopping_form_data']['folder'],
            cloth_a_s=session["shopping_form_data"]["cloth_a_s"],
            cloth_a_m=session["shopping_form_data"]["cloth_a_m"],
            cloth_a_l=session["shopping_form_data"]["cloth_a_l"],
            cloth_a_xl=session["shopping_form_data"]["cloth_a_xl"],
            cloth_a_xxl=session["shopping_form_data"]["cloth_a_xxl"],
            cloth_a_3xl=session["shopping_form_data"]["cloth_a_3xl"],
            cloth_a_4xl=session["shopping_form_data"]["cloth_a_4xl"],
            cloth_c_s=session["shopping_form_data"]["cloth_c_s"],
            cloth_c_m=session["shopping_form_data"]["cloth_c_s"],
            cloth_c_l=session["shopping_form_data"]["cloth_c_s"],
            cloth_c_xl=session["shopping_form_data"]["cloth_c_s"],
            cloth_c_3xl=session["shopping_form_data"]["cloth_c_s"],
            cloth_c_4xl=session["shopping_form_data"]["cloth_c_s"],
            total_cost=cost)
    else:
        cost = session['ticket_form_data']["ticket_cost"]
        new_order = Order(
            name=session['ticket_form_data']['name'],
            ticket=session['ticket_form_data']['ticket'],
            date=date.today().strftime("%B %d, %Y"),
            phone=session.ticket_form_data.phone,
            school=session['ticket_form_data']['school'],
            email=session['ticket_form_data']['email'],
            total_cost=cost)
    if form.validate_on_submit():
        db.session.add(new_order)
        db.session.commit()
        flash("Successfully logout")
        session.pop('ticket_form_data', None)
        session.pop('shopping_form_data', None)
        return redirect(url_for("home"))
    return render_template("check.html", form=form, session=session, cost=cost)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(Order, post_id)
    edit_form = TicketForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(Order, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
