import pymysql
from tkinter import messagebox
import re

global mycursor


# Conexión a la base de datos
def connect_database():
    global mycursor
    global conn
    try:
        conn = pymysql.connect(host='localhost', user='root', password='root')
        mycursor = conn.cursor()
    except:
        messagebox.showerror('Error',
                             'Algo ha ido mal. Por favor, abra la aplicación MySQL antes de volver a ejecutarla.')
        return

    mycursor.execute('CREATE DATABASE IF NOT EXISTS employee_data')
    mycursor.execute('USE employee_data')
    mycursor.execute(
        'CREATE TABLE IF NOT EXISTS data (auto_id INT AUTO_INCREMENT PRIMARY KEY, CI INT(20), Nombre VARCHAR(50), Teléfono INT(15), Rol VARCHAR(50), Género VARCHAR(20), Salario DECIMAL(10,2))')


# Inserción de datos en la base de datos con consulta parametrizada
def insert(CI, Nombre, Teléfono, Rol, Género, Salario):
    print(CI, Nombre, Teléfono, Rol, Género, Salario)
    # Inserta datos usando una consulta parametrizada
    mycursor.execute('INSERT INTO data (CI, Nombre, Teléfono, Rol, Género, Salario) VALUES (%s, %s, %s, %s, %s, %s)',
                     (CI, Nombre, Teléfono, Rol, Género, Salario))
    conn.commit()


# Verifica si el ID existe en la base de datos
def id_exists(CI):
    mycursor.execute('SELECT COUNT(*) FROM data WHERE CI=%s', (CI,))
    result = mycursor.fetchone()  # Obtiene el resultado de la consulta
    return result[0] > 0


# Obtiene todos los empleados
def fetch_employees():
    mycursor.execute('SELECT CI, Nombre, Teléfono, Rol, Género, Salario FROM data')
    result = mycursor.fetchall()
    return result


# Actualiza los datos de un empleado con validación
def update(CI, new_name, new_phone, new_role, new_gender, new_salary):
    # Validar cada entrada
    fields = [new_name, new_phone, new_role, new_gender, new_salary]
    clean_fields = []

    for field in fields:
        if not validar_entrada(field):
            raise ValueError("Error: La información introducida contiene caracteres no permitidos")
        clean_fields.append(field)

    # Ejecutar la consulta SQL con los datos validados
    query = '''
        UPDATE data 
        SET Nombre=%s, Teléfono=%s, Rol=%s, Género=%s, Salario=%s 
        WHERE CI=%s
    '''
    mycursor.execute(query, (*clean_fields, CI))
    conn.commit()


# Elimina un empleado
def delete(CI):
    query = 'DELETE FROM data WHERE CI=%s'
    mycursor.execute(query, (CI,))
    conn.commit()


'''
# Busca empleados en la base de datos
def search(value):

    values = (f"%{value}%",) * 6
    mycursor.execute('SELECT * FROM data WHERE id LIKE %s OR Nombre LIKE %s OR phone LIKE %s OR Rol LIKE %s OR Género LIKE %s OR Salario LIKE %s', values)
    result = mycursor.fetchall()
    return result
'''


# Busca empleados en la base de datos
def search(option, value):
    mycursor.execute(f'SELECT * FROM data WHERE {option}=%s', value)
    result = mycursor.fetchall()
    return result


# Verifica si un valor es numérico
def is_numeric(value):
    return value.isdigit()


# Inserción segura de datos en la base de datos
def safe_insert(CI, Nombre, Teléfono, Rol, Género, Salario):
    if not (is_numeric(CI) and is_numeric(Teléfono)):
        raise ValueError("Error: CI y teléfono deben ser valores numéricos")
    # Inserta datos seguros en la base de datos
    insert(CI, Nombre, Teléfono, Rol, Género, Salario)


# Función para validar la entrada usando solo caracteres permitidos
def validar_entrada(entrada):
    patron = r'^[A-Za-z0-9\s,.ñáéíóúÑÁÉÍÓÚ]*$'
    return bool(re.match(patron, entrada))


def delete_A(employee_id):
    try:
        mycursor.execute("DELETE FROM employees WHERE CI = %s", (employee_id,))
        conn.commit()
        return mycursor.rowcount  # Retorna la cantidad de filas afectadas
    except Exception as e:
        conn.rollback()
        raise e


def get_first_record():
    try:
        mycursor.execute("SELECT * FROM employees ORDER BY CI ASC LIMIT 1")  # Ajusta el nombre de la tabla y columnas
        return mycursor.fetchone()  # Devuelve el primer registro o None si no hay registros
    except Exception as e:
        raise e


# Conectar a la base de datos al iniciar el programa
connect_database()























