from tkinter.messagebox import showerror
from customtkinter import *
from tkinter import ttk, messagebox
import database


# Funciones para acciones
def treeview_data():
    employees = database.fetch_employees()
    tree.delete(*tree.get_children())
    for index, employee in enumerate(employees):
        tree.insert('', END, values=employee, iid=index)  # Usamos un índice único para cada fila
        window.update()
        add_action_buttons(index)  # Añadir botones a la fila


def add_action_buttons(row_id):
    # Crear los botones de acción para la fila específica
    edit_button = CTkButton(rightFrame, text="Editar", width=80, height=30,command=lambda: edit_record(row_id))
    delete_button = CTkButton(rightFrame, text="Eliminar", width=80, height=30,command=lambda: delete_record(row_id))
    # Colocarlos en la misma posición que la fila
    tree_row_bbox = tree.bbox(row_id)  # Obtener las coordenadas de la fila
    if tree_row_bbox:
        x, y, width, height = tree_row_bbox
        edit_button.place(x=tree_row_bbox[2] + (-230), y=tree_row_bbox[1])  # Al lado derecho del Treeview
        delete_button.place(x=tree_row_bbox[2] + (-100), y=tree_row_bbox[1])  # Junto al botón de editar



def edit_record(row_id):
    employee = tree.item(row_id)['values']
    messagebox.showinfo("Editar", f"Editar el registro: {employee}")
    # Aquí puedes abrir un formulario o ventana para editar
    lista_window = CTkToplevel()
    lista_window.title('Editar')
    lista_window.geometry("+0+0")
    lista_window.lift()
    lista_window.attributes('-topmost', 1)
    lista_window.resizable(False, False)
    lista_window.title('Editar')

    # Definir la función antes de usarla en el botón
    def update_employee():
        if not (validate_name(nameEntry.get()) and
                validate_salary(salaryEntry.get()) and
                validate_id(idEntry.get()) and
                validate_phone(phoneEntry.get())):
            lista_window.attributes('-topmost', True)  # Asegura que la ventana esté al frente
            lista_window.attributes('-topmost', False)  # Restablece la configuración
            messagebox.showerror('Error','La información proporcionada contiene caracteres prohibidos.',parent = lista_window)
            return
        if idEntry.get() == '':
            lista_window.attributes('-topmost', True)  # Asegura que la ventana esté al frente
            lista_window.attributes('-topmost', False)  # Restablece la configuración
            messagebox.showerror('Error', 'Seleccione el usuario',parent = lista_window)
        else:
            database.update(idEntry.get(), nameEntry.get(), phoneEntry.get(), roleBox.get(), genderBox.get(),
                            salaryEntry.get())
            lista_window.attributes('-topmost', True)  # Asegura que la ventana esté al frente
            lista_window.attributes('-topmost', False)  # Restablece la configuración
            messagebox.showinfo('Aviso', 'Se actualizó la información', parent=window)
            treeview_data()



    ################# Generacion de Frames Izq
    leftFrame = CTkFrame(lista_window)
    leftFrame.grid(row=1, column=0)
    ################# Generacion de Frames Izq
    ################## Contenido Frames Izq
    idLabel = CTkLabel(leftFrame, text='C.I.', font=('arial', 25, 'bold'), width=300, height=40)
    idLabel.grid(row=0, column=0, padx=20, pady=35, sticky='w')
    # Campo CI solo números
    idEntry = CTkEntry(leftFrame, font=('arial', 25, 'bold'), width=300, height=40)
    idEntry.grid(row=0, column=1)
    # Campo ID
    idEntry.configure(validate="key", validatecommand=(window.register(validate_id), '%S'))
    nameLabel = CTkLabel(leftFrame, text='Nombre', font=('arial', 25, 'bold'), width=300, height=40)
    nameLabel.grid(row=1, column=0, padx=20, pady=35, sticky='w')
    # Campo Name solo letras
    nameEntry = CTkEntry(leftFrame, font=('arial', 25, 'bold'), width=300, height=40)
    nameEntry.grid(row=1, column=1)
    # Campo Name
    # Campo Name
    nameEntry.configure(validate="key", validatecommand=(window.register(validate_name), '%S'))
    phoneLabel = CTkLabel(leftFrame, text='Teléfono', font=('arial', 25, 'bold'), width=300, height=40)
    phoneLabel.grid(row=2, column=0, padx=20, pady=35, sticky='w')
    # Campo Phone solo números
    phoneEntry = CTkEntry(leftFrame, font=('arial', 25, 'bold'), width=300, height=40)
    phoneEntry.grid(row=2, column=1, padx=20, pady=35, sticky='w')
    # Campo Phone
    phoneEntry.configure(validate="key", validatecommand=(window.register(validate_phone), '%S'))
    ##############
    roleLabel = CTkLabel(leftFrame, text='Cargo', font=('arial', 25, 'bold'), width=300, height=40)
    roleLabel.grid(row=3, column=0, padx=20, pady=35, sticky='w')
    role_options = ['Developer', 'Project Manager', 'HR Analyst', 'IT Support', 'Manager', 'Graphic Designer',
                    'Accountant', 'Sales Representative', 'Marketing', 'Data Scientist', 'Business Analyst',
                    'Web Designer', 'Software Engineer', 'System Administrator', 'Database Administrator',
                    'Network Engineer', 'Quality Assurance Engineer', 'Technical Support', 'Sales Manager',
                    'Product Manager', 'UI/UX Designer', 'Content Writer', 'Social Media Manager', 'SEO Specialist',
                    'Digital Marketing Specialist', 'Research Scientist', 'Operations Manager', 'Financial Analyst',
                    'Customer Service Representative', 'Security Analyst', 'Compliance Officer', 'Supply Chain Manager',
                    'Training Coordinator', 'Facilities Manager']
    roleBox = CTkComboBox(leftFrame, values=role_options, font=('arial', 25, 'bold'), width=300, height=40,state='readonly')
    roleBox.grid(row=3, column=1)
    roleBox.set(role_options[0])
    genderLabel = CTkLabel(leftFrame, text='Género', font=('arial', 25, 'bold'), width=300, height=40)
    genderLabel.grid(row=4, column=0, padx=20, pady=35, sticky='w')
    gender_options = ['Hombre', 'Mujer', 'Otro']
    genderBox = CTkComboBox(leftFrame, values=gender_options, font=('arial', 25, 'bold'), width=300, height=40,state='readonly')
    genderBox.grid(row=4, column=1)
    genderBox.set(gender_options[0])
    salaryLabel = CTkLabel(leftFrame, text='Salario', font=('arial', 25, 'bold'), width=300, height=40)
    salaryLabel.grid(row=5, column=0, padx=20, pady=35, sticky='w')
    salaryEntry = CTkEntry(leftFrame, font=('arial', 25, 'bold'), width=300, height=40)
    salaryEntry.grid(row=5, column=1, padx=20, pady=35, sticky='w')
    # Campo Salary
    salaryEntry.configure(validate="key", validatecommand=(window.register(validate_salary), '%S'))
    buttonFrame = CTkFrame(lista_window)
    buttonFrame.grid(row=2, column=0, columnspan=2, pady=10)
    updateButton = CTkButton(buttonFrame, text='Actualizar información', font=('arial', 25, 'bold'), width=180,height=50,command=update_employee)
    updateButton.grid(row=0, column=2, pady=5, padx=55)
    # Insertar valores en los campos
    idEntry.insert(0, employee[0])
    nameEntry.insert(0, employee[1])
    phoneEntry.insert(0, employee[2])
    roleBox.set(employee[3])
    genderBox.set(employee[4])
    salaryEntry.insert(0, employee[5])

