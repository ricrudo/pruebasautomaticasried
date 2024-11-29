from random import choice
import MusLib as ms

from math import floor, ceil

celulas_ritmicas_binario = {0: [-2], 1: [2], 2: [1, 1], 3: [1, -1], 4: [-1, 1], 5: [0.5, 0.5, 0.5, 0.5],
                            6: [1, 0.5, 0.5], 7: [0.5, 0.5, 1], 8: [0.5, 0.5, -1], 9: [-1, 0.5, 0.5],
                            10: [0.5, 1.5],
                            11: [-0.5, 0.5, 0.5, 0.5], 12: [-0.5, 0.5, 1], 13: [-0.5, 1, 0.5], 14: [-0.5, 1.5],
                            15: [-1, -0.5, 0.5], 16: [1.5, 0.5], 17: [0.5, 1, 0.5], 18: [1, 2, 1],
                            19: [-1, 2, 1], 20: [1, 2, -1], 21: [-1, 2, -1], 22: [8], 23: [-8], 24: [6], 25: [-6],
                            26: [4], 27: [-4]}

avance_binario = {0: [1], 1: [1], 2: [.5, .5], 3: [.35, .65], 4: [.35, .65], 5: [0.25, 0.25, 0.25, 0.25],
                  6: [0.5, 0.25, 0.25], 7: [0.25, 0.25, .5], 8: [0.2, 0.2, .6], 9: [.3, 0.3, 0.4],
                  10: [0.35, .65],
                  11: [0.25, 0.25, 0.25, 0.25], 12: [0.25, 0.25, .5], 13: [0.25, .5, 0.25], 14: [.35, .65],
                  15: [.25, 0.25, 0.5], 16: [.65, 0.35], 17: [0.25, .5, 0.25], 18: [0.5, 0.8, 0.7],
                  19: [0.5, 0.8, 0.7], 20: [0.5, 0.8, 0.7], 21: [0.5, 0.8, 0.7],
                  22: [4], 23: [4], 24: [3], 25: [3], 26: [2], 27: [2]}


celulas_ritmicas_ternario = {0: [-6], 1: [6], 2: [2, 2, 2], 3: [4, 2], 4: [2, 4], 5: [-2, 2, 2],
                             6: [-2, 4], 7: [-4, 2]}

avance_ternario = {0: [1], 1: [1], 2: [0.33, 0.33, 0.33], 3: [.6, 0.4], 4: [0.4, .6], 5: [0.33, 0.33, 0.33],
                   6: [0.4, .6], 7: [.6, 0.4]}

# define el contenido de las células rítmicas dependiendo de la subdivisión
def step1(subdivision_input):

    # forzar en modo test
    #    subdivision = subdivision_input

    if subdivision_input == "Binario":
        banco_celulas_ritmicas = celulas_ritmicas_binario
    else:
        banco_celulas_ritmicas = celulas_ritmicas_ternario

    return banco_celulas_ritmicas


def step2(tipo_de_ejercicio, tonalidad, modalidad, limite_grave, rango):
    tonalidad_de_ejercicio_input = tonalidad
    modalidad_de_ejercicio_input = modalidad

    # determinar el tipo de ejercicio seleccionado por el usuario
    tipo_de_ejercicio_input = tipo_de_ejercicio
    if tipo_de_ejercicio_input == "Rítmico":
        material_escala = ['B4']

    else:
        # determinar la escala para los ejercicios melódicos
        myScale = ms.escala(tonalidad_de_ejercicio_input, modalidad_de_ejercicio_input)

        rangos = {'unisono': 1, '2da': 2, '3ra': 3, '4ta': 4, '5ta': 5, '6ta': 6, '7ma': 7, '8va': 8,
                  '9na': 9, '10ma': 10, '11ma': 11, '12da': 12, '13ra': 13, '14ta': 14, '2 octavas': 15,
                  "2oct + 2da": 16, "2oct + 3ra": 17, "2oct + 4ta": 18, "2oct + 5ta": 19, "2oct + 6ta": 20,
                  "2oct + 7ma": 21, "3 octavas": 22}

        limite_agudo = rangos[rango]
        for t in myScale:
            if limite_grave[0] in t and limite_grave[-1] in t:
                index_lit_grave = myScale.index(t)
                break

        material_escala = []
        for xnote in range(limite_agudo):
            material_escala.append(myScale[index_lit_grave + xnote])

    return material_escala


