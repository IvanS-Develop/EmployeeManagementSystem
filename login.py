from customtkinter import *
from PIL import Image
from customtkinter import CTkImage
from tkinter import messagebox

def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Por favor, complete la información en todos los campos')
    elif usernameEntry.get() == 'admin' and passwordEntry.get() == '1234':
        messagebox.showinfo('Aviso', 'Se inició sesión correctamente')
        root.destroy()
        import ems  # Admin access
    elif usernameEntry.get() == 'guest'and passwordEntry.get() == '1234':  # Guest access
        messagebox.showinfo('Aviso', 'Se inició sesión correctamente')
        root.destroy()
        import ems_guest  # Import a separate module for guest access
    else:
        messagebox.showerror('Error', 'Credenciales Incorrectas')


root = CTk()
# Establece la geometría de la ventana a un tamaño que se ajuste a la pantalla
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
root.title('Login Page')

# Permite el redimensionamiento de la ventana
root.resizable(1, 1)

image = CTkImage(Image.open('login_image2.jpg'), size=(root.winfo_screenwidth(), root.winfo_screenheight()))  # Ajusta el tamaño de la imagen
imageLabel = CTkLabel(root, image=image, text='')
imageLabel.place(x=0, y=0, relwidth=1, relheight=1)  # La imagen ocupatodo el espacio disponible



headingLabel=CTkLabel(root,text='Employee Management System', bg_color='#FFFFFF', font=('Goudy Old Style',65,'bold'),text_color='#28818B')
headingLabel.place(x=10,y=10)

usernameEntry = CTkEntry(root, placeholder_text='Enter your Username', width=300, height=40)  # Ajustar el tamaño
usernameEntry.place(x=100,y=250)

passwordEntry = CTkEntry(root, placeholder_text='Enter your Password', show='*', width=300, height=40)  # Ajustar el tamaño
passwordEntry.place(x=100,y=350)

loginButton = CTkButton(root, text='Login', cursor='hand2', command=login, width=300, height=40)  # Ajustar el tamaño
loginButton.place(x=100,y=450)

root.mainloop()





