def add_employee():
    # Aquí puedes abrir un formulario o ventana para editar
    lista_window = CTkToplevel()
    lista_window.title('Nuevo Registro')
    lista_window.geometry("+0+0")
    lista_window.lift()
    lista_window.attributes('-topmost', 1)
    lista_window.resizable(False, False)
    lista_window.title('Nuevo Registro')

    # Definir la función antes de usarla en el botón
    def add():
        if not (validate_name(nameEntry.get()) and
                validate_salary(salaryEntry.get()) and
                validate_id(idEntry.get()) and
                validate_phone(phoneEntry.get())):
            lista_window.attributes('-topmost', True)  # Asegura que la ventana esté al frente
            lista_window.attributes('-topmost', False)  # Restablece la configuración
            messagebox.showerror('Error','La información proporcionada contiene caracteres prohibidos, sólo se aceptan los siguientes caractes A-Za-z0-9\s,.;ñáéíóúÑÁÉÍÓÚ]*$ y números del 0 al 9',parent=lista_window)
            return

        if idEntry.get() == '' or phoneEntry.get() == '' or nameEntry.get() == '' or salaryEntry.get() == '':
            lista_window.attributes('-topmost', True)  # Asegura que la ventana esté al frente
            lista_window.attributes('-topmost', False)  # Restablece la configuración
            messagebox.showerror('Error', 'Por favor, llene la información solicitada en todos los campos',parent = lista_window)
            return

        elif database.id_exists(idEntry.get()):
            lista_window.attributes('-topmost', True)  # Asegura que la ventana esté al frente
            lista_window.attributes('-topmost', False)  # Restablece la configuración
            messagebox.showerror('Error', 'La cédula proporcionada ya existe',parent = lista_window)
        else:
            try:
                # Llama a safe_insert para realizar la validación e inserción segura
                database.safe_insert(idEntry.get(), nameEntry.get(), phoneEntry.get(), roleBox.get(), genderBox.get(),
                                     salaryEntry.get())
                treeview_data()
                lista_window.attributes('-topmost', True)  # Asegura que la ventana esté al frente
                lista_window.attributes('-topmost', False)  # Restablece la configuración
                # Insertar valores en los campos
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                phoneEntry.delete(0, END)
                roleBox.set('Developer')
                genderBox.set('Hombre')
                salaryEntry.delete(0, END)
                messagebox.showinfo('Éxito', 'Empleado agregado exitosamente',parent=lista_window)
            except ValueError as e:
                lista_window.attributes('-topmost', True)  # Asegura que la ventana esté al frente
                lista_window.attributes('-topmost', False)  # Restablece la configuración
                messagebox.showerror('Error', str(e),parent = lista_window)
            except Exception as e:
                lista_window.attributes('-topmost', True)  # Asegura que la ventana esté al frente
                lista_window.attributes('-topmost', False)  # Restablece la configuración
                messagebox.showerror('Error', 'No se pudo agregar el empleado. Error en la base de datos.',parent = lista_window)
            treeview_data()
    ################# Generacion de Frames Izq
    leftFrame = CTkFrame(lista_window)
    leftFrame.grid(row=1, column=0)
    ################# Generacion de Frames Izq
    ################## Contenido Frames Izq
    idLabel = CTkLabel(leftFrame, text='C.I.', font=('arial', 25, 'bold'), width=300, height=40)
    idLabel.grid(row=0, column=0, padx=20, pady=35, sticky='w')
    # Campo CI solo números
    idEntry = CTkEntry(leftFrame, font=('arial', 25, 'bold'), width=300, height=40)
    idEntry.grid(row=0, column=1)
    # Campo ID
    idEntry.configure(validate="key", validatecommand=(window.register(validate_id), '%S'))
    nameLabel = CTkLabel(leftFrame, text='Nombre', font=('arial', 25, 'bold'), width=300, height=40)
    nameLabel.grid(row=1, column=0, padx=20, pady=35, sticky='w')
    # Campo Name solo letras
    nameEntry = CTkEntry(leftFrame, font=('arial', 25, 'bold'), width=300, height=40)
    nameEntry.grid(row=1, column=1)
    # Campo Name
    # Campo Name
    nameEntry.configure(validate="key", validatecommand=(window.register(validate_name), '%S'))
    phoneLabel = CTkLabel(leftFrame, text='Teléfono', font=('arial', 25, 'bold'), width=300, height=40)
    phoneLabel.grid(row=2, column=0, padx=20, pady=35, sticky='w')
    # Campo Phone solo números
    phoneEntry = CTkEntry(leftFrame, font=('arial', 25, 'bold'), width=300, height=40)
    phoneEntry.grid(row=2, column=1, padx=20, pady=35, sticky='w')
    # Campo Phone
    phoneEntry.configure(validate="key", validatecommand=(window.register(validate_phone), '%S'))
    ##############
    roleLabel = CTkLabel(leftFrame, text='Cargo', font=('arial', 25, 'bold'), width=300, height=40)
    roleLabel.grid(row=3, column=0, padx=20, pady=35, sticky='w')
    role_options = ['Developer', 'Project Manager', 'HR Analyst', 'IT Support', 'Manager', 'Graphic Designer',
                    'Accountant', 'Sales Representative', 'Marketing', 'Data Scientist', 'Business Analyst',
                    'Web Designer', 'Software Engineer', 'System Administrator', 'Database Administrator',
                    'Network Engineer', 'Quality Assurance Engineer', 'Technical Support', 'Sales Manager',
                    'Product Manager', 'UI/UX Designer', 'Content Writer', 'Social Media Manager', 'SEO Specialist',
                    'Digital Marketing Specialist', 'Research Scientist', 'Operations Manager', 'Financial Analyst',
                    'Customer Service Representative', 'Security Analyst', 'Compliance Officer', 'Supply Chain Manager',
                    'Training Coordinator', 'Facilities Manager']
    roleBox = CTkComboBox(leftFrame, values=role_options, font=('arial', 25, 'bold'), width=300, height=40,state='readonly')
    roleBox.grid(row=3, column=1)
    roleBox.set(role_options[0])
    genderLabel = CTkLabel(leftFrame, text='Género', font=('arial', 25, 'bold'), width=300, height=40)
    genderLabel.grid(row=4, column=0, padx=20, pady=35, sticky='w')
    gender_options = ['Hombre', 'Mujer', 'Otro']
    genderBox = CTkComboBox(leftFrame, values=gender_options, font=('arial', 25, 'bold'), width=300, height=40,state='readonly')
    genderBox.grid(row=4, column=1)
    genderBox.set(gender_options[0])
    salaryLabel = CTkLabel(leftFrame, text='Salario', font=('arial', 25, 'bold'), width=300, height=40)
    salaryLabel.grid(row=5, column=0, padx=20, pady=35, sticky='w')
    salaryEntry = CTkEntry(leftFrame, font=('arial', 25, 'bold'), width=300, height=40)
    salaryEntry.grid(row=5, column=1, padx=20, pady=35, sticky='w')
    # Campo Salary
    salaryEntry.configure(validate="key", validatecommand=(window.register(validate_salary), '%S'))
    buttonFrame = CTkFrame(lista_window)
    buttonFrame.grid(row=2, column=0, columnspan=2, pady=10)
    updateButton = CTkButton(buttonFrame, text='Agregar información', font=('arial', 25, 'bold'), width=180,height=50,command=add)
    updateButton.grid(row=0, column=2, pady=5, padx=55)
    # Insertar valores en los campos
    idEntry.delete(0,END)
    nameEntry.delete(0,END)
    phoneEntry.delete(0,END)
    roleBox.set('Developer')
    genderBox.set('Hombre')
    salaryEntry.delete(0,END)


