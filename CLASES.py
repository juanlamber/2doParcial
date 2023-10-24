import numpy as np
import datetime
#from queue import LifoQueue
from validaciones import *
from funciones import *
import pickle



##Listas enlazadas 

class Nodo:
    def __init__(self, value):
        self.valor = value
        self.prox = None

class ListaEnlazada:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def add_to_start(self, value): # Forma 1: Pasamos el valor del nodo y lo instanciamos
        new_node = Nodo(value)
        new_node.prox = self.head
        self.head = new_node

    def add_to_end(self, value): # Forma 2: Pasamos el nodo a linkear
        new_node = Nodo(value)
        if self.is_empty():
            self.head = new_node
            return
        current = self.head
        while current.prox:
            current = current.prox
        current.prox = new_node

    def pop(self):
        '''
        Este método pop devuelve el valor del nodo head y lo desenlaza de la lista.
        Ojo! En general el método pop devuelve el último nodo de la lista. Siempre revisar la
        implementación y/o la documentación de los métodos.
    
        '''
        if self.is_empty():
            return None
        popped_value = self.head.valor
        self.head = self.head.prox
        return popped_value

    def delete(self, dni):
        '''
        Este método busca el primer nodo cuyo valor se corresponde al argumento y lo desenlaza. 
        Tendría sentido hacer referencia al nodo directamente en lugar de su valor?
        '''
        if self.is_empty():
            return

        if self.head.valor.dni == dni:
            self.head = self.head.prox
            return

        current = self.head
        while current.prox:
            if current.prox.valor.dni == dni:
                current.prox = current.prox.prox
                return
            current = current.prox

    def __str__(self):
        text = ""
        current = self.head
        while current:
            text += str(current.valor.dni) + " -> "
            current = current.prox
        text += "None" # De qué otra manera podríamos agregarlo ?
        return text

##MAIN.PY

class Hotel:                                                    #atributos de instancia, ya que la compania puede tener mas de un hotel.
    def __init__(self, check_in, check_out, admin = None, metodos_pago = [], dict_usu = {}, lista_personal = ListaEnlazada(), lista_clientes_activos = ListaEnlazada(), pila_cuartos = None, dict_habitacion = {}):                   #Deberiámos hacer una matriz para los informes estadísticos?
        self.habitaciones = dict_habitacion
        self.pila_cuartos = pila_cuartos
        self.dict_usu = dict_usu
        self.lista_personal = lista_personal
        self.lista_clientes_activos = lista_clientes_activos
        self.metodos_pago = metodos_pago                          #Estaría bueno usar un set?
        self.check_in = check_in
        self.check_out = check_out
        self.admin=admin
    
    def asignar_admin(self, nuevo_usu):         #SE ASIGNA AL INICIAR EL PROGRAMA
        self.admin = nuevo_usu
        
    def agregar_habitacion(self, nro, precio, capacidad, tipo, banio, ventana, balcon, estado):
        self.habitaciones[nro]=[precio, capacidad, tipo, banio, ventana, balcon, estado] 
    
    def agregar_cuartosucio(self, nro):
        self.pila_cuartos.put(nro)
        
    def agregar_usuario(self, persona):
        if persona.nombre_usu in self.dict_usu.keys() or any(Usuario.dni == persona.dni for Usuario in self.dict_usu.values()): # una persona no se puede crear dos usuarios
            print('Ya existe un Usuario con ese DNI y/o nombre de Usuario.')
            return False
        else:
            self.dict_usu[persona.nombre_usu] = persona
            return True
        
        
    def crear_usuario(self, tipo):         #VALOR hace referencia a lo que ingresa el Usuario en menu, puede ser Personal admin, Cliente o administrador
        nombre, nombre_usu,  apellido, dni, telefono, mail, direccion, contrasenna = ingresar_persona()
        if tipo.upper() == "PERSONAL":
            persona= Personal_Administrativo(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)
            if self.agregar_usuario(persona):                                                        
                self.lista_personal.add_to_end(persona)
        elif tipo.upper() =='CLIENTE':
            persona = Cliente(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)
            if self.agregar_usuario(persona):
                self.lista_clientes_activos.add_to_end(persona)
        
        
    def eliminar_persona(self):
        DNI = input("Ingrese un DNI")
        persona = input("Ingrese A si quiere eliminar un miembro del Personal o B si quiere eliminar un Cliente")  #Falta validar que el Usuario introduzca A o B
        if persona == 'A':
            self.lista_personal.delete(DNI)
        elif persona == 'B':
            self.lista_clientes_activos.delete(DNI)

            
    def agregar_medio_pago(self, medio):
        self.metodos_pago.append(medio)
        
    
    def crear_pers_mantenimiento(self):
        
        persona = Personal_Mantenimiento()               #Agregamos Personal de mantenimiento a lista enlazada de Personal
    
    def crear_pers_limpieza(self):
        pass
    
    def save(self):
        with open('hotelPOO.pickle','wb') as f:
            pickle.dump(file=f,obj=self)
           


class Usuario:                                  #metodo cambiar contraseña
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
        

class Personal(Usuario):     
    historico_empleados=1
    def __init__(self,nombre, nombre_usu,  apellido, dni, telefono, mail, direccion, contrasenna):
        super().__init__( nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)
        self.legajo=Personal.historico_empleados
        Personal.historico_empleados+=1 
        
   
class Personal_Administrativo(Personal):
    def __init__(self, nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna):
        super().__init__(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)   

    
        
class Personal_Limpieza(Personal):
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu=None, contrasenna=None):
        super().__init__(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)

    def limpiar_cuarto(self, hotel: Hotel):
        if hotel.pila_cuartos.empty() == True:
            print("No hay cuartos para limpiar.")
            return
        hotel.pila_cuartos.get()
    
        
class Personal_Mantenimiento(Personal):
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu=None, contrasenna=None):
        super().__init__(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)

         
class Cliente(Usuario):
    def __init__(self, nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna):
        super().__init__(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)
        self.historialreserva=[]

    # def realizar_reserva(): #poner en el arg todo lo que se necesite para realizar una reserva
    #     res=reserva()
    #     self.historialreserva.append(res)


# class reserva:
#     def__init__(self, codigo, fecha_inicio, fecha_fin, valor_total, cliente_titular, habitaciones, cantidad_huespedes):
        
        
    







    
    