from flask import render_template, redirect, url_for, session, flash, request
from app.auth import login_required
from app import app
from app.forms import LoginForm, IngresoForm
from app.handlers import eliminar_ingreso, get_ingreso_por_id, validar_usuario, get_ingresos, agregar_ingreso
from datetime import datetime

@app.route('/')  # http://localhost:5000/
@app.route('/index')
@login_required
def index():
    if request.method == 'GET' and request.args.get('borrar'):
        eliminar_ingreso(request.args.get('borrar'))
        flash('Se ha eliminado el ingreso', 'success')
    return render_template('index.html', titulo="Inicio", ingresos=get_ingresos())


@app.route('/alta-ingreso', methods=['GET', 'POST'])
@login_required
def alta_ingreso():
    ingreso_form = IngresoForm()
    if ingreso_form.cancelar.data:  # si se apretó el boton cancelar, ingreso_form.cancelar.data será True
        return redirect(url_for('index'))
    if ingreso_form.validate_on_submit():
        datos_nuevos = { 'nombre': ingreso_form.nombre.data, 'apellido': ingreso_form.apellido.data, 
                         'motivo': ingreso_form.motivo.data,'fecha': datetime.strftime(ingreso_form.fecha.data, '%d/%m/%Y'),'dni': ingreso_form.dni.data }
        agregar_ingreso(datos_nuevos)
        flash('Se ha agregado un nuevo ingreso', 'success')
        return redirect(url_for('index'))
    return render_template('alta_ingreso.html', titulo="Ingreso", ingreso_form=ingreso_form)


@app.route('/editar-ingreso/<int:id_ingreso>', methods=['GET', 'POST'])
@login_required
def editar_ingreso(id_ingreso):
    ingreso_form = IngresoForm(data=get_ingreso_por_id(id_ingreso))
    if ingreso_form.cancelar.data:  # si se apretó el boton cancelar, ingreso_form.cancelar.data será True
        return redirect(url_for('index'))
    if ingreso_form.validate_on_submit():
        datos_nuevos = { 'nombre': ingreso_form.nombre.data, 'apellido': ingreso_form.apellido.data, 
                         'motivo': ingreso_form.motivo.data, 'fecha': datetime.strftime(ingreso_form.fecha.data, '%d/%m/%Y'), 'dni': ingreso_form.dni.data }
        eliminar_ingreso(id_ingreso)  # Eliminamos el ingreso antiguo
        agregar_ingreso(datos_nuevos)  # Agregamos el nuevo ingreso
        flash('Se ha editado el ingreso exitosamente', 'success')
        return redirect(url_for('index'))
    return render_template('editar_ingreso.html', titulo="Ingreso", ingreso_form=ingreso_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        usuario = login_form.usuario.data
        password = login_form.password.data
        if validar_usuario(usuario, password):
            session['usuario'] = usuario
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas', 'danger')
    return render_template('login.html', titulo="Login", login_form=login_form)


@app.route('/logout')
@login_required
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404 #código del error para el navegador