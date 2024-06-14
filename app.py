from flask import Flask
from flask import render_template,request,redirect, url_for, flash
from flaskext.mysql import MySQL
from flask import send_from_directory

from datetime import datetime
import os


app= Flask(__name__)
app.secret_key="Develoteca"

#coneccion con la db
mysql= MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema2'#nombre de la db
mysql.init_app(app)


CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

#Mostrar foto en la vista
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)


CARPETA2= os.path.join('Miscelanea')
app.config['CARPETA2']=CARPETA2

#Mostrar foto en la vista
@app.route('/Miscelanea/<nombreFoto>')
def Miscelanea(nombreFoto):
    return send_from_directory(app.config['CARPETA2'],nombreFoto)


#Ruta a index
@app.route('/')
def index():
    return render_template('empleados/index.html')

#Borrar
@app.route('/destroy/<int:id>')
def destroy(id):
    conn= mysql.connect()
    cursor=conn.cursor()

    #seleccion de datos
    cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
    #seleccionar fila
    fila=cursor.fetchall()
    #remover la fotografia
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM empleados WHERE id=%s", (id))
    conn.commit()
    return redirect('/')

#Editar
@app.route('/edit/<int:id>')
def edit(id):

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    empleados=cursor.fetchall()
    conn.commit()
    print(empleados)
    
    return render_template('empleados/edit.html', empleados=empleados)

#Actualizar
@app.route('/update', methods=['POST'])
def update():

    #Se reciben los datos
    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    id=request.form['txtID']

    #Se actualizan los datos
    sql ="UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s;"
    
    datos=(_nombre,_correo,id)
    
    #coneccion con DB
    conn= mysql.connect()
    cursor=conn.cursor()

    #actualizar la foto
    now= datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename!='':
        
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

        cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
        fila=cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s",(nuevoNombreFoto,id))
        conn.commit()


    #Sentencia de actualización
    cursor.execute(sql,datos)

    #Termino
    conn.commit()
    
    return redirect('/')


#Crear
@app.route('/create')
def create():
    return render_template('empleados/create.html')

#Guardar
@app.route('/store', methods=['POST'])
def storage():
    _nombre= request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']

    if _nombre=='' or _correo=='' or _foto=='':
        flash('Recuerda llenar todos los campos')
        return redirect (url_for('create'))

    now= datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    sql ="INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    
    datos=(_nombre,_correo,nuevoNombreFoto)
    
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

# Loggin
@app.route('/prueba')
def prueba():
    sql ="SELECT * FROM `empleados`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    empleados=cursor.fetchall()
    print(empleados)
    
    conn.commit()
    return render_template('empleados/prueba.html', empleados=empleados )


#FAQ
# Datos de las preguntas frecuentes
faqs = [
    {
        "question": "¿Cómo vuelvo al inicio desde mi ubicación?",
        "answer": "Dando click en el boton 'Inicio' el cual está ubicado en la barra de botones de la parte superior."
    },
    {
        "question": "¿Cómo Inicio Sesión?",
        "answer": "Accediendo a la sección de 'Registro de Usuarios' y rellenando los campos solicitados."
    },
    {
        "question": "¿Cómo obtengo mi Constancia?",
        "answer": "Una vez completados y aprobados los 'Retos' se te habilitará la obtencián de tu 'Constancia' en el boton con el mismo nombre."
    },
    {
        "question": "¿Cómo completo los Retos?",
        "answer": "Accediendo a la sección de retos a traves del boton con el mismo nombre. Una vez dentro de la seccion de retos deberás dar click en el boton de 'Iniciar Reto'."
    },
    {
        "question": "¿Darán de alta al pasante?",
        "answer": "Porfavor SI."
    }
]

#FAQ
@app.route('/Secciones/FAQ.html')
def FAQ():
    return render_template('/Secciones/FAQ.html', faqs=faqs)

#Videos
@app.route('/Secciones/Videos.html')
def Videos():
    return render_template('/Secciones/Videos.html')






#Reto1
@app.route('/Retos/RetoPrimero.html')
def RetoPrimero():
    return render_template('Retos/RetoPrimero.html')




    

if __name__== '__main__':
    app.run(debug=True)