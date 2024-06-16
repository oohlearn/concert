from datetime import date, datetime
from flask import Flask, abort, render_template, redirect, url_for, flash, request, session
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
# from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
# Import your forms from the forms.py
from forms import (TicketForm, ShoppingForm, CheckForm, InfoForm)
import smtplib
from email.mime.text import MIMEText

from config import Config
from jinja2 import Template


import os


ticket_count = 0
ticket_limit = int(os.environ.get("TICKET_LIMIT"))


app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
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


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "SQLALCHEMY_DATABASE_URI")

db = SQLAlchemy(model_class=Base)
db.init_app(app)
ticket_open = False


# CONFIGURE TABLES
class Order(db.Model):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(250))
    phone: Mapped[str] = mapped_column(String(250))
    email: Mapped[str] = mapped_column(Text, nullable=False)
    bank_account: Mapped[str] = mapped_column(Integer, nullable=False)
    paid_date: Mapped[str] = mapped_column(String(250), nullable=False)
    school: Mapped[bool] = mapped_column(Boolean, default=False)
    ticket: Mapped[int] = mapped_column(Integer, nullable=True)
    bag: Mapped[int] = mapped_column(Integer, nullable=True)
    folder: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_xs: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_s: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_m: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_l: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_xl: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_xxl: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_3xl: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_4xl: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_a_6xl: Mapped[int] = mapped_column(Integer, nullable=True)

    cloth_c_110: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_c_120: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_c_130: Mapped[int] = mapped_column(Integer, nullable=True)
    cloth_c_140: Mapped[int] = mapped_column(Integer, nullable=True)
    total_cost: Mapped[int] = mapped_column(Integer, nullable=True)


# TODO: Create a User table for all your registered users

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    result = db.session.execute(db.select(Order))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts,
                           ticket_count=ticket_count,
                           logged_in=current_user.is_authenticated,
                           user_id=current_user.id
                           if current_user.is_authenticated else None)


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-order", methods=["GET", "POST"])
def add_new_post():
    session.pop('shopping_form_data', None)
    if ticket_open:
        form = TicketForm()
        if form.email.data is None or form.name.data is None or form.phone.data is None or form.bank_account.data is None or form.paid_date.data is None:
            flash("訂購人姓名、電話、email、匯款帳號末五碼及匯款日期為必填資訊")
            return render_template("ticket.html", form=form)
        if form.validate_on_submit():

            cost = form.ticket.data * 500
            session['ticket_form_data'] = {
                'name': form.name.data,
                'ticket': form.ticket.data,
                'phone': form.phone.data,
                'school': False,
                'email': form.email.data,
                'ticket_cost': cost,
                "bank_account": form.bank_account.data,
                "paid_date": form.paid_date.data.strftime('%Y/%m/%d')
            }
            if form.submit.data:
                return redirect(url_for("check_order"))
            elif form.shopping.data:
                return redirect(url_for("shopping"))

    else:
        form = InfoForm()
        if form.email.data is None or form.name.data is None or form.phone.data is None or form.bank_account.data is None or form.paid_date.data is None:
            flash("訂購人姓名、電話、email、匯款帳號末五碼及匯款日期為必填資訊")
            return render_template("ticket.html", form=form)
        if form.validate_on_submit():
            session['ticket_form_data'] = {
                'name': form.name.data,
                'ticket': 0,
                'phone': form.phone.data,
                'school': False,
                'email': form.email.data,
                'ticket_cost': 0,
                "bank_account": form.bank_account.data,
                "paid_date": form.paid_date.data.strftime('%Y/%m/%d')
            }
            return redirect(url_for("shopping"))
    return render_template("ticket.html", form=form)


