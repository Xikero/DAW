from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email

# Formulario de Registro de Usuarios
class RegistrationForm(FlaskForm):
    # Campo para el nombre de usuario
    username = StringField('Username', validators=[DataRequired()])
    # Campo para el email del usuario con validación de formato de email
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Campo para la contraseña del usuario
    password = PasswordField('Password', validators=[DataRequired()])
    # Campo para confirmar la contraseña del usuario
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # Botón de envío del formulario
    submit = SubmitField('Register')

# Formulario de Inicio de Sesión
class LoginForm(FlaskForm):
    # Campo para el email del usuario
    email = StringField('Email', validators=[DataRequired()])
    # Campo para la contraseña del usuario
    password = PasswordField('Password', validators=[DataRequired()])
    # Casilla de verificación para recordar al usuario
    remember_me = BooleanField('Remember Me')
    # Botón de envío del formulario
    submit = SubmitField('Login')

# Formulario de Registro de Incidentes
class IncidentForm(FlaskForm):
    # Campo desplegable para seleccionar el proyecto
    project = SelectField('Proyecto', choices=[
        ('Madrid_T7', 'Madrid_T7'),
        ('Luxemburgo_T1', 'Luxemburgo_T1'),
        ('Brujas_T1', 'Brujas_T1'),
        ('Estocolmo_T2', 'Estocolmo_T2'),
        ('Paris_T6', 'Paris_T6'),
        ('Lisboa_T4', 'Lisboa_T4'),
        ('Roma_T2', 'Roma_T2'),
        ('Munich_T2', 'Munich_T2'),
        ('London_T2', 'London_T2')
    ], validators=[DataRequired()])
    
    # Campo de área de texto para describir el incidente
    description = TextAreaField('Descripción', validators=[DataRequired()])
    
    # Campo desplegable para seleccionar la posición
    position = SelectField('Posición', choices=[
        ('Estructuras', 'Estructuras'),
        ('Instalaciones', 'Instalaciones'),
        ('Montaje', 'Montaje'),
        ('Pintura', 'Pintura'),
        ('Terminado', 'Terminado'),
        ('Calidad', 'Calidad')
    ], validators=[DataRequired()])
    
    # Campo desplegable para seleccionar el responsable
    responsible = SelectField('Responsable', choices=[
        ('Electrico', 'Electrico'),
        ('Mecanico', 'Mecanico'),
        ('Calidad', 'Calidad'),
        ('Aprovisionamientos', 'Aprovisionamientos'),
        ('IT', 'IT')
    ], validators=[DataRequired()])
    
    # Campo desplegable para seleccionar el estado del incidente
    status = SelectField('Estado', choices=[
        ('Abierto', 'Abierto'),
        ('Cerrado', 'Cerrado')
    ], validators=[DataRequired()])
    
    # Botón de envío del formulario
    submit = SubmitField('Registrar Incidencia')