def creacion_list_random_ritm(cel_rit_deseadas, numerador, denominador, subdivision, cantidad_compases):

    # determina la cantidad de veces que tiene que escoger elementos segun el numerador de la signatura de medida
    if subdivision == "Binario":
        valor_pulso = 4 / int(denominador)
        pulso_por_compas = int(numerador)
        pulsos = cantidad_compases * pulso_por_compas
    else:
        val_pul = {8: 1.5, 4: 3, 16: .75, 32: 0.375, 64: 0.1875}
        valor_pulso = val_pul[denominador]
        pulso_por_compas = int(numerador / 3)
        pulsos = cantidad_compases * pulso_por_compas

    ritmos_finales = []


    cont = 0
    while cont < pulsos:
        rit_ale = choice(cel_rit_deseadas)
        if subdivision == "Binario" and rit_ale in [18, 19, 20, 21]:
            if numerador % 2 == 0:
                if cont % 2 == 0:
                    ritmos_finales.append(rit_ale)
                    cont += 2
            elif numerador > 1:
                if (cont + 1) % numerador == 0:
                    pass
                else:
                    ritmos_finales.append(rit_ale)
                    cont += 2
            else:
                return
        elif subdivision == "Binario" and rit_ale in [26, 27]:
            if numerador > 1:
                if (cont + 1) % numerador == 0:
                    pass
                else:
                    ritmos_finales.append(rit_ale)
                    cont += 2
            else:
                return
        elif subdivision == "Binario" and rit_ale in [24, 25]:
            if numerador > 2:
                if (cont + 1) % numerador == 0 or (cont + 2) % numerador == 0:
                    pass
                else:
                    ritmos_finales.append(rit_ale)
                    cont += 3
            else:
                return
        elif subdivision == "Binario" and rit_ale in [22, 23]:
            if numerador > 3:
                if (cont + 1) % numerador == 0 or (cont + 2) % numerador == 0 or (cont + 3) % numerador == 0:
                    pass
                else:
                    ritmos_finales.append(rit_ale)
                    cont += 4
            else:
                return
        else:
            ritmos_finales.append(rit_ale)
            cont += 1

    return ritmos_finales, valor_pulso, pulso_por_compas, pulsos


def generar_altura(ritmos_finales, banco_celulas_ritmicas, material_escala, nivel, tono, modo):
    pitch_necarios = 0

    for x in ritmos_finales:
        for y in banco_celulas_ritmicas[x]:
            if y > 0:
                pitch_necarios += 1

    index_actual = choice(range(0, len(material_escala)))

    if pitch_necarios > 0:

        if 'Escala' in nivel:
            if "Direct" in nivel:
                alturas_finales = escalaNivel(material_escala, pitch_necarios, index_actual)
            else:
                limite = int(nivel.split(" ")[-1][:-2])
                alturas_finales = interMaxNivel(material_escala, pitch_necarios, limite)
        elif "Arpeg" in nivel:
            material_arpegio = arpegiosNivel(material_escala, tono, modo)
            if "Direct" in nivel:
                alturas_finales = escalaNivel(material_arpegio, pitch_necarios, index_actual)
            else:
                limite = int(nivel.split(" ")[-1][:-2])
                if limite == 4:
                    limite = 2
                elif limite == 6:
                    limite = 3
                elif limite == 8:
                    limite = 4
                else:
                    limite = 5
                alturas_finales = interMaxNivel(material_arpegio, pitch_necarios, limite)
        elif 'Grados de Atracc.' in nivel:
            limite = int(nivel.split(" ")[-1][:-2])
            alturas_finales = gradosAtraccNivel(material_escala, pitch_necarios, tono, modo, limite)
        else:
            alturas_finales = []
    else:
        alturas_finales = []

    return alturas_finales


def escalaNivel(material_escala, pitch_necarios, index_actual):
    alturas_finales = []
    direction = choice(['ascending', 'descending'])
    if direction == 'descending':
        material_escala.reverse()
    material_espejo = material_escala[:]
    alturas_finales.append(material_espejo.pop(index_actual))
    if pitch_necarios - 1 > 0:
        for ptc in range(pitch_necarios - 1):
            try:
                alturas_finales.append(material_espejo.pop(index_actual))
            except:
                try:
                    material_escala.reverse()
                    material_espejo = material_escala[:]
                    index_actual = 1
                    alturas_finales.append(material_espejo.pop(index_actual))
                except:
                    alturas_finales.append(material_espejo[0])

    return alturas_finales


