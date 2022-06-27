from flask import Flask, render_template, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
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
        if not request.form['email'] or not request.form['password']:
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
    else:
        return render_template('receta.html')

@app.route('/recetas', methods = ['GET', 'POST'])
def recetas():
    if request.method == 'POST':
        if request.form['nombre'] and request.form['tiempo'] and request.form['elaboracion']:
            nueva_receta = Receta(nombre=request.form['nombre'],tiempo=request.form['tiempo'] ,elaboracion=request.form['elaboracion'],cantidadmegusta = 0,fecha = datetime.now(), usuarioid = __sesionactual.getUsuario().id)
            print(type(nueva_receta))
            db.session.add(nueva_receta)
            db.session.commit()
            receta_actual = Receta.query.filter_by(nombre = request.form['nombre']).first()
            print(receta_actual)

            __sesionactual.addreceta(receta_actual.usuarioid)
            return render_template('receta.html')
        else:
            return render_template('error.html')
    else:
        return render_template('receta.html')

@app.route('/ingredientes' , methods = ['GET', 'POST'])
def ingredientes():
    if request.method == 'POST':
        if request.form['nombre'] and request.form['Cantidad'] and request.form['Unidad']:
            
            nuevo_ingrediente = Ingrediente(nombre=request.form['nombre'],cantidad=request.form['Cantidad'] ,unidad=request.form['Unidad'], recetaid = __sesionactual.getReceta())
            db.session.add(nuevo_ingrediente)
            db.session.commit()
            return render_template('ingredientes.html')
        else:
            return render_template('error.html')
    else:
        return render_template('ingredientes.html')

@app.route('/ranking', methods = ['POST', 'GET'])
def lista_ranking():
    return render_template('rankings.html', receta = Receta.query.order_by(desc(Receta.cantidadmegusta)).all())


@app.route('/listar_tiempo', methods = ['POST', 'GET'])
def listar_tiempo():
    if request.method ==  'POST':
        if request.form['tiempo']:
            return render_template('listar_tiempo.html', tiempo= request.form['tiempo'], receta = Receta.query.filter(Receta.tiempo < int(request.form['tiempo'] )).all())
    else:
        return render_template('listar_tiempo.html')
@app


@app.route('/nuevo_usuario', methods = ['GET','POST'])
def nuevo_usuario():
    if request.method == 'POST':
        if not request.form['nombre'] or not request.form['email'] or not request.form['password']:
            return render_template('error.html')
        else:
            registro = Usuario(nombre = request.form['nombre'], correo = request.form['email'], clave = generate_password_hash(request.form['password']))
            db.session.add(registro)
            db.session.commit()
            return render_template('Iniciar.html')
    return  render_template('nuevo_usuario.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)