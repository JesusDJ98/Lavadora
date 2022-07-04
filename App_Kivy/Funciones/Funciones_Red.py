import os

import numpy
import tensorflow as tf
import numpy as np
from keras.models import load_model
#import h5py as h5
#import joblib


#------------------------------------------------------
#           FUNCIONES DE LAS REDES
#------------------------------------------------------

def Cargar_Redes():
    path = os.getcwd()
    path = path + '\Redes\RNN_Tejido.h5'
    #print('Entro en CargarRedes de Funciones_Red --> ', os.getcwd())
    #print('Direccion abs: ', path)
    #modelo1 = load_model('../Redes/RNN_Tejido.h5')
    modelo1 = load_model('./Redes/RNN_Tejido.h5')
    #modelo1 = load_model(path)
    #modelo1 = h5.File('./Redes/RNN_Temp.h5', 'r')
    #modelo1 = joblib.load('../Redes/RNN_Tejido.h5') # No such file or directory
    #modelo1 = joblib.load('./Redes/RNN_Tejido.h5')
    #print('Tejido cargado')
    modelo2 = load_model('./Redes/RNN_Temp.h5')  #Es el directorio del archivo del boton o del main.py, no de esta funcion
    #print('Temperatura cargado')
    modelo3 = load_model('./Redes/RNN_Centri.h5')
    #print('Centrifugado cargado')
    modelo4 = load_model('./Redes/RNN_Ciclo.h5')
    # Ciclo no estoy seguro pues entonces deberia ver que programas tienen ciclo largo, corto...
    # Y el programa lo dejo a eleccion del ususario, pues solo afectara segun la ropa que introduzca

    # Me gustaria, que cada vez que se use la app, se añada como una opcion mas, para que cada X time aprenda again
    # Ropa, tejido, color, manchas,.... Temp, ciclo,... Prelavado, Programa, Secado

    #print('Modelo ', modelo_Temp.summary())

    return modelo1, modelo2, modelo3, modelo4

#Dada las neuronas de entrada y un modelo devuelve su prediccion
def Ejecutar_modelo(modelo, entrada):
    return modelo.predict(entrada)

#Devuelve la prediccion de todos los modelos dados
def Ejecutar_Redes(entrada, Temp, Centri, Ciclo):
    return Ejecutar_modelo(Temp, entrada), Ejecutar_modelo(Centri, entrada), Ejecutar_modelo(Ciclo, entrada)

#------------------------------------------------------
#           FUNCIONES DE TRATAMIENTO DE DATOS
#------------------------------------------------------

# Eliminamos las tildes
def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


#Traduce lo que escribe el usuario en cadena de palabras
def Separacion(cadena):
    espacios = cadena.split()
    palabras = []
    for i in espacios:
        try:
            a = i.split(',')
            for j in a:
                palabras.append(j)      #Esto genera que introduzca valores vacios
                #if len(j) > 1:         #Esto genera que los valores de 1 caracter los ignore
                #    palabras.append(j)
        except:
            palabras.append(i)
    return palabras


# Modificamos la palabra para que sean entendibles por el programa
def UpperList(Rp, op):
    Lista = []
    if op == 0:
        for i in Rp:
            L = []
            [L.append(normalize(x).upper()) for x in i]
            if L[-1][-1] == 'S':
                aux = L[-1][:-1]
                L[-1] = aux
                # L = aux #No, pues añade un string y no una lista de un valor
                if L[-1][-1] == 'E':  # Quitamos tb por si termina en -es
                    aux = L[-1][:-1]
                    L[-1] = aux

            Lista.append(L)
    else:
        [Lista.append(normalize(x).upper()) for x in Rp]
        if Lista[-1][-1] == 'S':
            aux = Lista[-1][:-1]
            Lista[-1] = aux
            # L = aux #No, pues añade un string y no una lista de un valor
            if Lista[-1][-1] == 'E':  # Quitamos tb por si termina en -es
                aux = Lista[-1][:-1]
                Lista[-1] = aux

    return Lista



#Funcion que ejecuta lo anterior, para que sea entendible por el programa lo introducido por el user
def TratamientoRopa(ropa):
    return UpperList(ropa, 1)


#Convierte array en array de str
def ConvertirStr(entrada):
    L = []
    for i in entrada:
        L.append(str(i))
    return L
#Convierte array en array de str
def ConvertirInt(entrada):
    L = []
    for i in entrada:
        L.append(int(i))
    return L

#Une dos arrays
def UnirSalida(entrada, blanco, color, salida):
    entrada2 = ConvertirStr(entrada)
    salida2 = ConvertirStr(salida)
    L = []
    for r in entrada2:
        [L.append(x) for x in r]
    L.append(blanco)
    L.append(color)
    for r in salida2:
        [L.append(x) for x in r]
    L2 = ConvertirInt(L)
    return L2


