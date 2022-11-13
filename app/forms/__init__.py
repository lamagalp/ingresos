from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired('Este campo es requerido')])
    password = PasswordField('Contraseña', validators=[DataRequired('Este campo es requerido')])
    enviar = SubmitField('Iniciar sesión')


class IngresoForm(FlaskForm):
    fecha = DateField('Fecha', validators=[DataRequired('Este campo es requerido')]);
    apellido = StringField('Apellido', validators=[])
    nombre = StringField('Nombre', validators=[])   
    dni = StringField('DNI', validators=[DataRequired('Este campo es requerido')])
    motivo=StringField('Motivo', validators=[DataRequired('Este campo es requerido')])
    enviar = SubmitField('Guardar', render_kw={'class': 'btn btn-success'})
    cancelar = SubmitField('Cancelar', render_kw={'class': 'btn btn-secondary', 'formnovalidate': 'True'})

