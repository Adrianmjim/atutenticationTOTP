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
    return ale
    
def insertUser(nickName,name,email,country,password,salt):
    m=MongoClient()
    db=m.giw
    db.users.insert({name:name,
                     nickName:nickName,
                     email:email,
                     country:country,
                     password:password,
                     salt:salt})
