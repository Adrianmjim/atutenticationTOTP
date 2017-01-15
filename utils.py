# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 20:32:46 2017

@author: Propietario
"""
from pymongo import MongoClient
import uuid
import random
def saltGenerator(longi):
    ale=uuid.uuid4().hex
    while(len(ale)<longi):
        ale+=uuid.uuid4().hex
    return str(ale)

def getDB():
    m=MongoClient()
    db=m.giw
    return db
    
def insertUser(nickName,name,email,country,password,salt):
    db=getDB()
    db.users.insert_one({"name":name,
                     "_id":nickName,
                     "email":email,
                     "country":country,
                     "password":password,
                     "salt":salt})
    
def deleteUser(nickName):
    db=getDB()
    db.users.delete_one({"_id":nickName})
    
def getUser(nickName):
    db=getDB()
    user=db.users.find_one({"_id":nickName})
    return user

def modifyUser(nickName,passW,salt):
    db=getDB()
    db.users.update({"_id":nickName},{"$set":{"password":passW, "salt":salt}})
def secretGenerator():
    claves = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z',26:'2',27:'3',28:'4',29:'5',30:'6',31:'7'}
    salida = ""
    for i in range(16):
        salida +=claves[random.randint(0,31)]
    return salida
def insertUserTotp(nickName,name,email,country,password,salt,secret):
    db=getDB()
    db.users.insert_one({"name":name,
                     "_id":nickName,
                     "email":email,
                     "country":country,
                     "password":password,
                     "salt":salt,
                     "secret":secret})