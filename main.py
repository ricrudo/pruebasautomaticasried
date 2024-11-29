from kivy.core.window import Window
import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle, Color, Line, InstructionGroup
from kivy.uix.treeview import TreeViewLabel, TreeView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import sp, pt, dp
from kivy.metrics import MetricsBase
from kivy.logger import Logger
from kivy.clock import Clock
import os
import math
from functools import partial
import calculationmusthe
import midigenerator
import MusLib as ms
import printer
import sincronizar
import login_student
from kivy.core.audio import SoundLoader
from kivy.utils import platform
from time import sleep
from datetime import datetime

Window.size = (1200, 700)
kivy.config.Config.set('graphics', 'resizable', False)

# en teoría esto hace que se mueva el teclado
Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

resolution = [(1366, 768), (1920, 1080), (1440, 900),
              (1536, 864), (1600, 900), (1280, 720),
              (1280, 800), (1024, 768)]

size_screen = resolution[6]

rutaarchivos = ""
bloqueo = -1
pulsos_a_borrar = 1
listaneumas = []
listapentagramas = []
celulas_ritmicas = []
listDRMB = []
listDRMT = []
subdivision = "Binario"
transposition = "C"
subdivision_metrono = "1"
presets = []
listRoots = []
listNodes = []
lastScreen = "solfeo"
numerador = 4
ajuste_borr = 0  # ajuste necesario para el caso en el cual las figuras a borrar son más grandes que el pulso


# lo que sucede es que en estos casos la alarma de figura más grande que el pusl (una lista [none]
# la tiene listanuema, entonces el conteo de pulso se ajusta al tamaño de esa lista, pero la lista
# de canvas se descuadra en la contabilizada, entonces cada que suceda una alarma, se debe "detener"
# el conteo del canvas, y la opción que se encontró fue reducir el conteo por medio de este ajuste
# en el else: de if item2[0] is not None:



class MenuSlide(BoxLayout):
    pass

class LoginScreen(Screen):

    def login_student(self, instruc, student, password):
        global rutaarchivos

        if not instruc or not password or not student:
            popup = Popup(title="Faltan Datos",
                          content=Label(text="Uno o varios de los campos\nno contienen información", font_size='20sp'),
                          size_hint=(0.8, 0.4))
            popup.open()
        else:
            login = login_student.student_login(instruc, student, password)
            if login[0] == "Bienvenido a RiedMusicApp":
                conf_directory = "tt"
                if not os.path.exists(conf_directory):
                    os.makedirs(conf_directory)
                name = login[2] + ".dtl"
                path = os.path.join("tt", name)
                f = open(path, "w")
                f.close()
                rutaarchivos = name
                codigo = sincronizar.sinc(name)
                MainWindow.envio_presets(self, "inicio")
                titulo = "Bienvenido a RiedMusicApp"
                texto = '¡Hola ' + str(login[1]) + "!\nEsperamos que disfrutes tu experiencia con RiedMusicApp\nPuedes visitarnos en www.riedmusicapp.com"
                popup = Popup(title=titulo,
                              content=Label(text=texto, font_size='20sp', halign='center'),
                              size_hint=(0.8, 0.4))
                popup.open()
            elif login[0] == "Cuenta en uso":
                conexion_estado = 1
                titulo = "Problemas de Conexión"
                texto = 'Nuestro sistema indica que esta cuenta esta\n' \
                        'siendo usada por una IP diferente.\n' \
                        'Escríbanos a soporte@riedmusicapp.com si\n' \
                        'sigue encontrando dificultades para registrarse.'
                popup = Popup(title=titulo,
                              content=Label(text=texto, font_size='20sp', halign='center'),
                              size_hint=(0.8, 0.4))
                popup.open()
            elif login[0] == "Error de conexión":
                conexion_estado = 1
                titulo = "Problemas de Conexión"
                texto = 'Hemos tenido problemas para conectar con\nla base de datos.\nRevisa la conexión a internet.'
                popup = Popup(title=titulo,
                              content=Label(text=texto, font_size='20sp', halign='center'),
                              size_hint=(0.8, 0.4))
                popup.open()
            else:
                titulo = "Datos no encontrados"
                texto = 'El usuario o contraseña no existen en el sistema.\nIntente nuevamente.'
                popup = Popup(title=titulo,
                              content=Label(text=texto, font_size='20sp', halign='center'),
                              size_hint=(0.8, 0.4))
                popup.open()

