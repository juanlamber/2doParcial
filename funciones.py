from validaciones import *
from CLASES import Personal_Limpieza, Personal_Administrativo, Personal_Mantenimiento
##FUNCIONES.PY

def ingresar_persona(tipo): 
    # nombre = input("Ingrese un nombre: ")
    # apellido = input("Ingrese un apellido: ")
    # dni = es_digito(8,'Dni')
    # telefono = es_digito(11,'Telefono')
    # mail = contiene('@', 'mail', 1)    # Validar que sea un mail con @ y todas las cosas con mails
    # direccion = input("Ingrese una direccion: ")
    # if tipo=='1':
    #     nombre_usu = input("Ingrese un nombre de usuario: ")
    #     contrasenna = pedir_pword()                     #Validar requerimientos
    #     return nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna
    nombre= 'Juan'
    apellido = 'Gomez'
    dni= '12345678'
    telefono = '12345678910'
    mail = 'hola@com'
    direccion= 'bvjhbaksc'
    if tipo=='1':
        nombre_usu = 'jcasjc'
        contrasenna = 'AA1234578'                    
        return nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna
    return nombre, apellido, dni, telefono, mail, direccion

