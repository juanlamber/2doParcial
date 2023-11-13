import numpy as np
from datetime import *
from validaciones import *
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
            texto += str(current.valor.nombre) + '\t' + str(current.valor.apellido)+  '\t' + str(current.valor.dni)+ '\n'
            current = current.prox
        return texto

##MAIN.PY

class Hotel:                                                    #atributos de instancia, ya que la compania puede tener mas de un hotel.
    def __init__(self, check_in, check_out, admin = None, dict_usu = {}, lista_personal = ListaEnlazada(), lista_clientes_activos = ListaEnlazada(), dict_habitacion = {}, dict_buffet = {}):                 
        self.dict_habitacion = dict_habitacion
        self.dict_usu = dict_usu
        self.lista_personal = lista_personal
        self.lista_clientes_activos = lista_clientes_activos
        self.metodos_pago = {'TARJETA DE CREDITO', 'TARJETA DE DEBITO', 'EFECTIVO', 'TRANSFERENCIA BANCARIA', 'CHEQUE', 'CRIPTOMONEDAS'}                        
        self.check_in = check_in
        self.check_out = check_out
        self.admin=admin
        self.cant_limpieza=1
        self.cant_mantenimiento=1
        self.cant_administrativo=1
        self.tareas=['Limpiar recepcion','Limpiar cuartos','No anda la ducha, llamar a al personal de mantenimiento'
                     ,'Limpiar pasillos', 'Solicitar presupuesto', 'Hacer balance de gastos','Pagar a proovedor','Control del estado de la piscina']
        self.dict_buffet=dict_buffet
        self.almacen=None
        self.nrofactura=1
    
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
                self.lista_personal.add_to_end(persona) 
            self.cant_administrativo+=1
                
        elif tipo.upper() =='CLIENTE':
            persona = Cliente(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)
            if self.agregar_usuario(persona):
                self.lista_clientes_activos.add_to_end(persona)

        elif tipo.upper() == "PERSONAL LIMPIEZA": #Creamos objetos de la clase personal limpieza
            persona=Personal_Limpieza(nombre,apellido,dni,telefono,mail,direccion,nombre_usu,contrasenna)
            if self.agregar_usuario(persona): #Los agregamos como usuarios                                                       
                self.lista_personal.add_to_end(persona) 
            self.cant_limpieza+=1 
        elif tipo.upper() == "PERSONAL MANTENIMIENTO": #Creamos objetos de la clase personal mantenimiento
            persona=Personal_Mantenimiento(nombre,apellido,dni,telefono,mail,direccion,nombre_usu,contrasenna)
            if self.agregar_usuario(persona): #Los agregamos como usuarios                                                       
                self.lista_personal.add_to_end(persona)             
            self.cant_mantenimiento+=1      

    
    def eliminar_persona(self):
        '''
        Elimina un miembro del personal o un cliente (de la lista de clientes activos)
        '''
        persona = input("Ingrese A si quiere eliminar un miembro del Personal o B si quiere eliminar un Cliente: ")  #Falta validar que el Usuario introduzca A o B
        
        if persona == 'A':
            print('Aqui tiene una lista del personal activo')
            print(self.lista_personal)
            dni = input("Ingrese un DNI: ")
            return self.lista_personal.delete(dni)
        elif persona == 'B':
            print('Aqui tiene una lista de los clientes activos')
            print(self.lista_clientes_activos)
            dni = input("Ingrese un DNI: ")
            return self.lista_clientes_activos.delete(dni)

            
    def modificar_medio_pago(self, medio):
        '''
        Agrega o elimina un medio de pago. 
        '''
        modificar=input('Oprima "1" si desea agregarlo. \n Oprima "2" si desea eliminarlo. ')
        if modificar=='1':
            self.metodos_pago.add(medio.upper())
            print('Se agrego con exito el medio de pago')
        elif modificar=='2':
            if medio in self.metodos_pago:
                self.metodos_pago.discard(medio)
                print('Se elimino con exito el medio de pago')
            else:
                print('Ese medio de pago no está disponible')
        else:
            print('La opción ingresada no es válida')
        
                

    def save(self):
        '''
        Este metodo nos permite actualizar el pickle.
        '''
        with open('hotelPOO.pickle','wb') as f:
            pickle.dump(file=f,obj=self)

   
    def informe_estadistico(self):
        opcion= input('''
        Ingrese 
        "1" para obtener el porcentaje de ocupacion del hotel
        "2" para obtener el porcentaje de ocupacion de acuerdo a la categoría de las habitaciones
        "3" para obtener la cantidad de clientes por tipo
        "4" para obtener el total recaudado en el dia
        ''')
        ocupado = list(filter(lambda habitacion: any([intervalo_superpuesto((reserva.fecha_inicio, reserva.fecha_fin), (datetime.now(), datetime.now()))==False for reserva in habitacion.lista_reservas]), self.dict_habitacion.values())) #en esta funcion se busca para cada habitacion si posee una reserva activa 
        match opcion:
            case "1":
                
                porcen = (len(ocupado) / len(self.dict_habitacion.keys()))*100
                print("El porcentaje de habitaciones ocupadas en total es {}%".format(porcen))
                
            case "2":
                for cat in ('SIMPLE', 'SUITE', 'FAMILIAR', 'DOBLE'):
                    cant_categoria = list(filter(lambda habitacion: habitacion.categoria == cat, ocupado))
                    if len(cant_categoria)!=0:
                        porcen_categoria = (len(cant_categoria) / len(self.dict_habitacion.keys()))*100
                        print("El porcentaje de habitaciones ocupadas del tipo {} es {}%".format(cat, porcen_categoria))
                    else:
                        print("No tiene habitaciones ocupadas del tipo", cat)

            case "3": #Tipos: bronce 1-5000, oro 5000-20000, diamante +20000
                lista_clientes_historicos = list(filter(lambda usuario: isinstance(usuario, Cliente), self.dict_usu.values()))
                lista_categorias = [('BRONCE', 1, 5000), ('ORO', 5000, 20000), ('DIAMANTE', 20000 , 100000000000000)]
                for cat in lista_categorias:
                    lista_tipo = list(filter(lambda cliente: cat[1]<=(sum(np.array(list((reserva.monto_total for reserva in cliente.historialreserva)))))<cat[2], lista_clientes_historicos))
                    print('La cantidad de clientes de {} es: {}'.format(cat[0], len(lista_tipo)))
                    
            case "4":
                recaudacion=0
                for habitacion in self.dict_habitacion.values():
                    res_act=list(filter(lambda reserva: intervalo_superpuesto((reserva.fecha_inicio, reserva.fecha_fin),(datetime.now(), datetime.now()))==False, habitacion.lista_reservas))
                    if len(res_act)>0:
                        recaudacion+=habitacion.precio
                print('La recaudacion total es: '+str(recaudacion))