class MainWindow(Screen):

    def envio_presets(self, inicio):
        global presets, celulas_ritmicas, listRoots, listNodes, rutaarchivos

        fecha2 = datetime(2025, 11, 30)
        now = datetime.now()


        # Esta apliación se autodestruye
        if now > fecha2:
            return
        if rutaarchivos == "":
            conexion = open('conexion.dtl', 'r')
            conexion.seek(0)
            data_conexion = conexion.readlines()
            conexion.close()

            if not data_conexion:
                self.parent.current = "LoginScreen"
                return
            else:
                rutaarchivos = data_conexion[0].split("$!$")[1] + ".dtl"

        tv = TreeView(root_options=dict(text='My root label'), hide_root=True, indent_start=60)

        for child in tv.children:
            tv.remove_node(child)

        altura = 0
        presets = []
        listRoots = []
        listNodes = []

        celulas_ritmicas = []
        conf_directory = "tt"
        path = os.path.join(conf_directory, rutaarchivos)
        try:
            f = open(path, "r")
            for line in f.readlines():
                presets_cargados = ([x.split("$!$") for x in line[:-1].split("$$!$$")])
                presets.append(presets_cargados)

            f.close()

            for h in presets:
                h.pop(0)
                listRoots.append(h[0][0])
                presets_cargados2 = ([hlis for hlis in h[1:]])
                listNodes.append(presets_cargados2)

            for carpeta in range(len(listRoots)):
                folder = TreeViewLabel(text=listRoots[carpeta],
                                       color_selected=[41 / 255, 163 / 255, 208 / 255, 1], font_size='20sp')
                altura += 34
                tv.add_node(folder)
                for ejercicio in listNodes[carpeta]:
                    ejercItem = TreeViewLabel(text=ejercicio[0],
                                              color_selected=[41 / 255, 163 / 255, 208 / 255, 1], font_size='20sp')
                    tv.add_node(ejercItem, folder)
                    altura += 34
        except:
            pass
        tv.size_hint = [None, None]
        tv.size = [self.width, dp(altura)]
        self.manager.ids.PresetScreen.ids.scrollerpreset.add_widget(tv)
        if inicio == "inicio":
            for widget in range(3):  # único de la versión estudiante
                self.manager.ids.PresetScreen.ids.ContenedorBotones.remove_widget(
                    self.manager.ids.PresetScreen.ids.ContenedorBotones.children[0])
            btn1 = Button(text='Sincronizar', font_size='20sp')
            btn1.bind(on_release=PresetScreen.sincronizar)
            self.manager.ids.PresetScreen.ids.ContenedorBotones.add_widget(btn1)
            self.manager.ids.PresetScreen.ids.ContenedorBotones.add_widget(Label())  # único de la versión estudiante

        self.parent.current = "PresetScreen"
        self.manager.transition.direction = "right"


