import sqlite3
from tkinter import CENTER, E, END, W, Button, Entry, Label, LabelFrame, StringVar, Tk, Toplevel, ttk
from tkinter.font import BOLD

from Producto import Producto
from Ticket import Ticket

class HomeUsuario:                  
    def __init__(self, id): 
        self.bd_nombre = 'db/py_final.db'
        self.id_cliente = id 
        self.carrito = []
        self.wind = Tk()
        self.wind.title('SUPERMARK - CLIENTE')
        w, h = 700, 700#self.wind.winfo_screenwidth(), self.wind.winfo_screenheight()                                    
        self.wind.geometry("%dx%d+0+0" % (w, h))
        self.wind.config(bg='#fcfcfc')
        self.wind.resizable(width=0, height=0) 
        
        # Contenedor productos
        """
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
        """
        #Tabla
        self.tree = ttk.Treeview(height = 10, column = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER)
        
        #Botones de carga
        """
        ttk.Button(text = 'Eliminar', command = self.eliminar_productos).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'Editar', command = self.editor_productos).grid(row = 5, column = 1, sticky = W + E)
        """
        ttk.Button(text= 'Agregar al carrito', command= self.agregar_a_carrito).grid(row = 5, columnspan =2, sticky = W + E)
        #llenando filas
        self.traer_productos()

        #testo
        frame = LabelFrame(self.wind, text = 'Carrito')
        frame.grid(row = 3, column = 0, columnspan = 3, pady = 20)
        # tabla carrito
        self.tree2 = ttk.Treeview(column = ("c1", "c2", "c3"), show='headings', height = 10)
        self.tree2.grid(row = 10, column = 0, columnspan = 2)
        self.tree2.heading('c1', text = 'Nombre', anchor = CENTER)
        self.tree2.heading('c2', text = 'Precio', anchor = CENTER)
        self.tree2.heading("c3", text= 'Cantidad', anchor = CENTER)

        ttk.Button(text='Finalizar compra', command=self.ir_ticket).grid(row=20, columnspan =2, sticky = W + E)

    
    def ir_ticket(self):
        self.wind.destroy()
        Ticket(self.carrito, self.id_cliente)

    def agregar_a_carrito(self):
        item = self.tree.focus()
        print(self.tree.item(item))
        if (self.frecuencia(self.tree.item(item)['text']) == 0):
            producto = Producto(self.tree.item(item)['text'], self.tree.item(item)['values'], 1)
            self.carrito.append(producto)
        else:
            indice = self.get_index(self.tree.item(item)['text'])
            self.carrito[indice].cantidad += 1
        self.mostrar_carrito()

    def get_index(self,nombre):
        for indice in range(len(self.carrito)):
            if (self.carrito[indice].nombre == nombre):
                return indice

    def frecuencia(self,nombre):
        contador = 0
        for elemento in self.carrito:
            if (elemento.nombre == nombre):
                contador += 1
        return contador

    def mostrar_carrito(self):
        records = self.tree2.get_children()
        for elemento in records:
            self.tree2.delete(elemento)
        for row in self.carrito:
            self.tree2.insert('', 0 , text = row.nombre, values=(row.nombre, row.precio, row.cantidad))


    def ejecuta_consulta(self, query, parameters = ()):
        with sqlite3.connect(self.bd_nombre) as conn: 
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)    
            conn.commit()
            return result
    
    def traer_productos(self):
        #limpiando tabla
        records = self.tree.get_children()
        print(records)
        for element in records:
            self.tree.delete(element)
        #Consultando datos
        query = 'SELECT * FROM Producto ORDER BY nombre DESC'
        db_filas = self.ejecuta_consulta(query)
        for row in db_filas:
            print(row)
            self.tree.insert('', 0 , text = row[1], value = row[3])
    
    def validacion(self):
        return len(self.name.get()) !=0 and len(self.price.get()) !=0  
    
    def agregar_productos(self):
        if self.validacion():
            #query ='INSERT INTO Producto VALUES (Null, ?, ?)'
            #parameters = (self.name.get(), self.price.get())
            query ='INSERT INTO Producto VALUES (NULL, ?, ?, ?, ?)'
            parameters = (self.name.get(), 10, self.price.get(), 1)
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
        query = 'DELETE FROM Producto WHERE nombre = ?'
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
        query = 'UPDATE Producto SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'
        parameters =(nombre_nuevo, precio_nuevo, name, precio_viejo)
        self.ejecuta_consulta(query, parameters)
        self.edit_wind.destroy()
        self.mensaje['text'] = 'El {} ha sido actualizado correctramente'.format(name)
        self.traer_productos()