def arpegiosNivel(material_escala, tono, modalidad):
    if modalidad in ["Mayor", "Lidia", "Mixolidia", "Jónica"]:
        modo = "Arp. Mayor"
    elif modalidad in ["Men. Armónica", "Men. Melódica", "Men. Natural", "Dórica", "Frigia", "Eólica"]:
        modo = "Arp. Menor"
    elif modalidad in ["Lócria"]:
        modo = "Arp. Dim"
    arpegio = ms.escala(tono, modo)
    material_arpegio = []

    for x in arpegio:
        if x in material_escala:
            material_arpegio.append(x)

    return material_arpegio


def gradosAtraccNivel(material_escala, pitch_necarios, tono, modalidad, limite):
    if modalidad in ["Mayor", "Lidia", "Mixolidia", "Jónica",
                     "Men. Armónica", "Men. Melódica",
                     "Men. Natural", "Dórica", "Frigia", "Eólica", "Lócria"]:  #que sea posible solo con escalas hepátofonas

        alturas_finales = []

        escala = ms.escala(tono, modalidad)

        segundas = []
        cuartas = []
        sextas = []
        septimas = []

        for x in material_escala:
            if escala[1][:-1] in x:
                segundas.append(x)
            elif escala[3][:-1] in x:
                cuartas.append(x)
            elif escala[5][:-1] in x:
                sextas.append(x)
            elif escala[6][:-1] in x:
                septimas.append(x)

        if material_escala[0] in [sextas]:
            material_escala.pop(0)
        if material_escala[1] in [sextas] and limite == 2: # si es la segunda nota del ambito escogido, podría generar un eterno 6 5 6 5 6 5 6 5...
            material_escala.pop(-1)
            material_escala.pop(-1)
        if material_escala[-1] in septimas:
            material_escala.pop(-1)
        if material_escala[-2] in septimas and limite == 2: # si es la penútlima nota del ambito escogido, podría generar un eterno 7 8 7 8 7 8...
            material_escala.pop(-1)
            material_escala.pop(-1)

        if len(material_escala) < 2:
            return "Escala no permite grados de atracción"

        ultimo_pitch_necesario = []
        while pitch_necarios > 0:
            ultimo_pitch_necesario.append(pitch_necarios)

            notas_dentro_limite = []
            if alturas_finales:
                index_ultima = material_escala.index(alturas_finales[-1])
                for x in range((limite - 1) * -1, (limite)):    #  limite - 1 es la cantidad de pasos desde una nota,
                                                                    #  la multiplicación indica direcciónes eje (-1, 1) = limite 2da
                    if -1 < index_ultima + x < len(material_escala) and x != 0:
                        notas_dentro_limite.append(material_escala[index_ultima + x])
                nueva = choice(notas_dentro_limite)
            else:
                nueva = choice(material_escala)

            if len(ultimo_pitch_necesario) > 10:
                for i in range(-10, 0):
                    if ultimo_pitch_necesario[-1] != ultimo_pitch_necesario[i]:
                        break
                    else:
                        alturas_finales.pop(0)
                        pitch_necarios += 1

            if (nueva in segundas + cuartas + sextas + septimas) and (pitch_necarios < 2):
                pass
            elif nueva in segundas + cuartas + sextas + septimas:
                if nueva in segundas + cuartas:
                    if nueva == material_escala[0]:
                        if len(alturas_finales) > 0:
                            indxAnt = material_escala.index(alturas_finales[-1])
                            indxNueva = material_escala.index(nueva)
                            if abs(indxAnt - indxNueva) < limite:
                                if nueva != alturas_finales[-1]:
                                    alturas_finales.append(nueva)
                                    alturas_finales.append(material_escala[1])
                                    pitch_necarios -= 2
                        else:
                            alturas_finales.append(nueva)
                            alturas_finales.append(material_escala[1])
                            pitch_necarios -= 2
                    elif nueva == material_escala[-1]:
                        if len(alturas_finales) > 0:
                            indxAnt = material_escala.index(alturas_finales[-1])
                            indxNueva = material_escala.index(nueva)
                            if abs(indxAnt - indxNueva) < limite:
                                if nueva != alturas_finales[-1]:
                                    alturas_finales.append(nueva)
                                    alturas_finales.append(material_escala[-2])
                                    pitch_necarios -= 2
                        else:
                            alturas_finales.append(nueva)
                            alturas_finales.append(material_escala[-2])
                            pitch_necarios -= 2
                    else:
                        if len(alturas_finales) > 0:
                            indxAnt = material_escala.index(alturas_finales[-1])
                            indxNueva = material_escala.index(nueva)
                            if abs(indxAnt - indxNueva) < limite:
                                if nueva != alturas_finales[-1]:
                                    indseg = material_escala.index(nueva)
                                    direc = choice([indseg + 1, indseg - 1])
                                    alturas_finales.append(nueva)
                                    alturas_finales.append(material_escala[direc])
                                    pitch_necarios -= 2
                        else:
                            indseg = material_escala.index(nueva)
                            direc = choice([indseg + 1, indseg - 1])
                            alturas_finales.append(nueva)
                            alturas_finales.append(material_escala[direc])
                            pitch_necarios -= 2
                elif nueva in sextas:
                    if len(alturas_finales) > 0:
                        indxAnt = material_escala.index(alturas_finales[-1])
                        indxNueva = material_escala.index(nueva)
                        if abs(indxAnt - indxNueva) < limite:
                            if nueva != alturas_finales[-1]:
                                indcua = material_escala.index(nueva)
                                alturas_finales.append(nueva)
                                alturas_finales.append(material_escala[indcua - 1])
                                pitch_necarios -= 2
                    else:
                        indcua = material_escala.index(nueva)
                        alturas_finales.append(nueva)
                        alturas_finales.append(material_escala[indcua - 1])
                        pitch_necarios -= 2
                elif nueva in septimas:
                    if len(alturas_finales) > 0:
                        indxAnt = material_escala.index(alturas_finales[-1])
                        indxNueva = material_escala.index(nueva)
                        if abs(indxAnt - indxNueva) < limite:
                            if nueva != alturas_finales[-1]:
                                indcua = material_escala.index(nueva)
                                alturas_finales.append(nueva)
                                alturas_finales.append(material_escala[indcua + 1])
                                pitch_necarios -= 2
                    else:
                        indcua = material_escala.index(nueva)
                        alturas_finales.append(nueva)
                        alturas_finales.append(material_escala[indcua + 1])
                        pitch_necarios -= 2
            else:
                if ((len(alturas_finales) > 0) and (nueva == alturas_finales[-1])) or (limite == 2):
                    pass
                else:
                    if len(alturas_finales) > 0:
                        indxAnt = material_escala.index(alturas_finales[-1])
                        indxNueva = material_escala.index(nueva)
                        if abs(indxAnt - indxNueva) < limite:
                            if nueva != alturas_finales[-1]:
                                alturas_finales.append(nueva)
                                pitch_necarios -= 1
                    else:
                        alturas_finales.append(nueva)
                        pitch_necarios -= 1
    else:
        alturas_finales = "Escala no permite grados de atracción"

    return alturas_finales


