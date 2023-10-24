#Importar librerias
import numpy as np
import datetime
from funciones import *
from queue import LifoQueue
from validaciones import *
from CLASES import *
import pickle
##MENU

try:
    with open('hotelPOO.pickle','rb') as f:
        hotelPOO=pickle.load(f)
except:
    hotelPOO = Hotel('2', '3')   

#inicio

# hotelPOO.crear_usuario("CLIENTE")
# print(hotelPOO.lista_personal)
# print(hotelPOO.dict_usu)
# print(type(hotelPOO.dict_usu["sarme"]))
# hotelPOO.crear_usuario("CLIENTE")
# print(hotelPOO.lista_personal)
# print(hotelPOO.dict_usu)
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
                if hotelPOO.dict_usu[nombre].contrasenna == contrasenna:    #VERICAMOS QUE EL USUARIO Y CONTRASEÑA COINCIDAN
                
                    if nombre==hotelPOO.admin:  #MENU DEL ADMINISTRADOR
                        print('Administrador: ')
                
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


