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
        messagebox.showerror('Error', 'Algo ha ido mal. Por favor, abra la aplicación MySQL antes de volver a ejecutarla.')
        return

    mycursor.execute('CREATE DATABASE IF NOT EXISTS employee_data')
    mycursor.execute('USE employee_data')
    mycursor.execute('CREATE TABLE IF NOT EXISTS data (auto_id INT AUTO_INCREMENT PRIMARY KEY, Id INT(20), Name VARCHAR(50), Phone INT(15), Role VARCHAR(50), Gender VARCHAR(20), Salary DECIMAL(10,2))')

# Inserción de datos en la base de datos con consulta parametrizada
def insert(id, name, phone, role, gender, salary):
    print(id, name, phone, role, gender, salary)
    # Inserta datos usando una consulta parametrizada
    mycursor.execute('INSERT INTO data (Id, Name, Phone, Role, Gender, Salary) VALUES (%s, %s, %s, %s, %s, %s)', (id, name, phone, role, gender, salary))
    conn.commit()

# Verifica si el ID existe en la base de datos
def id_exists(id):
    mycursor.execute('SELECT COUNT(*) FROM data WHERE id=%s', (id,))
    result = mycursor.fetchone()  # Obtiene el resultado de la consulta
    return result[0] > 0

# Obtiene todos los empleados
def fetch_employees():
    mycursor.execute('SELECT Id, Name, Phone, Role, Gender, Salary FROM data')
    result = mycursor.fetchall()
    return result


# Actualiza los datos de un empleado con validación
def update(id, new_name, new_phone, new_role, new_gender, new_salary):
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
        SET name=%s, phone=%s, role=%s, gender=%s, salary=%s 
        WHERE id=%s
    '''
    mycursor.execute(query, (*clean_fields, id))
    conn.commit()

# Elimina un empleado
def delete(id):
    query = 'DELETE FROM data WHERE id=%s'
    mycursor.execute(query, (id,))
    conn.commit()

'''
# Busca empleados en la base de datos
def search(value):
  
    values = (f"%{value}%",) * 6
    mycursor.execute('SELECT * FROM data WHERE id LIKE %s OR name LIKE %s OR phone LIKE %s OR role LIKE %s OR gender LIKE %s OR salary LIKE %s', values)
    result = mycursor.fetchall()
    return result
'''


# Busca empleados en la base de datos
def search(option,value):
    mycursor.execute(f'SELECT * FROM data WHERE {option}=%s', value)
    result = mycursor.fetchall()
    return result


# Verifica si un valor es numérico
def is_numeric(value):
    return value.isdigit()

# Inserción segura de datos en la base de datos
def safe_insert(id, name, phone, role, gender, salary):
    if not (is_numeric(id) and is_numeric(phone)):
        raise ValueError("Error: CI y teléfono deben ser valores numéricos")
    # Inserta datos seguros en la base de datos
    insert(id, name, phone, role, gender, salary)

# Función para validar la entrada usando solo caracteres permitidos
def validar_entrada(entrada):
    patron = r'^[A-Za-z0-9\s,.ñáéíóúÑÁÉÍÓÚ]*$'
    return bool(re.match(patron, entrada))

def delete_A(employee_id):
    try:
        mycursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
        conn.commit()
        return mycursor.rowcount  # Retorna la cantidad de filas afectadas
    except Exception as e:
        conn.rollback()
        raise e

def get_first_record():
    try:
        mycursor.execute("SELECT * FROM employees ORDER BY id ASC LIMIT 1")  # Ajusta el nombre de la tabla y columnas
        return mycursor.fetchone()  # Devuelve el primer registro o None si no hay registros
    except Exception as e:
        raise e

# Conectar a la base de datos al iniciar el programa
connect_database()























