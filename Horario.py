#Importacion de librerias de la aplicacion
from fileinput import filename
import re
from flask import Flask
from flask import render_template,request,redirect,url_for
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os 

#Se crea la aplicacion Flask
app = Flask(__name__)

#Configuracion acceso a base de datos Mariadb
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='base'
mysql.init_app(app)

@app.route('/index')
def index():

    sql ="SELECT * FROM `prueba`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    registro=cursor.fetchall()
    print(registro)

    conn.commit()

    return render_template('registros/index.html', registro=registro)



@app.route('/create')
def create():
    return render_template('registros/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _id=request.form['txtid']
    _code=request.form['txtcode']
    _name=request.form['txtname']
    _tutor=request.form['txttutor']    
    _type=request.form['txttype']
    _modality=request.form['txtmodality']
    _area=request.form['txtarea']    
    sql ="INSERT INTO `prueba` (`id`, `code`, `name`, `tutor`, `type`, `modality`, `area`) VALUES (%s,%s,%s,%s,%s,%s,%s);"
    
    datos=(_id,_code,_name,_tutor,_type,_modality,_area)
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/index')


@app.route('/update', methods=['POST'])
def update():
    _code=request.form['txtcode']
    _name=request.form['txtname']
    _tutor=request.form['txttutor']    
    _type=request.form['txttype']
    _modality=request.form['txtmodality']
    _area=request.form['txtarea']  
    id=request.form['txtid']

    sql ="UPDATE prueba SET code=%s, name=%s, tutor=%s, type=%s, modality=%s, area=%s WHERE id=%s ;"
    
    datos=(_code,_name,_tutor,_type,_modality,_area, id)
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/index')


@app.route('/edit/<int:id>')
def edit(id):

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prueba WHERE id = %s", (id))
    registros=cursor.fetchall()
    conn.commit()
    print(registros)

    return render_template('registros/edit.html', registros=registros)


@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prueba WHERE id = %s",(id))
    conn.commit()
    return redirect('/index')


@app.route('/')
def loggin():
    return render_template('Inicio.html')

@app.route('/registro')
def registro():
    return render_template('Registro.html')

@app.route("/error")
def errorConexion():
    return render_template('ErrorConexion.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def Autenticate():

    username = request.form['u']
    password = request.form['p']
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM User WHERE username='" + username + "' and password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
        return render_template('ErrorConexion.html')
    else:
        return render_template('registros/home.html')

@app.route('/autentication', methods=['POST'])
def autentication():
    _usuario=request.form['txtUsuario']
    _contraseña=request.form['txtContraseña']

    sql ="INSERT INTO `User` (`username`, `password`) VALUES (%s,%s);"
    
    datos=(_usuario,_contraseña)
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()