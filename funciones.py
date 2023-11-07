from validaciones import *
from CLASES import *
##FUNCIONES.PY

def ingresar_persona(): 
    nombre = input("Ingrese un nombre: ")         ##COMO HACEMOS SI EL USUARIO INGRESA 'SALIR' EN CUALQUIERA DE LOS RENGLONES???
    apellido = input("Ingrese un apellido: ")
    dni = es_digito(8,'Dni')
    telefono = es_digito(11,'Telefono')
    mail = contiene('@', 'mail', 1)    # Validar que sea un mail con @ y todas las cosas con mails
    direccion = input("Ingrese una direccion: ")
    nombre_usu = input("Ingrese un nombre de usuario: ")
    contrasenna = pedir_pword()                     #Validar requerimientos   
    if any((nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna))=='SALIR':
        return None
    return nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna
    
    
def ingresar_reserva(): 
    cat= dato_en_lista('la categoria', ('SUITE', 'FAMILIAR', 'SIMPLE', 'DOBLE'))
    try:
        capacidad= int(es_digito(1,'Numero de capacidad valido (1-5)'))
    except:
        capacidad= None
    banio= dato_en_lista('si desea tener baño propio (CON BAÑO) o sin baño propio (SIN BAÑO): ', ('CON BAÑO', 'SIN BAÑO'))
    balcon= dato_en_lista('si desea tener balcon (CON BALCON) o sin balcon (SIN BALCON): ', ('CON BALCON', 'SIN BALCON'))
    print('Ingrese el intervalo de tiempo que se quedara: ')
    print('Fecha de llegada: ')
    fecha_ingreso= ingresar_fecha()
    print('Fecha de salida: ')
    fecha_final=fecha_valida(fecha_ingreso)
    if any((cat, capacidad, banio, balcon,(fecha_ingreso,fecha_final)))=='SALIR':
        return None
    return [cat, capacidad, banio, balcon,(fecha_ingreso,fecha_final)]

def mostrar_habitaciones(lista_habitaciones):
    for op in lista_habitaciones:
        print('Habitacion {}: {}, capacidad de {}, {}, {}, Precio por noche: {}'.format(op.nro, op.categoria, op.capacidad, op.banio, op.balcon, op.precio))
    return

def elegir_habitacion(lista_habitaciones, dict_habitaciones):
    nro_validos=tuple(map(lambda i: str(i.nro),lista_habitaciones))
    nro=dato_en_lista('el numero de la habitacion deseada', nro_validos)
    if nro=='SALIR':
        return 'SALIR'
    habitacion=dict_habitaciones[nro]
    return habitacion


    