# Traduccion de String ropa a neuronas de entrada
def AsignacionTipoRopa(dato):
    persona = Objeto = Pie = Piernas = Torso = Cuerpo = Interior = Medio = Exterior = Normal = Deporte = Formal = Abierto = Cama = Limpieza = Salon = Baño = Fuera = Especial = 0

    if dato == 'CALCETIN':
        persona = Pie = Interior = Normal = 1
    elif dato == 'CALZONCILLO' or dato == 'BRAGA' or dato == 'TANGA':
        persona = Piernas = Interior = Normal = 1
    elif dato == 'SUJETADOR':
        persona = Cuerpo = Interior = Normal = 1
    elif dato == 'TOP':
        persona = Cuerpo = Medio = Deporte = 1
    elif dato == 'PANTALON'  or dato == 'VAQUERO' or dato == 'CHINO':
        persona = Piernas = Exterior = Normal = 1
    elif dato == 'CALZONA':
        persona = Piernas = Medio = Deporte = 1
    elif dato == 'LEGGING' or dato == 'MAYA':
        persona = Piernas = Exterior = Deporte = 1
    elif dato == 'LEOTARDO' or dato == 'MEDIAS':
        persona = Piernas = Medio = Normal = 1
    elif dato == 'FALDA':
        persona = Piernas = Exterior = Formal = Abierto = 1
    elif dato == 'VESTIDO' or dato == 'MONO':
        persona = Cuerpo = Medio = Formal = Abierto = 1
    elif dato == 'CAMISA' or dato == 'BLUSA':
        persona = Torso = Medio = Formal = Abierto = 1
    elif dato == 'POLO':
        persona = Torso = Medio = Formal = 1
    elif dato == 'CAMISETA':
        persona = Torso = Medio = Normal = 1
    elif dato == 'CHALECO' or dato == 'JERSEY' or dato == 'REBECA' or dato == 'CARDIGAN':
        persona = Torso = Exterior = Formal = 1
    elif dato == 'SUDADERA':
        persona = Torso = Exterior = Normal = 1
    elif dato == 'CORTAVIENTO':
        persona = Torso = Exterior = Deporte = 1 #Lo que cogemos para salir a correr, no se si quitarlo
    elif dato == 'PIJAMA':
        persona = Piernas = Torso = Medio = Normal = Cama = 1
    elif dato == 'BATA':
        persona = Cuerpo = Exterior = Normal = Cama = 1
    elif dato == 'BAÑADOR' or dato == 'BIKINI':
        persona = Piernas = Torso = Cuerpo = Medio = Normal = 1
    elif dato == 'TOALLA' or dato == 'ALBORNOZ':
        Objeto = Abierto = Baño = 1
    elif dato == ' TOALLA DE PLAYA':
        Objeto = Fuera = 1
    elif dato == 'PAÑO':
        Objeto = Limpieza = 1
    elif dato == 'SABANAS' or dato == 'FUNDA DE ALMOHADA':
        Objeto = Cama = 1
    elif dato == 'MANTA' or dato == 'EDREDÓN':
        Objeto = Exterior = Cama = 1
    elif dato == 'CHAQUETA' or dato == 'TRAJE' or dato == 'ABRIGO' or dato == 'AMERICANA':
        persona = Torso = Exterior = Formal = Abierto = Especial = 1
    #else prenda no reconocida

    return [persona, Objeto, Pie, Piernas, Torso, Cuerpo, Interior, Medio, Exterior, Normal, Deporte, Formal, Abierto, Cama, Limpieza, Salon, Baño, Fuera, Especial]


def EliminarElementodeLista(lista, elemento):
    l = lista
    cantidad = l.count(elemento)
    for i in range(cantidad):
        l.remove(elemento)
    return l


def TraduccionRopa(palabras):
    separados = Separacion(palabras)
    ropa = EliminarElementodeLista(separados, '')
    #Elimino los valores nulos
    #if len(ropa) > 1:
    #    ropa.remove('')
    #    print('        Ahora sin valores vacios: ', ropa)
    ropaDesconocida = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    Salida = []
    NoReconocidos = []
    for i in ropa:
        tratada = TratamientoRopa([i])
        r = AsignacionTipoRopa(tratada[0])
        Salida.append(r)
        if np.array_equal(r, ropaDesconocida):
            NoReconocidos.append(i)#Añado los elementos que no conozco
    return Salida, NoReconocidos, ropa

def Convertir_Neurona(entrada, blanco, color, salida):
    return UnirSalida(entrada, blanco, color, salida)



#------------------------------------------------------
#           FUNCIONES DE LA SALIDA DE LAS REDES
#------------------------------------------------------

#Devolvemos todos aquellos superior a 20%
def Tejido_Probable(dato):
    tejido = [0,0,0,0,0,0]
    for i in range(len(dato)):
        if dato[i] > 0.20:
            tejido[i] = 1
    return tejido

#Devolvemos
def Elegir_Min_Indice(dato):
    min = dato[0]
    indice = 0
    for i in range(len(dato)):
        if dato[i] < min:
            min = dato[i]
            indice = i
    return indice

def Elegir_Max_Indice(dato):
    max = dato[0]
    indice = 0
    for i in range(len(dato)):
        if dato[i] > max:
            max = dato[i]
            indice = i
    return indice

def Elegir_Min(dato):
    min = dato[0]
    for i in range(len(dato)):
        if dato[i] < min:
            min = dato[i]
    return min


def Analisis(dato):
    L = []
    for i in dato:
        L.append(Elegir_Max_Indice(i))
    #La temperatura esta ordenada
    a = Elegir_Min(L)
    return a


