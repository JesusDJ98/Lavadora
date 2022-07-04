import kivy
from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.switch import Switch

#from kivymd.uix.datatables import MDDataTable
#from kivy.metrics import dp #Separacion de la tabla
#from kivy.lang import Builder
from kivymd.app import MDApp

#from table import Table #No se como usarlo

#Para las redes
#import tensorflow as tf
#import numpy as np
#from keras.models import load_model

kivy.require('1.9.0')

import Funciones.Funciones_Red as red

class prueba(Screen):
    nombre = 'Ha'
    v2 = ObjectProperty(None)
    def cambiar(self):
        print('Prueba cambiar')
        print(self.v2.text)

#-------------------------------------------------------
#               PANTALLA DE DETERGENTE
#-------------------------------------------------------
class ScreenDetergente(Screen):
    def Limpiar(self):
        TheLabApp.Lista_Ropa_Insertada = ''
        TheLabApp.Lista_Ropa_Tratada = []
        TheLabApp.Dic_Tejido = dict()
        TheLabApp.Dic_Ropa_Red = dict()
        TheLabApp.Blanco = False
        TheLabApp.Color = False
        TheLabApp.modeloTejido = 0
        TheLabApp.modeloTemp = 0
        TheLabApp.modeloCentri = 0
        TheLabApp.modeloCiclo = 0
        TheLabApp.TemperaturaElegida = ''
        TheLabApp.CentrifugadoElegida = ''
        TheLabApp.CicloElegida = ''
        TheLabApp.colores = ''
        TheLabApp.Prelavado = False
        TheLabApp.Programa = ''
        TheLabApp.Lavar = True

#-------------------------------------------------------
#               PANTALLA DE SALIDA
#-------------------------------------------------------
class ScreenSalida(Screen):
    def on_enter(self, *args):
        #print('------------------------------')
        #print('Entro en ScreenSalida')
        #print('Blanco: ', TheLabApp.Blanco, ' - Color: ', TheLabApp.Color, ' - Lavar: ', TheLabApp.Lavar)
        self.ids.SColor.text = str(TheLabApp.colores)
        if TheLabApp.Lavar:
            self.ids.SalidaLavar.text = str('')
        else:
            self.ids.SalidaLavar.text = str('Hay Prendas que NO se deben LAVAR')
        if TheLabApp.Color and TheLabApp.Blanco:
            self.ids.SalidaLavar.text = str('Se recomienda SEPARAR por color')
        else:
            self.ids.SalidaLavar.text = ''

        if TheLabApp.Prelavado:
            self.ids.SPrelavado.text = 'Si'
        else:
            self.ids.SPrelavado.text = 'No'
        self.ids.SPrograma.text = str(TheLabApp.Programa)
        self.ids.STemperatura.text = str(TheLabApp.TemperaturaElegida)
        self.ids.SCentrifugado.text = str(TheLabApp.CentrifugadoElegida)
        self.ids.SCiclo.text = str(TheLabApp.CicloElegida)






