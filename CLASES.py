import numpy as np
from datetime import *
from validaciones import *
# from funciones import *
import pickle
from collections import deque



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
        
    def buscar(self, dni):
        '''
        Busca un nodo que tiene el dni pedido.
        '''
        if self.is_empty():
            return

        if self.head.valor.dni == dni:
            return self.head.valor
        
        current = self.head
        while current.prox:
            if current.prox.valor.dni == dni:
                return current.prox.valor
            current = current.prox
        

    def __str__(self):
        texto = ''
        current = self.head
        while current:
            texto += str(current.valor.nombre) + '\t' + str(current.valor.apellido) + '\n'
            current = current.prox
        return texto

##MAIN.PY

class Hotel:                                                    #atributos de instancia, ya que la compania puede tener mas de un hotel.
    def __init__(self, check_in, check_out, admin = None, metodos_pago = [], dict_usu = {}, lista_personal = ListaEnlazada(), lista_clientes_activos = ListaEnlazada(), dict_habitacion = {}, dict_buffet = {}):                   #Deberiámos hacer una matriz para los informes estadísticos?
        self.habitaciones = dict_habitacion
        self.dict_usu = dict_usu
        self.lista_personal = lista_personal
        self.lista_clientes_activos = lista_clientes_activos
        self.metodos_pago = metodos_pago                         
        self.check_in = check_in
        self.check_out = check_out
        self.admin=admin
        self.cant_limpieza=1
        self.cant_mantenimiento=1
        self.cant_administrativo=1
        self.tareas=['Limpiar recepcion','Limpiar cuartos','No anda la ducha, llamar a al personal de mantenimiento'
                     ,'Limpiar pasillos', 'Solicitar presupuesto', 'Hacer balance de gastos','Pagar a proovedor','Control del estado de la piscina']
        self.dict_buffet=dict_buffet
        
    def asignar_admin(self, nombre_admin):         #SE ASIGNA AL INICIAR EL PROGRAMA
        self.admin = nombre_admin
        
    def actualizar_inventario_personal(self, empleado):
        '''
        Actualiza la cantidad de personal.
        '''
        if isinstance(empleado, Personal_Limpieza):
            self.cant_limpieza -= 1
        elif isinstance(empleado,Personal_Administrativo):
            self.cant_administrativo -= 1
        elif isinstance(empleado, Personal_Mantenimiento):
            self.cant_mantenimiento -= 1
        
        
    def agregar_usuario(self, persona):
        '''
        Agrega un usuario al diccionario de usuarios.
        '''
        if persona.nombre_usu in self.dict_usu.keys() or any(Usuario.dni == persona.dni for Usuario in self.dict_usu.values()): # una persona no se puede crear dos usuarios
            print('Ya existe un Usuario con ese DNI y/o nombre de Usuario.')
            return False
        else:
            self.dict_usu[persona.nombre_usu] = persona
            return True
        
        
    def crear_usuario(self, tipo):
        '''
        Crea un usuario. Puede ser del personal o un cliente.
        '''       
        nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna = ingresar_persona()
        if tipo.upper() == "PERSONAL ADMINISTRATIVO": #Creamos objetos de la clase personal administrativo
            persona= Personal_Administrativo(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)
            if self.agregar_usuario(persona): #Los agregamos como usuarios                                                       
                self.lista_personal.add_to_end(persona) #
            self.cant_administrativo+=1
                
        elif tipo.upper() =='CLIENTE':
            persona = Cliente(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)
            if self.agregar_usuario(persona):
                self.lista_clientes_activos.add_to_end(persona)

        elif tipo.upper() == "PERSONAL LIMPIEZA": #Creamos objetos de la clase personal limpieza
            persona=Personal_Limpieza(nombre,apellido,dni,telefono,mail,direccion,nombre_usu,contrasenna)
            if self.agregar_usuario(persona): #Los agregamos como usuarios                                                       
                self.lista_personal.add_to_end(persona) #
            self.cant_limpieza+=1 
        elif tipo.upper() == "PERSONAL MANTENIMIENTO": #Creamos objetos de la clase personal mantenimiento
            persona=Personal_Mantenimiento(nombre,apellido,dni,telefono,mail,direccion,nombre_usu,contrasenna)
            if self.agregar_usuario(persona): #Los agregamos como usuarios                                                       
                self.lista_personal.add_to_end(persona) #            
            self.cant_mantenimiento+=1      

    
    def eliminar_persona(self):
        '''
        Elimina un miembro del personal o un cliente (de la lista de clientes activos)
        '''
        dni = input("Ingrese un DNI: ")
        persona = input("Ingrese A si quiere eliminar un miembro del Personal o B si quiere eliminar un Cliente: ")  #Falta validar que el Usuario introduzca A o B
        if persona == 'A':
            return self.lista_personal.delete(dni)
        elif persona == 'B':
            return self.lista_clientes_activos.delete(dni)

            
    def agregar_medio_pago(self, medio):
        '''
        Agrega un medio de pago disponible.
        '''
        self.metodos_pago.append(medio)
        
                
    def elegir_fechas(self):                ##????????????????
        '''
        Método 
        '''
        self.fecha_inicio = datetime.strptime(input('Ingrese la fecha en la que desea iniciar su reserva, en el formato YYYY-mm-dd. '), "%Y-%m-%d")

    def save(self):
            with open('hotelPOO.pickle','wb') as f:
                pickle.dump(file=f,obj=self)