class PresetScreen(Screen):

    def testeo(self, cargado):
        global listaneumas, listapentagramas, celulas_ritmicas, listapulsos, \
            pulsos_finales, subdivision, cant_pulsos, numerador

        celulas_ritmicas = [int(x) for x in cargado[4:-8]]

        if celulas_ritmicas:

            # tipo_de_ejercicio_input.get() o tipo_de_ejercicio aparece en el código original
            if "False" in cargado[-8]:
                tipo_de_ejercicio = "Rítmico"
            else:
                tipo_de_ejercicio = "Melódico"

            clave = cargado[-5]
            numerador = int(cargado[1])
            denominador = int(cargado[2])
            tonalidad = cargado[-7]
            modalidad = cargado[-6]
            limite_grave = cargado[-4]
            rango = cargado[-3]
            nivel = cargado[-2] + " " + cargado[-1]
            cantidad_compases = 4

            subdivision = cargado[3]
            banco_celulas_ritmicas = calculationmusthe.step1(subdivision)

            material_escala = calculationmusthe.step2(tipo_de_ejercicio, tonalidad, modalidad, limite_grave, rango)

            ritmos_finales, valor_pulso, pulso_por_compas, cant_pulsos = calculationmusthe.creacion_list_random_ritm(
                celulas_ritmicas, numerador, denominador, subdivision, cantidad_compases)

            alturas_finales = calculationmusthe.generar_altura(ritmos_finales, banco_celulas_ritmicas, material_escala,
                                                               nivel, tonalidad, modalidad)

            pulsos_finales = calculationmusthe.generas_pulsos(ritmos_finales, alturas_finales, banco_celulas_ritmicas,
                                                              denominador)

            midigenerator.getNumerNote(pulsos_finales, subdivision, cant_pulsos, numerador, denominador, 60)

            compases_finales = calculationmusthe.generar_compases(pulsos_finales, cantidad_compases, pulso_por_compas)

            sistemas_finales = calculationmusthe.generar_sistemas(compases_finales)

            # Medidas básicas
            separador = 180
            selfh = self.height - 120  # Este ultimo número sale del label que hay que colocar para que no se cruce con el actionBar
            scroll_h = selfh * 0.75
            scroll_w = self.width
            if (len(sistemas_finales) * separador) + 80 <= scroll_h:
                leinzoH = scroll_h
                self.manager.ids.controlPlay.ids.lienzo.size_hint_y = 1
            else:
                leinzoH = (len(sistemas_finales) * separador) + 80
                self.manager.ids.controlPlay.ids.lienzo.size_hint_y = leinzoH / scroll_h

            # abreviatura para llegar al canvas
            c = self.manager.ids.controlPlay.ids.lienzo.canvas.before

            # Abreviatura para llegar al lienzo
            lienzoprt = self.manager.ids.controlPlay.ids.lienzo

            resolution = [(1366, 768), (1280, 800), (1920, 1080),
                          (1440, 900), (1536, 864), (1600, 900),
                          (1280, 720), (1024, 768)]

            try:
                resol = 1
            except:
                resol = 0
                print("No existe resolución")

            val_reso = [(11, (39, 10), 179, (85, 13), 171, (116, 3), 181, 10, (31, -5), (5, -11),
                         (-1, 37), (22, 22, 4, 6), 11, (30, -30), (0, 60, 30, 26, 12, 5, 6, 7), 7, 22, 8,
                         (0, 0, 0, 0, 0, 0)),

                        (9, (34, 1), 140, (72, 1), 141, (95, -3), 141, 5, (28, 0), (8, -8),
                         (-1, 37), (18, 19, 4, 6), 8, (24, -24), (5, 5, 7, 6, -5, 5, 6, 7), 7, 16, 6,
                         ((100, 70), 15, -18, (100, 70), 20, -18))
                        ]

            distancia_step_h = val_reso[resol][0]
            linea_central = (distancia_step_h * 13)
            clave_x = val_reso[resol][1][0]
            clave_y = linea_central - distancia_step_h + val_reso[resol][1][1]
            tam_clave = val_reso[resol][2]
            time_sig_x = val_reso[resol][3][0]
            time_sig_y = linea_central - distancia_step_h + val_reso[resol][3][1]
            tam_signatura = val_reso[resol][4]
            ajuste_neuma_x, ajuste_neuma_y = val_reso[resol][5]
            tam_neuma = val_reso[resol][6]
            distancia_barline = val_reso[resol][7]
            ajuste_UP_plica_X, ajuste_UP_plica_Y = val_reso[resol][8]
            ajuste_DOWN_plica_X, ajuste_DOWN_plica_Y = val_reso[resol][9]
            comienzo_li_adic, final_li_adic = val_reso[resol][10]
            ajuste_flag_X_pre = val_reso[resol][12]
            ajuste_flag_Y_pre = val_reso[resol][13]
            silen_redn_Y = linea_central + val_reso[resol][14][0]
            silen_blan_Y = linea_central + val_reso[resol][14][1]
            silen_neg_Y = linea_central + val_reso[resol][14][2]
            silen_cor_Y = linea_central + val_reso[resol][14][3]
            silen_semicor_Y = linea_central + val_reso[resol][14][4]
            silen_fusa_Y = linea_central + val_reso[resol][14][5]
            ajuste_puntillo_X = val_reso[resol][15]
            distancia_join = val_reso[resol][16]
            ancho_join = val_reso[resol][17]
            cantidadAlter, tipo_alter = ms.cantidadAlter(tonalidad, modalidad)
            if cantidadAlter < 0:
                ajst_arma_x = val_reso[resol][18][0]
                desplaza_arma = val_reso[resol][18][1]
                ajst_arma_y = val_reso[resol][18][2]
            elif cantidadAlter > 0:
                ajst_arma_x = val_reso[resol][18][3]
                desplaza_arma = val_reso[resol][18][4]
                ajst_arma_y = val_reso[resol][18][5]
            else:
                ajst_arma_x = (0, 0)
                desplaza_arma = 0
                ajst_arma_y = 0

            linea_start_x = 10
            linea_fin_x = scroll_w - linea_start_x
            dist_oct = distancia_step_h * 7

            di_clav = {"Sol": ["z", 0, [0, -3, 1, -2, 2, -1, 3, 0, -3, 1],
                               [-4, -1, -5, -2, 1, -3, 0, -4, -1, -5]],
                       "Fa": ["x", 0, [2, -1, 3, 0, 4, 1, 5, 2, -1, 3],
                              [-2, 1, -3, 0, 3, -1, 2, -2, 1, -3]],
                       "Do 3ra línea": ["c", 0, [1, -2, 2, -1, 3, 0, 4, 1, -2, 2],
                                        [-3, 0, -4, -1, 2, -2, 1, -3, 0, -4]],
                       "Do 4ta línea": ["c", -2, [-1, -4, 0, -3, 1, -2, 2, -1, -4, 0],
                                        [2, -2, 1, -3, 0, -4, -1, 2, -2, 1]],
                       "Do 5ta línea": ["c", -4, [-3, 1, -2, 2, -1, 3, 0, -3, 1, -2],
                                        [0, -4, -1, -5, -2, 1, -3, 0, -4, -1]],
                       "Do 2da línea": ["c", 2, [-4, 0, -3, 1, -2, 2, -1, -4, 0, -3],
                                        [-1, 2, -2, 1, -3, 0, -4, -1, 2, -2]],
                       "Do 1ra línea": ["c", 4, [-2, 2, -1, 3, 0, 4, -1, -2, 2, -1],
                                        [1, -3, 0, -4, -1, -5, -2, 1, -3, 0]],
                       "Fa 3ra línea": ["x", 2, [-3, -1, -2, 2, -1, 3, 0, -3, -1, -2],
                                        [0, -4, -1, -5, -2, 1, 2, 0, -4, -1]],
                       "Sol 1ra línea": ["z", 2, [2, -1, 3, 0, 4, 1, 5, 2, -1, 3],
                                         [-2, 1, -3, 0, 3, -1, 2, -2, 1, -3]]}

            datclave = di_clav[clave]

            # crea el group que necesito para despues poder borrar en la def clear_everything()
            grupo = InstructionGroup()

            grupo.add(Color(0, 0, 0, 1))

            for j in range(len(sistemas_finales)):
                grupo.add(Line(points=[linea_start_x,
                                       leinzoH - linea_central - (j * separador) + (distancia_step_h * 4),
                                       linea_start_x,
                                       leinzoH - linea_central - (j * separador) - (distancia_step_h * 4)]))
                grupo.add(Line(points=[linea_fin_x,
                                       leinzoH - linea_central - (j * separador) + (distancia_step_h * 4),
                                       linea_fin_x,
                                       leinzoH - linea_central - (j * separador) - (distancia_step_h * 4)]))
                for x in [-2, -1, 0, 1, 2]:
                    grupo.add(Line(points=[linea_start_x,
                                           leinzoH - linea_central - ((distancia_step_h * 2) * x) - (
                                                   j * separador),
                                           linea_fin_x,
                                           leinzoH - linea_central - (j * separador) - (
                                                   (distancia_step_h * 2) * x)],
                                   width=1))

                claveprint = Label(text=datclave[0], font_size=tam_clave, color=[0, 0, 0, 1], font_name='RIED_V5.otf',
                                   size_hint=[None, None],
                                   size=[0, 0],
                                   pos=[clave_x,
                                        leinzoH - clave_y - (j * separador) - (distancia_step_h * datclave[1])])

                lienzoprt.add_widget(claveprint)

            num_text = str(numerador)
            den_text = str(denominador)
            if subdivision.casefold() == "binario":
                pass
                # den_text = "4"
            else:
                pass
                # num_text = "6"

            numeradorprt = Label(text=num_text, font_size=tam_signatura, color=[0, 0, 0, 1], font_name='RIED_V5.otf',
                                 size_hint=[None, None],
                                 size=[0, 0], pos=[time_sig_x, leinzoH - time_sig_y], halign="left", valign="top")
            lienzoprt.add_widget(numeradorprt)

            denominadorprt = Label(text=den_text, font_size=tam_signatura, color=[0, 0, 0, 1], font_name='RIED_V5.otf',
                                   size_hint=[None, None],
                                   size=[0, 0], pos=[time_sig_x, leinzoH - (time_sig_y + (4 * distancia_step_h))],
                                   halign="left", valign="top")
            lienzoprt.add_widget(denominadorprt)

            if cantidadAlter != 0:
                if cantidadAlter < 0:
                    dic_arma = di_clav[clave][2]
                else:
                    dic_arma = di_clav[clave][3]
                for j in range(len(sistemas_finales)):
                    if j == 0:
                        posaltx = ajst_arma_x[0]
                    else:
                        posaltx = ajst_arma_x[1]
                    for alt in range(abs(cantidadAlter)):
                        armadura = Label(text=tipo_alter, font_size=tam_neuma, color=[0, 0, 0, 1],
                                         font_name='RIED_V5.otf',
                                         size_hint=[None, None],
                                         size=[0, 0],
                                         pos=[posaltx + (alt * desplaza_arma),
                                              leinzoH - (linea_central + ajst_arma_y + (j * separador) + (
                                                      dic_arma[alt] * distancia_step_h))],
                                         halign="left", valign="top")
                        lienzoprt.add_widget(armadura)

            sistemas_finales_en_y = calculationmusthe.generar_pos_y(sistemas_finales, separador,
                                                                    distancia_step_h, ajuste_neuma_y,
                                                                    subdivision, linea_central, clave)

            # empieza en análisis de los sistemas
            listapulsos = []
            sist_index = -1
            for sist in sistemas_finales_en_y:
                sist_index += 1
                # define la posición de la primera nota, dependiendo si es el primer sistema, pues es el
                # único que lleva la signatura de medida
                if sist_index == 0:
                    posi_X = ajuste_neuma_x + (abs(cantidadAlter) * desplaza_arma)
                else:
                    posi_X = ajuste_neuma_x - (ajuste_neuma_x - time_sig_x) + (abs(cantidadAlter) * desplaza_arma)

                # Determina la distancia entre las notas dependiende de la cantidad de notas por sistema y por compás
                pulsos_sistema = calculationmusthe.info_sistema(sist_index, pulso_por_compas, "beats")
                compases_sistema = calculationmusthe.info_sistema(sist_index, pulso_por_compas, "bars")
                avance = calculationmusthe.avance(posi_X, linea_fin_x, pulsos_sistema, compases_sistema,
                                                  distancia_barline)

                # empieza en análisis de los compases
                comp_index = -1
                for comp in sist:
                    comp_index += 1
                    # Genera la barra que termina el compás
                    if comp_index > 0:
                        grupo.add(Line(points=[posi_X,
                                               leinzoH - linea_central - (sist_index * separador) - (
                                                       distancia_step_h * 4),
                                               posi_X,
                                               leinzoH - linea_central - (sist_index * separador) + (
                                                       distancia_step_h * 4)]))
                        posi_X += distancia_barline
                    # empieza en análisis de los pulsos
                    pul_index = -1
                    for pul in comp:
                        # crea un InstructionGroup() para poder borrarlos por tiempo
                        grupopulso = InstructionGroup()
                        grupopulso.add(Color(0, 0, 0, 1))
                        listaneumapulso = []

                        pul_index += 1

                        if pul[0][0] is not None:

                            direction_plica = calculationmusthe.direction_plica(pul, sist_index, linea_central,
                                                                                separador, ajuste_neuma_y, denominador,
                                                                                subdivision, sistemas_finales,
                                                                                comp_index, pul_index)

                            barras_join = calculationmusthe.barras_join(sist_index, comp_index, pul_index,
                                                                        sistemas_finales, direction_plica, posi_X,
                                                                        avance, subdivision, pul, distancia_join,
                                                                        denominador)

                            flags = calculationmusthe.flags(direction_plica, sist_index, comp_index,
                                                            pul_index, sistemas_finales, subdivision, denominador)

                            nt_index = -1
                            for nt in pul:
                                nt_index += 1
                                avance_pul2 = avance * nt[2]
                                valor_fig = str(nt[1])
                                if nt[0] == 'silencio':
                                    silencios = printer.silencio(silen_redn_Y, silen_blan_Y, silen_neg_Y, silen_cor_Y,
                                                                 silen_semicor_Y,
                                                                 silen_fusa_Y, valor_fig, tam_neuma, posi_X,
                                                                 leinzoH, separador, sist_index)

                                    for l in silencios:
                                        lienzoprt.add_widget(l)
                                        listaneumapulso.append(l)

                                else:
                                    posi_Y = nt[0]
                                    neumas, usa_plica = printer.figuras(valor_fig, ajuste_puntillo_X, tam_neuma, posi_X,
                                                                        leinzoH, posi_Y)
                                    for l in neumas:
                                        lienzoprt.add_widget(l)
                                        listaneumapulso.append(l)

                                    if usa_plica:
                                        if direction_plica[0] == 'up':
                                            ajuste_plica_X = ajuste_UP_plica_X
                                            ajuste_plica_Y = ajuste_UP_plica_Y
                                            if direction_plica[1] is None:
                                                final_Y = posi_Y - dist_oct
                                            else:
                                                final_Y = direction_plica[1] - dist_oct

                                        else:
                                            ajuste_plica_X = ajuste_DOWN_plica_X
                                            ajuste_plica_Y = ajuste_DOWN_plica_Y
                                            if direction_plica[1] is None:
                                                final_Y = posi_Y + dist_oct
                                            else:
                                                final_Y = direction_plica[1] + dist_oct
                                        if len(direction_plica) > 2:
                                            for x in range(2):
                                                direction_plica.append(direction_plica.pop(0))
                                        grupopulso.add(Line(points=[posi_X + ajuste_plica_X,
                                                                    leinzoH - posi_Y + ajuste_plica_Y,
                                                                    posi_X + ajuste_plica_X,
                                                                    leinzoH - final_Y + ajuste_plica_Y]))

                                        if flags is not None:
                                            if nt_index == flags[0]:
                                                ajuste_flag_X = ajuste_plica_X + ajuste_flag_X_pre
                                                dic_text = {'0.5': 'd', '0.75': 'd', '0.25': 'f', '0.375': 'f',
                                                            '0.125': 'g', '0.0625': 'h', '0.03125': 'j'}
                                                if flags[1] == 'up':
                                                    text_fig = dic_text[valor_fig]
                                                    ajuste_flag_Y = ajuste_plica_Y + ajuste_flag_Y_pre[0]
                                                else:
                                                    text_fig = (dic_text[valor_fig]).upper()
                                                    ajuste_flag_Y = ajuste_plica_Y + ajuste_flag_Y_pre[1]
                                                l = Label(text=text_fig, font_size=tam_neuma, color=[0, 0, 0, 1],
                                                          font_name='RIED_V5.otf',
                                                          size_hint=[None, None], size=[0, 0],
                                                          pos=[posi_X + ajuste_flag_X,
                                                               leinzoH - posi_Y + ajuste_flag_Y])
                                                lienzoprt.add_widget(l)
                                                listaneumapulso.append(l)
                                                for x in range(2):
                                                    flags.append(flags.pop(0))

                                        if barras_join is not None:
                                            counter = 0
                                            for sub_b in range(len(barras_join)):
                                                for barra in range(barras_join[sub_b][0][0]):
                                                    for sub_c in range(len(barras_join[sub_b])):
                                                        grupopulso.add(Line(
                                                            points=[barras_join[sub_b][sub_c][1] + ajuste_plica_X - 1,
                                                                    leinzoH - final_Y + ajuste_plica_Y + (
                                                                            counter * barras_join[sub_b][sub_c][4]),
                                                                    barras_join[sub_b][sub_c][2] + ajuste_plica_X + 1,
                                                                    leinzoH - final_Y + ajuste_plica_Y + (
                                                                            counter * barras_join[sub_b][sub_c][4])],
                                                            width=ancho_join,
                                                            cap='none'))
                                                    counter += 1
                                            barras_join = None

                                        linea_adicional = calculationmusthe.linea_adicional(nt, linea_central,
                                                                                            sist_index, separador,
                                                                                            distancia_step_h,
                                                                                            ajuste_neuma_y)
                                        if linea_adicional is not None:
                                            for line in linea_adicional:
                                                grupopulso.add(Line(points=[posi_X + comienzo_li_adic,
                                                                            leinzoH - line,
                                                                            posi_X + final_li_adic,
                                                                            leinzoH - line]))

                                posi_X += avance_pul2

                            listapulsos.append(grupopulso)
                            c.add(grupopulso)
                            listaneumas.append(listaneumapulso)
                        else:
                            listaneumas.append([None])
            listapentagramas.append(grupo)
            c.add(grupo)
            try:
                self.parent.current = "controlPlay"
            except:
                pass

    def save_final(self, name, tipo):
        global data_simple, listNodes

        dato = ""
        for carpeta in range(len(listRoots)):
            dato += "$$!$$" + listRoots[carpeta]
            for ejercicio in listNodes[carpeta]:
                dato += "$$!$$" + "$!$".join(ejercicio)
            dato += '\n'

        conf_directory = "tt"
        if not os.path.exists(conf_directory):
            os.makedirs(conf_directory)
        path = os.path.join("tt", "ltd.dtl")
        f = open(path, "w")
        f.write(dato)
        f.close()

