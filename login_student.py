import requests

def student_login(instructor, student, password):

    login_data = {'instructor': instructor,
                  'student': student,
                  'password': password}

    with requests.Session() as s:
        url = "https://riedmusicapp.com/instructorlogin"
        timeout = 5
        try:
            request = requests.get(url, timeout=timeout)
            print("Connected to the Internet")
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("No internet connection.")
            return ["Error de conexion"]
        r = s.post(url, data=login_data)
        respuesta = r.content
        if str(respuesta).split("<p>")[1].split("</p>")[0] == "Bienvenido a RiedMusicApp":
            nombreestudiante = str(respuesta).split("<p>")[2][:-4]
            archivoID = str(respuesta).split("<p>")[3][:-5]
            file = open('conexion.dtl', 'w')
            file.write(nombreestudiante + '$!$' + archivoID)
            file.close()
            return ["Bienvenido a RiedMusicApp", nombreestudiante, archivoID]
        elif str(respuesta).split("<p>")[1].split("</p>")[0] == "Cuenta en uso":
            return ["Cuenta en uso"]
        elif str(respuesta).split("<p>")[1].split("</p>")[0] == "Usuario no registrado en el sistema":
            return ["instructor o constraseña incorrecta"]
        else:
            return ["Error de conexión"]
