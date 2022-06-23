'''@app.route('/recetas', methods = ['GET', 'POST'])
def recetas():
    if request.method == 'POST':
        if not request.form['nombre'] or not request.form['tiempo'] or not request.form['elaboracion']:
            return render_template('error.html')
        if request.form['cantIngredientes'] and int(request.form['cantIngredientes']) < 10:
            return render_template('receta.html', cantidadIngredientes = range(int(request.form['cantIngredientes'])))
        if request.form['nombre'] or not request.form['tiempo'] or not request.form['elaboracion']:
            nueva_receta = Receta(nombre = request.form['nombre'],tiempo = request.form['tiempo'], elaboracion = request.form['elaboracion'], cantidadmegusta = 0, fecha = datetime.now(), usuarioid = __sesionactual.getUsuario().id)
            db.session.add(nueva_receta)
            db.session.commit()
            return render_template('receta.html')
    return render_template('receta.html')
    '''