def interMaxNivel(material_escala, pitch_necarios, limite):
    if len(material_escala) < limite + 1:
        alturas_finales = randomNivel(material_escala, pitch_necarios)
    else:
        alturas_finales = []
        while pitch_necarios > 0:
            nueva = choice(material_escala)
            if len(alturas_finales) > 0:
                indxAnt = material_escala.index(alturas_finales[-1])
                indxNueva = material_escala.index(nueva)
                if abs(indxAnt - indxNueva) < limite:
                    if nueva != alturas_finales[-1]:
                        alturas_finales.append(nueva)
                        pitch_necarios -= 1
            else:
                alturas_finales.append(nueva)
                pitch_necarios -= 1

    return alturas_finales


def randomNivel(material_escala, pitch_necarios):
    alturas_finales = []
    for x in range(pitch_necarios):
        if len(material_escala) > 1:
            nueva = choice(material_escala)
            try:
                flag = 0
                while flag == 0:
                    if nueva != alturas_finales[-1]:
                        alturas_finales.append(nueva)
                        flag = 1
                    else:
                        nueva = choice(material_escala)
            except:
                alturas_finales.append(nueva)
        else:
            alturas_finales.append(material_escala[0])

    return alturas_finales


def generas_pulsos(ritmos_finales, alturas_finales, banco_celulas_ritmicas, denominador):
    pulsos_finales = []

    conversion_figuras = 2 / int(denominador)
    for r in ritmos_finales:
        pulsos_finales.append([])
        for m in banco_celulas_ritmicas[r]:
            if m > 0:
                pulsos_finales[-1].append([alturas_finales.pop(0), m * conversion_figuras, r])
            else:
                pulsos_finales[-1].append(["silencio", abs(m * conversion_figuras), r])
        if r in [18, 19, 20, 21, 26, 27]:
            pulsos_finales.append([[None]])
        elif r in [24, 25]:
            for vces in range(2):
                pulsos_finales.append([[None]])
        elif r in [22, 23]:
            for vces in range(3):
                pulsos_finales.append([[None]])

    return pulsos_finales


