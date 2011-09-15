# ---------------------------------------------------------------------------
# PollMap Config SCRIPT v0.1
# Alex Yule 9/15/11
# Created on: 2011-09-15
# Description: Builds and returns a PollMap config object
# ---------------------------------------------------------------------------

import arcpy
import pyodbc
from string import join

def status(msg): #logging function
    print msg
    arcpy.AddMessage(msg)
    arcpy.SetProgressorLabel(msg)

#db = r"D:\Data\SDE_CONNECTIONS\niflheim_express1_collegefootball_webeditor.sde"
dsn = "sqlexpress1"
db = "collegefootball"

connectStr = 'DSN='+dsn+';DATABASE='+db
configTableSelect = 'COUNT LOCATION FROM '+db+'.DBO.votes'
status(connectStr)
status(configTableSelect)
connect = pyodbc.connect(connectStr)
status(connect)
cursor = connect.cursor()
cursor.execute(configTableSelect)
print cursor.fetchall()

del cursor
del connect