def delete_record(row_id):
    employee = tree.item(row_id)['values']
    confirm = messagebox.askyesno("Eliminar", f"¿Desea eliminar el registro con C.I. {employee[0]}?")
    if confirm:
        # Elimina el registro de la base de datos
        database.delete(employee[0])
        treeview_data()




def validate_name(name):
    return all(char in " áéíóúñÑ" or char.isalpha() for char in name)


def validate_salary(salary):
    return all(char.isdigit() or char in ",." for char in salary)

def validate_id(employee_id):
    return employee_id.isdigit()


def validate_phone(phone):
    return all(char.isdigit() for char in phone)



def search_employee():
    searched_data = database.search(searchEntry.get())
    tree.delete(*tree.get_children())
    for employee in searched_data:
        tree.insert('', END, values=employee)

'''
    if searchEntry.get()=='':
        messagebox.showerror('Error','Ingresa un valor para buscar')
    elif searchBox.get()=='Bucar por':
        messagebox.showerror('Error','Por favor, selecciona una opción')
    else:
        searched_data=database.search(searchBox.get(),searchEntry.get())
        window.update()
        tree.delete(*tree.get_children())
        window.update()
        for employee in searched_data:
            tree.insert('', END, values=employee)
            window.update()
'''


'''
    #global button_pressed
    searched_data = database.search(searchEntry.get())
    tree.delete(*tree.get_children())
    for employee in searched_data:
        tree.insert('', END, values=employee)
'''

