#Importar librerias
import numpy as np
import datetime
from funciones import *
from queue import LifoQueue

#Establecer Clases

class hotel:                                                    #atributos de instancia, ya que la compania puede tener mas de un hotel.
    def __init__(self, metodos_pago, check_in, check_out, dict_usu = {}, lista_personal = ListaEnlazada(), lista_clientes_activos = ListaEnlazada(), pila_cuartos = LifoQueue(), dict_habitacion = {}):                   #Deberiámos hacer una matriz para los informes estadísticos?
        self.habitaciones = dict_habitacion
        self.pila_cuartos = pila_cuartos
        self.dict_usu = dict_usu
        self.lista_personal = lista_personal
        self.lista_clientes_activos = lista_clientes_activos
        self.metodos_pago = metodos_pago                          #Estaría bueno usar un set?
        self.check_in = check_in
        self.check_out = check_out
        
    def agregar_habitacion(self, nro, precio, capacidad, tipo, banio, ventana, balcon, estado):
        self.habitaciones[nro]=[precio, capacidad, tipo, banio, ventana, balcon, estado] 
    
    def agregar_cuartosucio(self, nro):
        self.pila_cuartos.put(nro)
        
    def agregar_usuario(self, persona):
        if persona.dni in self.dict_usu.key():
            return 'Ya existe un usuario con este dni'   
        self.dict_usu[persona.dni] = persona
        
        
    def crear_usuario(self, valor):         #VALOR hace referencia a lo que ingresa el usuario en menu, puede ser personal admin, cliente o administrador
        if valor.upper() == "PERSONAL":
            nombre_usu, nombre, apellido, dni, telefono, mail, direccion, contrasenna = ingresar_persona()
            per = personal_administrativo(nombre_usu, nombre, apellido, dni, telefono, mail, direccion, contrasenna)
            self.agregar_usuario(per)
            self.lista_personal.add_to_end(per)
        elif valor.upper() =='CLIENTE':
            nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna = ingresar_persona()
            cli = cliente(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)
            self.agregar_usuario(cli)
            self.lista_clientes_activos.add_to_end(cli)
        
        ##Administrador?? Podemos hacer una instancia de personal y almacenar su DNI en hotel
        
        
    def eliminar_persona(self):
        DNI = input("Ingrese un DNI")
        persona = input("Ingrese A si quiere eliminar un miembro del personal o B si quiere eliminar un cliente")  #Falta validar que el usuario introduzca A o B
        if persona == 'A':
            self.lista_personal.delete(DNI)
        elif persona == 'B':
            self.lista_clientes_activos.delete(DNI)

            
    def agregar_medio_pago(self, medio):
        self.metodos_pago.append(medio)
            


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
        
   
class personal_administrativo(personal):
    def __init__(self, nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna):
        super().__init__(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)   
        
class personal_limpieza(personal):
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion):
        super().__init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu=None, contrasenna=None)

    def limpiar_cuarto(self, hotel: hotel):
        if hotel.pila_cuartos.empty() == True:
            print("No hay cuartos para limpiar.")
            return
        hotel.pila_cuartos.get()
    
            
class personal_mantenimiento(personal):
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion):
        super().__init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu=None, contrasenna=None)
         
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