def generar_compases(pulsos_finales, cantidad_compases, pulso_por_compas):

    compases_finales = []

    for c in range(cantidad_compases):
        compases_finales.append([])
        for beat in range(pulso_por_compas):
            compases_finales[-1].append(pulsos_finales.pop(0))

    return compases_finales


def generar_sistemas(compases_finales):

    sistemas_finales = []

    for x in range(2):
        sistemas_finales.append([])
        for j in range(2):
            sistemas_finales[-1].append(compases_finales.pop(0))

    return sistemas_finales


def generar_pos_y(sistemas_finales, separador, distancia_step_h, ajuste_neuma_y, subdivision, linea_central, clave):

    global sistemas_finales_en_y

    notaNombres = ["C", "D", "E", "F", "G", "A", "B"]

    if subdivision == "Binario":
        avance_dic = avance_binario
    else:
        avance_dic = avance_ternario

    claves_posibles = ["Sol", "Fa", "Do 3ra línea", "Do 4ta línea",
                       "Do 5ta línea", "Do 2da línea", "Do 1ra línea",
                       "Fa 3ra línea", "Sol 1ra línea"]

    if clave == claves_posibles[0]:
        nota_central = "B4"
    elif clave == claves_posibles[1]:
        nota_central = "D3"
    elif clave == claves_posibles[2]:
        nota_central = "C4"
    elif clave == claves_posibles[3]:
        nota_central = "A3"
    elif clave == claves_posibles[4]:
        nota_central = "F3"
    elif clave == claves_posibles[5]:
        nota_central = "E4"
    elif clave == claves_posibles[6]:
        nota_central = "G4"
    elif clave == claves_posibles[7]:
        nota_central = "F3"
    elif clave == claves_posibles[8]:
        nota_central = "D5"

    octava_distancia = distancia_step_h * 7

    sistemas_finales_en_y = []
    sist_index = -1
    for sist in sistemas_finales:
        sist_index += 1
        com_index = -1
        sistemas_finales_en_y.append([])
        for com in sist:
            com_index += 1
            pulso_index = -1
            sistemas_finales_en_y[sist_index].append([])
            for pul in com:
                pulso_index += 1
                pulse = []
                notta_index = -1
                for notta in pul:
                    notta_index += 1
                    if notta[0] is not None:
                        av = avance_dic[notta[2]][notta_index]
                        if notta[0] != 'silencio':
                            distancia_rango_octava = notaNombres.index(nota_central[0]) - notaNombres.index(notta[0][0])
                            distancia_octavas = int(nota_central[-1]) - int(notta[0][-1])
                            posi_Y_neuma = (distancia_rango_octava * distancia_step_h) + \
                                           (distancia_octavas * octava_distancia) + linea_central
                            beat = [posi_Y_neuma + (separador * sist_index) + ajuste_neuma_y, notta[1], av]
                        else:
                            beat = [notta[0], notta[1], av]
                    else:
                        beat = [notta[0], notta[0], 0]
                    pulse.append(beat)
                sistemas_finales_en_y[sist_index][com_index].append(pulse)

    return sistemas_finales_en_y


def info_sistema(sistema, pulso_por_compas, dato):
    info_general = []

    cantidad_sistemas = len(sistemas_finales_en_y)

    for x in range(cantidad_sistemas):
        cantidad_compases = len(sistemas_finales_en_y[x])
        info_general.append(["sistema " + str(x) + ": ", str(cantidad_compases) + " compases",
                             str(cantidad_compases * pulso_por_compas) + " pulsos"])

    if dato == "bars":
        return int(info_general[sistema][1][:-9])
    elif dato == "beats":
        return int(info_general[sistema][2][:-6])


def avance(posi_X, linea_fin_x, pulsos_sistema, compases_sistema, distancia_barline):

    espacio_disponible = linea_fin_x - posi_X - ((compases_sistema - 1) * distancia_barline)

    return espacio_disponible / pulsos_sistema


