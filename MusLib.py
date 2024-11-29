def escala(Tono, Modo):
    notesNames = ["C", "D", "E", "F", "G", "A", "B"]

    noteCromatic = [("C", "B#", "Dbb"),
                    ("C#", "B##", "Db"),
                    ("D", "C##", "Ebb"),
                    ("D#", "Eb", "Fbb"),
                    ("E", "D##", "Fb"),
                    ("F", "E#", "Gbb"),
                    ("F#", "E##", "Gb"),
                    ("G", "F##", "Abb"),
                    ("G#", "Ab"),
                    ("A", "G##", "Bbb"),
                    ("A#", "Bb", "Cbb"),
                    ("B", "A##", "Cb")]

    dictIntCr = {"1": 0, "2": 2, "3": 4, "4": 5, "5": 7, "6": 9, "7": 11}
    dicalte = {"M": 0, "P": 0, "m": -1, "d": -1, "A": 1}

    #escalas_heptafonas = ["Mayor", "Jónica", "Eólica", "Men. Natural", "Men. Armónica",
    #                      "Men. Melódica", "Dórica", "Mixolidia", "Lidia", "Frigia",
    #                      "Lócria"]

    dicModos = {"Mayor": ("2M", "2M", "2m", "2M", "2M", "2M"),
                "Jónica": ("2M", "2M", "2m", "2M", "2M", "2M"),
                "Eólica": ("2M", "2m", "2M", "2M", "2m", "2M"),
                "Men. Natural": ("2M", "2m", "2M", "2M", "2m", "2M"),
                "Men. Armónica": ("2M", "2m", "2M", "2M", "2m", "2A"),
                "Men. Melódica": ("2M", "2m", "2M", "2M", "2M", "2M"),
                "Dórica": ("2M", "2m", "2M", "2M", "2M", "2m"),
                "Mixolidia": ("2M", "2M", "2m", "2M", "2M", "2m"),
                "Lidia": ("2M", "2M", "2M", "2m", "2M", "2M"),
                "Frigia": ("2m", "2M", "2M", "2M", "2m", "2M"),
                "Lócria": ("2m", "2M", "2M", "2m", "2M", "2M"),
                "Tonos": ("2M", "2M", "2M", "2M", "3d"),
                "Arp. Mayor": ("3M", "3m"),
                "Arp. Menor": ("3m", "3M"),
                "Arp. Aug": ("3M", "3M"),
                "Arp. Dim": ("3m", "3m")}


    if Tono[0] not in notesNames:
        print("Este nota no es soportada")
        exit()

    if len(Tono) > 2:
        for f in Tono[2:]:
            if f != Tono[1]:
                print("La combinación de alteraciones no es soportada")
                exit()

    for f in Tono[1:]:
        if f not in ("b", "#"):
            print("Esta alteración no es soportada")
            exit()

    escala = [Tono]

    # Organiza noteNames dejando el tono como primera nota
    while notesNames[0] != Tono[0]:
        notesNames.append(notesNames.pop(0))

    notesNames[0] = Tono

    while Tono not in noteCromatic[0]:
        noteCromatic.append(noteCromatic.pop(0))

    counter = 1
    countera = 0
    counterb = 0
    for intercr in dicModos[Modo]:
        countera += int(intercr[0]) - 1
        escala.append(notesNames[countera])
        if intercr[0] in ("2", "3", "6", "7"):
            if intercr[1] == "d":
                paso = -1
            else:
                paso = 0
        else:
            paso = 0
        if len(intercr) > 2:
            for alter in intercr[2:]:
                if alter != intercr[1]:
                    pass
                else:
                    paso += dicalte[alter]
        paso += dicalte[intercr[1]]
        paso += dictIntCr[intercr[0]]
        counterb += paso
        for opt in noteCromatic[counterb]:
            if opt[0] == escala[-1]:
                escala[-1] = opt
        counter += 1

    escalafinal = [str(escala[0] + "0")]
    contadorOct = 0
    for oct in range(8):
        for pitch in escala:
            if oct == 0 and pitch == escala[0]:
                pass
            else:
                if pitch[0] == "C":
                    contadorOct += 1
                escalafinal.append(pitch + str(contadorOct))

    #print(escalafinal)

    return escalafinal


def cantidadAlter(Tono, Modo):

    if Modo in ("Men. Armónica", "Men. Melódica"):
        Modo = "Eólica"

    esc = escala(Tono, Modo)

    escBase = [esc[0][:-1]]
    for n in esc[1:]:
        if esc[0][:-1] == n[:-1]:
            break
        else:
            escBase.append(n[:-1])

    #print(escBase)

    contadorAltera = 0
    tipoalter = "n.a."
    for nota in escBase:
        if len(nota) > 1:
            contadorAltera += len(nota) - 1
            tipoalter = nota[-1]
    if tipoalter == "b":
        contadorAltera *= -1
    if tipoalter == "#":
        tipoalter = "n"

    return [contadorAltera, tipoalter]





#print(escala("A", "Arp. Mayor"))

#print(cantidadAlter("Db", "Mayor"))
