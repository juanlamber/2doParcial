from validaciones import *
#Funciones listas enlazadas
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
    
def ingresar_persona(): 
    nombre = input("Ingrese un nombre: ")
    nombre_usu = input("Ingrese un nombre de usuario: ")
    apellido = input("Ingrese un apellido: ")
    dni= es_digito(8,'Dni')
    telefono= es_digito(11,'Telefono')
    mail = contiene('@', 'mail', 1)    # Validar que sea un mail con @ y todas las cosas con mails
    direccion = input("Ingrese una direccion: ")
    contrasenna = pedir_pword()                     #Validar requerimientos
    
    ##QUE HACEMOS CON EL SALIR?
     
    return nombre, nombre_usu, apellido, dni, telefono, mail, direccion, contrasenna

#PASAR A VALIDACIONES.PY