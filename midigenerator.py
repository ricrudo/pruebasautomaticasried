from midiutil import MIDIFile


def getNumerNote(pul_fils, subdi, cantidad_pulsos, nume, deno, tempo):
    global numNotasFinales, subdivision, cant_pulsos, numerador, speed

    pulsos_finales = pul_fils
    subdivision = subdi
    cant_pulsos = cantidad_pulsos
    numerador = nume
    speed = tempo
    NotasOctZero = {'C': 12, 'D': 14, 'E': 16, 'F': 17, 'G': 19, 'A': 21, 'B': 23}

    place_note = 0

    numNotasFinales = []
    for pul in pulsos_finales:
        for notta in pul:
            if notta != [None]:
                if (subdivision, deno) == ("Binario", 2) or (subdivision, deno) == ("Ternario", 4):
                    duration = notta[1] / 2  # in beats
                elif (subdivision, deno) == ("Binario", 8) or (subdivision, deno) == ("Ternario", 16):
                    duration = notta[1] * 2  # in beats
                else:
                    duration = notta[1]  # in beats
                if notta[0] not in ['silencio', None]:
                    if len(notta[0]) > 2:
                        if notta[0][1] == '#':
                            alteracion = 1
                        else:
                            alteracion = -1
                    else:
                        alteracion = 0
                    numberNote = NotasOctZero[notta[0][0]] + (12 * int(notta[0][-1])) + alteracion
                    numNotasFinales.append([notta[0], numberNote, duration, place_note])
                    place_note += duration  # in beats
                elif notta[0] == 'silencio':
                    place_note += duration  # in beats


def generarmidifile(speed, trans, **kwargs):
    dictransp = {0: 0, 2: -2, 4: -5, 5: -7, 6: -9, 9: -14, 13: -21}


    if subdivision == "Binario":
        preconteo = int(numerador)
    else:
        preconteo = int(numerador / 3)

    track = 0
    channel = 0
    volume = 100  # 0-127, as per the MIDI standard

    if subdivision.casefold() == "binario":
        tempo = int(speed)  # In BPM
        place_note = 0  # In beats
        duration_metronome = 1
    else:
        tempo = int(speed) * 1.5
        place_note = 0  # In beats
        duration_metronome = 1.5

    MyMIDI = MIDIFile(2)  # One track, defaults to format 1 (tempo track
    # automatically created)
    MyMIDI.addTempo(track, place_note, tempo)

    for notta in numNotasFinales:
        pitch = notta[1] + dictransp[trans]
        duration = notta[2]
        if subdivision.casefold() == "binario":
            place_note = notta[3] + preconteo
        else:
            place_note = notta[3] + (preconteo * 1.5)
        MyMIDI.addNote(track, channel, pitch, place_note, duration, volume)

    track = 1
    channel = 9
    volume = 100  # 0-127, as per the MIDI standard
    place_note = 0


    subdivision_metrono = 1
    # escribe el metronomo dependiendo de la subdivisión
    for key, value in kwargs.items():
        if key == "subdivision_metrono":
            print("value", value)
            subdivision_metrono = int(value)


    # posibles metronomes 48(tambor electronic), 56(cencerro 1), 60(bongo), 61(quemao), 63(tambor hi), 64(tambor lo),
    # 67(cencerro), 68 (campana), 75, 76(jamblock hi), 77(jamblock lo), 80(triangulo)]
    #  variables para cuando se pueda ajustar el sonido del metrónomo
    golpe_arriba = 75
    golpe_abajo = 77

    counter = 0
    for x in range((cant_pulsos + preconteo) * subdivision_metrono):
        if subdivision_metrono > 1:
            if counter == 0:
                pitch = golpe_arriba
            else:
                pitch = golpe_abajo
        else:
            pitch = golpe_arriba
        MyMIDI.addNote(track, channel, pitch, place_note, duration_metronome, volume)
        place_note += duration_metronome/subdivision_metrono
        if subdivision_metrono > 1:
            counter += 1
            if counter == subdivision_metrono:
                counter = 0

    with open("sequence.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
