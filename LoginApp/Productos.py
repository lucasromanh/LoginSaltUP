from tkinter import ttk
from tkinter import *

import sqlite3
import db

class Productos:
    
    bd_nombre ='py_final.db'
    
    def __init__(self, window):
        self.wind = window
        self.wind.title('SUPERMARK - PRODUCTOS')
        
        # Contenedor productos
        frame = LabelFrame(self.wind, text = 'Registra un Producto nuevo')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
    
     # Entrada de nombre
        Label(frame, text = "Nombre de Producto nuevo").grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)
        
        #Precio de Productos
        Label(frame, text = 'Precio de Producto').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)
        
        
        #Boton Agregar productos
        ttk.Button(frame, text= 'Guardar Producto', command = self.agregar_productos).grid(row = 3, columnspan =2, sticky = W + E)
        
        #Mensajes de Salida
        
        self.mensaje = Label(text = '', fg = 'red')
        self.mensaje.grid(row = 3, column = 0, columnspan =2, sticky = W + E)
        
        #Tabla
        self.tree = ttk.Treeview(height = 10, column = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER)
        
        #Botones de carga
        
        ttk.Button(text = 'Eliminar', command = self.eliminar_productos).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'Editar', command = self.editor_productos).grid(row = 5, column = 1, sticky = W + E)
        
        #llenando filas
        self.traer_productos()
    
    def ejecuta_consulta(self, query, parameters = ()):
        with sqlite3.connect(self.bd_nombre) as conn: 
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)    
            conn.commit()
            return result
    
    def traer_productos(self):
        #limpiando tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #Consultando datos
        query = 'SELECT * FROM Producto ORDER BY Nombre DESC'
        db_filas = self.ejecuta_consulta(query)
        for row in db_filas:
            self.tree.insert('', 0 , text = row[1], value = row[2])
    
    def validacion(self):
        return len(self.name.get()) !=0 and len(self.price.get()) !=0  
    
    def agregar_productos(self):
        if self.validacion():
            query ='INSERT INTO Producto VALUES (Null, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.ejecuta_consulta(query, parameters)
            self.mensaje['text'] = 'El Producto {} ha sido agregado de forma satisfactoria'.format (self.name.get())
            self.name.delete(0, END)
            self.price.delet(0, END)
        else:
            self.mensaje['text'] = 'El Nombre y el Precio son requeridos'
            self.traer_productos()
            
    def eliminar_productos(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'] [0] 
        except IndexError as e:
            self.mensaje['text'] = 'Selecciona un elemento o fila'
            return
        name=self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Producto WHERE Nombre = ?'
        self.ejecuta_consulta(query, (name,))
        self.mensaje['text'] = 'El producto {} ha sido eliminado de forma correcta'.format(name)
        self.traer_productos()
    
    def editor_productos(self):
        self.mensaje['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'] [0]
        except IndexError as e:
            self.mensaje['text'] = 'Selecciona un elemento o fila'
            return
        name = self.tree.item(self.tree.selection())['text']    
        precio_viejo = self.tree.item(self.tree.selection())['values'] [0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Producto'
        
        #Viejo Nombre
        Label(self.edit_wind, text = 'Viejo Nombre').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        #Nombre nuevo
        Label(self.edit_wind, text = 'Nuevo Nombre').grid(row = 1, column = 1)
        nombre_nuevo = Entry(self.edit_wind)
        nombre_nuevo.grid(row = 1, column = 2)
        
        #Precio Viejo
        Label(self.edit_wind, text = 'Precio Viejo').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = precio_viejo), state = 'readonly').grid(row = 2, column = 2)
        
        
        #Precio Nuevo
        Label(self.edit_wind, text = 'Precio Nuevo').grid(row = 3, column = 1)
        precio_nuevo = Entry(self.edit_wind)
        precio_nuevo.grid(row = 3, column = 2)
        
        #Boton de actualizar nombre y precios
        Button (self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(nombre_nuevo.get(), name, precio_nuevo.get(), precio_viejo)).grid(row = 4, column =2, sticky = W)
        
    def edit_records(self, nombre_nuevo, name, precio_nuevo, precio_viejo):
        query = 'UPDATE Producto SET Nombre = ?, Precio = ? WHERE Nombre = ? AND Precio = ?'
        parameters =(nombre_nuevo, precio_nuevo, name, precio_viejo)
        self.ejecuta_consulta(query, parameters)
        self.edit_wind.destroy()
        self.mensaje['text'] = 'El {} ha sido actualizado correctramente'.format(name)
        self.traer_productos()
           
    
if __name__ == '__main__':
    windoww = Tk()
    aplicacion = Productos(windoww)
    windoww.mainloop()
    