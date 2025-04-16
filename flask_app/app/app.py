# flask_app/app/app.py
from flask import Blueprint, render_template

# Create Blueprint instance
main_bp = Blueprint('main', __name__)

# --- Routes ---
@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/about")
def about():
    return render_template("about_me.html")

@main_bp.route("/resume")
def resume():
    return render_template("resume.html")

@main_bp.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@main_bp.route("/skills")
def skills():
    return render_template("skills.html")

@main_bp.route("/blog")
def blog():
    return render_template("blog.html")

@main_bp.route("/contact")
def contact():
    return render_template("contact_me.html")