#    def botonCargar(self):
#        PresetScreen.cargar_preset(self)

    def guardar(self):
        global index_carpeta, counter_ejercicio

        index_carpeta, counter_ejercicio = PresetScreen.leerTreeview(self, "guardar")

        if index_carpeta is None:
            print("Seleccione una carpeta, o cree una nueva con el botón +")
            return

        PresetScreen.ventanaGuardarName(self, "guardar")

    def leerTreeview(self, uso):

        counter_ejercicio = ""
        counter_carpeta = ""
        index_ejercicio = -1

        if len(self.ids.scrollerpreset.children[0].children) == len(listRoots):  # las carpetas estan cerradas
            if uso == "cargar":
                return None, None
            elif uso in ["guardar", "borrar", "borrar definitivo"]:
                for x in self.ids.scrollerpreset.children[0].children:
                    if x.is_selected:
                        counter_carpeta = x.text
                        index_carpeta = listRoots.index(counter_carpeta)
                        if uso in ["guardar", "borrar"]:
                            return index_carpeta, None
                        elif uso in ["borrar definitivo"]:
                            return index_carpeta, None, x, None
                if uso in ["guardar", "borrar"]:
                    return None, None
                elif uso in ["borrar definitivo"]:
                    return None, None, None, None
        else:
            for x in self.ids.scrollerpreset.children[0].children:
                if x.text in listRoots:
                    if counter_ejercicio != "":
                        counter_carpeta = x.text
                        index_carpeta = listRoots.index(counter_carpeta)
                        if uso == "cargar":
                            return index_carpeta, counter_ejercicio
                        elif uso in ["guardar", "borrar", "borrar definitivo"]:
                            if uso == "guardar":
                                return index_carpeta, counter_ejercicio
                            elif uso == "borrar":
                                return index_carpeta, index_ejercicio
                            elif uso == "borrar definitivo":
                                return index_carpeta, index_ejercicio, x, node
                        break  # esto es porque Kivy organiza al revés entonces primero va a encontrar el ejercicio y luego la carpeta
                    else:
                        if x.is_selected:
                            if uso == "cargar":
                                return None, None
                            elif uso in ["guardar", "borrar", "borrar definitivo"]:
                                counter_carpeta = x.text
                                index_carpeta = listRoots.index(counter_carpeta)
                                if uso in ["guardar", "borrar"]:
                                    return index_carpeta, None
                                elif uso in ["borrar definitivo"]:
                                    return index_carpeta, None, x, None
                else:
                    if x.is_selected:
                        counter_ejercicio = x.text
                        node = x
                        index_ejercicio = 0
                    else:
                        if index_ejercicio >= 0:
                            index_ejercicio += 1
        if uso in ["borrar definitivo"]:
            return None, None, None, None
        else:
            return None, None

    def cargar_preset(self):
        global celulas_ritmicas, lastScreen, cargado

        app = App.get_running_app()
        presetPantalla = app.root.ids.PresetScreen

        index_carpeta, counter_ejercicio = PresetScreen.leerTreeview(presetPantalla, "cargar")

        if index_carpeta is None:
            return

        for ejer in listNodes[index_carpeta]:
            if ejer[0] == counter_ejercicio:

                cargado = ejer
                PresetScreen.testeo(presetPantalla, cargado)
                #self.ids.scrollerpreset.clear_widgets()
                try:
                    presetPantalla.parent.current = "controlPlay"
                    lastScreen = "PresetScreen"
                except:
                    pass

    def clear(self):
        global celulas_ritmicas, lastScreen
        celulas_ritmicas = []

        lastScreen = "solfeo"
        self.manager.ids.PresetScreen.ids.CargarBoton.text = "Cargar"
        self.manager.ids.PresetScreen.ids.BorrarBoton.text = "Borrar"
        self.manager.ids.PresetScreen.ids.VolverBoton.text = "Volver"
        self.ids.scrollerpreset.clear_widgets()

    def sincronizar(self):

        conexion = open('conexion.dtl', 'r')
        conexion.seek(0)
        data_conexion = conexion.readlines()
        conexion.close()
        if not data_conexion:
            return
        else:
            filename = data_conexion[0].split("$!$")[1] + ".dtl"

        codigo = sincronizar.sinc(filename)
        if codigo == 200:
            self.parent.parent.children[1].clear_widgets()
            self.parent.parent.children[1].scroll_y = 1
            MainWindow.envio_presets(self.parent.parent.parent.parent, "otro")
            titulo = "Sincronización exitosa"
            texto = '¡Los ejercicios han sido sincronizados!'
        elif codigo == 404:
            titulo = "Fallo en la sincronización"
            texto = 'Los ejercicios no se han podido sincronizar\nEs posible que su profesor no haya sincronizado ejercicio aún.'
        elif codigo == "problemas de conexión":
            titulo = "Problemas de conexión"
            texto = 'No fue posible conectarse. Revisé su conexión a internet\nSi el problema persiste contacte al Servicio Técnico Ried.'
        else:
            return

        popup = Popup(title=titulo,
                      content=Label(text=texto, font_size='20sp', halign='center'),
                      size_hint=(0.8, 0.4))
        popup.open()


