from cryptography.fernet import Fernet
import json

cml = b'XrD0nQ1fMK0y6InRmSntNfpV2yXfU07X1kGZnWrFdvc='

def encriptar_texto(cml, texto):
    fernet = Fernet(cml)
    texto_encriptado = fernet.encrypt(texto.encode())  
    return texto_encriptado

def desencriptar_texto(cml, texto_encriptado):
    fernet = Fernet(cml)
    texto_desencriptado = fernet.decrypt(texto_encriptado).decode()  
    return texto_desencriptado

def encriptar_dict(cml, diccionario):
    diccionario_json = json.dumps(diccionario)
    texto_encriptado = encriptar_texto(cml, diccionario_json)
    return texto_encriptado

def desencriptar_dict(cml, texto_encriptado):
    diccionario_json = desencriptar_texto(cml, texto_encriptado)
    diccionario = json.loads(diccionario_json)
    return diccionario

def rtmp_ivalid(texto):
    if isinstance(texto, dict):
        return encriptar_dict(cml, texto)
    return encriptar_texto(cml, texto)

def rtmp_valid(texto):
    try:
        diccionario = desencriptar_dict(cml, texto)
        return diccionario
    except Exception as e:
        texto_d = desencriptar_texto(cml, texto)
        return texto_d
