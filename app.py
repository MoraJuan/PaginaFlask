from flask import Flask, render_template, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from usuario import ClaseUsuario

__sesionactual = ClaseUsuario()

app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import Ingrediente, db
from models import Usuario, Receta

@app.route('/')
def usuario():
    return render_template('Iniciar.html')

@app.route('/bienvenida',methods = ['GET','POST'])
def bienvenida():
    if request.method == 'POST':
            print()

@app.route('/incio_sesion', methods = ['GET','POST'])
def iniciar_sesion():
    if request.method == 'POST':
        if not request.form['nombre'] or not request.form['email'] or not request.form['password']:
            return render_template('error.html')
        else:
            usuario_actual = Usuario.query.filter_by(correo = request.form['email']).first()
            if usuario_actual is None:
                return render_template('error.html')
            else:
                clave_cifrada = hashlib.md5(bytes(request.form['password'], encoding = "utf-8"))
                if clave_cifrada.hexdigest() == usuario_actual.clave:
                    __sesionactual.addusuario(usuario_actual)
                    return render_template('bienvenida.html')
                else:
                    return render_template('error.html')

@app.route('/recetas', methods = ['GET', 'POST'])
def recetas():
    if request.method == 'POST':
        if request.form['cantIngredientes'] and int(request.form['cantIngredientes']) < 10:
            return render_template('receta.html', cantIngredientes = int(request.form['cantIngredientes']))
        if request.form['nombre'] and request.form['tiempo'] and request.form['descripcion']:
            nueva_receta = Receta(nombre=request.form['nombre'],tiempo=request.form['tiempo'] ,descripcion=request.form['descripcion'],cantidadmegusta = 0,fecha = datetime.now(),userioid = __sesionactual.getUsuario().id)

        else:
            return render_template('error.html')
    else:
        return render_template('receta.html', cantIngredientes = 0)

        

@app.route('/nuevo_usuario', methods = ['GET','POST'])
def nuevo_usuario():
    if request.method == 'POST':
        if not request.form['nombre'] or not request.form['email'] or not request.form['password']:
            return render_template('error.html')
        else:
            registro = Usuario(nombre = request.form['nombre'], correo = request.form['email'], clave = generate_password_hash(request.form['password']))
            db.session.add(registro)
            db.session.commit()
            return render_template('iniciar.html')
    return  render_template('nuevo_usuario.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)