class SolfeoControlPlayWindow(Screen):

    def avance(self):

        app = App.get_running_app()
        tree = app.root.ids.PresetScreen.ids.scrollerpreset.children[0]
        label = app.root.ids.controlPlay.ids.info1


        counter = 0
        for x in tree.children:
            if x == tree.selected_node:
                if counter != 0:
                    try:
                        SolfeoControlPlayWindow.clear_everything(self)
                    except:
                        pass
                    try:
                        label.text = tree.children[counter - 1].text
                        tree.select_node(tree.children[counter - 1])
                        PresetScreen.cargar_preset(app.root.ids.PresetScreen)
                    except:
                        pass
                break
            counter += 1

    def retroceder(self):

        app = App.get_running_app()
        tree = app.root.ids.PresetScreen.ids.scrollerpreset.children[0]
        label = app.root.ids.controlPlay.ids.info1

        counter = 0
        for x in tree.children:
            if x == tree.selected_node:
                if counter != len(tree.children) - 2:
                    try:
                        SolfeoControlPlayWindow.clear_everything(self)
                    except:
                        pass
                    try:
                        label.text = tree.children[counter + 1].text
                        tree.select_node(tree.children[counter + 1])
                        PresetScreen.cargar_preset(app.root.ids.PresetScreen)

                    except:
                        pass
                break
            counter += 1

    def reiniciar(self):
        app = App.get_running_app()

        tree = app.root.ids.PresetScreen.ids.scrollerpreset.children[0]
        SolfeoControlPlayWindow.clear_everything(self)
        label = app.root.ids.controlPlay.ids.info1

        label.text = tree.children[- 2].text
        tree.select_node(tree.children[-2])
        PresetScreen.cargar_preset(app.root.ids.PresetScreen)



