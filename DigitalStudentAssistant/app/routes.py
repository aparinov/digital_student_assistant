from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, AddProjectForm, ContactForm
from flask_login import current_user, login_user
from app.models import User, Project
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from datetime import datetime
from app.forms import EditProfileForm
from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("index.html",title = 'Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, usertype = form.usertype.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    projects = user.projects
    return render_template('user.html', user=user, projects = projects)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.preferences = form.preferences.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.preferences.data = current_user.preferences
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = AddProjectForm()
    if form.validate_on_submit():
        project = Project(title=form.title.data, body=form.body.data, type=form.type.data, view = form.view.data, max_students = form.max_students.data)
        current_user.projects.append(project)
        current_user.accepted = 'yes'
        db.session.add(project)
        db.session.commit()
        flash('Congratulations, you are added a new project!')
        return redirect(url_for('add_project'))
    return render_template('add_project.html', title='Add Project', form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        if form.submit.data:
            pass
        elif form.submit2.data:
            pass
    return render_template('contact.html', form=form)



@app.route('/visual', methods=['GET', 'POST'])
def visual():
    df = pd.read_csv('https://raw.githubusercontent.com/arsruts/SummerPractice/main/final_res_edited.csv', encoding='utf-16', error_bad_lines=False, sep=' ')
    grouped = df.groupby(['Campus']).count()

    labels = grouped.index
    values = grouped['Name'].values

    fig = go.Figure()
    fig.add_trace(go.Pie(values=values, labels=labels, hole=0.5))

    fig.update_layout(
        title = 'Number of Projects by Campuses'
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("visual.html",title = 'Visual', graphJSON = graphJSON)