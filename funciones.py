from validaciones import *
##FUNCIONES.PY

def ingresar_persona(): 
    nombre = input("Ingrese un nombre: ")
    nombre_usu = input("Ingrese un nombre de usuario: ")
    apellido = input("Ingrese un apellido: ")
    dni= es_digito(8,'Dni')
    telefono= es_digito(11,'Telefono')
    mail = contiene('@', 'mail', 1)    # Validar que sea un mail con @ y todas las cosas con mails
    direccion = input("Ingrese una direccion: ")
    contrasenna = pedir_pword()                     #Validar requerimientos
    
    ##QUE HACEMOS CON EL SALIR?
     
    return nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna

