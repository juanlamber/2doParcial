#Importar librerias
import numpy as np
import datetime
from funciones import *
from queue import LifoQueue

#Establecer Clases

class hotel:                                                    #atributos de instancia, ya que la compania puede tener mas de un hotel.
    def __init__(self, lista_personal = ListaEnlazada(), lista_clientes_activos = ListaEnlazada(), pila_cuartos = LifoQueue(), dict_habitacion ={}):                   #Deberiámos hacer una matriz para los informes estadísticos?
        self.habitaciones = dict_habitacion
        self.pila_cuartos = pila_cuartos
        self.lista_personal = lista_personal
        self.lista_clientes_activos = lista_clientes_activos
        
    def agregar_habitacion(self, nro, precio, capacidad, tipo, banio, ventana, balcon, estado):
        self.habitaciones[nro]=[precio, capacidad, tipo, banio, ventana, balcon, estado] 
    
    def agregar_cuartosucio(self, nro):
        self.pila_cuartos.put(nro)
    
    def limpiar_cuarto(self):
        if self.pila_cuartos.empty() == True:
            print("No hay cuartos para limpiar.")
            return
        self.pila_cuartos.get()
    
    def modificar_persona(self):
        persona = input("Ingrese A si quiere modificar el personal o B si quiere modificar un cliente") #Falta validar que el usuario introduzca A o B
        valor = input("Ingrese '1' si desea agregar, '2' si desea eliminar.")   ##Esto podria estar en el menu
        while valor != '1' and valor != '2':
                valor = input("Ingrese una opción válida.")
        if persona == "A":
            if valor == '1':
                nombre_usu, nombre, apellido, dni, telefono, mail, direccion, contrasenna = ingresar_persona()
                self.lista_personal.add_to_end(personal(nombre_usu, nombre, apellido, dni, telefono, mail, direccion, contrasenna))
            
            else:
                DNI = input("Ingrese un DNI")
                self.lista_personal.delete(DNI)
        else:
            if valor == '1':
                nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna = ingresar_persona()
                self.lista_clientes_activos.add_to_end(cliente(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna))
            
            else:
                DNI = input("Ingrese un DNI")
                self.lista_clientes_activos.delete(DNI)
            

            

hotelPOO = hotel()
hotelPOO.agregar_habitacion(1, 50, 2, 8,7,7,7)
print(hotelPOO.habitaciones)
hotelPOO.modificar_personal()



class usuario:                                  #metodo cambiar contraseña
    def __init__(self, nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna):
        self.nombre_usu=nombre_usu
        self.nombre = nombre
        self.apellido=apellido
        self.fecha_alta=datetime.datetime.now().time()
        self.fecha_baja=None
        self.dni=dni
        self.telefono=telefono
        self.mail=mail
        self.direccion=direccion
        self.contrasenna = contrasenna
        

class personal(usuario):
    historico_empleados=1
    def __init__(self,nombre, nombre_usu,  apellido, dni, telefono, mail, direccion, contrasenna):
        super().__init__( nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)
        self.legajo=personal.historico_empleados
        personal.historico_empleados+=1 
        
        
        
class personal_limpieza(personal):
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion):
        super().__init__(self, nombre, apellido, dni, telefono, mail, direccion)
    
            
class personal_mantenimiento(personal):
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion):
        super().__init__(self, nombre, apellido, dni, telefono, mail, direccion)
         
class cliente(usuario):
    def __init__(self, nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna):
        super().__init__(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)
        self.historialreserva=[]
    
    # def realizar_reserva(): #poner en el arg todo lo que se necesite para realizar una reserva
    #     res=reserva()
    #     self.historialreserva.append(res)
class reserva:
    reservas={}
    def __init__(self, codigo, cliente:cliente, ):
        pass


        


##DENTRO DE UN INIT, NO DEBE HABER INPUTS
##FALTAN LAS VERIFICACIONES 


