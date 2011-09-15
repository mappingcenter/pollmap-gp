# ---------------------------------------------------------------------------
# PollMap Config SCRIPT v0.1
# Alex Yule 9/15/11
# Created on: 2011-09-15
# Description: Builds and returns a PollMap config object
# ---------------------------------------------------------------------------

import arcpy
import json
from string import join

def status(msg): #logging function
    print msg
    arcpy.AddMessage(msg)
    arcpy.SetProgressorLabel(msg)

db = r"\\niflheim\data\SDE_CONNECTIONS\niflheim_express1_collegefootball_webeditor.sde"
tablePrefix = db + "\\collegefootball.dbo."

choicesTable = tablePrefix + "choices"
mapsTable = tablePrefix + "maps"
questionsTable = tablePrefix + "questions"
configTable = tablePrefix + "config"

questionsRows = arcpy.SearchCursor(questionsTable)
questionFields = arcpy.ListFields(questionsTable)
for row in questionsRows:
    for field in questionFields:
        print "%s: %s" % (field.name, row.getValue(field.name))

del questionsRows