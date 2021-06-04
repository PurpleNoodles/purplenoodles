from flask.templating import render_template
from app import app
from app import config

@app.route('/')
def home():
    return config

# redirects
