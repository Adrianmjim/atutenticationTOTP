# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 20:32:46 2017

@author: Propietario
"""
from pymongo import MongoClient
import uuid
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