@app.route("/shopping", methods=["POST", "GET"])
def shopping():
    shopping_form = ShoppingForm()
    session.pop('shopping_form_data', None)
    if shopping_form.validate_on_submit():
        cost = (shopping_form.bag.data*300 + shopping_form.folder.data*130
                + shopping_form.cloth_a_xs.data*200
                + shopping_form.cloth_a_s.data*200
                + shopping_form.cloth_a_m.data*200
                + shopping_form.cloth_a_l.data*200
                + shopping_form.cloth_a_xl.data*200
                + shopping_form.cloth_a_xxl.data*200
                + shopping_form.cloth_a_3xl.data*200
                + shopping_form.cloth_a_4xl.data*200
                + shopping_form.cloth_a_6xl.data*200
                + shopping_form.cloth_c_110.data*200
                + shopping_form.cloth_c_120.data*200
                + shopping_form.cloth_c_130.data*200
                + shopping_form.cloth_c_140.data*200
                )
        session['shopping_form_data'] = {
            'bag': shopping_form.bag.data,
            'folder': shopping_form.folder.data,
            "cloth_a_xs": shopping_form.cloth_a_xs.data,
            "cloth_a_s": shopping_form.cloth_a_s.data,
            "cloth_a_m": shopping_form.cloth_a_m.data,
            "cloth_a_l": shopping_form.cloth_a_l.data,
            "cloth_a_xl": shopping_form.cloth_a_xl.data,
            "cloth_a_xxl": shopping_form.cloth_a_xxl.data,
            "cloth_a_3xl": shopping_form.cloth_a_3xl.data,
            "cloth_a_4xl": shopping_form.cloth_a_4xl.data,
            "cloth_a_6xl": shopping_form.cloth_a_6xl.data,

            "cloth_c_110": shopping_form.cloth_c_110.data,
            "cloth_c_120": shopping_form.cloth_c_120.data,
            "cloth_c_130": shopping_form.cloth_c_130.data,
            "cloth_c_140": shopping_form.cloth_c_140.data,
            'shopping_cost': cost
        }
        return redirect(url_for("check_order"))
    return render_template("shopping.html",
                           form=shopping_form,
                           ticket_open=ticket_open)


