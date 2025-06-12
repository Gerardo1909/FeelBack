from flask import render_template, request, redirect, url_for, flash
from app.routes import main
from app import db


@main.route('/', methods=['GET', 'POST'])
def login():
    """Ruta de login."""
    return render_template('login.html')