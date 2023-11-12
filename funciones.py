from validaciones import *
from CLASES import *
##FUNCIONES.PY
'''Esta funcion la utilizamos en diferentes ocaciones parra crear usuarios de cualquier tipo
'''
def ingresar_persona(): 
    nombre = input("Ingrese un nombre: ")        
    apellido = input("Ingrese un apellido: ")
    dni = es_digito(8,'Dni')            #chequeamos que el dni tenga 8 digitos y que sean digitos
    telefono = es_digito(11,'Telefono')
    mail = contiene('@', 'mail', 1)    # Validar que sea un mail con @ 
    direccion = input("Ingrese una direccion: ")
    nombre_usu = input("Ingrese un nombre de usuario: ")
    contrasenna = pedir_pword()                     #Validar requerimientos para la contrasena  
    if any((nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna))=='SALIR': #si algun dato es salir,no se hace nada con los datos pedidos
        return None
    return nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna
    
    
def ingresar_reserva():  
    ''' 
    Esta funcion la utilizamos para tomar los datos que el cliente quiere para su reservaam
    '''
    cat= dato_en_lista('la categoria', ('SUITE', 'FAMILIAR', 'SIMPLE', 'DOBLE'))
    try:
        capacidad= int(es_digito(1,'Numero de capacidad valido (1-5)'))
    except ValueError:
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
    '''
    Le permite al usuario ver las habitaciones disponibles a la hora de llevar a cabo la reserva.  
    '''
    
    for op in lista_habitaciones:
        print('Habitacion {}: {}, capacidad de {}, {}, {}, Precio por noche: {}'.format(op.nro, op.categoria, op.capacidad, op.banio, op.balcon, op.precio))
    return

def elegir_habitacion(lista_habitaciones, dict_habitaciones):
    '''
    Le permite al usuario seleccionar una habitacion al realizar una reserva. 
    '''
    nro_validos=tuple(map(lambda i: str(i.nro),lista_habitaciones))
    nro=dato_en_lista('el numero de la habitacion deseada', nro_validos)
    if nro=='SALIR':
        return 'SALIR'
    habitacion=dict_habitaciones[nro]
    return habitacion

def generar_factura(pago,lista,usuario,metodopago,hotelPOO):
    '''
    Esta funcion genera una factura (archivo.txt) al finalizar una compra de un cliente en el buffet.
    Lo elegimos sobre el csv ya que al entregarle la factura va a ser mas legible   
    '''
    nombrearchivo=str(hotelPOO.nrofactura)
    f=open(nombrearchivo,'w')
    f.write('Numero de factura: '+nombrearchivo+'\n')
    f.write(usuario.nombre+'\t'+usuario.apellido+'\n')
    f.write(usuario.dni+'\n')
    f.write('Metodo de pago: '+metodopago+'\n')
    for elemento in range(len(lista)):
        f.write('Producto: '+ lista[elemento][0]+'\t'+'Cantidad: '+lista[elemento][1]+'\t'+'Precio unitario: '+hotelPOO.dict_buffet[lista[elemento][0]][0])
    f.write('\n'+"El monto total es: "+str(pago))
    f.close()

    #lista =[(pedido,cant)]
    #dic={"pedido": [precio,stock]}
    
    #pago total
    

    