class Usuario:                                  #metodo cambiar contraseña
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna):
        self.nombre_usu=nombre_usu
        self.nombre = nombre
        self.apellido=apellido
        self.fecha_alta=date.today()
        self.fecha_baja=None #FIJARSE SI PONER FECHA DE BAJA O ELIMINARLOS
        self.dni=dni
        self.telefono=telefono
        self.mail=mail
        self.direccion=direccion
        self.contrasenna = contrasenna
        

class Personal(Usuario):
   
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna):
        super().__init__(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)
        self.tareas_pendientes=deque()  
        self.dict_ingreso_egreso = {'1':[], '2':[], '3':[], '4':[], '5':[], '6':[], '7':[], '8':[], '9':[], '10':[], '11':[], '12':[]} #Los numeros representan los nros de los meses
    
    def visualizar_tareas_pendientes(self):
        '''
        Estas son sus tareas pendientes.
        '''
        print('Sus tareas pendientes son: ')
        print()
        for tarea in self.tareas_pendientes:
            print(tarea)
    
    def realizar_tarea_pendiente(self):
        '''
        Permite al usuario registrar cuando un empleado realice una tarea.
        '''
        if len(self.tareas_pendientes)==0:
            print('No tiene tareas pendientes!!!!')
        else:
            tarea_realizada=self.tareas_pendientes.popleft()   
            print('Usted realizo la tarea'+tarea_realizada)

    
    def agregar_ingreso_egreso(self, fecha_ingreso): #Sacamos las variables del main (son objetos datetime)
        mes = str(fecha_ingreso.month)
        fecha_egreso=datetime.now()
        self.dict_ingreso_egreso[mes].append((fecha_ingreso, fecha_egreso)) 
   
   
