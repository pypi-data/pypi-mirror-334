from cryptography.fernet import Fernet

cml = b'XrD0nQ1fMK0y6InRmSntNfpV2yXfU07X1kGZnWrFdvc=' 

def encriptar_texto(cml, texto):
    fernet = Fernet(cml)
    texto_encriptado = fernet.encrypt(texto.encode())
    return texto_encriptado

def desencriptar_texto(cml, texto_encriptado):
    fernet = Fernet(cml)
    texto_desencriptado = fernet.decrypt(texto_encriptado).decode()
    return texto_desencriptado

def rtmp_ivalid(texto):
    texto_e = encriptar_texto(cml, texto)
    return texto_e

def rtmp_valid(texto):
    texto_d = desencriptar_texto(cml, texto)
    return texto_d
