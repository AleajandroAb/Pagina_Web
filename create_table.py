import sqlite3

conn = sqlite3.connect('database.db')
print("Base de datos conectada")

#SKU es la clave primaria
#Nombre es el producto y se utiliza para generar la clave primaria
#Descripcion es la descripcion del producto
#Precio es el precio del producto
#Stock es la cantidad de producto que queda

conn.execute('CREATE TABLE Productos (sku INT PRIMARY KEY, nombre TEXT, descripcion TEXT, precio INT, stock INT)')
print("Tabla creada correctamente")

conn.close()