def direction_plica(pul, sist_index, linea_central, separador, ajuste_neuma_y, denominador, subdivision, sistemas_finales, comp_index, pul_index):
    sum_val = 0
    cant_val = 0
    tam_pul = 0
    list_val = []
    lis_individual = []

    pul_info = (sistemas_finales[sist_index][comp_index][pul_index][0][2])

    try:
        for x in pul:
            tam_pul += x[1]
            if isinstance(x[0], int):
                list_val.append(x[0])
                sum_val += (x[0]) - (sist_index * separador)
                cant_val += 1
                if (x[0]) - (sist_index * separador) >= linea_central + ajuste_neuma_y:
                    lis_individual.append("up")
                    lis_individual.append(None)
                else:
                    lis_individual.append("down")
                    lis_individual.append(None)

        prome_val = sum_val / cant_val

        if subdivision.casefold() == "binario":
            dicFactores = {4: 1, 8: 2, 2: 0.5}
            tam_pul *= dicFactores[denominador]

        if cant_val > 1:
            if [tam_pul, len(pul)] == [1.5, 2] or [tam_pul, len(pul)] == [2, 3] or\
                    [tam_pul, len(pul), denominador] == [1, 2, 2] or [tam_pul, len(pul), denominador] == [3.0, 3, 4] \
                    or [tam_pul, len(pul), denominador] == [3.0, 2, 4]:
                return lis_individual
            elif [tam_pul, len(pul), denominador] == [1, 3, 2]:
                if pul[0][1] == 1.0:
                    prome_val = (pul[1][0] + pul[2][0]) / 2
                    if prome_val >= linea_central + ajuste_neuma_y:
                        if pul[0][0] != 'silencio':
                            return [lis_individual[0], lis_individual[1], 'up', min(list_val), 'up', min(list_val)]
                        else:
                            return ['up', min(list_val), 'up', min(list_val)]
                    else:
                        if pul[0][0] != 'silencio':
                            return [lis_individual[0], lis_individual[1], 'down', max(list_val), 'down', max(list_val)]
                        else:
                            return ['down', max(list_val), 'down', max(list_val)]
                elif pul[2][1] == 1.0:
                    if pul[0][0] == 'silencio':
                        return lis_individual
                    else:
                        prome_val = (pul[0][0] + pul[1][0]) / 2
                        if prome_val >= linea_central + ajuste_neuma_y:
                            if pul[2][0] != 'silencio':
                                return ['up', min(list_val), 'up', min(list_val), lis_individual[4], lis_individual[5]]
                            else:
                                return ['up', min(list_val), 'up', min(list_val)]
                        else:
                            if pul[2][0] != 'silencio':
                                return ['down', max(list_val), 'down', max(list_val), lis_individual[4], lis_individual[5]]
                            else:
                                return ['up', min(list_val), 'up', min(list_val)]
                else:
                    return lis_individual
            else:
                if prome_val >= linea_central + ajuste_neuma_y:
                    return ['up', min(list_val)]
                else:
                    return ['down', max(list_val)]
        else:
            if prome_val >= linea_central + ajuste_neuma_y:
                return ['up', None]
            else:
                return ['down', None]
    except:
        pass


