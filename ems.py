from tkinter.messagebox import showerror
from customtkinter import *
from PIL import Image
from tkinter import ttk,messagebox
import database

################
#Functions


def add_employee():
    if not (validate_name(nameEntry.get()) and
            validate_salary(salaryEntry.get()) and
            validate_id(idEntry.get()) and
            validate_phone(phoneEntry.get())):
        messagebox.showerror('Error',
                             'La información proporcionada contiene caracteres prohibidos, sólo se aceptan los siguientes caractes A-Za-z0-9\s,.;ñáéíóúÑÁÉÍÓÚ]*$ y números del 0 al 9')
        return

    if idEntry.get() == '' or phoneEntry.get() == '' or nameEntry.get() == '' or salaryEntry.get() == '':
        messagebox.showerror('Error', 'Por favor, llene la información solicitada en todos los campos')
        return

    elif database.id_exists(idEntry.get()):
        messagebox.showerror('Error', 'La cédula proporcionada ya existe')
    else:
        try:
            # Llama a safe_insert para realizar la validación e inserción segura
            database.safe_insert(idEntry.get(), nameEntry.get(), phoneEntry.get(), roleBox.get(), genderBox.get(),
                                 salaryEntry.get())
            treeview_data()
            clear()
            messagebox.showinfo('Éxito', 'Empleado agregado exitosamente')
        except ValueError as e:
            messagebox.showerror('Error', str(e))
        except Exception as e:
            messagebox.showerror('Error', 'No se pudo agregar el empleado. Error en la base de datos.')

def treeview_data():
   employees=database.fetch_employees()
   tree.delete(*tree.get_children())
   for employee in employees:
       tree.insert('', END,values=employee)

def clear(value=False):
    if value:
        tree.selection_remove(tree.focus())
    idEntry.delete(0,END)
    nameEntry.delete(0,END)
    phoneEntry.delete(0,END)
    roleBox.set('Developer')
    genderBox.set('Hombre')
    salaryEntry.delete(0,END)

# Función que se ejecuta al hacer clic en el Treeview
def selection(event):
    # Verificar si el evento viene del Treeview
    if event.widget == tree:
        selected_item = tree.selection()
        if selected_item:
            row = tree.item(selected_item)['values']
            clear()
            idEntry.insert(0, row[0])
            nameEntry.insert(0, row[1])
            phoneEntry.insert(0, row[2])
            roleBox.set(row[3])
            genderBox.set(row[4])
            salaryEntry.insert(0, row[5])

def update_employee():
    selected_item=tree.selection()
    if not (validate_name(nameEntry.get()) and
            validate_salary(salaryEntry.get()) and
            validate_id(idEntry.get()) and
            validate_phone(phoneEntry.get())):
        messagebox.showerror('Error', 'La información proporcionada contiene caracteres prohibidos, sólo se aceptan los siguientes caractes A-Za-z0-9\s,.;ñáéíóúÑÁÉÍÓÚ]*$ y números del 0 al 9')
        return
    if not selected_item:
        messagebox.showerror('Error','Seleccione el usuario')
    else:
        database.update(idEntry.get(),nameEntry.get(),phoneEntry.get(),roleBox.get(),genderBox.get(),salaryEntry.get())
        treeview_data()
        clear()
        messagebox.showinfo('Aviso','Se actualizó la información')

def delete_employee():
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror('Error','Seleccione el usuario')
    else:
        database.delete(idEntry.get())
        treeview_data()
        clear()
        messagebox.showinfo('Aviso', 'Se eliminó el usuario')

# Variable global para rastrear el estado del botón
#button_pressed = False

def search_employee():
    #global button_pressed

    searched_data = database.search(searchEntry.get())
    tree.delete(*tree.get_children())
    for employee in searched_data:
        tree.insert('', END, values=employee)

        # Resetea el estado del botón si se realiza una búsqueda
        #button_pressed = False




def show_all():
        treeview_data()  # Muestra todos los datos
        searchEntry.delete(0, END)  # Limpia el campo de búsqueda


def validate_name(name):
    return all(char in " áéíóúñÑ" or char.isalpha() for char in name)


