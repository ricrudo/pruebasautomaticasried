import requests
import os

def sinc(filename):
    conf_directory = "tt"
    if not os.path.exists(conf_directory):
        os.makedirs(conf_directory)
    path = os.path.join("tt", filename)
    url = 'https://riedmusicapp.com/test1/upload/' + filename
    try:
        r = requests.get(url, allow_redirects=True)
        respuesta = r.status_code
        if str(respuesta) == "200":
            l = open(path, 'wb')
            l.write(r.content)
            l.close()
        return respuesta
    except:
        return "problemas de conexión"