##VALIDACIONES.PY
from datetime import *
def es_digito(largo, dato):
    """"
    validacion si todos los caracteres son digitos y el largo de la cadena
    """
    valor = input("Ingrese un {}: ".format(dato))
    while valor.isdigit()==False or len(valor)!=largo:
        if valor.upper()=='SALIR':                                               ##EN EL MENU DEBEMOS ACLARAR QUE PARA SALIR DEL MENU, DEBE ESCRIBIR 'SALIR'
            return 'SALIR'
        valor = input('El {} ingresado no es valido, por favor, intentelo nuevamente: '.format(dato))
    return str(abs(int(valor)))


def contiene(caracter, dato, cantidad):
    """
    validacion si hay una cantidad de caracteres especificos dentro de la cadena
    """
    cad = input('Ingrese un {}: '.format(dato))
    while cad.count(caracter)!=cantidad:
        if cad.upper()=='SALIR':                                               ##EN EL MENU DEBEMOS ACLARAR QUE PARA SALIR DEL MENU, DEBE ESCRIBIR 'SALIR'
            break
        cad = input('El {} ingresado no es valido, por favor, intentelo nuevamente: '.format(dato))
    return cad
   
def pword_fuerte(pword, longmin):
    '''
    Valida si la contraseña es fuerte
    '''
    cant_dig= True if sum(1 for char in pword if char.isdigit())>=1 else False
    cant_mayus = True if sum(1 for i in pword if i.isupper())>=2 else False
    len_min = True if len(pword)>=longmin else False
    return (cant_dig and cant_mayus and len_min)


def pedir_pword():
    print('Ingrese una contraseña con los sigientes requisitos:' + '\n' 
          + 'Requisitos: 1- Al menos un digito.' + '\n' 
          + '2- Al menos dos mayusculas.' + '\n' 
          + '3- Por lo menos 8 carcateres.' + '\n')
    pword=input('Contraseña: ')
    while pword_fuerte(pword,8)!=True:
        pword=input('La contraseña no cumple los requisitos, ingresela nuevamente: ')
        if pword.upper()=='SALIR':
            break
    return pword

def dato_en_lista(dato,lista): #Agregar el domingo al doc gral
    '''Dado el dato introducido, verifica que este se encuentre en la tupla de valores determinados'''
    cat=input('Introduzca {} : '.format(dato))
    while cat.upper() not in lista:
        cat=input('Dato invalido. Por favor introduzca {} nuevamente o introduzca "SALIR": '.format(dato))
        if cat.upper()== 'SALIR':
            break
    return cat.upper()

def ingresar_fecha():
    fecha=None
    while fecha==None:
        try:
            fecha=input('Ingresar una fecha del formato "YYYY-MM-DD": ')
            if fecha.upper()=='SALIR':
                return 'SALIR'
            fecha=datetime.strptime(fecha, '%Y-%m-%d')
            # if date(fecha)<date.now():
            #     print('Por favor ingrese una fecha posterior a la de hoy: ')
            #     fecha=None
        except ValueError:
            fecha=None
    return fecha

def fecha_valida(fecha_i):
    fecha_f=ingresar_fecha()
    if fecha_i=='SALIR' or fecha_f=='SALIR':
        return 'SALIR'
    while fecha_f<=fecha_i:
        print('Porfavor ingrese una fecha valida')
        fecha_f=ingresar_fecha()
    return fecha_f

def formato_datetime(fecha):
    if len(fecha):
        pass

def intervalo_superpuesto(intervalo_padre, intervalo_hijo): # Comprueba si el intervalo hijo está contenido en el intervalo padre
    inicio_padre, fin_padre = intervalo_padre
    inicio_hijo, fin_hijo = intervalo_hijo
    if fin_padre < inicio_hijo or fin_hijo < inicio_padre:
        return True
    else:
        return False