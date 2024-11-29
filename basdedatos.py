import requests
import os


#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file
def sincronizar():
    url = "https://riedmusicapp.com/load/"
    path = os.path.join('tt', 'ltd.dtl')
    fin = open(path, 'rb')
    files = {'file': fin}
    try:
        r = requests.post(url, files=files)
        respuesta = r.status_code
        fin.close()
        return respuesta
    except:
        fin.close()
        return "problemas de conexión"