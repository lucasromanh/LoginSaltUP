from re import S
import sqlite3
import string
from tkinter import CENTER, E, N, W, Label, LabelFrame, Tk, ttk

from HomeUsuario import *

#from HomeUsuario import HomeUsuario


class Ticket:
    def __init__(self, carrito, id):
        self.carrito = carrito
        self.id_cliente = id
        self.bd_nombre = 'db/py_final.db' 
        self.wind = Tk()
        self.wind.title('SUPERMARK - Ticket')
        w, h = 900, 700#self.wind.winfo_screenwidth(), self.wind.winfo_screenheight()                                    
        self.wind.geometry("%dx%d+0+0" % (w, h))
        self.wind.config(bg='#fcfcfc')
        self.wind.resizable(width=0, height=0) 


        self.tree3 = ttk.Treeview(column = ("c1", "c2", "c3", "c4"), show='headings', height = 10)
        self.tree3.grid(row = 10, column = 0, columnspan = 2)
        self.tree3.heading('c1', text = 'Nombre', anchor = CENTER)
        self.tree3.heading('c2', text = 'Precio', anchor = CENTER)
        self.tree3.heading("c3", text= 'Cantidad', anchor = CENTER)
        self.tree3.heading("c4", text= 'Total', anchor = CENTER)
        
        self.cargar_tabla()

        frame = Label(self.wind, text = 'TOTAL FINAL: ')
        frame.grid(row = 50, column = 0, columnspan = 3, pady = 20)
        frame = Label(self.wind, text = f'{self.calcular_total()}')
        frame.grid(row = 50, column = 1, columnspan = 3, pady = 20)

        ttk.Button(text= 'Finalizar', command=self.finalizar_carrito).grid(row = 60, columnspan =2, sticky = W + E)


    def finalizar_carrito(self):
        self.guardar_carrito()
        self.wind.destroy()
        HomeUsuario(self.id_cliente)

    def guardar_carrito(self):
        with sqlite3.connect(self.bd_nombre) as conn: 
            cursor = conn.cursor()
            for elemento in self.carrito:
                query = 'INSERT INTO Detalle (id, producto, cantidad, id_cliente) values (NULL, ?,?,?)'
                parameters = (elemento.nombre, elemento.cantidad, self.id_cliente)
                result = cursor.execute(query, parameters)    
                conn.commit()
            return result
            
    def calcular_total(self):
        total = 0
        for elemento in self.carrito:
            total += (elemento.cantidad * float(elemento.precio[0]))

        return total
    def cargar_tabla(self):
        for row in self.carrito:
            total = float(row.precio[0]) * row.cantidad
            self.tree3.insert('', 0 , text = row.nombre, values=(row.nombre, row.precio, row.cantidad, total))