class Usuario:                                  
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
   
    def __init__(self, nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna):
        super().__init__(nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna)
        self.tareas_pendientes=deque()  
        self.dict_ingreso_egreso = {'1':[], '2':[], '3':[], '4':[], '5':[], '6':[], '7':[], '8':[], '9':[], '10':[], '11':[], '12':[]} #Los numeros representan los nros de los meses
    
    def visualizar_tareas_pendientes(self):
        '''
        Estas son sus tareas pendientes.
        '''
        if len(self.tareas_pendientes)==0:
            print('No tiene tareas pendientes.')
        else:
            print('Sus tareas pendientes son: ')
            for tarea in self.tareas_pendientes:
                print(tarea)
    
    def realizar_tarea_pendiente(self):
        '''
        Permite al usuario registrar cuando un empleado realice una tarea.
        '''
        if len(self.tareas_pendientes)==0:
            print('No tiene tareas pendientes!')
        else:
            tarea_realizada=self.tareas_pendientes.popleft()   
            print('Usted realizo la tarea'+ '\n' + tarea_realizada)

    
    def agregar_ingreso_egreso(self, fecha_ingreso): #Sacamos las variables del main (son objetos datetime
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
        if dni!='SALIR':                   
            persona=hotel.lista_personal.buscar(dni)
            if persona!=None:
                print('Ingrese la tarea que desa asignarle a {}'.format(persona.nombre))
                try:
                    indice=int(input('0-Limpiar recepcion \n 1-Limpiar cuartos \n 2-No anda la ducha, llamar a al personal de mantenimiento \n 3-Limpiar pasillos \n 4-Solicitar presupuesto \n 5-Hacer balance de gastos \n 6-Pagar a proovedores  \n 7-Control del estado de la piscina: '))
                    if indice>=len(hotel.tareas) or indice<0:
                        print('No existe esa tarea, intente nuevamente')
                        return
                    tarea=hotel.tareas[indice]
                    persona.tareas_pendientes.append(tarea)
                    print('Usted ingreso correctamente la tarea')
                except ValueError:
                    print('No existe esa opcion de tarea...')
            else:
                print('No existe una persona con ese dni...')
            
        else:
            return dni
        
    def visualizar_ingreso_egreso(self, hotelPOO):
        dni = es_digito(8, 'DNI')
        mes = dato_en_lista('un Mes',('1','2','3','4','5','6','7','8','9','10','11','12'))
        persona=hotelPOO.lista_personal.buscar(dni)
        if persona!=None:
            try:
                if len(persona.dict_ingreso_egreso[mes])==0:
                    print('No tiene ingresos en ese mes.')
                    return
                for i in persona.dict_ingreso_egreso[mes]:
                    
                    print('Fecha de ingreso: ', datetime.strftime(i[0], '%d de %b del %Y a las %H:%M'))
                    print('Fecha de egreso: ', datetime.strftime(i[1], '%d de %b del %Y a las %H:%M') )
                    print()
            except KeyError:
                    print('Ingrese un mes valido: ')
        else:
            print('Ese dni no pertenece a nadie del personal: ')
            
    def visualizar_nomina_clientes(self, hotelPOO):
        
        '''
        Nos permite visualizar la nomina de clientes del hotel.
        '''
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
        '''
        Método que permite visualizar las reservas de un cliente en especifico. 
        '''
        print('\n' +'Reserva' + '\t' + 'Fecha de inicio' + '\t' + 'Fecha de fin' + '\t' + 'Monto total')
        for reserva in self.historialreserva:
            print('\n')
            fecha_i = datetime.strftime(reserva.fecha_inicio,'%d-%b-%Y')
            fecha_f = datetime.strftime(reserva.fecha_fin,'%d-%b-%Y')
            print(str(reserva.nro) + '\t' + fecha_i + '\t' + fecha_f + '\t' + str(reserva.monto_total))
                        
    def pedido_buffet(self,hotelPOO):
        '''
        Este metodo permite al usuario llevar a cabo un pedido en el buffet del hotel. 
        '''
        try:
            reservaactual=list(filter(lambda reserva: intervalo_superpuesto((reserva.fecha_inicio, reserva.fecha_fin),(datetime.now(), datetime.now()))==False,self.historialreserva))[0] 
        except IndexError:
            print('No tiene reservas activas en el momento')
            return None,None,None
        print('Bienvenido al buffet del HotelPOO \n')
        for item,info in hotelPOO.dict_buffet.items():
            if info[1]!= 0:
                print('{} : ${}'.format(item,info[0]))
        pedido=input('Por favor, ingrese el alimento que desee: ').upper()
        print('Aviso: debe ingresar una cantidad de hasta 9 items')
        pago, lista= 0, []
        while pedido!='LISTO':
            if pedido=='SALIR':
                return None,None,None
            while pedido not in hotelPOO.dict_buffet.keys() and pedido!='LISTO':
                print('{} no se encuentra en nuestro menu.'.format(pedido))
                pedido=input('Por favor, ingrese el alimento que desee: ').upper()
                if pedido=='SALIR':
                    return None,None,None
            if pedido =='LISTO':
                break
            cantidad=es_digito(1,'numero de articulos')
            if cantidad=='SALIR':
                return None,None,None
            while int(cantidad)>hotelPOO.dict_buffet[pedido][1]:
                print('Actualmente no podemos ofrecerle {} {}, puede solicitar como mucho {} {}'.format(cantidad, pedido, hotelPOO.dict_buffet[pedido][1], pedido))
                cantidad=es_digito(1,'numero de articulos')
                if cantidad=='SALIR':
                    return None,None,None
            pago+=hotelPOO.dict_buffet[pedido][0]*int(cantidad)
            hotelPOO.dict_buffet[pedido][1]-=int(cantidad)
            lista.append((pedido, int(cantidad)))
            pedido=input('Por favor, ingrese el alimento que desee o ingrese "LISTO" para finalizar la compra: ').upper()
            
        if lista !=[]:
            print('Su pedido total es:')
            for i in lista:
                print('{} - {}'.format(i[1],i[0]))
            print('El monto a pagar es $', pago)
            print('Se aceptan los siguientes metodos de pago: ')
            for metodo in hotelPOO.metodos_pago:
                print(metodo)
            metodopago=input('Ingrese algun metodo de pago:')
            while metodopago.upper() not in hotelPOO.metodos_pago:            
                print('Se aceptan los siguientes metodos de pago: ')
                for metodo in hotelPOO.metodos_pago:          
                    print(metodo)
                metodopago=input('Ingrese algunos de los metodos de pago: '+'\n')

            reservaactual.monto_total+=pago
            return metodopago, lista, pago
        

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
        '''
        Le asigna una reserva a un usuario determinado, confirmando la transaccion.
        '''
        nro_reserva=usuario.nombre_usu + ' ' + str(len(usuario.historialreserva))
        reserva=Reserva(nro_reserva, inter[0] ,inter[1])
        self.lista_reservas.append(reserva)
        usuario.historialreserva.append(reserva)
        reserva.monto_total+=((inter[1]-inter[0]).days)* self.precio
        print('La operacion ha sido exitosa. Usted ha reservado la habitacion {} con las siguientes comodidades: {}, {}, {}, {}; desde el {} al {} con un total de ${}'
              .format(self.nro, self.categoria, self.capacidad, self.banio, self.balcon, datetime.strftime(inter[0],'%d de %b del %Y'), datetime.strftime(inter[1],'%d de %b del %Y'), reserva.monto_total))
        print('Su número de reserva es: ', nro_reserva)


