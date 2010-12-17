#!/usr/bin/python2.5
"""Uses an sqlite database"""

import os,sys,re
import sqlite3
import random

def createTables(db):
    ""
    c = db.cursor()
    c.execute('''CREATE TABLE data
(id int, chan int, energy real,
 counts int, file real)''')

def linkTables(db):
    ""
    
def fillDataTable(db):
    ""
    c = db.cursor()
    
    for i in range(300):
        num1 = random.randint(0,3000)
        num2 = random.randrange(0,3000)
        counts = random.randint(0,30000)
        f = random.randint(0,10)
        res = c.execute("INSERT INTO data VALUES (?,?,?,?,?) ",(i,num1,num2,counts,f))
        print res
    
def printData(db):
    ""
    c = db.cursor()
    c.execute("SELECT * FROM data")
    
    for row in c:
        print row
    
if __name__=="__main__":
    db = sqlite3.connect(':memory:')
    
    c = db.cursor()
    
    createTables(db)
    fillDataTable(db)
    linkTables(db)
    
    printData(db)
    
    