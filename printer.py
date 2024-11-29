from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, Line, InstructionGroup


def silencio(silen_redn_Y, silen_blan_Y, silen_neg_Y, silen_cor_Y, silen_semicor_Y, silen_fusa_Y, valor_fig,
             tam_neuma, posi_X, leinzoH, separador, sist_index):

    silencios = []

    font_silencio = {'4.0': ['q', silen_redn_Y, 20, 15], '2.0': ['w', silen_blan_Y, 20, 12],
                     '1.0': ['e', silen_neg_Y, 25, 15],
                     '0.5': ['r', silen_cor_Y, 20, 12],
                     '0.25': ['t', silen_semicor_Y, 0, 0],
                     '0.125': ['y', silen_fusa_Y, 0, 0], '0.0625': ['u', 0, 0, 0],
                     '0.03125': ['i', 0, 0, 0]}

    if valor_fig in ['4.0', '2.0', '1.0', '0.5', '0.25', '0.125', '0.0625', '0.03125']:
        text_fig = font_silencio[valor_fig][0]
        posi_Y = font_silencio[valor_fig][1]
    else:
        sin_puntillo = str(float(valor_fig) * (2 / 3))
        text_fig = font_silencio[sin_puntillo][0]
        posi_Y = font_silencio[sin_puntillo][1]
        ajus_puntX = font_silencio[sin_puntillo][2]
        ajus_puntY = font_silencio[sin_puntillo][3]

        l = Label(text=".", font_size=tam_neuma, color=[0, 0, 0, 1],
                  font_name='RIED_V5.otf',
                  size_hint=[None, None], size=[36, 27],
                  pos=[posi_X + ajus_puntX,
                       leinzoH - posi_Y - (separador * sist_index) + ajus_puntY])
        silencios.append(l)

    l = Label(text=text_fig, font_size=tam_neuma, color=[0, 0, 0, 1],
              font_name='RIED_V5.otf',
              size_hint=[None, None], size=[36, 27],
              pos=[posi_X, leinzoH - posi_Y - (separador * sist_index)])

    silencios.append(l)

    return silencios


def figuras(valor_fig, ajuste_puntillo_X, tam_neuma, posi_X, leinzoH, posi_Y):

    listaneumapulso = []

    if float(valor_fig) < 2:
        if float(valor_fig) in [1, 0.5, 0.25, .125, 0.0625, 0.03125]:
            text_fig = "s"
            ajus_pun = 0
        else:
            text_fig = "S"
            ajus_pun = ajuste_puntillo_X

        usa_plica = True
    else:
        if valor_fig == '8.0':
            text_fig = "V"
            ajus_pun = 0
        elif valor_fig == '6.0':
            text_fig = "T"
            ajus_pun = 0
        elif valor_fig == '4.0':
            text_fig = "U"
            ajus_pun = 0
        elif valor_fig == '3.0':
            text_fig = "A"
            ajus_pun = ajuste_puntillo_X
        else:
            text_fig = "a"
            ajus_pun = 0

        if float(valor_fig) < 4:
            usa_plica = True
        else:
            usa_plica = False

    l = Label(text=text_fig, font_size=tam_neuma, color=[0, 0, 0, 1],
              font_name='RIED_V5.otf',
              size_hint=[None, None], size=[36, 27],
              pos=[posi_X + ajus_pun, leinzoH - posi_Y])

    listaneumapulso.append(l)

    return listaneumapulso, usa_plica


