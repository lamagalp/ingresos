import json
import hashlib
from datetime import datetime

def hashear_contrasena(contrasena):
    return hashlib.sha256(str(contrasena).encode('utf8')).hexdigest()


def validar_contrasena(contrasena, contrasena_hash):
    # Si la contraseña ingresada es igual a la almacenada en el archivo devuelve True
    return hashear_contrasena(contrasena) == contrasena_hash


def validar_usuario(usuario, contrasena):
    """
    Valida que el usuario y la contraseña sean correctos

    :param usuario: nombre de usuario
    :param contrasena: contraseña
    :return: True si el usuario y la contraseña son correctos, False en caso contrario    
    """
    # Si el usuario y la contraseña ingresados son iguales a los almacenados en el archivo devuelve True
    with open('app/files/usuarios.json', 'r') as archivo:
        lista_usuarios = json.load(archivo)  # carga todos los usuarios
        if usuario in lista_usuarios:  # si el usuario existe
            return validar_contrasena(contrasena, lista_usuarios[usuario])
        else:
            return False


def get_ingresos():
    """Devuelve una lista de ingresos """

    with open('app/files/ingresos.json', 'r') as archivo:
        lista_ingresos = json.load(archivo)  # carga todos los usuarios
    return lista_ingresos


def get_ingreso_por_id(id):
    """Devuelve el ingreso con el id indicado. Si el ingreso no existe devuelve None

    :param id: id del ingreso
    :return: datos del ingreso
    """
    with open('app/files/ingresos.json', 'r') as archivo:
        lista_ingresos = json.load(archivo)  # carga todos los ingresos
    for ingreso in lista_ingresos:
        if ingreso['id'] == id:
            ingreso['fecha'] = datetime.strptime(ingreso['fecha'], '%d/%m/%Y')
            return ingreso     
            
    return None


def agregar_ingreso(datos_nuevos):
    """
    Guarda los datos de un nuevo ingreso en el archivo de ingresos
    """
    with open('app/files/ingresos.json', 'r') as archivo:
        lista_ingresos = json.load(archivo)  # carga todos los ingresos
    # Obtener el último id, si no hay ningún ingreso, el id es 1
    if not lista_ingresos:
        id_nuevo = 1
    else:
        id_nuevo = int(max(lista_ingresos, key=lambda x:x['id'])['id']) + 1
    datos_nuevos['id'] = id_nuevo
    lista_ingresos.append(datos_nuevos)
    with open('app/files/ingresos.json', 'w') as archivo:
        json.dump(lista_ingresos, archivo, indent=4)


def eliminar_ingreso(id):
    #  Elimina el ingreso con el id indicado    
    id = int(id)
    with open('app/files/ingresos.json', 'r') as archivo:
        lista_ingresos = json.load(archivo)  # carga todos los usuarios
    # Crea una lista con los ingresos que no tengan el id indicado
    lista_ingresos = [p for p in lista_ingresos if p['id'] != id]
    with open('app/files/ingresos.json', 'w') as archivo:
        json.dump(lista_ingresos, archivo, indent=4)

