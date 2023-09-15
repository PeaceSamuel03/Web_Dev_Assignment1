from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo

class RegisterForm(FlaskForm):
    user_id = StringField("Enter a user name:", validators=[InputRequired()])
    password = PasswordField("Enter your password:", validators=[InputRequired()])
    password2 = PasswordField("Re-enter your password:", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("User ID:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class ReviewForm(FlaskForm):
    name_of_product = StringField("Name of Product:", validators=[InputRequired()])
    review = StringField("Enter your review:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class SubscriptionForm(FlaskForm):
    email = StringField("Enter your email:", validators=[InputRequired()])
    submit = SubmitField("Submit")


class CheckoutForm(FlaskForm):
    user_id = StringField("Please enter your User ID:", validators=[InputRequired()])
    submit = SubmitField("Submit")


#admin login:[update items, keep track of stock, change description of items, sales??]

#checkout: order confirmation
#home page 
#subscription
#cart
#customer reviews
#remove from cart
