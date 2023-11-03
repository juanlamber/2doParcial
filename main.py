#Importar librerias
import numpy as np
from funciones import *
from validaciones import *
from CLASES import *
import pickle
##MENU

try:
    with open('hotelPOO.pickle','rb') as f:
        hotelPOO=pickle.load(f)
except:
    hotelPOO = Hotel('2', '3')   

print('HOTELPOO' + '\n'*2 + 'Bienvenido')


inicio = None

while inicio != 'SALIR':
    inicio = input('Seleccione "1" si desea iniciar sesion \n "2" si desea crear un usuario \n Escriba salir para finalizar el programa: ')
    inicio=inicio.upper()
    match inicio:
        case '1':
            nombre = input("Ingrese su nombre de usuario: ")    #PEDIMOS EL NOMBRE DE USUARIO
            contrasenna = input("Ingrese su contraseña: ")      #PEDIMOS LA CONTRASEÑA 
            try:
                if hotelPOO.dict_usu[nombre].contrasenna == contrasenna and hotelPOO.dict_usu[nombre].fecha_baja==None:    #VERICAMOS QUE EL USUARIO Y CONTRASEÑA COINCIDAN
                    inicio_sub=None
                    if nombre==hotelPOO.admin:  #MENU DEL ADMINISTRADOR
                        print('Administrador: ')
                        
                        while inicio_sub != 'SALIR':
                            inicio_sub=input('''Ingrese "1" si desea agregar personal administrativo  \n 
                                             "2" si desea agregar personal de limpieza  \n 
                                             "3" si desea agregar personal de mantenimiento \n 
                                             "4" si desea eliminar algun empleado o algun cliente \n
                                             "5" si desea visualizar el inventario del persona''') 
                            match inicio_sub:
                                    case '1':
                                        hotelPOO.crear_usuario('PERSONAL ADMINISTRATIVO')
                                    case '2':
                                        hotelPOO.crear_personal_sin_usuario('PERSONAL LIMPIEZA')
                                    case '3':
                                        hotelPOO.crear_personal_sin_usuario('PERSONAL MANTENIMIENTO')
                                    case '4':
                                        emple=hotelPOO.eliminar_persona()
                                        hotelPOO.identificar_tipo_empleado(emple) if emple is not None else None
                                    case '5':
                                        print('La cantidad de Personales Administrativos es: ', hotelPOO.cant_administrativo)
                                        print('La cantidad de Personales de Limpieza es: ', hotelPOO.cant_limpieza)
                                        print('La cantidad de Personales de Mantenimiento es: ', hotelPOO.cant_mantenimiento)
                    elif isinstance(hotelPOO.dict_usu[nombre], Personal_Administrativo): #MENU DEL PERSONAL ADMINISTRATIVO
                        print('Personal administrativo: ')
                        
                        
                    
                    elif isinstance(hotelPOO.dict_usu[nombre], Cliente): # MENU DE LOS CLIENTES
                        print('Cliente: ')
                    
                else:
                    print("El usuario y la contraseña no coinciden. Vuelve y juega!")
            except KeyError: #SI EL USUARIO NO EXISTE SE MUESTRA POR PANTALLA ESTO 
                print('El usuario ingresado no existe. Porfavor ingrese 2 para crear un usuario o vuelva a intentarlo.')
        
        case '2':         #El administrador crea los usuarios para su personal
            hotelPOO.crear_usuario('CLIENTE')
hotelPOO.save()