#-------------------------------------------------------
#               PANTALLA DE EDITAR TEJIDOS
#-------------------------------------------------------
class ScreenTejido(Screen):
    Cabecera = ['Ropa', 'Algodon', 'Lino', 'Lana', 'Seda', 'Cuero', 'Sintetico']
    #def RediseñarGrid(self):
    def __init__(self, **kwargs):  #Esto es al inicio
        super(ScreenTejido, self).__init__(**kwargs)
        for i in self.Cabecera:
            b = Label(text=str(i), size_hint_y=None, height=30, color=(0,0,0,1))
            self.ids.cabecera.add_widget(b)

    def on_enter(self, *args):
        self.LimpiarGrid()
        for key in TheLabApp.Dic_Tejido:  #Aqui recorre las key
            b = Label(text=str(key), size_hint_y=None, height=30, color=(0, 0, 0, 1))
            self.ids.scroll_grid.add_widget(b)
            for j in TheLabApp.Dic_Tejido[key]:
                #r = round(j, 4)
                #   SI QUEREMOS QUE DEVUELVE LA SALIDA
                #   O 0 Y 1 SI ESTA ACTIVADO (>0.20)
                b = TextInput(text=str(j), size_hint_y=None, height=30, halign='center', font_size='12sp')
                self.ids.scroll_grid.add_widget(b)

    def LimpiarGrid(self):
        for child in [child for child in self.ids.scroll_grid.children]:
            self.ids.scroll_grid.remove_widget(child)

    def Continuar(self, instance, modeloT, modeloCe, modeloCi):
        self.ActualizarTejidos(instance)
        self.Predecir(modeloT, modeloCe, modeloCi)

    def ActualizarTejidos(self, instance):
        cnt = 0
        #print('Antiguo Diccionario: ',TheLabApp.Dic_Tejido)
        a = instance.children[::-1]
        ciclo = 0
        lista = []
        key = ''
        dic_aux = dict()
        for child in a:
            if ciclo == 0:
                #Actualizamos
                key = str(child.text)
                lista = TheLabApp.Dic_Tejido[str(child.text)]
            else:
                a = 0
                if child.text.isdigit():
                    aux = int(child.text)
                    if aux > 1:
                        a = 1
                    else:
                        a = aux
                else:
                    try:
                        aux = int(float(child.text))
                        if aux > 1:
                            a = 1
                        else:
                            a = aux
                    except:
                        a = 0
                lista[ciclo - 1] = a
            if ciclo == 6:#Termina con el elemento y lo añadimos
                dic_aux[str(key)] = lista
            cnt += 1
            ciclo = cnt % 7
        TheLabApp.Dic_Tejido = dic_aux

    def Predecir(self, mTemp, mCentri, mCiclo):
        #print('Neuronas: ', TheLabApp.Lista_Ropa_Red)
        #print('Tejidos: ', TheLabApp.Dic_Tejido)
        #print('Dicc Neuronas: ', TheLabApp.Dic_Ropa_Red)
        temperatura = ['No Lavar', 'Fria', '30', '40', '60', '90']
        centrifugado = ['Sin', '400', '600', '800', '1000', '1200', '1400']
        ciclo = ['No lavar', 'Corto', 'Normal', 'Largo']
        Entradas = []
        b = 0
        c = 0
        if TheLabApp.Blanco:
            TheLabApp.colores = 'Blanco'
            b = 1
        if TheLabApp.Color:
            TheLabApp.colores = 'Color'
            c = 1
        if b and c:
            TheLabApp.colores = 'Ambos'
        elif not b and not c:
            TheLabApp.colores = 'Desconocido'
        for key in TheLabApp.Dic_Tejido:
            salida = TheLabApp.Dic_Tejido[str(key)]
            tejido = TheLabApp.Dic_Ropa_Red[str(key)]
            Entrada = red.Convertir_Neurona(tejido, b, c, salida)
            Entradas.append(Entrada)
            #predi_T = red.Ejecutar_modelo(mTemp, [Entrada])
        #print('Mis Neuronas de ENTRADA: ', Entradas)
        temp = red.Ejecutar_modelo(mTemp, Entradas)
        centri = red.Ejecutar_modelo(mCentri, Entradas)
        c = red.Ejecutar_modelo(mCiclo, Entradas)
        #print('Temperaturas: ', temp)
        #print('Centrifugados: ', centri)
        #print('Ciclos: ', c)
        tempElegida = red.Analisis(temp)
        centriElegida = red.Analisis(centri)
        cicloElegida = red.Analisis(c)
        if tempElegida == 0:
            TheLabApp.Lavar = False
        elif cicloElegida == 0:
            TheLabApp.Lavar = False
        else:
            TheLabApp.Lavar = True
        #print('Temperatura Elegida = ', temperatura[tempElegida], ' - ', tempElegida)
        #print('Centrifugado Elegida = ', centrifugado[centriElegida], ' - ', centriElegida)
        #print('Ciclo Elegida = ', ciclo[cicloElegida], ' - ', cicloElegida)
        #print('-------------------')
        TheLabApp.TemperaturaElegida = temperatura[tempElegida]
        TheLabApp.CentrifugadoElegida = centrifugado[centriElegida]
        TheLabApp.CicloElegida = ciclo[cicloElegida]




#-------------------------------------------------------
#               PANTALLA DE ELEGIR PROGRAMA
#-------------------------------------------------------
class ScreenProgramas(Screen):
    def on_enter(self, *args):
        self.ids.BtnSwitch.active = TheLabApp.Prelavado
        self.ids.inputPrograma.text = str(TheLabApp.Programa)

    def StatusSwitch(self, valor):
        if valor:
            TheLabApp.Prelavado = True
        else:
            TheLabApp.Prelavado = False

    def ActualizarPrograma(self):
        TheLabApp.Programa = str(self.ids.inputPrograma.text)

