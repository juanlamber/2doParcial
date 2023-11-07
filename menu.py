from funciones import *
from datetime import *
from validaciones import *



def menu_cliente( hotel, usuario):
    inicio_sub=input('''
    Ingrese:
     
    "1" si desea realizar una reserva. 
    "2" para visualizar todas sus reservas.  
    "3" para realizar un pedido al buffet.
    
    "SALIR" si desea salir del programa.
    ''')
    match inicio_sub:
        case '1':
            pedido=ingresar_reserva()           ##COMENTAR BIEN
            if pedido!=None:
                list_filtrado = list(filter(lambda habitacion: list(vars(habitacion).values())[2:6] == pedido[0:4], hotel.dict_habitacion.values()))  #En esta lista se filtran las habitaciones que cumplan con todos los requisitos del pedido
                lista_filtrada2 =list(filter(lambda habitacion: any([intervalo_superpuesto((reserva.fecha_inicio, reserva.fecha_fin), pedido[4]) for reserva in habitacion.lista_reservas]) or habitacion.lista_reservas==[], list_filtrado)) #En esta lista se filtran las habitaciones segun las fechas fijandose si ya esta reservada 
                if len(lista_filtrada2)==0:
                    print('No se han encontrado opciones disponibles que coincida en este momento con su pedido.')
                else:
                    print('Seleccione una de las opciones siguientes o introduzca "SALIR" para volver al menu: ')
                    mostrar_habitaciones(lista_filtrada2)
                    eleccion=elegir_habitacion(lista_filtrada2,hotel.dict_habitacion)
                    print('Has salido correctamente.') if eleccion=='SALIR' else eleccion.asignar_habitacion(pedido[4], usuario)
            else:
                print('Has salido correctamente.')
        
        case '2':
            usuario.visualizar_reservas()
            pass
        case '3':
            usuario.pedido_buffet(hotel)
        
    return inicio_sub

        
        
def menu_admin(hotelPOO, usuario):          
    inicio_sub=input('''
    Ingrese:
    
    "1" si desea visualizar tareas pendientes
    "2" si desea dar por realizada la tarea 
    "3" si desea agregar personal        
    "4" si desea eliminar algun empleado o algun cliente
    "5" si desea visualizar el inventario del personal
    "6" si desea agregar una tarea
    "7" si desea visualizar los ingresos y egresos de algun empleado
    "8" si desea visualizar la nómina de los clientes activos
    "9" si desea visualizar los medios de pago disponibles y/o agregar uno

    "SALIR" si desea salir del programa. 
    ''')
    
    match inicio_sub:
        case '1':
            usuario.visualizar_tareas_pendientes()
        case '2':
            usuario.realizar_tarea_pendiente()
        case '3':
            opcion = input('''
        Ingrese:
    
        "A" si desea agregar personal administrativo
        "B" si desea agregar personal de limpieza 
        "C" si desea agregar personal de mantenimiento''')
            
            match opcion.upper():
                case 'A':
                    hotelPOO.crear_usuario('PERSONAL ADMINISTRATIVO')
                case 'B':
                    hotelPOO.crear_usuario('PERSONAL LIMPIEZA')
                case 'C':
                    hotelPOO.crear_usuario('PERSONAL MANTENIMIENTO')
                    
        case '4':
            emple=hotelPOO.eliminar_persona() #ELIMINA LA PERSONA DE LA LISTA CORRESPONDIENTE
            hotelPOO.actualizar_inventario_personal(emple) if emple is not None else None #ACTUALIZA LA CANTIDAD DE EMPLEADOS Y NO HACE NADA SI ES UN CLIENTE
            del hotelPOO.dict_usu[emple.nombre_usu]
        
        case '5':
            print('La cantidad de Personales Administrativos es: ', hotelPOO.cant_administrativo)
            print('La cantidad de Personales de Limpieza es: ', hotelPOO.cant_limpieza)
            print('La cantidad de Personales de Mantenimiento es: ', hotelPOO.cant_mantenimiento)
        case '6':
            usuario.asignar_tarea(hotelPOO)
        case '7':
            usuario.visualizar_ingresos_egresos(hotelPOO)
        case '8':
            usuario.visualizar_nomina_clientes(hotelPOO)
        case '9':
            print('Los medios de pago disponibles son:')
            for med in hotelPOO.metodos_pago:
                print(med)
            valor = input("Seleccione '1' si desea agregar un medio de pago, de lo contrario oprima un botón.")
            if valor == 1:
                medio = input("Ingrese el medio a agregar: ")
                hotelPOO.agregar_medio_pago(medio)
    
    return inicio_sub



def menu_personal_admin(hotelPOO, usuario, AlmacenPOO):
    inicio_sub=input('''
    Ingrese:
     
    "1" si desea visualizar tareas pendientes.
    "2" si desea dar por realizada una tarea.
    "3" si desea agregar una tarea.
    "4" si desea visualizar los ingresos y egresos de algun empleado.
    "5" si desea visualizar la nómina de los clientes activos.
    "6" si desea visualizar los medios de pago disponibles y/o agregar uno
    "7" si desea realizar un pedido al almacen
    "8" si desea agregar stock al buffet
    
    "SALIR" si desea salir del programa.
    ''')
    
    match inicio_sub:
        case '1':
            usuario.visualizar_tareas_pendientes()
        case '2':
            usuario.realizar_tarea_pendiente()
        case '3':
            usuario.asignar_tarea(hotelPOO)
        case '4':
            usuario.visualizar_ingresos_egresos(hotelPOO)
        case '5':
            usuario.visualizar_nomina_clientes(hotelPOO)
        case '6':
            print('Los medios de pago disponibles son:')
            for med in hotelPOO.metodos_pago:
                print(med)
            valor = input("Seleccione '1' si desea agregar un medio de pago, de lo contrario oprima un botón.")
            if valor == 1:
                medio = input("Ingrese el medio a agregar: ")
                hotelPOO.agregar_medio_pago(medio)
        case '7':
            AlmacenPOO.agregar_ingredientes()
        case '8':
            AlmacenPOO.agregar_stock(hotelPOO)
            
    return inicio_sub


def menu_personal_limpieza_y_mantenimiento(usuario):
    inicio_sub=input('''
    Ingrese:
     
    "1" si desea visualizar tareas pendientes.
    "2" si desea dar por realizada una tarea.
    
    "SALIR" si desea salir del programa.
    ''')
    match inicio_sub:
        case '1':
            usuario.visualizar_tareas_pendientes()
        case '2':
            usuario.realizar_tarea_pendiente()