# Configuración de la ventana principal
window = CTk()
window.geometry("0+0")
window.resizable(False, False)
window.title("Employee Management System")
# Generación de Frames
rightFrame = CTkFrame(window)
rightFrame.grid(row=1, column=0)
# Entrada de búsqueda

search_options=['Id','Name','Phone','Gender','Salary']
searchBox=CTkComboBox(rightFrame,values=search_options,state='readonly')
searchBox.grid(row=3,column=0)
searchBox.set('Buscar por')

searchEntry = CTkEntry(rightFrame, placeholder_text="Buscar por", font=('arial', 25, 'bold'), width=180, height=50)
searchEntry.grid(row=3, column=1, pady=15, sticky='w')

searchButton = CTkButton(rightFrame, text='Buscar', font=('arial', 25, 'bold'), width=180, height=50,command=search_employee)
#searchButton = CTkButton(rightFrame, text='Buscar', font=('arial', 25, 'bold'), width=180, height=50, command=treeview_data)
searchButton.grid(row=3, column=2)

addButton = CTkButton(rightFrame, text='Nuevo', font=('arial', 25, 'bold'), width=180, height=50,command=add_employee)
#searchButton = CTkButton(rightFrame, text='Buscar', font=('arial', 25, 'bold'), width=180, height=50, command=treeview_data)
addButton.grid(row=3, column=3)



