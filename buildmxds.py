#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      alex6294
#
# Created:     09/09/2011
# Copyright:   (c) alex6294 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import arcpy
import arcpy.mapping

mxd = arcpy.mapping.MapDocument('D:\\data\\FANMAP_COLLEGEFOOTBALL\\FanMap_CollegeFootball_Template.mxd')
choicesTable = arcpy.mapping.ListTableViews(mxd,"*choices*")[0]

choicesSC = arcpy.SearchCursor(choicesTable)

del choicesSC
del choicesTable
del mxd