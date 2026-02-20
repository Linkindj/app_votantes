from flask import Flask, flash, render_template, request, redirect, url_for,abort, jsonify
import pandas as pd
import os
from flask_sqlalchemy import SQLAlchemy
from flask import send_file
from io import BytesIO
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Votante, lugarVotacion, Lider

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username']
        ).first()

        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        else: 
            flash ('usuario o contraseña incorrecta')  
            return render_template ('login.html')

    return render_template('login.html')

@app.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        password_hash = generate_password_hash(password)

        nuevo_usuario = User(
            username=username,
            password=password_hash
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Usuario creado correctamente')
        return redirect(url_for('login'))

    return render_template('crear_usuario.html')
from flask_login import current_user

from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

@app.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar():
    puntos = lugarVotacion.query.all()
    lideres = Lider.query.all()
    if request.method == 'POST':

        # Normalizar cédula
        cedula = request.form['cedula'].strip().replace('.', '').replace(' ', '')

        # Verificar duplicado
        existe = Votante.query.filter_by(cedula=cedula).first()
        if existe:
            flash('⚠️ Esta cédula ya está registrada')
            return redirect(url_for('registrar'))

        votante = Votante(
            nombre=request.form['nombre'].strip(),
            cedula=cedula,
            edad=request.form['edad'],
            ocupacion=request.form['ocupacion'],
            telefono=request.form['telefono'],
            punto_id=request.form['punto'],
            mesa_vacunacion=request.form['mesa'],
            lider_referencia=request.form['lider_r'],
            lider_id=request.form['lider'],
            usuario_id=current_user.id
        )
        db.session.add(votante)
        db.session.commit()

        flash('✅ Votante registrado correctamente')
        return redirect(url_for('dashboard'))

    return render_template('register_votantes.html', puntos=puntos, lideres=lideres)

@app.route('/exportar_excel')
@login_required
def exportar_excel():

    votantes = Votante.query.all()

    data = []
    for v in votantes:
        data.append({
            'Nombre': v.nombre,
            'Cédula': v.cedula,
            'Edad': v.edad,
            'Punto de vacunación': v.punto_vacunacion,
            'Mesa': v.mesa_vacunacion,
            'Líder': v.lider_id
        })

    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Votantes')

    output.seek(0)

    return send_file(
        output,
        download_name='votantes.xlsx',
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@app.route('/test')
def test():
    usuarios = User.query.all()
    return f"Usuarios encontrados: {len(usuarios)}"
@app.route('/dashboard')
@login_required
def dashboard():
    lideres = Lider.query.all()
    puntos = lugarVotacion.query.all()
    lider = request.args.get('lider')
    punto = request.args.get('punto')
    cedula = request.args.get('cedula')

    query = Votante.query

    if lider:
        query = query.filter(Votante.lider_id==lider)
    if punto:
        query = query.filter(Votante.punto_id==punto)

    if cedula:
        query = query.filter(Votante.cedula.like(f"%{cedula}%"))

    votantes = query.all()

    return render_template(
        'dashboard.html',
        votantes=votantes,
        lider=lider,
        punto=punto,
        cedula=cedula,
        lideres=lideres,
        puntos=puntos
    )

@app.route('/validar_cedula')
@login_required
def validar_cedula():
    cedula = request.args.get('cedula', '').strip()

    if not cedula:
        return jsonify({'existe': False})

    existe = Votante.query.filter_by(cedula=cedula).first() is not None

    return jsonify({'existe': existe})

@app.route('/buscar_votantes')
@login_required
def buscar_votantes():
    puntos = lugarVotacion.query.all()
    cedula = request.args.get('cedula', '')
    nombre= request.args.get('nombre', '')
    punto = request.args.get('punto', '')

    query = Votante.query

    if cedula:
        query = query.filter(Votante.cedula.like(f"%{cedula}%"))
    if nombre:
        query = query.filter(Votante.nombre.like(f"%{nombre}%"))

    if punto:
        query = query.filter(Votante.punto_id==punto)

    votantes = query.all()

    return render_template(
        'tabla_votantes.html',
        votantes=votantes, puntos=puntos
    )

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_votante(id):
    votante = Votante.query.get_or_404(id)
    puntos = lugarVotacion.query.all()
    lideres = Lider.query.all()
    # 🔐 Seguridad: solo quien lo creó puede editar
    if votante.usuario_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        votante.nombre = request.form['nombre']
        votante.edad = request.form['edad']
        votante.telefono = request.form['telefono']
        votante.ocupacion = request.form['ocupacion']
        votante.punto_id = request.form['punto']
        votante.mesa = request.form['mesa']
        votante.lider_referencia = request.form['lider_r']
        votante.lider_id = request.form['lider']

        db.session.commit()
        flash('Votante actualizado correctamente')
        return redirect(url_for('dashboard'))
    return render_template('editar_votante.html', votante=votante, puntos=puntos, lideres=lideres )

@app.route('/eliminar/<int:id>')
@login_required
def eliminar_votante(id):
    votante = Votante.query.get_or_404(id)

    # 🔐 Seguridad
    if votante.usuario_id != current_user.id:
        abort(403)

    db.session.delete(votante)
    db.session.commit()

    flash('Votante eliminado correctamente')
    return redirect(url_for('dashboard'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

with app.app_context():
    db.create_all()

print("DB URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))