def validate_salary(salary):
    return all(char.isdigit() or char in ",." for char in salary)

def validate_id(employee_id):
    return employee_id.isdigit()


def validate_phone(phone):
    return all(char.isdigit() for char in phone)


##############

window=CTk()

################### Banner
#fg_color='#161C30'
window.configure()
# Establece la geometría de la ventana a un tamaño que se ajuste a la pantalla
window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}+0+0")
window.resizable(False,False)
window.title('Employee Management System')


logo = CTkImage (Image.open('Banner3.jpg'), size=(1425,100))  # Ajusta el tamaño de la imagen )
logoLabel=CTkLabel(window,image=logo,text='')
logoLabel.place(x=0, y=0, relwidth=1, relheight=1)
################### Banner



################# Generacion de Frames
logoLabel.grid(row=0,column=0,columnspan=2)
################# Generacion de Frames



################# Generacion de Frames Izq
leftFrame=CTkFrame(window)
leftFrame.grid(row=1,column=0)
################# Generacion de Frames Izq



################## Contenido Frames Izq
idLabel=CTkLabel(leftFrame,text='C.I.',font=('arial', 25, 'bold'), width=300, height=40)
idLabel.grid(row=0,column=0,padx=20,pady=35,sticky='w')

# Campo CI solo números
idEntry = CTkEntry(leftFrame, font=('arial', 25, 'bold'), width=300, height=40)
idEntry.grid(row=0, column=1)
# Campo ID
idEntry.configure(validate="key", validatecommand=(window.register(validate_id), '%S'))


nameLabel=CTkLabel(leftFrame,text='Nombre',font=('arial', 25, 'bold'), width=300, height=40)
nameLabel.grid(row=1,column=0,padx=20,pady=35,sticky='w')


# Campo Name solo letras
nameEntry = CTkEntry(leftFrame,font=('arial', 25, 'bold'), width=300, height=40)
nameEntry.grid(row=1, column=1)
# Campo Name
# Campo Name
nameEntry.configure(validate="key", validatecommand=(window.register(validate_name), '%S'))


phoneLabel=CTkLabel(leftFrame,text='Teléfono',font=('arial', 25, 'bold'), width=300, height=40)
phoneLabel.grid(row=2,column=0,padx=20,pady=35,sticky='w')

# Campo Phone solo números
phoneEntry = CTkEntry(leftFrame, font=('arial', 25, 'bold'), width=300, height=40)
phoneEntry.grid(row=2, column=1, padx=20, pady=35, sticky='w')
# Campo Phone
phoneEntry.configure(validate="key", validatecommand=(window.register(validate_phone), '%S'))
##############

roleLabel=CTkLabel(leftFrame,text='Cargo', font=('arial', 25, 'bold'), width=300, height=40)
roleLabel.grid(row=3,column=0,padx=20,pady=35,sticky='w')

role_options=['Developer','Project Manager','HR Analyst','IT Support','Manager','Graphic Designer','Accountant','Sales Representative','Marketing','Data Scientist','Business Analyst','Web Designer','Software Engineer','System Administrator','Database Administrator','Network Engineer','Quality Assurance Engineer','Technical Support','Sales Manager','Product Manager','UI/UX Designer','Content Writer','Social Media Manager','SEO Specialist','Digital Marketing Specialist','Research Scientist','Operations Manager','Financial Analyst','Customer Service Representative','Security Analyst','Compliance Officer','Supply Chain Manager','Training Coordinator','Facilities Manager']
roleBox=CTkComboBox(leftFrame,values=role_options, font=('arial', 25, 'bold'), width=300, height=40,state='readonly')
roleBox.grid(row=3,column=1)
roleBox.set(role_options[0])


genderLabel=CTkLabel(leftFrame,text='Género',font=('arial', 25, 'bold'), width=300, height=40)
genderLabel.grid(row=4,column=0,padx=20,pady=35,sticky='w')

gender_options=['Hombre','Mujer','Otro']
genderBox=CTkComboBox(leftFrame,values=gender_options,font=('arial', 25, 'bold'), width=300, height=40 ,state='readonly')
genderBox.grid(row=4,column=1)
genderBox.set(gender_options[0])

