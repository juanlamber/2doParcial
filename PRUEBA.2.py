import numpy as np
import datetime
from queue import LifoQueue


##MAIN.PY

class hotel:                                                    #atributos de instancia, ya que la compania puede tener mas de un hotel.
    def __init__(self, check_in, check_out, admin = None, metodos_pago = [], dict_usu = {}, lista_personal = ListaEnlazada(), lista_clientes_activos = ListaEnlazada(), pila_cuartos = LifoQueue(), dict_habitacion = {}):                   #Deberiámos hacer una matriz para los informes estadísticos?
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
        if persona.nombre_usu in self.dict_usu.keys() or any(usuario.dni == persona.dni for usuario in hotelPOO.dict_usu.values()): # una persona no se puede crear dos usuarios
            print('Ya existe un usuario con ese DNI y/o nombre de usuario.')
            return False
        else:
            self.dict_usu[persona.nombre_usu] = persona
            return True
        
        
    def crear_usuario(self, tipo):         #VALOR hace referencia a lo que ingresa el usuario en menu, puede ser personal admin, cliente o administrador
        nombre, nombre_usu,  apellido, dni, telefono, mail, direccion, contrasenna = ingresar_persona()
        if tipo.upper() == "PERSONAL":
            persona= personal_administrativo(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)
            if self.agregar_usuario(persona):                                                        
                self.lista_personal.add_to_end(persona)
        elif tipo.upper() =='CLIENTE':
            persona = cliente(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)
            if self.agregar_usuario(persona):
                self.lista_clientes_activos.add_to_end(persona)
        
        
    def eliminar_persona(self):
        DNI = input("Ingrese un DNI")
        persona = input("Ingrese A si quiere eliminar un miembro del personal o B si quiere eliminar un cliente")  #Falta validar que el usuario introduzca A o B
        if persona == 'A':
            self.lista_personal.delete(DNI)
        elif persona == 'B':
            self.lista_clientes_activos.delete(DNI)

            
    def agregar_medio_pago(self, medio):
        self.metodos_pago.append(medio)
        
    
    def crear_pers_mantenimiento(self):
        
        persona = personal_mantenimiento()               #Agregamos personal de mantenimiento a lista enlazada de personal
    
    def crear_pers_limpieza(self):
        pass
    
            


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
        

class personal(usuario):     #PODRIAMOS AGREGAR UN ATTRIBUTO "TIPO DE PERSONAL" Y EVITAR CREAR TANTAS CLASES??
    historico_empleados=1
    def __init__(self,nombre, nombre_usu,  apellido, dni, telefono, mail, direccion, contrasenna):
        super().__init__( nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)
        self.legajo=personal.historico_empleados
        personal.historico_empleados+=1 
        
   
class personal_administrativo(personal):
    def __init__(self, nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna):
        super().__init__(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)   

    
        
class personal_limpieza(personal):
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu=None, contrasenna=None):
        super().__init__(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)

    def limpiar_cuarto(self, hotel: hotel):
        if hotel.pila_cuartos.empty() == True:
            print("No hay cuartos para limpiar.")
            return
        hotel.pila_cuartos.get()
    
    
        
class personal_mantenimiento(personal):
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu=None, contrasenna=None):
        super().__init__(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)
         
class cliente(usuario):
    def __init__(self, nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna):
        super().__init__(nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna)
        self.historialreserva=[]
    
    # def realizar_reserva(): #poner en el arg todo lo que se necesite para realizar una reserva
    #     res=reserva()
    #     self.historialreserva.append(res)

    
    







    
    