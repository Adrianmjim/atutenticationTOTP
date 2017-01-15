# -*- coding: utf-8 -*-

#
# CABECERA AQUI
#


from bottle import run, post, request
# Resto de importaciones
from pymongo import MongoClient
import hashlib 
import utils
import onetimepass
import urllib
##############
# APARTADO 1 #
##############

# 
# Explicación detallada del mecanismo escogido para el almacenamiento de c
# contraseñas, explicando razonadamente por qué es seguro
#


@post('/signup')
def signup():
    nickname = request.forms.get('nickname')
    name = request.forms.get('name')
    country = request.forms.get('country')
    email = request.forms.get('email')
    password = request.forms.get('password')
    password2 = request.forms.get('password2')
    if password != password2:
        return "<b>Las contraseñas no coinciden</b>"
    elif utils.getUser(nickname) != None:
        return "<b>El alias del usuario ya existe</b>"
    salt = utils.saltGenerator(len(password))
    m = hashlib.sha256()
    m.update(password)
    m.update(salt)
    m.update("123456789")
    password = m.hexdigest()
    utils.insertUser(nickname,name,email,country,password,salt)
    
@post('/change_password')
def change_password():
    nickname = request.forms.get('nickname') 
    old_password = request.forms.get('old_password')
    new_password = request.forms.get('new_password')
    user = utils.getUser(nickname)
    if user == None:
        return "<b>Usuario o contraseña incorrectos</b>"
    m = hashlib.sha256()
    m.update(old_password)
    m.update(user['salt'])
    m.update("123456789")
    auxPassword = m.hexdigest()
    if auxPassword == user['password']:
        salt = utils.saltGenerator(len(new_password))
        m = hashlib.sha256()
        m.update(new_password)
        m.update(salt)
        m.update("123456789")
        auxPassword = m.hexdigest()
        utils.modifyUser(nickname,auxPassword,salt)
        return "<b>La contraseña del usuario "+nickname+" ha sido modificada</b>"
    else:
        return "<b>Usuario o contraseña incorrectos</b>"
    
@post('/login')
def login():
    nickname = request.forms.get('nickname')
    password = request.forms.get('password')
    user = utils.getUser(nickname)
    if user == None:
        return "<b>Usuario o contraseña incorrectos</b>"
    m = hashlib.sha256()
    m.update(password)
    m.update(user['salt'])
    m.update("123456789")
    auxPassword = m.hexdigest()
    if auxPassword == user['password']:
        return "<b>Bienvenido "+user['name']+"</b>"
    else:
        return "<b>Usuario o contraseña incorrectos</b>"

##############
# APARTADO 2 #
##############


def gen_secret():
    # >>> gen_secret()
    # '7ZVVBSKR22ATNU26'
    return utils.secretGenerator()
    
    
def gen_gauth_url(app_name, username, secret):
    # >>> gen_gauth_url( 'GIW_grupoX', 'pepe_lopez', 'JBSWY3DPEHPK3PXP')
    # 'otpauth://totp/pepe_lopez?secret=JBSWY3DPEHPK3PXP&issuer=GIW_grupoX
    return "otpauth://totp/"+username+"?secret="+secret+"&issuer="+app_name
        

def gen_qrcode_url(gauth_url):  
    # >>> gen_qrcode_url('otpauth://totp/pepe_lopez?secret=JBSWY3DPEHPK3PXP&issuer=GIW_grupoX')
    # 'http://api.qrserver.com/v1/create-qr-code/?data=otpauth%3A%2F%2Ftotp%2Fpepe_lopez%3Fsecret%3DJBSWY3DPEHPK3PXP%26issuer%3DGIW_grupoX'
    return "http://api.qrserver.com/v1/create-qr-code/?data="+gauth_url
    


@post('/signup_totp')
def signup_totp():
    nickname = request.forms.get('nickname')
    name = request.forms.get('name')
    country = request.forms.get('country')
    email = request.forms.get('email')
    password = request.forms.get('password')
    password2 = request.forms.get('password2')
    if password != password2:
        return "<b>Las contraseñas no coinciden</b>"
    elif utils.getUser(nickname) != None:
        print utils.getUser(nickname)
        return "<b>El alias del usuario ya existe</b>"
    salt = utils.saltGenerator(len(password))
    m = hashlib.sha256()
    m.update(password)
    m.update(salt)
    m.update("123456789")
    password = m.hexdigest()
    secret = gen_secret()
    utils.insertUserTotp(nickname,name,country,email,password,salt,secret)
    qr = urllib.urlopen(gen_qrcode_url(gen_gauth_url("GIW_grupo13", nickname, secret))).read()
    return "<b>"+nickname+ " "+secret+"</b>" + qr 
    
        
@post('/login_totp')        
def login_totp():
    nickname = request.forms.get('nickname')
    password = request.forms.get('password')
    totp= request.forms.get('totp')
    user = utils.getUser(nickname)
    if user == None:
        return "<b>Usuario o contraseña incorrectos</b>"
    m = hashlib.sha256()
    m.update(password)
    m.update(user['salt'])
    m.update("123456789")
    auxPassword = m.hexdigest()
    if auxPassword == user['password'] and onetimepass.valid_totp(token=totp, secret=user['secret']):
        return "<b>Bienvenido "+user['name']+"</b>"
    else:
        return "<b>Usuario o contraseña incorrectos</b>"

    
if __name__ == "__main__":
    # NO MODIFICAR LOS PARÁMETROS DE run()
    run(host='localhost',port=8080,debug=True)