
def es_digito(largo, dato):
    """"
    validacion si todos los caracteres son digitos y el largo de la cadena
    """
    valor = input("Ingrese un {}: ".format(dato))
    while valor.isdigit()==False or len(valor)!=largo:
        if valor.upper()=='SALIR':                                               ##EN EL MENU DEBEMOS ACLARAR QUE PARA SALIR DEL MENU, DEBE ESCRIBIR 'SALIR'
            break
        valor = input('El {} ingresado no es valido, por favor, intentelo nuevamente: '.format(dato))
    return valor

#print(es_digito(2, 'dni'))


def contiene(caracter, dato, cantidad):
    """
    validacion si hay una cantidad de caracteres especificos dentro de la cadena
    """
    cad = input('Ingrese un {}: '.format(dato))
    while cad.count(caracter)!=cantidad:
        if cad.upper()=='SALIR':                                               ##EN EL MENU DEBEMOS ACLARAR QUE PARA SALIR DEL MENU, DEBE ESCRIBIR 'SALIR'
            break
        cad = input('El {} ingresado no es valido, por favor, intentelo nuevamente: '.format(dato))

   
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

