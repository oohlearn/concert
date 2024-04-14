from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, URL, NumberRange
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class TicketForm(FlaskForm):
    name = StringField("訂購者姓名", validators=[DataRequired()])
    phone = StringField("連絡電話", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    ticket = IntegerField("欲購買票數（定價：500元/張）")
    school = BooleanField("是否為團內購票(團內購票享有原價75折優惠，350元/張")
    sit_together = BooleanField("座位是否需連號？")
    submit = SubmitField("送出訂單")
    shopping = SubmitField("訂購紀念品")


class ShoppingForm(FlaskForm):
    bag = IntegerField("帆布包（定價：300元/個）", default=0)
    folder = IntegerField("譜夾（定價：130元/個）", default=0)
    cloth_xs = IntegerField("團T-XS號（定價：200元/件）", default=0)
    cloth_s = IntegerField("團T-S號（定價：200元/件）", default=0)
    cloth_m = IntegerField("團T-M號（定價：200元/件）", default=0)
    cloth_l = IntegerField("團T-L號（定價：200元/件）", default=0)
    cloth_xl = IntegerField("團T-XL號（定價：200元/件）", default=0)
    submit = SubmitField("送出訂單")


class ClothAdultForm(FlaskForm):
    cloth_a_s = IntegerField("大人-S（身高155公分）", default=0)
    
class ClothChildren(FlaskForm):
    cloth_a_s = IntegerField("大人-S（身高155公分）", default=0)

    



class CheckForm(FlaskForm):
    submit_btn = SubmitField("確認訂單")

# TODO: Create a RegisterForm to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    submit_btn = SubmitField("SIGN ME UP!")


# TODO: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit_btn = SubmitField("LET ME IN!")


# TODO: Create a CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    comment = CKEditorField("Comment")
    submit_btn = SubmitField("Send Comment")
