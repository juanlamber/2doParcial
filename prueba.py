import numpy as np
import datetime
from queue import LifoQueue


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
            self.head.valor.fecha_baja = date.today() #Le cambiamos la fecha de baja
            self.head = self.head.prox
            return 

        current = self.head
        while current.prox:
            if current.prox.valor.dni == dni:
                current.prox.valor.fecha_baja = date.today() #Le cambiamos la fecha de baja
                print(current.prox.valor.fecha_baja)
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


class Reserva:
    # codigo=1  VER QUE HACER CON ESTO
    def __init__(self, fecha_inicio, fecha_fin):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        

class Habitacion:
    def __init__(self, nro, categoria, precio, capacidad):
        self.nro = nro
        self.reserva_actual = None
        self.categoria = categoria
        self.precio = precio
        self.capacidad = capacidad
        self.lista_reservas = []
        

def intervalo_superpuesto(intervalo_padre, intervalo_hijo):
    inicio_padre, fin_padre = intervalo_padre
    inicio_hijo, fin_hijo = intervalo_hijo

    # Comprueba si el intervalo hijo está contenido en el intervalo padre
    if fin_padre <= inicio_hijo or fin_hijo <= inicio_padre:
        return True
    else:
        return False
    
    



pedido = ['Familiar', 100000, 4]


habitacion1 = Habitacion(1, 'Suite', 45000, 2)

habitacion2 = Habitacion(2, 'Familiar', 100000, 4)

habitacion3 = Habitacion(3, 'Familiar', 100000, 4)

reserva1 = Reserva(datetime.datetime.strptime('2022-01-02', '%Y-%m-%d'), datetime.datetime.strptime('2022-01-15', '%Y-%m-%d'))
reserva2 = Reserva(datetime.datetime.strptime('2022-01-05', '%Y-%m-%d'), datetime.datetime.strptime('2022-01-20', '%Y-%m-%d'))

reserva3 = Reserva(datetime.datetime.strptime('2021-01-05', '%Y-%m-%d'), datetime.datetime.strptime('2021-01-20', '%Y-%m-%d'))
reserva4 = Reserva(datetime.datetime.strptime('2021-01-02', '%Y-%m-%d'), datetime.datetime.strptime('2021-01-15', '%Y-%m-%d'))


habitacion1.lista_reservas.append(reserva1)
habitacion1.lista_reservas.append(reserva2)

habitacion2.lista_reservas.append(reserva3)
habitacion2.lista_reservas.append(reserva4)


dict_habitaciones = {'1':habitacion1, '2':habitacion2, '3':habitacion3}

atributos = vars(habitacion1)
print(atributos)
valores = list(atributos.values())[2:5]
print(valores)

list_filtrado = list(filter(lambda habitacion: list(vars(habitacion).values())[2:5] == pedido, dict_habitaciones.values()))

intervalo = (datetime.datetime.strptime('2021-01-10', '%Y-%m-%d'), datetime.datetime.strptime('2021-01-28', '%Y-%m-%d'))

print(list_filtrado)
print(intervalo)
print(list_filtrado[0].nro)
#print(list_filtrado[1].nro)

lista_filtrada2 = list(filter(lambda habitacion: any([intervalo_superpuesto((reserva.fecha_inicio, reserva.fecha_fin), intervalo) for reserva in habitacion.lista_reservas]) or habitacion.lista_reservas==[], list_filtrado))

print(intervalo_superpuesto((datetime.datetime.strptime('2022-01-02', '%Y-%m-%d'), datetime.datetime.strptime('2022-01-15', '%Y-%m-%d')), intervalo))

print(lista_filtrada2)
print(lista_filtrada2[0].nro)
print(lista_filtrada2[0].lista_reservas)


######### MAIN #########