#-------------------------------------------------------
#               PANTALLA DE INTRODUCIR ROPA
#-------------------------------------------------------
class ScreenRopa(Screen):
    pasamos = True
    msj = ''

    def on_enter(self, *args):
        self.ids.InputRopa.text = TheLabApp.Lista_Ropa_Insertada
        #print('Blanco: ', TheLabApp.Blanco, ' - Color: ', TheLabApp.Color)
        self.ids.checkColor.active = TheLabApp.Color
        self.ids.checkBlanco.active = TheLabApp.Blanco

    #Obligo a que haya siemre uno activado
    def ClickCheckColor(self):
        if TheLabApp.Color:
            TheLabApp.Color = False
            self.ids.Respuesta.text = ''
        else:
            TheLabApp.Color = True
            self.ids.Respuesta.text = "Se recomienda separar por colores PARECIDOS"
    def ClicCheckBlanco(self):
        a = TheLabApp.Blanco
        if TheLabApp.Blanco:
            TheLabApp.Blanco = False
        else:
            TheLabApp.Blanco = True
        #print('Cambio Color de ', a, ' --> ', TheLabApp.Blanco)

    def Continuar(self, instance, modelo):
        TheLabApp.Lista_Ropa_Insertada = instance.text

        Lista_Ropa_Red, no_conocidos, TheLabApp.Lista_Ropa_Tratada = red.TraduccionRopa(instance.text)

        if len(no_conocidos) == 0 and TheLabApp.Lista_Ropa_Insertada != '' and len(TheLabApp.Lista_Ropa_Tratada) != 0:
            self.pasamos = True
            self.msj = ''
        elif len(no_conocidos) > 0:
            self.pasamos = False
            self.msj = 'Hay elementos no reconocidos: ' + str(no_conocidos)
        else:
            self.pasamos = False
            self.msj = 'Introduzca alguna prenda'
        self.ids.mensaje.text = self.msj

        if self.pasamos:
            TheLabApp.Dic_Tejido.clear()
            TheLabApp.Dic_Ropa_Red.clear()
            #Rellenamos el diccionario
            #salida = TheLabApp.Predecir()  #NO Funciona... por motivo de arriba, habria que pasarle el modelo x parametro
            salida = red.Ejecutar_modelo(modelo, Lista_Ropa_Red)
            for i in range(len(Lista_Ropa_Red)):
                s = red.Tejido_Probable(salida[i])
                TheLabApp.Dic_Tejido[str(TheLabApp.Lista_Ropa_Tratada[i])] = s
                TheLabApp.Dic_Ropa_Red[str(TheLabApp.Lista_Ropa_Tratada[i])] = Lista_Ropa_Red[i]


#-------------------------------------------------------
#               PANTALLA DE INICIO
#-------------------------------------------------------
class ScreenInicio(Screen):
    pass




class TheLabApp(MDApp):
    # ---------------------------------------------
    #                   VARIABLES
    # ---------------------------------------------

    modeloTejido = 0#tf.keras.model
    modeloTemp = 0
    modeloCentri = 0
    modeloCiclo = 0
    Lista_Ropa_Insertada = ''
    Lista_Ropa_Tratada = []
    #Lista_Ropa_Red = []
    Dic_Tejido = dict()
    Dic_Ropa_Red = dict()
    Blanco = False
    Color = False
    colores = ''
    TemperaturaElegida = ''
    CentrifugadoElegida = ''
    CicloElegida = ''
    Prelavado = False
    Programa = ''
    Lavar = True


    #Manejo las pantallas
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(ScreenInicio(name="screen_inicio"))
        screen_manager.add_widget(ScreenRopa(name="screen_Ropa"))
        screen_manager.add_widget(ScreenProgramas(name="screen_Programas"))
        screen_manager.add_widget(ScreenTejido(name="screen_Tejido"))
        screen_manager.add_widget(ScreenSalida(name="screen_Salida"))
        screen_manager.add_widget(ScreenDetergente(name="screen_Detergente"))
        screen_manager.add_widget(prueba(name="prueba"))
        return screen_manager

    # ---------------------------------------------
    #                FUNCIONES REDES
    # ---------------------------------------------
    def CargarRedes(self):
        carga = True
        try:
            self.modeloTejido, self.modeloTemp, self.modeloCentri, self.modeloCiclo = red.Cargar_Redes()
            #print('Modelo Tejido', self.modeloTejido.summary())    #Funcionas perfe
        except Exception as e:
            print('Exception ', e)
            carga = False

    def Inicializar(self):
        #self.InicializarVar()
        self.CargarRedes()










if __name__ == "__main__":
    TheLabApp().run()

#sample_app = TheLabApp()
#sample_app.run()