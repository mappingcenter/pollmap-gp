# ---------------------------------------------------------------------------
# PollMap Config SCRIPT v0.1
# Alex Yule 9/15/11
# Created on: 2011-09-15
# Description: Builds and returns a PollMap config object
# ------------------------------------------------------------------------
import arcpy
import json
from string import join
from sys import exc_info # disable for prod
import traceback # disable for prod

def status(msg): #logging function
    print msg
    arcpy.AddMessage(msg)
    arcpy.SetProgressorLabel(msg)


db = arcpy.GetParameterAsText(0) or r"\\niflheim\data\SDE_CONNECTIONS\niflheim_express1_collegefootball_webeditor.sde"

if arcpy.GetParameterAsText(1) == '#' or not arcpy.GetParameterAsText(1):
    tablePrefix = db + "\\collegefootball.dbo."
else:
    tablePrefix = db + arcpy.GetParameterAsText(1)

status(db)
status(tablePrefix)

RESULT = ""
choicesTable = tablePrefix + "choices"
mapsTable = tablePrefix + "maps"
questionsTable = tablePrefix + "questions"
configTable = tablePrefix + "config"


def tableToObj(table, choicesField=''):
    status("tableToObj")
    obj = {}
    tableRows = arcpy.SearchCursor(table)
    tableFields = arcpy.ListFields(table)
    obj = []
    for row in tableRows:
        rowObj = {}
        for field in tableFields:
            if (field.name == choicesField):
                robObj[field.name] = buildChoicesObj(row.getValue(field.name))
            else:
                rowObj[field.name] = row.getValue(field.name)
        obj.append(rowObj)
    del tableRows
    del tableFields
    return obj

def buildChoicesObj(choiceStr, table=choicesTable, key='field'):
    status("buildChoicesObj")
    choicesObj = []
    choices = choiceStr.split(',')
    choicesFields = arcpy.ListFields(table)
    for choice in choices:
        choiceObj = {}
        choiceRow = arcpy.SearchCursor(table,key+"='"+choice+"'").next()
        for field in choicesFields:
            choiceObj[field.name] = choiceRow.getValue(field.name)
        choicesObj.append(choiceObj)
        del choiceRow
    return choicesObj

try:
    #configObj = tableToObj(configTable)
    configObj = {}
    configObj['maps'] = tableToObj(mapsTable)
    configObj['questions'] = tableToObj(questionsTable)

    RESULT = json.dumps(configObj)
    status(RESULT)
    arcpy.SetParameterAsText(2, RESULT)

except arcpy.ExecuteError:
    # Get the tool error messages
    #
    msgs = arcpy.GetMessages(2)

    # Return tool error messages for use with a script tool
    #
    arcpy.AddError(msgs)

    # Print tool error messages for use in Python/PythonWin
    #
    print msgs

except: # disable all this for prod
     #Get the traceback object

    tb = exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

     #Concatenate information together concerning the error into a message string

    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

    #Return python error messages for use in script tool or Python Window

    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)

    # Print Python error messages for use in Python / Python Window

    print pymsg + "\n"
    print msgs