class Almacen:
    def __init__(self, pila_ingredientes=deque()):
        self.pila_ingredientes=pila_ingredientes
        
    def agregar_ingredientes(self):
        '''
        Le permite a un administrador agregar almentos nuevos al hotel. 
        '''
        ingrediente=input('Ingrese el alimento que desea comprar: ')
        while ingrediente.isalpha()==False:
            ingrediente=input('Por favor ingrese un alimento valido: ')
        cantidad= input('Ingrese la cantidad de {}: '.format(ingrediente))
        while cantidad.isdigit()==False:
            cantidad= input('Por favor ingrese una cantidad de {} valida: '.format(ingrediente)) #ACA SE REGISTRAN LOS INGREDIENTES QUE INGRESAN AL ALMACEN
        self.pila_ingredientes.append((ingrediente,int(cantidad)))
        print('Se registraron {} {}.'.format(cantidad,ingrediente))
    
    def agregar_stock(self, hotelPOO):
        '''
        Le permite a un administrador agregar stock de algun alimento ya existente al hotel. 
        '''
        if len(self.pila_ingredientes)==0:
            print('La pila de stock se encuentra vacia.')
            return
        stock=self.pila_ingredientes.pop()
        ingrediente, cantidad= stock[0], stock[1]
        if ingrediente not in hotelPOO.dict_buffet.keys():
            precio=input('{} no se encuentra en el buffet. Ingrese un precio de venta: '.format(ingrediente))
            while precio.isdigit()==False:
                precio=input('Por favor, ingrese un valor valido: ')
            hotelPOO.dict_buffet[ingrediente]=[int(precio),cantidad]
        else:
            hotelPOO.dict_buffet[ingrediente][1]+=cantidad
        print('Su stock de productos es: ')
        for item, info in hotelPOO.dict_buffet.items():
            print(item + '\t' + ', Precio: $' + str(info[0]) + '\t' + ', Cantidad: ' + str(info[1]))

def ingresar_persona(): 
    '''
    Le permite al administrador agregar una persona nueva al sistema. 
    '''
    nombre = input("Ingrese un nombre: ")         
    apellido = input("Ingrese un apellido: ")
    dni = es_digito(8,'Dni')
    telefono = es_digito(11,'Telefono')
    mail = contiene('@', 'mail', 1)    
    direccion = input("Ingrese una direccion: ")
    nombre_usu = input("Ingrese un nombre de usuario: ")
    contrasenna = pedir_pword()                     
    if any((nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna))=='SALIR':
        return None
    return nombre, apellido, dni, telefono, mail, direccion, nombre_usu, contrasenna
