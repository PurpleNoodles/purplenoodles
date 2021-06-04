from flask.templating import render_template
from app import app
from app import config
from flask import render_template, redirect, url_for, request

@app.route('/')
def home():
    return config

# redirects
