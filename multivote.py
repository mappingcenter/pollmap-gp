#################################
# VOTE SCRIPT v1.6.1
# Alex Yule 3/2/11
# last updated 9/8/11 4pm for college football fanmap (before that: 4/13/11 12:32 AM)
# fixed error in handling of old-style votes. should now work for any kind of fanmap
# for simple incremental voting, pass in votes as space-separated list of fields to increment "CHOICE01 CHOICE03"
# otherwise, semicolon-separated set of space-separated field/value pairs "CHOICE01 20; CHOICE02 30; CHOICE03 40"
#################################

import arcpy
from datetime import datetime
from sys import exc_info # disable for prod
import traceback # disable for prod

def status(msg): #logging function
    print msg
    arcpy.AddMessage(msg)
    arcpy.SetProgressorLabel(msg)
    X = 3

#CONFIG 
db = r"\\niflheim\data\SDE_CONNECTIONS\niflheim_express1_collegefootball_webeditor.sde"
features = db  + "\\collegefootball.DBO.zips_winkel"
votes_table = db + "\\collegefootball.DBO.votes"

uid_field = "COOKIE"
location_field = "LOCATION" #"POSTAL" # "GEONAMEID" # both the votes and zips_winkel (eventually to become generic "places") must have a field called "LOCATION"

# don't change stuff past here
location = arcpy.GetParameterAsText(0) or "14256" #or "T7A"
uid = arcpy.GetParameterAsText(1) or None
input_votes = arcpy.GetParameterAsText(2) or "CHOICE01"

search_where = location_field+" = '"+location+"'"

#process vars
votes = []
if (input_votes.count(";")): #if vote string is in new format
    for vote in input_votes.split(";"):
        votes.append(vote.split())
else: # otherwise fill new votes list with default increment value of 1 to mimic previous script
    for vote in input_votes.split():
        votes.append([vote, '1'])
status("Votes processed: "+str(votes))


# votes --> [['CHOICE01', '60'], ['CHOICE02', '39'], ['CHOICE03', '1']]

def updateFeatures(_features):
    status("Updating Features: "+_features)
    status("Where: "+search_where)
    cursor_update = arcpy.UpdateCursor(_features, search_where) #needs error handling to deal with db lock?
    update_row = cursor_update.next()
    
    for vote in votes:
        status("Incrementing field: "+vote[0]+" by "+vote[1])
        value = update_row.getValue(vote[0])
        if value == None:
            value = 0
        update_row.setValue(vote[0], value+int(vote[1]))
        #print update_row.getValue(field)
    
    cursor_update.updateRow(update_row)
    del update_row
    del cursor_update
    status("Vote successfully added to feature class")

try: 
    status("Processing votes for Location: "+location)
    status("Votes: "+str(votes))
    
    cursor_insert = arcpy.InsertCursor(votes_table)
    vote_row = cursor_insert.newRow()
    for vote in votes:
        status("Inserting vote for "+vote[0])
        vote_row.setValue(vote[0], vote[1])
        status("Value set")
    status("Setting datetime field: "+str(datetime.now()))

    vote_row.DATETIME = datetime.now()
    vote_row.setValue(location_field, location)
    vote_row.setValue(uid_field, uid)
    cursor_insert.insertRow(vote_row)
    del vote_row
    del cursor_insert
    status("Vote successfully added to votes_table")

    updateFeatures(features)
    #updateFeatures(polys)
    
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
            
#except: # disable all this for prod
    ## Get the traceback object
    ##
    #tb = exc_info()[2]
    #tbinfo = traceback.format_tb(tb)[0]
    
    ## Concatenate information together concerning the error into a message string
    ##
    #pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(exc_info()[1])
    #msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

    ## Return python error messages for use in script tool or Python Window
    ##
    #arcpy.AddError(pymsg)
    #arcpy.AddError(msgs)

    ## Print Python error messages for use in Python / Python Window
    ##
    #print pymsg + "\n"
    #print msgs 
    

    



    
