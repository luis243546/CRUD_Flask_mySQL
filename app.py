import os
from flask import Flask, redirect, render_template,request
from bd import obtener_conexion
from datetime import datetime
from flask import send_from_directory

app=Flask(__name__)


@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/sitio/img'),imagen)

@app.route('/libros')
def libros():

    conexion=obtener_conexion()
    cursor=conexion.cursor()
    cursor.execute("select * from `libros`")
    libros=cursor.fetchall()
    conexion.commit()
    print(libros)

    return render_template('sitio/libros.html', libros=libros)


@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')


@app.route('/admin/')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/libros')
def admin_libros():

    conexion=obtener_conexion()
    cursor=conexion.cursor()
    cursor.execute("select * from `libros`")
    libros=cursor.fetchall()
    conexion.commit()
    print(libros)
    return render_template('admin/libros.html',libros=libros)

@app.route('/admin/libros/guardar', methods=['POST'])
def admin_libros_guardar():

    _nombre=request.form['txtNombre']
    _url=request.form['txtURL']
    _archivo=request.files['txtImagen']

    tiempo=datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')

    if _archivo.filename!="":
        nuevoNombre=horaActual+"_"+_archivo.filename
        _archivo.save("templates/sitio/img/"+nuevoNombre)

    query="insert into `libros`(`id`, `nombre`, `imagen`, `url`) values (NULL,%s,%s,%s)"
    data=(_nombre, nuevoNombre, _url)

    conexion=obtener_conexion()
    cursor=conexion.cursor()
    cursor.execute(query,data)
    
    conexion.commit()
    print(_nombre)
    print(_url)
    print(_archivo)

    return redirect('/admin/libros')

@app.route('/public/<path:filename>')
def public_file(filename):
    return app.send_static_file(filename)

@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_borrar():
    
    _id=request.form['txtID']
    print(_id)

    conexion=obtener_conexion()
    cursor=conexion.cursor()
    cursor.execute("SELECT imagen FROM `libros` WHERE id=%s", (_id))
    libro=cursor.fetchall()
    conexion.commit()
    print(libro)

    if os.path.exists("templates/sitio/img/"+str(libro[0][0])):
        os.unlink("templates/sitio/img/"+str(libro[0][0]))

    conexion=obtener_conexion()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id=%s", (_id))
    conexion.commit()

    return redirect('/admin/libros')



if __name__ =='__main__':
    app.run(debug=True)