def barras_join(sist_index, comp_index, pul_index, sistemas_finales, direction_plica,
                posi_X, avance, subdivision, pul, distancia_join, denominador):

    dic_barras = {0.5: 1, 0.75: 1, 0.375: 2, 0.25: 2, 0.125: 3, 0.0625: 4, 0.03125: 5}

    pul_info = (sistemas_finales[sist_index][comp_index][pul_index][0][2])

    referencia_direction = ""
    posicion_Y_1 = ""
    joiner = False
    posi_barra_Y_pre = ""

    if direction_plica is not None:
        if len(direction_plica) > 2:
            for x in range(len(direction_plica)):
                if direction_plica[x] not in (None, 'up', 'down'):
                    referencia_direction = direction_plica[x-1]
                    posi_barra_Y_pre = direction_plica[x]
                    joiner = True
                    break

        if referencia_direction == "":
            referencia_direction = direction_plica[0]

        if not joiner:
            if direction_plica[0] is not None:
                joiner = True

        if posi_barra_Y_pre == "":
            posi_barra_Y_pre = direction_plica[1]

        if posi_barra_Y_pre is None:
            return
        if denominador == 2 and pul_info in [12]:
            return

        if referencia_direction == 'up':
            distancia_join *= -1
        # determina si existe la posibilidad de usar el join
        if joiner:
            if (subdivision.casefold() == "binario" and pul_info in [2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17]) \
                    or (subdivision.casefold() == "ternario" and pul_info in [2, 5]) \
                    or (subdivision.casefold() == "ternario" and pul_info in [3, 4] and denominador == 16):
                fig_mayor_valor = 0
                # determina la figura de mayor valor, para saber cuantas barras lleva el join 1, que es el que corresponde
                # a la subdivisión mayor
                for beats in pul:
                    if beats[0] != 'silencio':
                        if fig_mayor_valor < beats[1] < 1.0:
                            fig_mayor_valor = beats[1]
                cantidad_barras = dic_barras[fig_mayor_valor]
                # se fijan las variables sin modificar de inicio y fin para el join 1
                inicio_barra_X = posi_X
                final_barra_X = posi_X
                # Se determina el comienzo del join 1 evadiendo algun silencio al comienzo
                for x in range(len(pul)):
                    if pul[x][0] == 'silencio' or pul[x][1] >= 1.0:
                        inicio_barra_X += (avance * pul[x][2])
                    else:
                        break
                # determina la posición de la ultima figura que no sea un silencio
                contador = 1
                for x in range(len(pul), -1, -1):
                    if pul[x-1][0] == 'silencio' or pul[x-1][1] >= 1.0:
                        contador += 1
                    else:
                        break
                # determina la posición final del join 1
                for beat in range(len(pul) - contador):
                    final_barra_X += (avance * (pul[beat][2]))
                posi_barra_Y = posi_barra_Y_pre
                # cada retorno es una join de subdivisión diferente, retorno 1 = join 1
                retorno1 = [cantidad_barras, inicio_barra_X, final_barra_X, posi_barra_Y, distancia_join]
                if subdivision.casefold() == "binario" and pul_info in [6, 7] and denominador != 2:
                    # determina la segunda figura de mayor valor, para saber cuantas barras lleva el join 2
                    fig_mayor_valor2 = 0
                    for beats in pul:
                        if beats[1] < fig_mayor_valor:
                            if beats[1] > fig_mayor_valor2:
                                fig_mayor_valor2 = beats[1]
                    cantidad_barras2 = dic_barras[fig_mayor_valor2] - dic_barras[fig_mayor_valor]
                    # se fijan las variables sin modificar de inicio y fin para el join 2
                    inicio_barra_X2 = posi_X
                    final_barra_X2 = posi_X
                    # Se determina el comienzo del join 2 evadiendo la figura de mayor valor
                    for x in range(len(pul)):
                        if pul[x][1] == fig_mayor_valor:
                            inicio_barra_X2 += (avance * pul[x][2])
                        else:
                            break
                    # determina la posición de la ultima figura que no sea igual al mayor valor
                    contador = 1
                    for x in range(len(pul), -1, -1):
                        if pul[x - 1][1] == fig_mayor_valor:
                            contador += 1
                        else:
                            break
                    # determina la posición final del join 2
                    for beat in range(len(pul) - contador):
                        final_barra_X2 += (avance * (pul[beat][2]))
                    posi_barra_Y2 = direction_plica[1]
                    # cada retorno es una join de subdivisión diferente, retorno 1 = join 2
                    retorno2 = [cantidad_barras2, inicio_barra_X2, final_barra_X2, posi_barra_Y2, distancia_join]
                    return [[retorno1], [retorno2]]
                elif (subdivision.casefold() == "binario" and pul_info in [10, 12, 13, 16, 17]) \
                        or (subdivision.casefold() == "ternario" and pul_info in [3, 4] and denominador == 16):
                    # determina la segunda figura de mayor valor, para saber cuantas barras lleva el join 2
                    fig_menor_valor2 = 100
                    for beats in pul:
                        if beats[1] < fig_mayor_valor and beats[0] != 'silencio':
                            if beats[1] < fig_menor_valor2:
                                fig_menor_valor2 = beats[1]
                    cantidad_barras2 = dic_barras[fig_menor_valor2] - dic_barras[fig_mayor_valor]
                    # se fijan las variables sin modificar de inicio y fin para el fakejoin 2
                    inicio_barra_X2 = posi_X
                    final_barra_X2 = posi_X
                    # Se determina el comienzo del fakejoin 2 evadiendo la figura de mayor valor
                    for x in range(len(pul)):
                        if pul[x][1] > fig_menor_valor2 or pul[x][0] == 'silencio':
                            inicio_barra_X2 += (avance * pul[x][2])
                        else:
                            if (pul_info in [10, 12, 17]) \
                                    or (subdivision.casefold() == "ternario" and pul_info in [4] and denominador == 16):
                                # determina la posición final del fakejoin 2
                                final_barra_X2 = inicio_barra_X2 + ((avance * pul[x][2]) * .4)
                            elif pul_info in [13, 16] \
                                    or (subdivision.casefold() == "ternario" and pul_info in [3] and denominador == 16):
                                final_barra_X2 = inicio_barra_X2 + ((avance * pul[x][2]) * -.4)
                            break
                    posi_barra_Y2 = direction_plica[1]
                    # cada retorno es una join de subdivisión diferente, retorno 1 = join 2
                    retorno2 = [cantidad_barras2, inicio_barra_X2, final_barra_X2, posi_barra_Y2, distancia_join]
                    if pul_info in [10, 12, 13, 16] \
                            or (subdivision.casefold() == "ternario" and pul_info in [3, 4] and denominador == 16):
                        return [[retorno1], [retorno2]]
                    else:
                        # se fijan las variables sin modificar de inicio y fin para el fakejoin 2
                        inicio_barra_X3 = posi_X
                        # Se determina el comienzo del fakejoin 2 evadiendo la figura de mayor valor
                        for x in range(len(pul)-1):
                            inicio_barra_X3 += (avance * pul[x][2])
                        final_barra_X3 = inicio_barra_X3 + ((avance * pul[-1][2]) * -.4)
                        posi_barra_Y3 = direction_plica[1]
                        # cada retorno es una join de subdivisión diferente, retorno 1 = join 2
                        retorno3 = [cantidad_barras2, inicio_barra_X3, final_barra_X3, posi_barra_Y3, distancia_join]
                        return [[retorno1], [retorno2, retorno3]]
                else:
                    return [[retorno1]]
            else:
                print("no hay joiner")
                return None
        else:
            return None
    else:
        return None


