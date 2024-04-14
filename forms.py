from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, URL, NumberRange
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class TicketForm(FlaskForm):
    name = StringField("訂購者姓名（必填）", validators=[DataRequired()])
    phone = StringField("連絡電話（必填）", validators=[DataRequired()])
    email = StringField("Email（必填）", validators=[DataRequired()])
    ticket = IntegerField("欲購買票數（定價：500元/張，每人限購兩張）",
                          default=0, validators=[NumberRange(min=0, max=2)])
    school = BooleanField("是否為團內購票(團內購票享有原價75折優惠，350元/張")
    sit_together = BooleanField("座位是否需連號？")
    submit = SubmitField("送出訂單")
    shopping = SubmitField("訂購紀念品")


class ShoppingForm(FlaskForm):
    bag = IntegerField("帆布包（定價：300元/個）", default=0, validators=[NumberRange(min=0)])
    folder = IntegerField("譜夾（定價：130元/個）", default=0, validators=[NumberRange(min=0)])
    cloth_a_s = IntegerField("團T：大人 - S號（身高155公分）", default=0, validators=[NumberRange(min=0)])
    cloth_a_m = IntegerField("團T：大人 - M號（身高160公分）", default=0, validators=[NumberRange(min=0)])
    cloth_a_l = IntegerField("團T：大人 - L號（身高165公分）", default=0, validators=[NumberRange(min=0)])
    cloth_a_xl = IntegerField("團T：大人 - XL號（身高170公分）", default=0, validators=[NumberRange(min=0)])
    cloth_a_xxl = IntegerField("團T：大人 - XXL號（身高175公分）", default=0, validators=[NumberRange(min=0)])
    cloth_a_3xl = IntegerField("團T：大人 - 3XL號（身高180公分）", default=0, validators=[NumberRange(min=0)])
    cloth_a_4xl = IntegerField("團T：大人 - 4XL號（身高185公分）", default=0, validators=[NumberRange(min=0)])
    cloth_c_s = IntegerField("團T：小孩 - s號（身高90公分）", default=0, validators=[NumberRange(min=0)])
    cloth_c_m = IntegerField("團T：小孩 - m號（身高100公分）", default=0, validators=[NumberRange(min=0)])
    cloth_c_l = IntegerField("團T：小孩 - l號（身高110公分）", default=0, validators=[NumberRange(min=0)])
    cloth_c_xl = IntegerField("團T：小孩 - xl號（身高120公分）", default=0, validators=[NumberRange(min=0)])
    cloth_c_xxl = IntegerField("團T：小孩 - xxl號（身高130公分）", default=0, validators=[NumberRange(min=0)])
    cloth_c_3xl = IntegerField("團T：小孩 - 3xl號（身高140公分）", default=0, validators=[NumberRange(min=0)])
    cloth_c_4xl = IntegerField("團T：小孩 - 4xl號（身高150公分）", default=0, validators=[NumberRange(min=0)])


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