# 查詢訂單功能
@app.route("/check_order", methods=["GET", "POST"])
def check_order():
    global ticket_count
    global ticket_open
    global ticket_limit
    form = CheckForm()
    order_info = {}
    order_list = {}
    if "shopping_form_data" in session:
        cost = session['shopping_form_data']["shopping_cost"] + session['ticket_form_data']["ticket_cost"]
        new_order = Order(
            name=session['ticket_form_data']['name'],
            ticket=session['ticket_form_data']['ticket'],
            date=date.today().strftime("%B %d, %Y"),
            phone=session['ticket_form_data']['phone'],
            bank_account=session["ticket_form_data"]["bank_account"],
            paid_date=session["ticket_form_data"]["paid_date"],
            school=False,
            email=session['ticket_form_data']['email'],
            bag=session['shopping_form_data']['bag'],
            folder=session['shopping_form_data']['folder'],
            cloth_a_xs=session["shopping_form_data"]["cloth_a_xs"],
            cloth_a_s=session["shopping_form_data"]["cloth_a_s"],
            cloth_a_m=session["shopping_form_data"]["cloth_a_m"],
            cloth_a_l=session["shopping_form_data"]["cloth_a_l"],
            cloth_a_xl=session["shopping_form_data"]["cloth_a_xl"],
            cloth_a_xxl=session["shopping_form_data"]["cloth_a_xxl"],
            cloth_a_3xl=session["shopping_form_data"]["cloth_a_3xl"],
            cloth_a_4xl=session["shopping_form_data"]["cloth_a_4xl"],
            cloth_a_6xl=session["shopping_form_data"]["cloth_a_6xl"],

            cloth_c_110=session["shopping_form_data"]["cloth_c_110"],
            cloth_c_120=session["shopping_form_data"]["cloth_c_120"],
            cloth_c_130=session["shopping_form_data"]["cloth_c_130"],
            cloth_c_140=session["shopping_form_data"]["cloth_c_140"],
            total_cost=cost)
    else:
        cost = session['ticket_form_data']["ticket_cost"]
        new_order = Order(
            name=session['ticket_form_data']['name'],
            ticket=session['ticket_form_data']['ticket'],
            date=date.today().strftime("%B %d, %Y"),
            phone=session['ticket_form_data']["phone"],
            school=False,
            email=session['ticket_form_data']['email'],
            bank_account=session["ticket_form_data"]["bank_account"],
            paid_date=session["ticket_form_data"]["paid_date"],
            total_cost=cost)
    order_info = {
            "訂購者姓名": new_order.name,
            "電話": new_order.phone,
            "email": new_order.email,
            "匯款帳號末五碼": new_order.bank_account,
            "匯款日期": new_order.paid_date,
    }
    order_list = {
            "音樂會門票": new_order.ticket,
            "帆布包": new_order.bag,
            "譜夾": new_order.folder,
            "團T：大人 - XS 號": new_order.cloth_a_xs,
            "團T：大人 - S 號": new_order.cloth_a_s,
            "團T：大人 - M 號": new_order.cloth_a_m,
            "團T：大人 - L 號": new_order.cloth_a_l,
            "團T：大人 - XL 號": new_order.cloth_a_xl,
            "團T：大人 - XXL 號": new_order.cloth_a_xxl,
            "團T：大人 - 3XL 號": new_order.cloth_a_3xl,
            "團T：大人 - 4XL 號": new_order.cloth_a_4xl,
            "團T：大人 - 6XL 號": new_order.cloth_a_6xl,

            "團T：小孩 - 身高110公分": new_order.cloth_c_110,
            "團T：小孩 - 身高120公分": new_order.cloth_c_120,
            "團T：小孩 - 身高130公分": new_order.cloth_c_130,
            "團T：小孩 - 身高140公分": new_order.cloth_c_140,
        }
    if form.validate_on_submit():
        mail_content = """
        <h3>您的訂單資料如下，請確認以下內容是否正確，並於訂購當日匯款</h3>
        <h3>若有問題請洽小佳老師</h3>
      <p>訂購者資訊</p>
      <ul>
        {%for key, value in order_info.items() %} {% if value != None %}
        <li>{{key}}：{{value}}</li>
        {%endif%}{%endfor%}
      </ul>
      <p>商品明細</p>
      <ol>
        {%for key, value in order_list.items() %} {% if value != None and value
        != 0 %}
        <li>{{key}}：{{value}}</li>
        {%endif%} {%endfor%}
      </ol>
      <h3 style="color: brown">總金額：{{cost}}</h3>
      <hr>
      <p>匯款資料</p>
      <ul>
      <li>帳號：郵局(700) 0002661 0374550</li>
      <li>戶名：臺北市南港區成德國民小學國樂團家長後援會游修靜</li>
      </ul>
        """
        template = Template(mail_content)
        mail_content = template.render(order_info=order_info, order_list=order_list, cost=cost)
        sender = "testc1386@gmail.com"
        receiver = order_info["email"]
        my_email = "testc1386@gmail.com"
        password = os.environ.get("PASSWORD")
        mime = MIMEText(mail_content, "html", "utf-8")
        mime["Subject"] = "成德國小十周年音樂會門票及紀念品訂單明細"
        msg = mime.as_string()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.login(user=my_email, password=password)
            connection.sendmail(sender,
                                receiver,
                                msg)
        db.session.add(new_order)
        db.session.commit()
        flash("訂單已送出，明細已寄送至填寫的信箱（請檢查垃圾郵件）")
        flash("若有問題，請聯絡小佳老師")
        if ticket_open:
            ticket_count += new_order.ticket
        if ticket_count >= ticket_limit:
            ticket_open = False
        session.pop('ticket_form_data', None)
        session.pop('shopping_form_data', None)
        return redirect(url_for("home"))
    return render_template("check.html", form=form, session=session,
                           cost=cost, order_list=order_list,
                           order_info=order_info,
                           )


if __name__ == "__main__":
    app.run(debug=False, port=5002)