def flags(direction_plica, sist_index, comp_index, pul_index, sistemas_finales, subdivision, denominador):

    ritmo = (sistemas_finales[sist_index][comp_index][pul_index][0][2])

    if subdivision.casefold() == "binario":
        if denominador == 2:
            if ritmo in (10, 12, 13, 15, 16, 17):
                if ritmo in [10]:
                    return [0, direction_plica[0]]
                if ritmo in [13, 15]:
                    return [2, direction_plica[0]]
                if ritmo in [12, 15, 16]:
                    return [1, direction_plica[0]]
                if ritmo in [17]:
                    return [0, direction_plica[0], 2, direction_plica[4]]
                else:
                    pass
            else:
                return None
        elif denominador == 4:
            if ritmo in (3, 4, 14, 15, 18, 19, 20):
                if ritmo in [3, 20]:
                    return [0, direction_plica[0]]
                elif ritmo in [15]:
                    return [2, direction_plica[0]]
                if ritmo in [4, 14, 15]:
                    return [1, direction_plica[0]]
                elif ritmo == 18:
                    return [0, direction_plica[0], 2, direction_plica[4]]
                elif ritmo == 19:
                    return [2, direction_plica[2]]
                else:
                    pass
            else:
                return None
        elif denominador == 8:
            if ritmo in (1, 3, 4, 14, 15, 18, 19, 20, 21):
                if ritmo in [1, 3]:
                    return [0, direction_plica[0]]
                elif ritmo in [15]:
                    return [2, direction_plica[0]]
                if ritmo in [4, 14, 15, 21]:
                    return [1, direction_plica[0]]
                elif ritmo == 18:
                    return [0, direction_plica[0], 1, direction_plica[2],  2, direction_plica[4]]
                elif ritmo == 19:
                    return [1, direction_plica[0], 2, direction_plica[2]]
                elif ritmo == 20:
                    return [0, direction_plica[0], 1, direction_plica[2]]
                else:
                    pass
            else:
                return None

    else:
        if denominador == 4:
            return None
        elif denominador == 8:
            if ritmo in (3, 4, 7):
                if ritmo == 4:
                    return [0, direction_plica[0]]
                if ritmo == 3:
                    return [1, direction_plica[2]]
                else:
                    return [1, direction_plica[0]]
            else:
                return None
        elif denominador == 16:
            if ritmo in [1, 6, 7]:
                if ritmo == 1:
                    return [0, direction_plica[0]]
                if ritmo in [6, 7]:
                    return [1, direction_plica[0]]
            else:
                return None


def linea_adicional(nt, linea_central, sist_index, separador, distancia_step_h, ajuste_neuma_y):

    posicion_en_sistema_cero = nt[0] - (sist_index * separador) - ajuste_neuma_y
    distanci_desde_centro_en_step = int(((posicion_en_sistema_cero - linea_central)/distancia_step_h))

    pos_lin_ad = []
    if abs(distanci_desde_centro_en_step) >= 6:
        for j in range(5, abs(distanci_desde_centro_en_step), 2):
            if distanci_desde_centro_en_step < 0:
                pos_lin_ad.append(linea_central - (distancia_step_h * (j+1)) + (separador*sist_index))
            else:
                pos_lin_ad.append(linea_central + (distancia_step_h * (j+1)) + (separador*sist_index))


        return pos_lin_ad
    else:
        return None
