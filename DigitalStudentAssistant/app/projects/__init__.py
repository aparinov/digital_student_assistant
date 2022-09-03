from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import current_user, login_required

from app import db
from app.models import Project, User

projects = Blueprint('projects', __name__, template_folder='templates')

@projects.route('/')
@login_required
def index():
    projects = Project.query.all()

    return render_template('projects/index.html', projects = projects)

@projects.route('/<string:title>', methods=['GET', 'POST'])
@login_required
def project_detail(title):
    project = Project.query.filter(Project.title == title).first()
    users =  project.users
    if request.method == 'POST':
        if request.form.get('Apply') == 'Apply':
            if current_user.usertype == 'Student' and current_user not in project.users and project.current_number_of_students < project.max_students:
                current_user.projects.append(project)
                project.current_number_of_students += 1
                db.session.commit()
                flash('Successfully applied for a project')
                return redirect(url_for('projects.project_detail', title=project.title))
            elif current_user.usertype == 'Teacher':
                flash('Teachers can not apply for a project')
                return redirect(url_for('projects.project_detail', title=project.title))
            elif current_user in project.users:
                flash('Your are already applied for this project')
                return redirect(url_for('projects.project_detail', title=project.title))
            elif project.current_number_of_students == project.max_students:
                flash('Project team is fulfilled')
                return redirect(url_for('projects.project_detail', title=project.title))
        elif request.form.get('Remove') == 'Remove':
            if current_user.usertype == 'Student':
                if current_user in project.users:
                    project.users.remove(current_user)
                    project.current_number_of_students = project.current_number_of_students - 1
                    db.session.commit()
                    flash('Successfully removed from a project')
            elif current_user not in project.users:
                flash('You are not applied for a project yet')
    return render_template('projects/project_detail.html', project = project, users = users)




