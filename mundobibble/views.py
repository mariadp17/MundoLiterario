from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route('/')
def base():
    return render_template("index.html")