class Personal_Administrativo(Personal):
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna):
        super().__init__(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)
                                                                                            
    def asignar_tarea(self, hotel):
        '''
        Permite asignar tareas.
        El personal administrativo se encarga de asignarle tareas al resto del personal (como a si mismo). 
        Ingresa la informacion al sistema en forma de una cola unica para cada persona, la cual se idetifica a traves del DNI.
        '''
        dni=es_digito(8,'DNI')
        if dni!='SALIR':                        ##CHEQUEAR LO DE SALIR
            persona=hotel.lista_personal.buscar(dni)
            if persona!=None:
                indice=int(input('Ingrese la tarea que desa asignrle a {} \n 0-Limpiar recepcion \n 1-Limpiar cuartos \n 2-No anda la ducha, llamar a al personal de mantenimiento \n 3-Limpiar pasillos \n 4-Solicitar presupuesto \n 5-Hacer balance de gastos \n 6-Pagar a proovedores  \n 7-Control del estado de la piscina: ').format(persona.nombre)) 
                if indice>=len(hotel.tareas) or indice<0:
                    print('No existe esa tarea, intente nuevamente')
                    return
                tarea=hotel.tareas[indice]
                persona.tareas_pendientes.append(tarea)
            else:
                print('No existe una persona con ese dni...')
            #print(persona.tareas_pendientes)
            
            ##PODEMOS HACER QUE SE LE ASIGNE LA TAREA A EL EMPLEADO QUE MENOS TAREAS TIENE
                    #chequear que pasa si tienen la misma cantidad de tareas, podes asignar aleatoriamente
            
        else:
            return dni
        
    def visualizar_ingreso_egreso(self, hotelPOO):
        dni = es_digito(8, 'DNI')
        mes = dato_en_lista('un Mes',('1','2','3','4','5','6','7','8','9','10','11','12'))
        persona=hotelPOO.lista_personal.buscar(dni)
        if persona!=None:
            try:
                for i in persona.dict_ingreso_egreso[mes]:
                    if len(i)==0:
                        print('No tiene ingresos en ese mes.')
                        break
                    print('Fecha de ingreso: ', datetime.strftime(i[0], '%d de %b del %Y a las %H:%M'))
                    print('Fecha de egreso: ', datetime.strftime(i[1], '%d de %b del %Y a las %H:%M') )
                    print()
            except KeyError:
                    print('Ingrese un mes valido: ')
        else:
            print('Ese dni no pertenece a nadie del personal: ')
            
    def visualizar_nomina_clientes(self, hotelPOO):
        print(hotelPOO.lista_clientes_activos)
        
 
    
        
class Personal_Limpieza(Personal):
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna):
        super().__init__(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)

        
class Personal_Mantenimiento(Personal):
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna):
        super().__init__(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)

         
class Cliente(Usuario):
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna):
        super().__init__(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)
        self.historialreserva=[]
    
    def visualizar_reservas(self):
        print('\n' +'Reserva' + '\t' + 'Fecha de inicio' + '\t' + 'Fecha de fin' + '\t' + 'Monto total')
        for reserva in self.historialreserva:
            print('\n')
            fecha_i = datetime.strftime(reserva.fecha_inicio,'%d-%b-%Y')
            fecha_f = datetime.strftime(reserva.fecha_fin,'%d-%b-%Y')
            print(str(reserva.nro) + '\t' + fecha_i + '\t' + fecha_f + '\t' + str(reserva.monto_total))
                        
    def pedido_buffet(self,hotelPOO):
        try:
            reservaactual=list(filter(lambda reserva: intervalo_superpuesto((reserva.fecha_inicio, reserva.fecha_fin),(datetime.now(), datetime.now()))==False,self.historialreserva))[0]
        except IndexError:
            print('No tiene reservas activas en el momento')
            return
        print('Bienvenido al buffet del HotelPOO \n')
        for item,info in hotelPOO.dict_buffet.items():
            if info[1]!= 0:
                print('{} : ${}'.format(item,info[0]))
        pedido=input('Por favor, ingrese el alimento que desee: ').upper()
        print('Aviso: debe ingresar una cantidad de hasta 9 items')
        pago, lista= 0, []
        while pedido!='LISTO':
            if pedido=='SALIR':
                return
            while pedido not in hotelPOO.dict_buffet.keys():
                print('{} no se encuentra en nuestro menu.'.format(pedido))
                pedido=input('Por favor, ingrese el alimento que desee: ').upper()
            cantidad=es_digito(1,'numero de articulos')
            if cantidad=='SALIR':
                return
            while int(cantidad)>hotelPOO.dict_buffet[pedido][1]:
                print('Actualmente no podemos ofrecerle {} {}, puede solicitar como mucho {} {}'.format(pedido,cantidad,hotelPOO.dict_buffet[pedido][1],pedido))
                cantidad=es_digito(1,'numero de articulos')
                if cantidad=='SALIR':
                    return
            pago+=hotelPOO.dict_buffet[pedido][0]*int(cantidad)
            hotelPOO.dict_buffet[pedido][1]-=int(cantidad)
            lista.append((pedido, int(cantidad)))
            pedido=input('Por favor, ingrese el alimento que desee o ingrese "LISTO" para finalizar la compra: ').upper()
        print('Su pedido total es:')
        for i in lista:
            print('{} - {}'.format(i[1],i[0]))
        print('El monto a pagar es $', pago)
        reservaactual.monto_total+=pago
        

