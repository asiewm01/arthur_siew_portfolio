from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_app.models import db, Comment, User
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm

auth_bp = Blueprint('auth', __name__)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists.", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user"] = user.username  # Optional: for display
            flash("Login successful!", "success")
            return redirect(url_for("scratch.scratch"))
        else:
            flash("Invalid credentials.", "danger")
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            flash("A password reset link would be sent here (feature not implemented).", "info")
        else:
            flash("No account found with that email.", "warning")
        return redirect(url_for("auth.login"))

    return render_template("auth/password_reset.html")

@auth_bp.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to view the dashboard.", "danger")
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])
    return render_template("auth/dashboard.html", user=user)

