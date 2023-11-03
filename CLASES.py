import numpy as np
from datetime import *
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
            eleminado=self.head.valor
            self.head.valor.fecha_baja = date.today() #Le cambiamos la fecha de baja
            self.head = self.head.prox
            return eleminado

        current = self.head
        while current.prox:
            if current.prox.valor.dni == dni:
                eleminado=current.prox.valor
                current.prox.valor.fecha_baja = date.today() #Le cambiamos la fecha de baja
                current.prox = current.prox.prox
                return eleminado
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
        self.cant_limpieza=0
        self.cant_mantenimiento=0
        self.cant_administrativo=0
        
    def asignar_admin(self, nuevo_usu):         #SE ASIGNA AL INICIAR EL PROGRAMA
        self.admin = nuevo_usu
        
    #def agregar_habitacion(self, nro, precio, capacidad, tipo, banio, ventana, balcon, estado):
        #self.habitaciones[nro]=[precio, capacidad, tipo, banio, ventana, balcon, estado]
        self.habitaciones = {'Simple' : {'CV' : {'CBAL' : {'CBAN' : [], 'SBAN' : []}, 'SBAL' : {'CBAN' : [], 'SBAN' : []}}, 'SV' : {'CBAL' : {'CBAN' : [], 'SBAN' : []}, 'SBAL' : {'CBAN' : [], 'SBAN' : []}}}, 
                             'Doble' : {'CV' : {'CBAL' : {'CBAN' : [], 'SBAN' : []}, 'SBAL' : {'CBAN' : [], 'SBAN' : []}}, 'SV' : {'CBAL' : {'CBAN' : [], 'SBAN' : []}, 'SBAL' : {'CBAN' : [], 'SBAN' : []}}},
                             'Suite' : {'CV' : {'CBAL' : {'CBAN' : [], 'SBAN' : []}, 'SBAL' : {'CBAN' : [], 'SBAN' : []}}, 'SV' : {'CBAL' : {'CBAN' : [], 'SBAN' : []}, 'SBAL' : {'CBAN' : [], 'SBAN' : []}}},
                             'Familiar' : {'CV' : {'CBAL' : {'CBAN' : [], 'SBAN' : []}, 'SBAL' : {'CBAN' : [], 'SBAN' : []}}, 'SV' : {'CBAL' : {'CBAN' : [], 'SBAN' : []}, 'SBAL' : {'CBAN' : [], 'SBAN' : []}}}} 
        
    def identificar_tipo_empleado(self,empleado):

        if isinstance(empleado, Personal_Limpieza):
            self.cant_limpieza -= 1
        elif isinstance(empleado,Personal_Administrativo):
            self.cant_administrativo -= 1
        elif isinstance(empleado, Personal_Mantenimiento):
            self.cant_mantenimiento -= 1

            
    def agregar_cuartosucio(self, nro):
        self.pila_cuartos.put(nro)
        
    def agregar_usuario(self, persona):
        if persona.nombre_usu in self.dict_usu.keys() or any(Usuario.dni == persona.dni for Usuario in self.dict_usu.values()): # una persona no se puede crear dos usuarios
            print('Ya existe un Usuario con ese DNI y/o nombre de Usuario.')
            return False
        else:
            self.dict_usu[persona.nombre_usu] = persona
            return True
        
        
    def crear_usuario(self, tipo):       
        nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna = ingresar_persona('1')
        if tipo.upper() == "PERSONAL ADMINISTRATIVO": #Creamos objetos de la clase personal administrativo
            persona= Personal_Administrativo(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)
            if self.agregar_usuario(persona): #Los agregamos como usuarios                                                       
                self.lista_personal.add_to_end(persona) #
            self.cant_administrativo+=1
                
        elif tipo.upper() =='CLIENTE':
            persona = Cliente(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)
            if self.agregar_usuario(persona):
                self.lista_clientes_activos.add_to_end(persona)
        
    def crear_personal_sin_usuario(self, tipo):
        nombre, apellido, dni, telefono, mail, direccion = ingresar_persona('0')
        if tipo.upper() == "PERSONAL LIMPIEZA": #Creamos objetos de la clase personal limpieza
            persona=Personal_Limpieza(nombre,apellido,dni,telefono,mail,direccion)
            self.cant_limpieza+=1                                              
        if tipo.upper() == "PERSONAL MANTENIMIENTO": #Creamos objetos de la clase personal mantenimiento
            persona=Personal_Mantenimiento(nombre,apellido,dni,telefono,mail,direccion)
            self.cant_mantenimiento+=1      
        self.lista_personal.add_to_end(persona) #Lo agregamos a la lista de personal activo
    
    def eliminar_persona(self):
        DNI = input("Ingrese un DNI: ")
        persona = input("Ingrese A si quiere eliminar un miembro del Personal o B si quiere eliminar un Cliente: ")  #Falta validar que el Usuario introduzca A o B
        if persona == 'A':
            return self.lista_personal.delete(DNI)
        elif persona == 'B':
            self.lista_clientes_activos.delete(DNI)

            
    def agregar_medio_pago(self, medio):
        self.metodos_pago.append(medio)
        pass
    
    
    def save(self):
        with open('hotelPOO.pickle','wb') as f:
            pickle.dump(file=f,obj=self)


# class Reserva:
#     codigo=1
#     def __init__(self, fecha_inicio, fecha_fin, valor_total, cliente_titular, habitaciones, cantidad_huespedes):
#         self.codigo = Reserva.codigo
#         Reserva.codigo +=1
#         self.fecha_reserva=date.today()
        
                
    def elegir_fechas(self):
        self.fecha_inicio = datetime.datetime.strptime(input('Ingrese la fecha en la que desea iniciar su reserva, en el formato YYYY-mm-dd. '), "%Y-%m-%d")



# class Habitacion:
#     def __init__(self, nro, reserva_actual, categoria, precio, capacidad, lista_reservas = ListaEnlazada()):
#         self.nro = nro
#         self.reserva_actual=reserva_actual #REVISAR
        
#     def agregar_reserva(self, reserva: Reserva()):
#         self.lista_reservas.add_to_end(reserva)
        

class Usuario:                                  #metodo cambiar contraseña
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna):
        self.nombre_usu=nombre_usu
        self.nombre = nombre
        self.apellido=apellido
        self.fecha_alta=date.today()
        self.fecha_baja=None
        self.dni=dni
        self.telefono=telefono
        self.mail=mail
        self.direccion=direccion
        self.contrasenna = contrasenna
        

class Personal(Usuario):
    historico_empleados=1     
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna):
        super().__init__( nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)
        self.legajo=Personal.historico_empleados
        
   
class Personal_Administrativo(Personal):
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna):
        super().__init__(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)   
        
    
        
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
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna):
        super().__init__(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)
        self.historialreserva=[]

    # def realizar_reserva(): #poner en el arg todo lo que se necesite para realizar una reserva
    #     res=reserva()
    #     self.historialreserva.append(res)


if __name__ == "__main__":
    hotelPOO = Hotel('2', '3')          
    hotelPOO.crear_personal_sin_usuario('PERSONAL LIMPIEZA')
    print(hotelPOO.lista_personal)
    print(hotelPOO.cant_limpieza)
    emple=hotelPOO.eliminar_persona()  
    hotelPOO.identificar_tipo_empleado(emple)
    print(hotelPOO.lista_personal)
    print(hotelPOO.cant_limpieza)











    
    