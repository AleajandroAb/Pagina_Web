from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)

# Raiz de la ruta
@app.route("/")
def home():
    # Nos conectamos con la base de datos 
    # Y realizamos una consulta SELECT.
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT sku, * FROM Productos")

    rows = cur.fetchall()
    con.close()
    msg=" "
    # Los resultados de la consulta son enviados a home
    return render_template("home.html",rows=rows,msg=msg)

# Ruta para añadir un producto
@app.route("/enternew")
def enternew():
    return render_template("producto.html")

# Ruta para añadir el producto definido
@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
    # Comprobamos que sea un metodo de tipo POST
    if request.method == 'POST':
        try:

            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT sku, * FROM Productos")

            rows = cur.fetchall()
            con.close()

            nom = request.form['nombre']
            sku = (abs(hash(nom))) % (10 ** 8)
            des = request.form['descripcion']
            pre = request.form['precio']
            st = request.form['stock']

            # Nos conectamos con la base de datos para realizar la operacion INSERT
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO productos (sku, nombre, descripcion, precio, stock) VALUES (?,?,?,?,?)",(sku, nom, des, pre, st))

                con.commit()
                msg="Se ha añadido correctamente"
        except:
            con.rollback()
            msg="Ha ocurrido un error en el proceso de eñadir un nuevo elemento"
            return render_template('error.html',msg=msg)

        finally:
            con.close()
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT SKU, * FROM Productos")

            rows = cur.fetchall()
            con.close()
            # Volvemos a la pagina inicial
            return render_template("home.html",rows=rows,msg=msg)

# Ruta para modificar un elemento
@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            # Obtenemos la PK SKU
            id = request.form['id']
            # Nos conectamos a la base de datos y realizamos la consulta
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT sku, * FROM Productos WHERE sku = " + id)

            rows = cur.fetchall()
        except:
            id=None
        finally:
            con.close()
            # Nos envia a la pagina de edicion del producto
            return render_template("edit.html",rows=rows)

# Este metodo actualizara la base de datos
@app.route("/editrec", methods=['POST','GET'])
def editrec():
    # Comprobamos si se corresponde con el tipo de operacion POST
    if request.method == 'POST':
        try:
            # Obtenemos los nuevos datos
            sku = request.form['sku']
            nom = request.form['nombre']
            des = request.form['descripcion']
            pre = request.form['precio']
            st = request.form['stock']

            # Actualizamos la base de datos
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE Productos SET nombre='" + nom + "', descripcion='" + des + "', precio='" + pre + "', stock='" + st + "' WHERE sku=" + sku)

                con.commit()
                msg="Se ha modificado correctamente"
        except:
            con.rollback()
            msg="Ha ocurrido un error en el proceso de edicion de un nuevo elemento"

        finally:
            con.close()
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM Productos")

            rows = cur.fetchall()
            con.close()
            # Volvemos a la pagina inicial
            return render_template("home.html",rows=rows,msg=msg)

# Ruta para eliminar un producto   
@app.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
            # Obtiene el numero de fila del formulario
            sku = request.form['id']
            # Se conecta a la base de datos
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM Productos WHERE sku="+sku)

                con.commit()
                msg="El proceso de eliminacion se ha realizado correctamente"
        except:
            con.rollback()
            msg="Ha ocurrido un error en el proceso de eliminacion"

        finally:
            con.close()
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT sku, * FROM Productos")

            rows = cur.fetchall()
            con.close()
            # Volvemos a la pagina inicial
            return render_template("home.html",rows=rows,msg=msg)