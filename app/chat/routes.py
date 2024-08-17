from flask import render_template
from app.chat import bp

@bp.route('/')
def index():
    return render_template('base.html')