class Reserva:
    def __init__(self, nro_reserva, fecha_inicio, fecha_fin):
        self.nro= nro_reserva              #EL NUMERO DE RESERVA ES EL NOMBRE DE USUARIO Y UN NUMERO QUE REPRESENTA LA CANTIDAD DE RESERVAS HASTA EL MOMENTO
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.monto_total = 0
    
    def __str__(self):
        cadena='Su reserva con numero '+self.nro+' comienza el '+ datetime.strftime(self.fecha_inicio,'%d de %b del %Y')+' ,termina el '+datetime.strftime(self.fecha_fin,'%d de %b del %Y')+ ' y el monto a pagar es '+str(self.monto_total)
        return cadena
        

class Habitacion:
    def __init__(self, nro, categoria, capacidad, banio, balcon, precio):
        self.nro = nro
        self.reserva_actual = None
        self.categoria = categoria
        self.capacidad = capacidad
        self.banio = banio
        self.balcon = balcon
        self.precio = precio
        self.lista_reservas = []
        
    def asignar_habitacion(self, inter, usuario):
        nro_reserva=usuario.nombre_usu + ' ' + str(len(usuario.historialreserva))
        reserva=Reserva(nro_reserva, inter[0] ,inter[1])
        self.lista_reservas.append(reserva)
        usuario.historialreserva.append(reserva)
        reserva.monto_total+=((inter[1]-inter[0]).days)* self.precio
        print('La operacion ha sido exitosa. Usted ha reservado la habitacion {} con las siguientes comodidades: {}, {}, {}, {}; desde el {} al {} con un total de ${}'
              .format(self.nro, self.categoria, self.capacidad, self.banio, self.balcon, datetime.strftime(inter[0],'%d de %b del %Y'), datetime.strftime(inter[1],'%d de %b del %Y'), reserva.monto_total))
        print('Su número de reserva es: ', nro_reserva)
        print(self.lista_reservas)

class Almacen:
    def __init__(self, pila_ingredientes=deque()):
        self.pila_ingredientes=pila_ingredientes
        
    def agregar_ingredientes(self):
        ingrediente=input('Ingrese el ingrediente que desea comprar: ')
        cantidad= input('Ingrese la cantidad de {}: '.format(ingrediente))
        while cantidad.isdigit()==False:
            cantidad= input('Porfavor ingrese ua cantidad cantidad de {} valida '.format(ingrediente)) #ACA SE REGISTRAN LOS INGREDIENTES QUE INGRESAN AL ALMACEN
        self.pila_ingredientes.append((ingrediente,int(cantidad)))
        print('Se registraron {} {}.'.format(cantidad,ingrediente))
    
    def agregar_stock(self, hotelPOO):
        stock=self.pila_ingredientes.pop()
        ingrediente, cantidad= stock[0], stock[1]
        if ingrediente not in hotelPOO.dict_buffet.keys():
            precio=input('Este ingrediente no se encuentra en el buffet. Ingrese un precio de venta')
            while precio.isdigit()==False:
                precio=input('por favor, ingrese un valor valido')
            hotelPOO.dict_buffet[ingrediente]=[int(precio),cantidad]
        hotelPOO.dict_buffet[ingrediente][1]+=cantidad

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
