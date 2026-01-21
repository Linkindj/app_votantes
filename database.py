from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Votante

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    votantes = Votante.query.all()
    return render_template('dashboard.html', votantes=votantes)

@app.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar():
    if request.method == 'POST':
        votante = Votante(
            nombre=request.form['nombre'],
            cedula=request.form['cedula'],
            edad=request.form['edad'],
            punto_vacunacion=request.form['punto'],
            mesa_vacunacion=request.form['mesa'],
            lider_principal=request.form['lider'],
            usuario_id=1
        )
        db.session.add(votante)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('register_votante.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