# Configuración del Treeview

tree = ttk.Treeview(rightFrame, height=28)
tree.grid(row=1, column=0, columnspan=4)
tree['columns'] = ('CI', 'Name', 'Phone', 'Role', 'Gender', 'Salary','Edit','Remove')
tree.heading('CI', text='C.I.')
tree.heading('Name', text='Nombre')
tree.heading('Phone', text='Teléfono')
tree.heading('Role', text='Cargo')
tree.heading('Gender', text='Género')
tree.heading('Salary', text='Salario')
tree.heading('Edit', text='')
tree.heading('Remove', text='')

tree.config(show='headings')
tree.column('CI', width=130)
tree.column('Name', width=130)
tree.column('Phone', width=130)
tree.column('Role', width=130)
tree.column('Gender', width=130)
tree.column('Salary', width=130)
tree.column('Edit', width=130)
tree.column('Remove', width=130)

# Estilo
style = ttk.Style()
style.configure('Treeview.Heading', font=('arial', 18, 'bold'))
style.configure('Treeview', font=('arial', 9, 'normal'))

# Scrollbar
scrollBar = ttk.Scrollbar(rightFrame, orient=VERTICAL, command=tree.yview)
scrollBar.grid(row=1, column=4, sticky='ns')
tree.config(yscrollcommand=scrollBar.set)

# Cargar datos iniciales
treeview_data()
window.update()
window.mainloop()