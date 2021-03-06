# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1c0CmWDwO-5rrDcc2-tNH1wEr8ZVxQJFc
"""

#           ----------------------------------------------
#          |            LIBRERIAS NECESARIAS              |
#           ----------------------------------------------

import tensorflow as tf
import numpy as np              #red neuronal
import pandas as pd             #Leer fichero
#import xlrd                     #Leer fichero
import matplotlib.pyplot as plt #graficar
#import seaborn as sns
#from sklearn.externals import joblib    #Para guardar las Redes Neuronales
import joblib   #Guardar las redes
import sklearn  #Para separar de manera aleatoria
import time

#           ----------------------------------------------
#          |               VARIABLES GLOBALES             |
#           ----------------------------------------------

#Hago esto para poder modificar lo que quiera de una manera mas rapida y visual

  #Entradas
dimTipo = 19
Persona = Objeto = Pie = Piernas = Torso = Cuerpo = Interior = Medio = Exterior = Normal = Deporte = Formal = Abierto = Cama = Limpieza = Salon = Baño = Fuera = Especial = 0 #Tipo
dimColor = 2
Blanco = Color = 0                                    #Color
dimTejido = 6
EAlgodon = Lana = Lino = Seda = Piel = ESintetico = 0 #Tejido
dimManchas = 1
Mancha = 0
dimE = dimTipo + dimColor + dimTejido
  #Salidas
dimLavado = 13
dimTemp = 5
dimCiclo = 3
dimCentri = 7
dimLavar = 1
dimS = dimLavado + dimTemp + dimCiclo + dimCentri + dimLavar
Prelavado = Delicado = Lana = aMano = Algodon = Sinteticos = Ropa_Cama = Rapido = Sport = Antiarrugas = Mixtos = Centrifugado = Aclarado = Eco = 0  #Programa
T_Fria = T_30 = T_40 = T_60 = T_90 = 0                        #Temperatura
C_Corto = C_Medio = C_Largo = 0                               #Ciclo
C_Sin = C_400 = C_600 = C_800 = C_1000 = C_1200 = C_1400 = 0  #Centrifugado
No_Lavar = 0

#           ----------------------------------------------
#          |       FUNCIONES PARA TRATAR LOS DATOS        |
#           ----------------------------------------------


# Inicializar variables globales
def InitVarPrenda():
  global Persona, Objeto, Pie, Piernas, Torso, Cuerpo, Interior, Medio, Exterior, Normal, Deporte, Formal, Abierto, Cama, Limpieza, Salon, Baño, Fuera, Especial
  Persona = Objeto = Pie = Piernas = Torso = Cuerpo = Interior = Medio = Exterior = Normal = Deporte = Formal = Abierto = Cama = Limpieza = Salon = Baño = Fuera = Especial = 0
  
def InitVarColor():
  global Blanco, Color
  Blanco = Color = 0

def InitVarTejido():
  global EAlgodon, Lana, Lino, Seda, Piel, ESintetico
  EAlgodon = Lana = Lino = Seda = Piel = ESintetico = 0


def InitVarTemp():
  global No_Lavar,T_Fria, T_30, T_40, T_60, T_90
  T_Fria = T_30 = T_40 = T_60 = T_90 = 0 
  No_Lavar = 0

def InitVarCentri():
  global C_Sin, C_400, C_600, C_800, C_1000, C_1200, C_1400
  C_Sin = C_400 = C_600 = C_800 = C_1000 = C_1200 = C_1400 = 0

def InitVarCiclo():
  global No_Lavar, C_Corto, C_Medio, C_Largo
  C_Corto = C_Medio = C_Largo = 0
  No_Lavar = 0


def InicializarVars():
  InitVarPrenda()
  InitVarColor()
  InitVarTejido()
  InitVarTemp()
  InitVarCentri()
  InitVarCiclo()

#Leer archivo
def LeerArchivo(dir, name, pag, inicio, fin):
  arch = dir+'/'+name
  df_0 = pd.read_excel(arch, sheet_name=pag)
  df = df_0.loc[:,inicio:fin]
  df = df.fillna('0') #Cambiar valores nan por 0

  return df



#Eliminamos las tildes
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

#Modificamos la palabra para que sean entendibles por el programa
def UpperList(Rp, op):
  Lista = []
  if op == 0: #Para lista de listas de datos
    for i in Rp:
      L = []
      [L.append(normalize(x).upper()) for x in i]
      if L[-1][-1] == 'S':
        aux = L[-1][:-1]
        L[-1] = aux
        #L = aux #No, pues añade un string y no una lista de un valor
        if L[-1][-1] == 'E':  #Quitamos tb por si termina en -es
          aux = L[-1][:-1]
          L[-1] = aux

      Lista.append(L)
  elif op == 1: #Para lista de datos
    [Lista.append(normalize(x).upper()) for x in Rp]
    if Lista[-1][-1] == 'S':
      aux = Lista[-1][:-1]
      Lista[-1] = aux
      #L = aux #No, pues añade un string y no una lista de un valor
      if Lista[-1][-1] == 'E':  #Quitamos tb por si termina en -es
        aux = Lista[-1][:-1]
        Lista[-1] = aux
  elif op == 2:   #Para DataFrame
    for i in range(len(Rp)):
      aux = []
      for x in Rp.loc[i]:
        x2 = normalize(x).upper()
        x_add = x2
        if x2[-1] == 'S':
          x3 = x2[:-1]
          x_add = x3
          if x3[-1] == 'E':
            x4 = x3[:-1]
            x_add = x4

        aux.append(x_add)
      Lista.append(aux)

   
    
  return Lista





#Segun el nombre de la prenda le asignamos unos valores a las neuronas de entrada
def AsignacionTipoRopa(dato):
  global Persona, Objeto, Pie, Piernas, Torso, Cuerpo, Interior, Medio, Exterior, Normal, Deporte, Formal, Abierto, Cama, Limpieza, Salon, Baño, Fuera, Especial
  if dato == 'CALCETIN':
    Persona = Pie = Interior = Normal = 1
  elif dato == 'CALZONCILLO' or dato == 'BRAGA' or dato == 'TANGA':
    Persona = Piernas = Interior = Normal = 1
  elif dato == 'SUJETADOR':
    Persona = Cuerpo = Interior = Normal = 1
  elif dato == 'TOP':
    Persona = Cuerpo = Medio = Deporte = 1
  elif dato == 'PANTALON'  or dato == 'VAQUERO' or dato == 'CHINO':
    Persona = Piernas = Exterior = Normal = 1
  elif dato == 'CALZONA':
    Persona = Piernas = Medio = Deporte = 1
  elif dato == 'LEGGING' or dato == 'MAYA':
    Persona = Piernas = Exterior = Deporte = 1
  elif dato == 'LEOTARDO' or dato == 'MEDIAS':
    Persona = Piernas = Medio = Normal = 1
  elif dato == 'FALDA':
    Persona = Piernas = Exterior = Formal = Abierto = 1
  elif dato == 'VESTIDO' or dato == 'MONO':
    Persona = Cuerpo = Medio = Formal = Abierto = 1
  elif dato == 'CAMISA' or dato == 'BLUSA':
    Persona = Torso = Medio = Formal = Abierto = 1
  elif dato == 'POLO':
    Persona = Torso = Medio = Formal = 1
  elif dato == 'CAMISETA':
    Persona = Torso = Medio = Normal = 1
  elif dato == 'CHALECO' or dato == 'JERSEY' or dato == 'REBECA' or dato == 'CARDIGAN':
    Persona = Torso = Exterior = Formal = 1
  elif dato == 'SUDADERA':
    Persona = Torso = Exterior = Normal = 1
  elif dato == 'CORTAVIENTO':
    Persona = Torso = Exterior = Deporte = 1 #Lo que cogemos para salir a correr, no se si quitarlo
  elif dato == 'PIJAMA':
    Persona = Piernas = Torso = Medio = Normal = Cama = 1
  elif dato == 'BATA':
    Persona = Cuerpo = Exterior = Normal = Cama = 1
  elif dato == 'BAÑADOR' or dato == 'BIKINI':
    Persona = Piernas = Torso = Cuerpo = Medio = Normal = 1
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
    Persona = Torso = Exterior = Formal = Abierto = Especial = 1
  #else prenda no reconocida





#Segun el color encontrado determina que hacer, POCO trabajado, no se como separar colores pasteles de oscuros y de vivos
def AsignacionColorRopa(dato):
  global Blanco, Color
  if dato == 'BLANCO':
    Blanco = 1
    Color = 0
  else:
    Color = 1


#Pasaremos dos lista de 3 o 4 dimensiones en el que diremos que material esta compuesto
# y la otra con su porcentaje
def AsignacionTejidoRopa(ListaTejido, ListaValores):  
  global EAlgodon, Lana, Lino, Seda, Piel, ESintetico
  for i in range(len(ListaTejido)):
    if ListaTejido[i] == 'ALGODON':
      EAlgodon = 1#int(ListaValores[i])/100
    elif ListaTejido[i] == 'LANA':
      Lana = 1#int(ListaValores[i])/100
    elif ListaTejido[i] == 'LINO':
      Lino = 1#int(ListaValores[i])/100
    elif ListaTejido[i] == 'SEDA':
      Seda = 1#int(ListaValores[i])/100
    elif ListaTejido[i] == 'PIEL' or ListaTejido[i] == 'CUERO':
      #Piel += int(ListaValores[i])/100
      Piel = 1
    else:
      ESintetico = 1
      #ESintetico += int(ListaValores[i])/100



def AsignacionTemperatura(dato):
  global T_Fria, T_30, T_40, T_60, T_90
  if dato == 0:
    T_Fria = 1
  elif dato == 30:
    T_30 = 1
  elif dato == 40:
    T_40 = 1
  elif dato == 60:
    T_60 = 1
  elif dato == 90:
    T_90 = 1
  else:
    No_Lavar = 1


def AsignacionCiclo(dato):
  global C_Corto, C_Medio, C_Largo
  if dato == 'CORTO':
    C_Corto = 1
  elif dato == 'MEDIO' or dato == 'NORMAL':
    C_Medio = 1
  elif dato == 'LARGO':
    C_Largo = 1
  else: 
    No_Lavar = 1

def AsignacionCentrifugado(dato):
  global C_Sin, C_400, C_600, C_800, C_1000, C_1200, C_1400
  if dato == 0:
    C_Sin = 1
  elif dato == 400:
    C_400 = 1
  elif dato == 600:
    C_600 = 1
  elif dato == 800:
    C_800 = 1
  elif dato == 1000:
    C_1000 = 1
  elif dato == 1200:
    C:1200 = 1
  elif dato == 1400:
    C_1400 = 1
  #else:
  #  No_Lavar = 1


def UnirSalida(entrada, blanco, color, salida):
  L = []
  for r in entrada:
    [L.append(x) for x in r]
  L.append(blanco)
  L.append(color)
  for r in salida:
    [L.append(x) for x in r]
  return L

#Ponemos todos los datos en mayuscula, en singular y sin caracteres especiales
def LimpiarDatos(df):
  
  Id = df['Id']
  NomRopa = UpperList(df['Nombre'],1)
  ColRopa = UpperList(df['Color'],1)
  TejRopa = UpperList(df.loc[:,'Tejido 1':'Tejido 3'], 2)
  ValoresTej = df.loc[:,'Porciento T1':'Porciento T3'].values
  Temp = df['Temperatura']
  Cent = df['Centrifugado']
  CicloLav = UpperList(df['Ciclo'],1)

  return Id, NomRopa, ColRopa, TejRopa, ValoresTej, Temp, Cent, CicloLav

#           ----------------------------------------------
#          |   CONVERTIR LOS DATOS TRATADOS EN NEURONAS   |
#           ----------------------------------------------



def NeuronasEntrada(Id,Rp, C, T, NumT):
  lista = [(0, Persona, Objeto, Pie, Piernas, Torso, Cuerpo, Interior, Medio, Exterior, Normal, Deporte, Formal, Abierto, Cama, Limpieza, Salon, Baño, Fuera, Especial, Blanco, Color, EAlgodon, Lana, Lino, Seda, Piel, ESintetico)]
  Entrada = pd.DataFrame(lista,
                         columns=['Id','Persona', 'Objeto', 'Pie', 'Piernas', 'Torso', 'Cuerpo', 'Interior', 'Medio', 'Exterior', 'Normal', 'Deporte', 'Formal', 'Abierto', 'Cama', 'Limpieza', 'Salon', 'Baño', 'Fuera', 'Especial', 'Blanco', 'Color', 'EAlgodon', 'Lana', 'Lino', 'Seda', 'Piel', 'ESintetico'])
 
  for i in range(len(Rp)):
    InitVarPrenda()
    InitVarColor()
    InitVarTejido()
    AsignacionTipoRopa(Rp[i])
    AsignacionColorRopa(C[i])
    AsignacionTejidoRopa(T[i],NumT[i])
    Entrada.loc[i] = [Id[i],Persona, Objeto, Pie, Piernas, Torso, Cuerpo, Interior, Medio, Exterior, Normal, Deporte, Formal, Abierto, Cama, Limpieza, Salon, Baño, Fuera, Especial, Blanco, Color, EAlgodon, Lana, Lino, Seda, Piel, ESintetico]
  
  return Entrada



def NeuronasSalidaTemp(Id,Temperatura):
  InitVarTemp()
  lista = [(0,No_Lavar,T_Fria, T_30, T_40, T_60, T_90)]
  Salida = pd.DataFrame(lista,
                        columns = ['Id','LavarT','T_Fria', 'T_30', 'T_40', 'T_60', 'T_90'])

  contador = 0
  for i in Temperatura:
    InitVarTemp()
    AsignacionTemperatura(i)
    Salida.loc[contador] = [Id[contador],No_Lavar,T_Fria, T_30, T_40, T_60, T_90]
    contador += 1

  return Salida



def NeuronasSalidaCentri(Id,Centrifugado):
  lista = [(0,C_Sin, C_400, C_600, C_800, C_1000, C_1200, C_1400)]
  Salida = pd.DataFrame(lista,
                        columns = ['Id','C_Sin', 'C_400', 'C_600', 'C_800', 'C_1000', 'C_1200', 'C_1400'])

  contador = 0
  for i in Centrifugado:
    InitVarCentri()
    AsignacionCentrifugado(i)
    Salida.loc[contador] = [Id[contador],C_Sin, C_400, C_600, C_800, C_1000, C_1200, C_1400]
    contador += 1

  return Salida


def NeuronasSalidaCiclo(Id,Ciclo):
  lista = [(0, No_Lavar, C_Corto, C_Medio, C_Largo)]
  Salida = pd.DataFrame(lista,
                        columns=['Id', 'LavarC', 'C_Corto', 'C_Medio', 'C_Largo'])
  contador = 0
  for i in Ciclo:
    InitVarCiclo()
    AsignacionCiclo(i)
    Salida.loc[contador] =[Id[contador], No_Lavar, C_Corto, C_Medio, C_Largo]
    contador+=1

  return Salida



def ObtenerDataFrame(Id, NomRopa,ColRopa,TejRopa,TejNum, Temp, Cent, CicloLav):
  P = NeuronasEntrada(Id,NomRopa,ColRopa,TejRopa,TejNum)
  T = NeuronasSalidaTemp(Id,Temp)
  SaCentri = NeuronasSalidaCentri(Id,Cent)
  SaC = NeuronasSalidaCiclo(Id,CicloLav)
  #Fusionar
  #https://www.analyticslane.com/2018/09/10/unir-y-combinar-dataframes-con-pandas-en-python/
  #https://www.delftstack.com/es/howto/python-pandas/how-to-add-one-row-to-pandas-dataframe/
  Completo1 = pd.merge(P,T, on='Id')
  Completo2 = pd.merge(SaCentri, SaC, on='Id')
  Completo = pd.merge(Completo1,Completo2, on='Id')

  return Completo


#Dado la direccion del archivo devuelve el dataset ya tratado
def CargarDataSet(direccion, archivo, pagina):
  ini = 'Id'
  fin = 'Ciclo'
  df = LeerArchivo(direccion, archivo, pagina, ini, fin)
  Id, NomRopa, ColorRopa, TejRopa, NumTej, TempLav, CentriLav, CicloLav = LimpiarDatos(df)
  DataSet = ObtenerDataFrame(Id, NomRopa, ColorRopa, TejRopa, NumTej, TempLav, CentriLav, CicloLav)
  #DataSet = ObtenerDataFrame(LimpiarDatos(df))

  return DataSet

#Dado el dataset y la porcion deseada, devide en train & test
def train_test_split_Final(DataSet, grupo):
  parte = int(len(DataSet)/grupo)
  train = DataSet[:-parte]
  test = DataSet.tail(parte)

  return train,test

#Dado el train y el test, divide entre X e Y
def train_test_split_Inicio(DataSet_train, DataSet_test, iniEntrada, finEntrada, iniSalida, finSalida):
  train_x = DataSet_train.loc[:,iniEntrada:finEntrada]
  train_y = DataSet_train.loc[:,iniSalida:finSalida]
  test_x = DataSet_test.loc[:,iniEntrada:finEntrada]
  test_y = DataSet_test.loc[:,iniSalida:finSalida]

  return train_x, train_y, test_x, test_y

#Dado el dataset de entrenamiento y las variables necesarias entrena la red neuronal
def Entrenamiento(X_train, Y_train, capasIntermedias, delta, epocas, Xtest, Ytest):
  oculta1 = tf.keras.layers.Dense(units=capasIntermedias, input_shape=[len(X_train.columns)], name='Oculta1')
  oculta2 = tf.keras.layers.Dense(units=capasIntermedias, name='Oculta2')
  salida = tf.keras.layers.Dense(units=len(Y_train.columns))
  modelo = tf.keras.Sequential([oculta1, oculta2,salida])
  #https://stackoverflow.com/questions/43589842/test-score-vs-test-accuracy-when-evaluating-model-using-keras
  modelo.compile(
    optimizer = tf.keras.optimizers.Adam(delta),
    loss = 'mean_squared_error'
    ,metrics=['acc', 'mse']
    #,metrics=['acc', 'mse', 'val_loss', 'val_acc']
    #,metrics=[tf.keras.metrics.SparseCategoricalAccuracy()]
    #metrics=["sparse_categorical_accuracy"]
  )
  historial = modelo.fit(X_train, Y_train, epochs=epocas, verbose=False, validation_data=(Xtest,Ytest))
  return modelo, historial, oculta1, oculta2


def TratamientoRopa(dato):
  #print('TratamientoRopa --> ', dato)
  #dato2 = [dato]
  p = UpperList(dato,1)
  #print('TratamientoRopa --> ', p)
  InicializarVars()
  AsignacionTipoRopa(p[0])
  prenda = [[Persona, Objeto, Pie, Piernas, Torso, Cuerpo, Interior, Medio, Exterior, Normal, Deporte, Formal, Abierto, Cama, Limpieza, Salon, Baño, Fuera, Especial]]
  return prenda


#Dado un valor y un modelo, devuelve la prediccion del modelo
def PrediccionRed(dato, modelo):
  resultado = modelo.predict(dato)
  return resultado


def Prediccion(dato, modeloTej, modeloTemp, modeloCentri, modeloCiclo):
  prenda = TratamientoRopa(dato)
  tejido = PrediccionRed(prenda, modeloTej)
  #entrada1 = UnirSalida(prenda, Blanco, Color, tejido)
  entrada1 = UnirSalida(prenda, 1, 0, tejido) #Unimos la prenda con su color y tejido
  entrada2 = UnirSalida(prenda, 0, 1, tejido) #Unimos la prenda con su color y tejido

  opTemp = ['No Lavar', 'T_Fria', 'T_30', 'T_40', 'T_60', 'T_90']
  temp1 = PrediccionRed(entrada1, modeloTemp)
  temp2 = PrediccionRed(entrada2, modeloTemp)
  opCentri = ['C_Sin', 'C_400', 'C_600', 'C_800', 'C_1000', 'C_1200', 'C_1400']
  centri1 = PrediccionRed(entrada1, modeloCentri)
  centri2 = PrediccionRed(entrada2, modeloCentri)
  opCiclo = ['No Lavar', 'C_Corto', 'C_Medio', 'C_Largo']
  ciclo1 = PrediccionRed(entrada1, modeloCiclo)
  ciclo2 = PrediccionRed(entrada2, modeloCiclo)

#Cargar y separar datos
def Cargar(dir, name, hoja):
  df = CargarDataSet(dir,name, hoja)
  #Dividir en train & test
  df_shuffle = sklearn.utils.shuffle(df)#Reordenarlo de manera aleatoria
  train,test = train_test_split_Final(df, 5)#20% de test, 80% de entrenamiento
  return train, test

def MainEntrenar(train, test, capasIntermedias, delta, epocas):
  #df = CargarDataSet(dir,name, hoja)
  #Dividir en train & test
  #df_shuffle = sklearn.utils.shuffle(df)#Reordenarlo de manera aleatoria
  #train,test = train_test_split_Final(df, 5)#20% de test, 80% de entrenamiento
  #Redes Neuronales
  
  #   Primera, segun la ropa determina cual es su composicion
  X_train_1, Y_train_1, X_test_1, Y_test_1 = train_test_split_Inicio(train, test, 'Persona', 'Especial', 'EAlgodon', 'ESintetico')
  modelo1, h1, oculta1_1, oculta2_1 = Entrenamiento(X_train_1, Y_train_1, capasIntermedias, delta, epocas,X_test_1, Y_test_1)

  
  score1 = modelo1.evaluate(X_test_1, Y_test_1)
  print('Score de red entrenada del Tejido: ', score1, ' - Con ', X_test_1.shape[1], ' neuronas de entrada y ', Y_test_1.shape[1], ' neuronas de salida')

  msg = 'Red de Tejido con 2 capas ocultas con ' + str(capasIntermedias) + ' neuronas cada una'
  plt.figure()
  plt.title(msg)
  plt.xlabel("# Epoca")
  plt.ylabel("Evolucion")
  plt.plot(h1.history["loss"])
  plt.plot(h1.history["acc"])
  plt.plot(h1.history["val_acc"])
  plt.plot(h1.history["val_loss"])
  plt.legend(['Loss', 'Accuracy', 'Val_Acc', 'Val_Loss'])

  #   Segunda, dada la prenda el color y su composicion, determina su Temperatura
  X_train_2, Y_train_2, X_test_2, Y_test_2 = train_test_split_Inicio(train, train, 'Persona', 'ESintetico', 'LavarT', 'T_90')
  modelo2, h2, oculta1_2, oculta2_2 = Entrenamiento(X_train_2, Y_train_2, capasIntermedias, delta, epocas,X_test_2, Y_test_2)
  
  score2 = modelo2.evaluate(X_test_2, Y_test_2)
  #verbose=0, es que no se vea el progreso
  print('Score de red entrenada de la Temperatura: ', score2, ' - Con ', X_test_2.shape[1], ' neuronas de entrada y ', Y_test_2.shape[1], ' neuronas de salida')

  msg = 'Red de Temperatura con 2 capas ocultas con ' + str(capasIntermedias) + ' neuronas cada una'
  plt.figure()
  plt.title(msg)
  plt.xlabel("# Epoca")
  plt.ylabel("Evolucion")
  plt.plot(h2.history["loss"])
  plt.plot(h2.history["acc"])
  plt.plot(h2.history["val_acc"])
  plt.plot(h2.history["val_loss"])
  plt.legend(['Loss', 'Accuracy', 'Val_Acc', 'Val_Loss'])

  #   Tercera, dada la prenda el color y su composicion, determina su Centrifugado
  X_train_3, Y_train_3, X_test_3, Y_test_3 = train_test_split_Inicio(train, train, 'Persona', 'ESintetico', 'C_Sin', 'C_1400')
  modelo3, h3, oculta1_3, oculta2_3 = Entrenamiento(X_train_3, Y_train_3, capasIntermedias, delta, epocas,X_test_3, Y_test_3)

  score3 = modelo3.evaluate(X_test_3, Y_test_3)
  print('Score de red entrenada del Centrifugado: ', score3, ' - Con ', X_test_3.shape[1], ' neuronas de entrada y ', Y_test_3.shape[1], ' neuronas de salida')

  msg = 'Red de Centrifugado con 2 capas ocultas con ' + str(capasIntermedias) + ' neuronas cada una'
  plt.figure()
  plt.title(msg)
  plt.xlabel("# Epoca")
  plt.ylabel("Evolucion")
  plt.plot(h3.history["loss"])
  plt.plot(h3.history["acc"])
  plt.plot(h3.history["val_acc"])
  plt.plot(h3.history["val_loss"])
  plt.legend(['Loss', 'Accuracy', 'Val_Acc', 'Val_Loss'])
  
  #   Cuarta, dada la prenda el color y su composicion, determina su Ciclo
  X_train_4, Y_train_4, X_test_4, Y_test_4 = train_test_split_Inicio(train, train, 'Persona', 'ESintetico', 'LavarC', 'C_Largo')
  modelo4, h4, oculta1_4, oculta2_4 = Entrenamiento(X_train_4, Y_train_4, capasIntermedias, delta, epocas,X_test_4, Y_test_4)

  score4 = modelo4.evaluate(X_test_4, Y_test_4)
  print('Score de red entrenada del Ciclo: ', score4, ' - Con ', X_test_4.shape[1], ' neuronas de entrada y ', Y_test_4.shape[1], ' neuronas de salida')
  #print('Cuyas conexiones tienen un peso de:')
  #print('Oculta1: ', oculta1_4.gethei)

  msg = 'Red de Ciclo con 2 capas ocultas con ' + str(capasIntermedias) + ' neuronas cada una'
  plt.figure()
  plt.title(msg)
  plt.xlabel("# Epoca")
  plt.ylabel("Evolucion")
  plt.plot(h4.history["loss"])
  plt.plot(h4.history["acc"])
  plt.plot(h4.history["val_acc"])
  plt.plot(h4.history["val_loss"])
  plt.legend(['Loss', 'Accuracy', 'Val_Acc', 'Val_Loss'])
  

  return (modelo1, h1, oculta1_1, oculta2_1), (modelo2, h2, oculta1_2, oculta2_2), (modelo3, h3, oculta1_3, oculta2_3), (modelo4, h4, oculta1_4, oculta2_4)

#   ENTRENAMOS REDES
tiempo = 5
delta = 0.1
epocas = 500
#Cargo los datos y separo train de test
print('                    -----------------------------------------------------------------')
print('                               CANTIDAD DE ELEMENTOS ESTUDIADOS')
print('                    -----------------------------------------------------------------')
train, test = Cargar('Dato','AppDatos.xlsx', 'Datos')
print('Estudiamos ',train.shape[0], ' elementos')
print('Evaluamos con ',test.shape[0], ' elementos')
print('Realizamos ',epocas, ' epocas')
print('Con un factor de aprendizaje de ',delta, ' (delta)')
print(' ')
# 'Dato','AppDatos.xlsx', 'Datos'
print('                    -----------------------------------------------------------------')
print('                               REDES NEURONALES ENTRENADAS')
print('                    -----------------------------------------------------------------')
capasIntermedias = 5
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes5 = MainEntrenar(train, test, capasIntermedias, delta, epocas)
time.sleep(tiempo) #Descansamos los segundos deseados
capasIntermedias = 10
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes10 = MainEntrenar(train, test, capasIntermedias, delta, epocas)
time.sleep(tiempo)
capasIntermedias = 15
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes15 = MainEntrenar(train, test, capasIntermedias, delta, epocas)
time.sleep(tiempo)  #NO sirve para que dibuje los plots entre cada analisis...
capasIntermedias = 20
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes20 = MainEntrenar(train, test, capasIntermedias, delta, epocas)

init = 'RNN_'
it_red = str(epocas)
extension = '.h5'
n = str(5)
print(init+'Tejido_'+it_red+'_'+n+extension)

#test.iloc[:,20:28]

# GUARDAR REDES
#Guardo las redes en formato para luego porder leerla en pycharm, pkl no sirve
  #5 neuronas en capas intermedias
joblib.dump(redes5[0][0], init+'Tejido_'+it_red+'_'+n+extension)
joblib.dump(redes5[1][0], init+'Temp_'+it_red+'_'+n+extension)
joblib.dump(redes5[2][0], init+'Centri_'+it_red+'_'+n+extension)
joblib.dump(redes5[3][0], init+'Ciclo_'+it_red+'_'+n+extension)
  #10 neuronas en capas intermedias
n = str(10) 
joblib.dump(redes10[0][0], init+'Tejido_'+it_red+'_'+n+extension)
joblib.dump(redes10[1][0], init+'Temp_'+it_red+'_'+n+extension)
joblib.dump(redes10[2][0], init+'Centri_'+it_red+'_'+n+extension)
joblib.dump(redes10[3][0], init+'Ciclo_'+it_red+'_'+n+extension)
  #15 neuronas en capas intermedias
n = str(15)
joblib.dump(redes15[0][0], init+'Tejido_'+it_red+'_'+n+extension)
joblib.dump(redes15[1][0], init+'Temp_'+it_red+'_'+n+extension)
joblib.dump(redes15[2][0], init+'Centri_'+it_red+'_'+n+extension)
joblib.dump(redes15[3][0], init+'Ciclo_'+it_red+'_'+n+extension)
  #20 neuronas en capas intermedias
n = str(20)
joblib.dump(redes20[0][0], init+'Tejido_'+it_red+'_'+n+extension)
joblib.dump(redes20[1][0], init+'Temp_'+it_red+'_'+n+extension)
joblib.dump(redes20[2][0], init+'Centri_'+it_red+'_'+n+extension)
joblib.dump(redes20[3][0], init+'Ciclo_'+it_red+'_'+n+extension)

# -----------------------------------------------------
#               COMPROBAR REDES Y COSAS
# -----------------------------------------------------

def ComprobarTejido(p, modelo):
  prenda = p
  InicializarVars()
  prueba = TratamientoRopa(prenda)
  resultado = modelo.predict(prueba)
  return prenda, resultado, prueba

def SiguienteRed(prenda, blanco, color, tejido):
   return UnirSalida(prenda, blanco, color, tejido)

#PrediccionRed(entrada, modelo)

#Devuelve la posicion del dato mayor
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
    a = Elegir_Min(L)
    return a

#-----------------------------------
#  COMPROBAR EFICIENCIA REAL
#-------------------------------------

prenda_op = ['camisa', 'camiseta', 'chaleco', 'sudadera', 'calzoncillo', 'chaqueta', 'vaquero', 'sabana', 'traje', 'error']
indice = 8
prenda = [prenda_op[indice]]
m = redes20         #Modelo
m_tej = m[0][0] 
m_temp = m[1][0]
m_centri = m[2][0]
m_ciclo = m[3][0]
b = 1 #Blanco
c = 0 #Color
introducido, tejido, entrada = ComprobarTejido(prenda, m_tej)
print('Prenda: ', prenda)
print(' EAlgodon  -     Lana     -      Lino     -      Seda     -      Piel      -  ESintetico')
print(tejido)
Entrada_SigRed = [UnirSalida(entrada, b, c, tejido)]

V_Temperatura = ['No Lavar', 'Fria', '30', '40', '60', '90']
V_Centrifugado = ['Sin', '400', '600', '800', '1000', '1200', '1400']
V_Ciclo = ['No Lavar', 'Corto', 'Medio', 'Largo']
S_Temperatura = PrediccionRed(Entrada_SigRed, m_temp)
S_Centrifugado = PrediccionRed(Entrada_SigRed, m_centri)
S_Ciclo = PrediccionRed(Entrada_SigRed, m_ciclo)
E_temp = Analisis(S_Temperatura)
E_centri = Analisis(S_Centrifugado)
E_ciclo = Analisis(S_Ciclo)
print(E_temp, ' - ', E_centri, ' - ', E_ciclo)
print('Temperatura: ', V_Temperatura[E_temp])
print('Centrifugado: ', V_Centrifugado[E_centri])
print('Ciclo: ', V_Ciclo[E_ciclo])





#-----------------------------------------------------------------------------------------------------------



#   ENTRENAMOS REDES
tiempo = 5
delta = 0.1
epocas = 100
#Cargo los datos y separo train de test
print('                    -----------------------------------------------------------------')
print('                               CANTIDAD DE ELEMENTOS ESTUDIADOS')
print('                    -----------------------------------------------------------------')
train, test = Cargar('Dato','AppDatos.xlsx', 'Datos')
print('Estudiamos ',train.shape[0], ' elementos')
print('Evaluamos con ',test.shape[0], ' elementos')
print('Realizamos ',epocas, ' epocas')
print('Con un factor de aprendizaje de ',delta, ' (delta)')
print(' ')
# 'Dato','AppDatos.xlsx', 'Datos'
print('                    -----------------------------------------------------------------')
print('                               REDES NEURONALES ENTRENADAS')
print('                    -----------------------------------------------------------------')
capasIntermedias = 5
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes5 = MainEntrenar(train, test, capasIntermedias, delta, epocas)
time.sleep(tiempo) #Descansamos los segundos deseados
capasIntermedias = 10
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes10 = MainEntrenar(train, test, capasIntermedias, delta, epocas)
time.sleep(tiempo)
capasIntermedias = 15
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes15 = MainEntrenar(train, test, capasIntermedias, delta, epocas)
time.sleep(tiempo)  #NO sirve para que dibuje los plots entre cada analisis...
capasIntermedias = 20
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes20 = MainEntrenar(train, test, capasIntermedias, delta, epocas)





#   ENTRENAMOS REDES
tiempo = 5
delta = 0.1
epocas = 1000
#Cargo los datos y separo train de test
print('                    -----------------------------------------------------------------')
print('                               CANTIDAD DE ELEMENTOS ESTUDIADOS')
print('                    -----------------------------------------------------------------')
train, test = Cargar('Dato','AppDatos.xlsx', 'Datos')
print('Estudiamos ',train.shape[0], ' elementos')
print('Evaluamos con ',test.shape[0], ' elementos')
print('Realizamos ',epocas, ' epocas')
print('Con un factor de aprendizaje de ',delta, ' (delta)')
print(' ')
# 'Dato','AppDatos.xlsx', 'Datos'
print('                    -----------------------------------------------------------------')
print('                               REDES NEURONALES ENTRENADAS')
print('                    -----------------------------------------------------------------')
capasIntermedias = 5
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes5 = MainEntrenar(train, test, capasIntermedias, delta, epocas)
time.sleep(tiempo) #Descansamos los segundos deseados
capasIntermedias = 10
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes10 = MainEntrenar(train, test, capasIntermedias, delta, epocas)
time.sleep(tiempo)
capasIntermedias = 15
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes15 = MainEntrenar(train, test, capasIntermedias, delta, epocas)
time.sleep(tiempo)  #NO sirve para que dibuje los plots entre cada analisis...
capasIntermedias = 20
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes20 = MainEntrenar(train, test, capasIntermedias, delta, epocas)







#   ENTRENAMOS REDES
tiempo = 5
delta = 0.1
epocas = 2000
#Cargo los datos y separo train de test
print('                    -----------------------------------------------------------------')
print('                               CANTIDAD DE ELEMENTOS ESTUDIADOS')
print('                    -----------------------------------------------------------------')
train, test = Cargar('Dato','AppDatos.xlsx', 'Datos')
print('Estudiamos ',train.shape[0], ' elementos')
print('Evaluamos con ',test.shape[0], ' elementos')
print('Realizamos ',epocas, ' epocas')
print('Con un factor de aprendizaje de ',delta, ' (delta)')
print(' ')
# 'Dato','AppDatos.xlsx', 'Datos'
print('                    -----------------------------------------------------------------')
print('                               REDES NEURONALES ENTRENADAS')
print('                    -----------------------------------------------------------------')
capasIntermedias = 5
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes5 = MainEntrenar(train, test, capasIntermedias, delta, epocas)
time.sleep(tiempo) #Descansamos los segundos deseados
capasIntermedias = 10
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes10 = MainEntrenar(train, test, capasIntermedias, delta, epocas)
time.sleep(tiempo)
capasIntermedias = 15
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes15 = MainEntrenar(train, test, capasIntermedias, delta, epocas)
time.sleep(tiempo)  #NO sirve para que dibuje los plots entre cada analisis...
capasIntermedias = 20
print('-----------------------------------------------------------------')
print('        Tiene ',capasIntermedias, ' neuronas en cada capa oculta')
print('-----------------------------------------------------------------')
redes20 = MainEntrenar(train, test, capasIntermedias, delta, epocas)





















#Cargar las redes YA ENTRENADAS
  #5 neuronas en capas intermedias
joblib.load('RNN_Tejido_5.h5')
joblib.load('RNN_Temp_5.h5')
joblib.load('RNN_Centri_5.h5')
joblib.load('RNN_Ciclo_5.h5')
  #10 neuronas en capas intermedias
joblib.load('RNN_Tejido_10.h5')
joblib.load('RNN_Temp_10.h5')
joblib.load('RNN_Centri_10.h5')
joblib.load('RNN_Ciclo_10.h5')
  #15 neuronas en capas intermedias
joblib.load('RNN_Tejido_15.h5')
joblib.load('RNN_Temp_15.h5')
joblib.load('RNN_Centri_15.h5')
joblib.load('RNN_Ciclo_15.h5')
  #20 neuronas en capas intermedias
joblib.load('RNN_Tejido_20.h5')
joblib.load('RNN_Temp_20.h5')
joblib.load('RNN_Centri_20.h5')
joblib.load('RNN_Ciclo_20.h5')