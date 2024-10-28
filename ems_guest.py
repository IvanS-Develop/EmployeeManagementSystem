from tkinter import messagebox
from customtkinter import *
from tkinter import ttk, messagebox
import database

def treeview_data():
    employees = database.fetch_employees()
    tree.delete(*tree.get_children())
    for employee in employees:
        tree.insert('', END, values=employee)

def clear():
    pass  # No se necesita limpiar nada

# Inicialización de la ventana
window = CTk()
window.geometry('930x580+100+100')
window.title('Employee Management System - Guest')

# Configura el grid para el window
window.grid_rowconfigure(1, weight=1)  # Permite que la fila 1 se expanda
window.grid_columnconfigure(1, weight=1)  # Permite que la columna 1 se expanda

################# Generación de Frames Der
rightFrame = CTkFrame(window)
rightFrame.grid(row=1, column=1, sticky='nsew')

# Configura el grid para que se expanda
rightFrame.grid_rowconfigure(0, weight=1)  # Permite que la fila 0 se expanda
rightFrame.grid_columnconfigure(0, weight=1)  # Permite que la columna 0 se expanda

tree = ttk.Treeview(rightFrame)
tree.grid(row=0, column=0, columnspan=4, sticky='nsew')  # Asegúrate de que el sticky esté configurado
################# Generación de Frames Der


tree['columns']=('Id','Name','Phone','Role','Gender','Salary')


tree.heading('Id',text='C.I.')
tree.heading('Name',text='Nombre')
tree.heading('Phone',text='Teléfono')
tree.heading('Role',text='Cargo')
tree.heading('Gender',text='Género')
tree.heading('Salary',text='Salario')

tree.config(show='headings')
tree.column('Id',width=100)
tree.column('Name',width=100)
tree.column('Phone',width=100)
tree.column('Role',width=100)
tree.column('Gender',width=90)
tree.column('Salary',width=90)

style=ttk.Style()
style.configure('Treeview.Heading',font=('arial',18,'bold'))
style.configure('Treeview',font=('arial',9,'normal'))

scrollBar = ttk.Scrollbar(rightFrame, orient=VERTICAL, command=tree.yview)
scrollBar.grid(row=0, column=4, sticky='ns')

tree.config(yscrollcommand=scrollBar.set)

# ...
# Llama a la función para cargar los datos
treeview_data()

window.mainloop()