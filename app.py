from flask import Flask, render_template, session, request, redirect,url_for, g
from forms import RegisterForm, LoginForm, ReviewForm, SubscriptionForm, CheckoutForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlite3 import IntegrityError
from database import get_db,close_db
from flask_session import Session
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.config["SESSION_PERMENANT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.teardown_appcontext(close_db)

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwrags):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(**kwrags)
    return wrapped_view

@app.route("/")
def index():
    return render_template("index.html")# homepage

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password.data
        db = get_db()
        possible_clashing_user = db.execute("""SELECT * FROM users
                                                WHERE user_id = ?; """,(user_id,)).fetchone()
        if possible_clashing_user is not None:
            form.user_id.errors.append("User id is already taken!")
        else:
            db.execute("""INSERT INTO users (user_id, password)
                            VALUES (?, ?);""",(user_id, generate_password_hash(password)))
            db.commit()
            return redirect( url_for("login") )
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        matching_user = db.execute("""SELECT * FROM users
                                                WHERE user_id = ?; """,(user_id,)).fetchone()
        if matching_user is None:
            form.user_id.errors.append("User not found(unknown user id)")
        elif not check_password_hash(matching_user["password"], password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect( url_for("index") )

@app.route("/account")
@login_required
def account():
    if "user_id" in session:
        user = session["user_id"]
    return render_template("account.html", user=user)

@app.route("/products")
def products():
    db = get_db()
    jewellery = db.execute("""SELECT * FROM jewellery;""").fetchall()
    return render_template("products.html", jewellery=jewellery)

@app.route("/jewellery/<int:jewellery_id>")
def jewel(jewellery_id):
    db = get_db()
    jewel = db.execute("""SELECT * FROM jewellery
                        WHERE jewellery_id = ?;""", (jewellery_id,)).fetchone()
    return render_template("jewellery.html", jewel=jewel)

@app.route("/cart")
@login_required
def cart():
    jewel = ""
    if "cart" not in session:
        session["cart"] = {}
    names= {}
    prices={}
    db = get_db()
    for jewellery_id in session["cart"]:
        jewel = db.execute("""SELECT * FROM jewellery
                             WHERE jewellery_id = ?;""", (jewellery_id,)).fetchone()
        price = jewel["price"]
        prices[jewellery_id] = price
        name = jewel["name"]
        names[jewellery_id] = name
    return render_template("cart.html", cart=session["cart"], names=names, prices=prices,jewel=jewel)

@app.route("/add_to_cart/<int:jewellery_id>")
@login_required
def add_to_cart(jewellery_id):
    if "cart" not in session:
        session["cart"] = {}
    if jewellery_id not in session["cart"]:
        session["cart"][jewellery_id] = 0
    session["cart"][jewellery_id] = session["cart"][jewellery_id] + 1 
    return redirect( url_for("cart") )

@app.route("/remove_from_cart/<int:jewellery_id>")
def remove_from_cart(jewellery_id):
    if jewellery_id in session["cart"]:
        session["cart"][jewellery_id] = session["cart"][jewellery_id] - 1
    if session["cart"][jewellery_id] == 0:
        session["cart"].pop(jewellery_id)
    return redirect( url_for("cart") )

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        user_id = form.user_id.data 
        if "cart" in session:
            session.pop("cart")
        return render_template("success.html", user_id=user_id)
    return render_template("checkout_form.html",form=form) 


@app.route("/all_reviews")
def all_reviews():
    db = get_db() 
    reviews = db.execute("""SELECT * FROM  reviews;""").fetchall() 
    return render_template("reviews.html" ,reviews=reviews)

@app.route("/insert_review", methods=["GET", "POST"])
@login_required
def insert_review():
    form = ReviewForm()
    if form.validate_on_submit():
        name_of_product = form.name_of_product.data
        review = form.review.data
        db = get_db()
        db.execute("""INSERT INTO reviews (name_of_product, review)
                            VALUES (?, ?)""",(name_of_product, review))
        db.commit() 
        return redirect( url_for("all_reviews") )
    return render_template("insert_review.html", form=form)

@app.route("/subscription", methods=["GET","POST"])
@login_required
def subscription():
    form = SubscriptionForm()
    if form.validate_on_submit():
        email = form.email.data
        db = get_db()
        db.execute("""INSERT INTO emails (email)
                    VALUES (?);""",(email,))
        db.commit()
        return render_template("feedback.html", message="Thank you for subcribing to our online store! You will be able to receive monthly emails to keep you up to date on everything!")
    return render_template("subscription.html", form=form)
