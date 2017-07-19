from flask import render_template
# from flask import session, redirect, url_for
from datetime import datetime

from . import main
# from .forms import NameForm
# from .. import db
# from ..models import User


@main.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username=form.name.data)
#             db.session.add(user)
#             session['known'] = False
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         return redirect(url_for('.index'))
# return render_template("index.html", form=form,
# name=session.get('name'), known=session.get('known', False),
# current_time=datetime.utcnow())
def index():
    return render_template("index.html", current_time=datetime.utcnow())


@main.route('/about/')
def about():
    return render_template("about.html")