#        for child in app.root.ids.PresetScreen.ids.scrollerpreset.children[0].children:
#            if

    def tipo(self, spinner):

        app = App.get_running_app()

        tree = app.root.ids.PresetScreen.ids.scrollerpreset.children[0]

        print(spinner.text)
        #listselecte app.

        counter = 0
        for x in tree.children:
            x.is_open = False
            if x.text == spinner.text:
                x.is_open = True
                tree.select_node(x)
                break


        for x in tree.children:
            print(x.text, x.is_open)
        #SolfeoControlPlayWindow.avance(self)

        #app.root.ids.controlPlay.ids.info1.text =

    def updateTempo(self, text):
        tempoA = int(self.manager.ids.controlPlay.ids.tempo.text)
        tempoB = int(text)
        tempoC = tempoA + tempoB
        self.manager.ids.controlPlay.ids.tempo.text = str(tempoC)

    def routingScreen(self):
        self.parent.current = lastScreen

    def clear_everything(self):
        global listaneumas, listapentagramas, contador_pulsos_play, temp, bloqueo, playback

        try:
            Clock.unschedule(temp)
            temp.cancel()
        except:
            pass

        SolfeoControlPlayWindow.menudeslizable(self, "nuevo")

        for x in range(len(self.manager.ids.controlPlay.ids.lienzo.children)):
            self.manager.ids.controlPlay.ids.lienzo.remove_widget(
                self.manager.ids.controlPlay.ids.lienzo.children[0])
        item = listapentagramas.pop(-1)
        self.manager.ids.controlPlay.ids.lienzo.canvas.before.remove(item)
        for x in range(len(listapulsos)):
            item = listapulsos.pop(-1)
            self.manager.ids.controlPlay.ids.lienzo.canvas.before.remove(item)
        if playback:
            try:
                sound.stop()
                sound.release()
            except:
                try:
                    sound.stop()
                    sound.unload()
                except:
                    pass
            playback = False

        listaneumas = []


    def borrar_nota_anota(self):
        global listaneumas, listapulsos, temp, contador_pulsos_play, ajuste_borr, bloqueo, menudesplegable, playback

        contador_pulsos_play += 1

        try:
            if sound.state == "play":
                tocando = True
        except:
            try:
                if sound.isPlaying():
                    tocando = True
            except:
                tocando = False

        if subdivision == "Binario":
            preconteo = int(numerador)
        else:
            preconteo = int(numerador)/3

        if pulsos_a_borrar < 3:
            pasadas = int(pulsos_a_borrar)
        else:
            pasadas = int(preconteo)
        try:
            if tocando:
                if contador_pulsos_play > preconteo - 1:
                    try:
                        bloqueo += 1
                        if bloqueo % pasadas == 0:
                            for x in range(pasadas):
                                item2 = listaneumas[int(contador_pulsos_play - preconteo)]
                                if item2[0] is not None:
                                    item = listapulsos[int(contador_pulsos_play - preconteo - ajuste_borr)]
                                    self.manager.ids.controlPlay.ids.lienzo.canvas.before.remove(item)
                                    for neu in item2:
                                        self.manager.ids.controlPlay.ids.lienzo.remove_widget(neu)
                                else:
                                    ajuste_borr += 1
                                contador_pulsos_play += 1
                            contador_pulsos_play -= pasadas
                        else:
                            pass
                    except:
                        sleep(.5)  # para que la ultima nota no quede cortada
                        print("no hay nada más que borrar")
                        bloqueo = -1
                        temp.cancel()
                        contador_pulsos_play = 0
                        self.reload()
                        menudesplegable = False
                        try:
                            sound.release()
                        except:
                            sound.unload()
                        playback = False
            else:
                try:
                    Clock.unschedule(temp)
                    temp.cancel()
                except:
                    pass
        except:
            sleep(.5)  # para que la ultima nota no quede cortada
            Clock.unschedule(temp)
            temp.cancel()
            print("no hay nada más que borrar")
            bloqueo = -1
            temp.cancel()
            contador_pulsos_play = 0
            self.reload()
            menudesplegable = False
            try:
                sound.release()
            except:
                sound.unload()
            playback = False

    def crear_nuevo(self):

        global contador_pulsos_play, sound, temp, playback

        if playback:
            if platform == "macosx":
                sound.stop()
                sound.release()
            elif platform == "android":
                sound.stop()
                sound.unload()
            Clock.unschedule(temp)
            temp.cancel()
            playback = False

        contador_pulsos_play = 0
        PresetScreen.testeo(self, cargado)

    def reload(self):
        global listaneumas, listapulsos

        d = self.manager.ids.controlPlay.ids.lienzo.canvas.before

        lienzoprt = self.manager.ids.controlPlay.ids.lienzo

        for item in listapulsos:
            if item not in d.children:
                d.add(item)

        for item2 in listaneumas:
            if item2[0] is not None:
                for item3 in item2:
                    if item3 not in lienzoprt.children:
                        lienzoprt.add_widget(item3)

    def play_midi(self):

        global sound, temp, contador_pulsos_play, ajuste_borr, menudesplegable, bloqueo, playback

        if self.ids.MenuBoton.state == "down":
            SolfeoControlPlayWindow.menudeslizable(self, "nuevo")

        ajuste_borr = 0

        try:
            Clock.unschedule(temp)
        except:
            pass

        tempo = self.manager.ids.controlPlay.ids.tempo.text

        trans1 = transposition

        if trans1 != "C":
            trans = int(trans1.split(" ")[-1][:-1])
        else:
            trans = 0

        segundos = 60 / int(tempo)

        contador_pulsos_play = 0
        bloqueo = -1

        self.reload()

        print(platform)

        if platform == "macosx":
            if playback:
                sound.stop()
                sound.unload()
                playback = False
            else:
                midigenerator.generarmidifile(tempo, trans, subdivision_metrono=subdivision_metrono)
                sound = SoundLoader.load('sequence.mid')
                sound.play()
                temp = Clock.schedule_interval(lambda dt: self.borrar_nota_anota(), segundos)
                playback = True
        elif platform == "android":
            if playback:
                sound.stop()
                sound.release()
                playback = False
            else:
                midigenerator.generarmidifile(tempo, trans, subdivision_metrono=subdivision_metrono)
                MediaPlayer = autoclass('android.media.MediaPlayer')
                sound = MediaPlayer()
                sound.setDataSource('sequence.mid')
                sound.prepare()
                sound.start()
                temp = Clock.schedule_interval(lambda dt: self.borrar_nota_anota(), segundos)
                playback = True

    def menudeslizable(self, *args):

        global menudesplegable, subdivision_metrono, transposition, pulsos_a_borrar

        #print("menu args", args)

        #print(menudesplegable)
        app = App.get_running_app()

        for arg in args:
            if arg == "nuevo":
                return
                app.root.ids.controlPlay.ids.MenuBoton.state = "normal"
                if not menudesplegable:
                    return

        widget = app.root.ids.controlPlay.ids

        if not menudesplegable:
            if "MenuSlide" not in str(widget.lienzo.children[0]):
                # solo crea el menu si no lo tiene
                size_scroller = app.root.ids.controlPlay.ids.scroller.size
                widget.lienzo.add_widget(MenuSlide())
                widget.lienzo.children[0].size = [size_scroller[0]/2, size_scroller[1]*0.75]
                pos_Y_menuDes = widget.lienzo.size[1] - widget.lienzo.children[0].size[1]
                widget.lienzo.children[0].pos = [0 - widget.lienzo.children[0].size[0], pos_Y_menuDes]
            else:
                # es necesario tener el dato para la animación
                pos_Y_menuDes = widget.lienzo.size[1] - widget.lienzo.children[0].size[1]
            widget.lienzo.children[0].ids.transposition.text = transposition
            widget.lienzo.children[0].ids.subdivision_metrono.text = subdivision_metrono
            if pulsos_a_borrar == 1:
                pulsos_a_borrar_text = "1 pulso"
            elif pulsos_a_borrar == 2:
                pulsos_a_borrar_text = "2 pulsos"
            else:
                pulsos_a_borrar_text = "Compás"
            widget.lienzo.children[0].ids.ocultar.text = pulsos_a_borrar_text
            anim = Animation(pos=[0, pos_Y_menuDes], duration=.3)
            anim.start(widget.lienzo.children[0])
            menudesplegable = True
            return
        else:
            pos_Y_menuDes = widget.lienzo.size[1] - widget.lienzo.children[0].size[1]
            pos_X_menuDes = widget.lienzo.children[0].pos[0]
            if pos_X_menuDes == 0:
                new_pos = [0 - widget.lienzo.children[0].size[0], pos_Y_menuDes]
                duration_mov = .3
                transposition = widget.lienzo.children[0].ids.transposition.text
                if widget.lienzo.children[0].ids.ocultar.text == "1 pulso":
                    pulsos_a_borrar = 1
                elif widget.lienzo.children[0].ids.ocultar.text == "2 pulsos":
                    pulsos_a_borrar = 2
                else:
                    pulsos_a_borrar = 3
                subdivision_metrono = widget.lienzo.children[0].ids.subdivision_metrono.text

            else:
                new_pos = [0, pos_Y_menuDes]
                duration_mov = .3
            anim = Animation(pos=new_pos, duration=duration_mov)
            anim.start(widget.lienzo.children[0])
            menudesplegable = False


menudesplegable = False
contador_pulsos_play = 0
playback = False


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("test.kv")


class RiedAdmision(App):

    def build(self):
        # Set the background color for the window
        Window.clearcolor = (75 / 255, 80 / 255, 80 / 255, 1)

        return kv


RiedAdmision().run()
