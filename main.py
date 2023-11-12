#Importar librerias
import numpy as np
from funciones import *
from validaciones import *
from CLASES import *
from menu import *
import pickle
from collections import deque

##MENU

try:
    with open('hotelPOO.pickle','rb') as f:
        hotelPOO=pickle.load(f)
        AlmacenPOO=hotelPOO.almacen
except:
    hotelPOO = Hotel('11', '15')
    hotelPOO.almacen=Almacen()
    hotelPOO.dict_habitacion= {'100':Habitacion(100,'SIMPLE',2,'CON BAÑO','CON BALCON',100), 
                            '101':Habitacion(101,'SIMPLE',2, 'SIN BAÑO', 'SIN BALCON', 50), 
                           '200':Habitacion(200,'DOBLE',4,'CON BAÑO','CON BALCON',200),
                           '201':Habitacion(201,'DOBLE',4,'SIN BAÑO','SIN BALCON',150),
                           '300':Habitacion(300,'FAMILIAR',5,'SIN BAÑO','CON BALCON',150),
                           '301':Habitacion(301,'FAMILIAR',5,'CON BAÑO', 'SIN BALCON',200),
                           '400':Habitacion(400, 'SUITE', 2, 'CON BAÑO', 'CON BALCON', 500),
                           '401':Habitacion(401, 'SUITE', 2, 'CON BAÑO', 'CON BALCON', 500)}
    usuario1=Personal_Administrativo('santiago','armengol','12345628','11111111111','sarmen@gmail.com','igauzu 1032','sarmen','SANTI12345')
    hotelPOO.asignar_admin('sarmen')
    usuario2=Cliente('maggie','lencina','12312312','12345678901','maggie@gmail.com','los patos 120','maggie','MAGGIE12345')
    usuario3=Personal_Mantenimiento('pedro','galansky','14312312','12345678201','pedro@gmail.com','atuel 900','pedro','PEDRO12345')
    usuario4=Personal_Limpieza('juan','lambertucci','14312365','12345690201','juan@gmail.com','desembarco 900','juan','JUAN12345')
    hotelPOO.agregar_usuario(usuario1)
    hotelPOO.agregar_usuario(usuario2)
    hotelPOO.agregar_usuario(usuario3)
    hotelPOO.agregar_usuario(usuario4)
    hotelPOO.lista_personal.add_to_end(usuario1)
    hotelPOO.lista_personal.add_to_end(usuario3)
    hotelPOO.lista_personal.add_to_end(usuario4)
    hotelPOO.lista_clientes_activos.add_to_end(usuario2)
    hotelPOO.dict_buffet={'MANZANA':[5,20], 'BANANA':[7,30], 'MEDIALUNAS': [10,50], 'PANQUEQUES': [10,60], 'CAFE':[3,40]}
    

print('HOTELPOO' + '\n'*2 + 'Bienvenido')

inicio = None

while inicio != 'SALIR':
    inicio = input('\n Seleccione "1" si desea iniciar sesion \n "2" si desea crear un usuario \n Escriba salir para finalizar el programa: \n')
    inicio=inicio.upper()
    match inicio:
        case '1':

            nombre_usu = input("Ingrese su nombre de usuario: ")    #PEDIMOS EL NOMBRE DE USUARIO
            contrasenna = input("Ingrese su contraseña: ")      #PEDIMOS LA CONTRASEÑA 
            try:
                if hotelPOO.dict_usu[nombre_usu].contrasenna == contrasenna and hotelPOO.dict_usu[nombre_usu].fecha_baja==None:    #VERICAMOS QUE EL USUARIO Y CONTRASEÑA COINCIDAN
                    inicio_sub=None
                    usuario = hotelPOO.dict_usu[nombre_usu]
                    fecha_ingreso = datetime.now()
                    if nombre_usu==hotelPOO.admin:  #MENU DEL ADMINISTRADOR
                        
                        print('Bienvenido al menu de administrador ')
                        while inicio_sub != 'SALIR':
                            continuar=input('Ingrese enter para continuar: ') #esto esta para poder visualizar los resultados mas amigablemente
                            inicio_sub = menu_admin(hotelPOO, usuario)
                            if inicio_sub == 'SALIR':
                                usuario.agregar_ingreso_egreso(fecha_ingreso)
                                    
                    elif isinstance(hotelPOO.dict_usu[nombre_usu], Personal_Administrativo): #MENU DEL PERSONAL ADMINISTRATIVO
                        print('Bienvenido al menu de personal administrativo: ')
                        while inicio_sub != 'SALIR':
                            inicio_sub = menu_personal_admin(hotelPOO, usuario, AlmacenPOO)
                            if inicio_sub == 'SALIR':
                                usuario.agregar_ingreso_egreso(fecha_ingreso)

                    elif isinstance(hotelPOO.dict_usu[nombre_usu], Personal_Limpieza):
                        print('Bienvenido al menu de personal de limpieza: ')
                        while inicio_sub != 'SALIR':
                            inicio_sub = menu_personal_limpieza_y_mantenimiento( usuario)
                            if inicio_sub == 'SALIR':
                                usuario.agregar_ingreso_egreso(fecha_ingreso)
                                
                    elif isinstance(hotelPOO.dict_usu[nombre_usu], Personal_Mantenimiento):
                        print('Bienvenido al menu de personal de mantenimiento: ')
                        while inicio_sub != 'SALIR':
                            inicio_sub = menu_personal_limpieza_y_mantenimiento(usuario)
                            if inicio_sub == 'SALIR':
                                usuario.agregar_ingreso_egreso(fecha_ingreso)
                    
                    elif isinstance(hotelPOO.dict_usu[nombre_usu], Cliente): # MENU DE LOS CLIENTES
                        print('Cliente: ')
                        while inicio_sub!='SALIR':
                            inicio_sub= menu_cliente(hotelPOO, usuario)
                            
                            
                else:
                    print("El usuario y la contraseña no coinciden. Vuelve y juega!")
            except KeyError: #SI EL USUARIO NO EXISTE SE MUESTRA POR PANTALLA ESTO 
                print('El usuario ingresado no existe. Porfavor ingrese 2 para crear un usuario o vuelva a intentarlo.')
        
        case '2':         #El administrador crea los usuarios para su personal
            hotelPOO.crear_usuario('CLIENTE')
            
hotelPOO.save()

#admin
#sarmen
#SANTI12345