salaryLabel=CTkLabel(leftFrame,text='Salario', font=('arial', 25, 'bold'), width=300, height=40)
salaryLabel.grid(row=5,column=0,padx=20,pady=35,sticky='w')

salaryEntry = CTkEntry(leftFrame, font=('arial', 25, 'bold'), width=300, height=40)
salaryEntry.grid(row=5, column=1, padx=20, pady=35, sticky='w')
# Campo Salary
salaryEntry.configure(validate="key", validatecommand=(window.register(validate_salary), '%S'))

##############


################## Contenido Frames Izq



################# Generacion de Frames Der
rightFrame=CTkFrame(window)
rightFrame.grid(row=1,column=1)
################# Generacion de Frames Der

##############

#############__________Botones
'''
search_options=['Id','Name','Phone','Gender','Salary']
searchBox=CTkComboBox(rightFrame,values=search_options,state='readonly')
searchBox.grid(row=0,column=0)
searchBox.set('Search By')
'''

searchEntry=CTkEntry(rightFrame, placeholder_text="Buscar por",font=('arial', 25, 'bold'), width=180, height=50)
searchEntry.grid(row=0,column=1,pady=15,sticky='w')

searchButton=CTkButton(rightFrame,text='Buscar',font=('arial', 25, 'bold'), width=180, height=50,command=search_employee)
searchButton.grid(row=0,column=2)

'''
showallButton=CTkButton(rightFrame,text='Show All',width=100,command=show_all)
showallButton.grid(row=0,column=3)
'''

#############__________Botones

tree=ttk.Treeview(rightFrame,height=28)
tree.grid(row=1,column=0,columnspan=4)

tree['columns']=('CI','Name','Phone','Role','Gender','Salary')


tree.heading('CI',text='C.I.')
tree.heading('Name',text='Nombre')
tree.heading('Phone',text='Teléfono')
tree.heading('Role',text='Cargo')
tree.heading('Gender',text='Género')
tree.heading('Salary',text='Salario')

tree.config(show='headings')
tree.column('CI',width=110)
tree.column('Name',width=110)
tree.column('Phone',width=110)
tree.column('Role',width=110)
tree.column('Gender',width=110)
tree.column('Salary',width=110)

style=ttk.Style()
style.configure('Treeview.Heading',font=('arial',18,'bold'))
style.configure('Treeview',font=('arial',9,'normal'))


scrollBar = ttk.Scrollbar(rightFrame, orient=VERTICAL, command=tree.yview)
scrollBar.grid(row=1, column=4, sticky='ns')

tree.config(yscrollcommand=scrollBar.set)
#scrollBar=ttk.Scrollbar(rightFrame,orient=VERTICAL,command=tree.yview)
#scrollBar.grid(row=1,column=4,sticky='ns')

#tree.config(yscrollcommand=scrollbar.set)

#################  Botones bottom

buttonFrame=CTkFrame(window)
buttonFrame.grid(row=2,column=0,columnspan=2,pady=10)
'''
newButton=CTkButton(buttonFrame,text='New Employee',font=('arial',15,'bold'),width=160)
newButton.grid(row=0,column=0,pady=5)

'''
addButton=CTkButton(buttonFrame,text='Agregar empleado',font=('arial', 25, 'bold'), width=180, height=50,command=add_employee)
addButton.grid(row=0,column=1,pady=5,padx=55)


updateButton=CTkButton(buttonFrame,text='Actualizar información',font=('arial', 25, 'bold'), width=180, height=50,command=update_employee)
updateButton.grid(row=0,column=2,pady=5,padx=55)

deleteButton=CTkButton(buttonFrame,text='Eliminar empleado',font=('arial', 25, 'bold'), width=180, height=50,command=delete_employee)
deleteButton.grid(row=0,column=3,pady=5,padx=55)

'''
deleteallButton=CTkButton(buttonFrame,text='Delete All',font=('arial',15,'bold'),width=160)
deleteallButton.grid(row=0,column=4,pady=5,padx=5)
'''


# Vincular la función al Treeview específicamente
tree.bind('<ButtonRelease-1>', selection)

treeview_data()



window.mainloop()