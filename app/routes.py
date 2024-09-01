from flask import request, jsonify, Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Incident
from .forms import RegistrationForm, LoginForm, IncidentForm
from datetime import datetime

# Crear un Blueprint para las rutas principales
main = Blueprint('main', __name__)

# Ruta para la página principal
@main.route('/')
@main.route('/index')
@login_required
def index():
    nombre_usuario = current_user.username
    return render_template('index.html', nombre_usuario=nombre_usuario)

# Ruta para el dashboard
@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        delete_id = request.form.get('delete_id')
        if delete_id:
            incident_to_delete = Incident.query.get(delete_id)
            if incident_to_delete:
                db.session.delete(incident_to_delete)
                db.session.commit()
                flash('Incident deleted successfully.', 'success')
            else:
                flash('Incident not found.', 'danger')
        return redirect(url_for('main.dashboard'))

    project_filter = request.args.get('project', '')
    responsible_filter = request.args.get('responsible', '')
    status_filter = request.args.get('status', '')
    
    query = Incident.query
    
    if project_filter:
        query = query.filter_by(project=project_filter)
    if responsible_filter:
        query = query.filter_by(responsible=responsible_filter)
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    incidents = query.all()
    return render_template('dashboard.html', incidents=incidents)

# Ruta para el registro de usuarios
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        
        # Iniciar sesión automáticamente después del registro
        login_user(new_user)
        flash('Account created and logged in successfully.', 'success')
        return redirect(url_for('main.profile'))  # Redirigir al perfil en lugar de la página de inicio
    return render_template('register.html', form=form)

# Ruta para el inicio de sesión
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.profile'))
    return render_template('login.html', title='Sign In', form=form)

# Ruta para el perfil del usuario
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

# Ruta para cerrar sesión
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# Ruta para registrar un incidente
@main.route('/register_incident', methods=['GET', 'POST'])
@login_required
def register_incident():
    if request.method == 'POST':
        project = request.form.get('project')
        description = request.form.get('description')
        position = request.form.get('position')
        responsible = request.form.get('responsible')
        status = request.form.get('status')
        created_by = current_user.username

        new_incident = Incident(
            project=project,
            description=description,
            position=position,
            responsible=responsible,
            status=status,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        db.session.add(new_incident)
        db.session.commit()
        flash('Incident registered successfully.', 'success')
        return redirect(url_for('main.dashboard'))

    form = IncidentForm()
    return render_template('register_incident.html', form=form)

# Ruta para cerrar un incidente
@main.route('/close_incident/<int:incident_id>', methods=['POST'])
@login_required
def close_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if incident:
        incident.status = 'Cerrado'
        db.session.commit()
        flash('Incident closed successfully.', 'success')
    else:
        flash('Incident not found.', 'danger')
    return redirect(url_for('main.dashboard'))

# Ruta para reabrir un incidente
@main.route('/reopen_incident/<int:incident_id>', methods=['POST'])
@login_required
def reopen_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if incident:
        incident.status = 'Abierto'
        db.session.commit()
        flash('Incident reopened successfully.', 'success')
    else:
        flash('Incident not found.', 'danger')
    return redirect(url_for('main.dashboard'))

# Ruta para mostrar los KPIs
@main.route('/kpis')
@login_required
def kpis():
    incidents = Incident.query.all()
    incidents_dict = [incident.to_dict() for incident in incidents]
    return render_template('KPI.html', incidents=incidents_dict)

# Ruta para gestionar usuarios
@main.route('/manage_users')
@login_required
def manage_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)
