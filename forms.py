from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, NumberRange


# WTForm for creating a blog post
class TicketForm(FlaskForm):
    name = StringField("訂購者姓名（必填）", validators=[DataRequired()])
    phone = StringField("連絡電話（必填）", validators=[DataRequired()])
    email = StringField("Email（必填，訂單送出後會寄送訂單明細）", validators=[DataRequired()])
    bank_account = StringField("匯款帳號末五碼（必填）", validators=[DataRequired()])
    paid_date = DateField("匯款日期（必填）", validators=[DataRequired()])
    ticket = IntegerField("欲購買票數（定價：500元/張，每人限購兩張）",
                          default=0, validators=[NumberRange(min=0, max=2)])
    school = BooleanField("是否為團內購票（團內購票享有原價7折優惠，350元/張）")
    submit = SubmitField("送出訂單")
    shopping = SubmitField("訂購紀念品")


class InfoForm(FlaskForm):
    name = StringField("訂購者姓名（必填）", validators=[DataRequired()])
    phone = StringField("連絡電話（必填）", validators=[DataRequired()])
    email = StringField("Email（必填）", validators=[DataRequired()])
    bank_account = IntegerField("匯款帳號末五碼（必填）", validators=[DataRequired()])
    paid_date = DateField("匯款日期（必填）", validators=[DataRequired()])
    shopping = SubmitField("訂購紀念品")


class ShoppingForm(FlaskForm):
    bag = IntegerField("帆布包（售價：300元/個）", default=0, validators=[NumberRange(min=0)])
    folder = IntegerField("譜夾（售價：130元/個）", default=0, validators=[NumberRange(min=0)])
    cloth_a_xs = IntegerField("團T：大人 - XS號", default=0, validators=[NumberRange(min=0)])
    cloth_a_s = IntegerField("團T：大人 - S號", default=0, validators=[NumberRange(min=0)])
    cloth_a_m = IntegerField("團T：大人 - M號", default=0, validators=[NumberRange(min=0)])
    cloth_a_l = IntegerField("團T：大人 - L號", default=0, validators=[NumberRange(min=0)])
    cloth_a_xl = IntegerField("團T：大人 - XL號", default=0, validators=[NumberRange(min=0)])
    cloth_a_xxl = IntegerField("團T：大人 - XXL號", default=0, validators=[NumberRange(min=0)])
    cloth_a_3xl = IntegerField("團T：大人 - 3XL號", default=0, validators=[NumberRange(min=0)])
    cloth_a_4xl = IntegerField("團T：大人 - 4XL號", default=0, validators=[NumberRange(min=0)])
    cloth_a_6xl = IntegerField("團T：大人 - 6XL號", default=0, validators=[NumberRange(min=0)])

    cloth_c_110 = IntegerField("團T：小孩 - 身高110公分", default=0, validators=[NumberRange(min=0)])
    cloth_c_120 = IntegerField("團T：小孩 - 身高120公分", default=0, validators=[NumberRange(min=0)])
    cloth_c_130 = IntegerField("團T：小孩 - 身高130公分", default=0, validators=[NumberRange(min=0)])
    cloth_c_140 = IntegerField("團T：小孩 - 身高140公分", default=0, validators=[NumberRange(min=0)])
    submit = SubmitField("送出訂單")



class CheckForm(FlaskForm):
    submit_btn = SubmitField("確認訂單")
