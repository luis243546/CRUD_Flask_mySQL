from flask import Flask, redirect, render_template,request
from bd import obtener_conexion

app=Flask(__name__)

print("hola mundo")




@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/libros')
def libros():
    return render_template('sitio/libros.html')


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
    query="insert into `libros`(`id`, `nombre`, `imagen`, `url`) values (NULL,%s,%s,%s)"
    data=(_nombre, _archivo.filename, _url)
    conexion=obtener_conexion()
    cursor=conexion.cursor()
    cursor.execute(query,data)
    
    conexion.commit()
    print(_nombre)
    print(_url)
    print(_archivo)

    return redirect('/admin/libros')

if __name__ =='__main__':
    app.run(debug=True)