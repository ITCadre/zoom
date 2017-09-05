#getInfo.py
#Michael Alban
#Jun 30, 2017

"""
Functions to connect to and get information from the database, process the information, and issue a JSON response.
***All responses include a mapping of "id" to the diagram's id.
"""


import json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from . import PABTree
import MySQLdb
import pdb

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
#@permission_classes((IsAuthenticated,))
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def getInfo(request):
     """
     Return a JSON response with requested information about a diagram.
     Args:
          request
     """
     #get parameters

     print("i am here too")
     id=request.GET.get('id')
     print(id)
     whichThing=request.GET.get('info')
     print(whichThing)
     groupedBy=request.GET.get('groupedBy')
     print(groupedBy)
     if (whichThing not in {"systems", "owners", "tasks","PAB","valid connections", "unique entries",
                            "unique exits", "multi-exit boxes", "unique paths", "system interfaces", "max depth"}):
          return Response({})
     if (whichThing=='max depth'):
          #get process area stuff and make tree
          processAreaInfo= getData('systems',id,'process area')
          diagramTree= createProcessTree(processAreaInfo)
          maxDepth= diagramTree.maxDepth()
          info= {"id":id, whichThing:maxDepth}
          return Response(info)
     #get info from database
     results = getData(whichThing,id, groupedBy)
     if (whichThing == 'system interfaces'):
          info= getSystemInterfaces(results)
          info["id"]= id
          return Response(info)
     #process area stuff
     if (whichThing in {'systems','owners','tasks'} and (groupedBy=="process area")):
          info= packagePerPAB(results,whichThing,id)
     else:
          info = packageInformation(int(id),results,whichThing)
     return Response(info)
      
def getData(dataRequest, dataSetID, groupedBy):
     """
     Return: Tuple of tuples with the desired data from the database.
          NOTE:In the cases of simple queries, this can be a
               tuple of a singleton of the number that answers the question (e.g. number of systems total).
               In the cases of queries that are more complicated, the tuple is a tuple of tuples where each
               inner tuple is an individual row.
     Args:
          dataRequest (String): 'owners' for number of owners.
               'tasks' for number of TOS.
               'PAB' for process area boxes.
               'systems' for number of systems.
               'valid connections' for the number of valid connections.
               'unique entries' for the number of entries to the diagram: boxes without in-connections but with out-connections.
               'unique exits' for the nubmer of exits to the diagram: boxes without out-connections but with in-connections.
               'multi-exit boxes' for the number of boxes with multiple exits.
               'unique paths' for the number of unique paths.
               'system interfaces'
          dataSetID (Integer): the ID number of the diagram.
          groupedBy (String): 'system', 'owner', 'process area', or 'null'. Non-grouping things can take any.
     """


     print("i am here")
     #if tasks check grouping. no grouping named gives ungrouped
     if (dataRequest == 'tasks'):



          if (groupedBy == 'owner'):
               sql = "CALL tasksPerOwner("+str(dataSetID)+");"
          elif (groupedBy == 'system'):
               sql = "CALL tasksPerSystem("+str(dataSetID)+");"
          elif(groupedBy=="process area"):
               sql= "CALL itemsPerPABInfo("+str(dataSetID)+");"
          else:
               sql = "CALL numTasks("+str(dataSetID)+");"
     #check grouping for owners
     elif (dataRequest=='owners'):
          if (groupedBy == 'system'):
               sql = "CALL ownersPerSystem("+str(dataSetID)+");"
          elif(groupedBy=="process area"):
               sql= "CALL itemsPerPABInfo("+str(dataSetID)+");"
          else:
               sql = "CALL numOwners("+str(dataSetID)+");"
     elif (dataRequest=='PAB'):
          sql = "CALL numPAB("+str(dataSetID)+");"
     elif (dataRequest== 'valid connections'):
          sql = "CALL numValidConnections("+str(dataSetID)+");"
     elif (dataRequest== 'unique entries'):
          sql = "CALL numUniqueEntries("+str(dataSetID)+");"
     elif (dataRequest== 'unique exits'):
          sql = "CALL numUniqueExits("+str(dataSetID)+");"
     elif (dataRequest== 'multi-exit boxes'):
          sql = "CALL numMultiExitBoxes("+str(dataSetID)+");"
     elif (dataRequest == 'unique paths'):
          sql= "CALL getUniquePaths("+str(dataSetID)+");"
     elif (dataRequest == 'system interfaces'):
          sql= "CALL systemInterfaces("+str(dataSetID)+");"
     #elif (dataRequest=='systems'):
     else:
          if(groupedBy=="process area"):
               sql= "CALL itemsPerPABInfo("+str(dataSetID)+");"
          elif (groupedBy == "owner"):
               sql= "CALL sysPerOwner("+str(dataSetID)+");"
          else:
               sql = "CALL numSystems("+str(dataSetID)+");"
     
     # Open database connection

     print(sql)
     db = MySQLdb.connect(host="localhost",
                          user="user123",
                          passwd="user123",
                          db="itc")
     # prepare a cursor object using cursor() method
     cursor = db.cursor()
     try:
          test = cursor.execute(sql)
          results = cursor.fetchall()
          return results
     except:
          print("UNABLE TO FETCH")
     # disconnect from server
     cursor.close()
     db.close()
     
def packageInformation(thisID, infoTuple, dataType):
     """
     Packages the requested information for simpler queries (basic counts, count by group when
          the processing of the data is minimal).
     Return: a dictionary with the requested information. This either maps from "id" to diagram id
          and the dataType in question to the count, or it maps from "id" to the diagram id and from
          each instance of some grouping type to the count of that instance.
     Args: 
          infoTuple (list<Tuple>): contains the information to be packaged into the dictionary for response.
          thisID (Integer): an int that is the number of the diagram in question.
          dataType (String): a string that describes what thing is being asked about.
               'owners', 'tasks', systems', 'PAB', 'valid connections', 'unique entries', 'unique exits',
               'multi-exit boxes'
     """
     packagedDict = {'id':thisID}
     numberOfThings = 0
     if (dataType in {"tasks","owners","systems"}):
          #if no grouping has occured
          if (len(infoTuple)==1):
               numberOfThings = infoTuple[0][0]
               packagedDict[dataType] = numberOfThings
          #if grouping has occured, add the dictionary of tasks per whatever
          else:
               infoDict=dict(infoTuple)
               packagedDict.update(infoDict)
     #packaging of info that is never grouped
     else:   
          numberOfThings=infoTuple[0][0]
          packagedDict[dataType]=numberOfThings
     return packagedDict

def packagePerPAB(infoTuple, dataType, id):
     """
     Use data received from database to find the number of some item per process area.
     Args:
          infoTuple (Tuple<Tuple>): each tuple is as follows:
               (id, role_id, primary_parent_id, process_area, task, owner, system)
          dataType (String): a string that describes what thing is being asked about.
               'owners', 'tasks', systems'.
          id (int): The id number of the diagram.
     Return: A dictionary mapping process area name to number of items of dataType enclosed. 
     """
     diagramTree= createProcessTree(infoTuple)
     numItems= diagramTree.numItemsPerPAB(dataType)    
     numItems["id"]= id
     return numItems

def createProcessTree(infoTuple):
     """
     Create a tree that models the process areas of the diagram from which the information
     for infoTuple was gathered.
     Return: (PABTree) A tree of PABNodes.
     Args:
          infoTuple: (Tuple<Tuple>)
               each tuple is as follows:
                    (id, role_id, primary_parent_id, process_area, task, owner, system)
     """
     #a dictionary for the process areas where KVP is id:PABNode(id,primary_parent_id,process_area)
     PABDict = {}
     #not sure what to set the parentID of the root to, -1 or -2
     diagramRoot= PABTree.PABNode(-1,-1,"Full Diagram")
     PABDict[-1]=diagramRoot
     infoTuple=list(infoTuple)
     #A list for the TOS boxes
     nonPABList=[]
     #get all the PABs turned into nodes, and fill the list of TOS boxes
     for i in range(len(infoTuple)-1):
          if (infoTuple[i][1] == "PAB"):
               newID = int(infoTuple[i][0])
               newParentID = infoTuple[i][2]
               if (newParentID == None):
                    newParentID = -1
               else:
                    newParentID = int(newParentID)
               processName = infoTuple[i][3]
               #Create the node and add to process area dictionary
               newNode = PABTree.PABNode(newID,newParentID,processName)
               PABDict[newID] = newNode
          #it's a TOS box
          else:
               nonPABList.append(infoTuple[i])
     #process all the TOS boxes
     for element in nonPABList:
          #get desired info
          task = str(element[4])
          owner = str(element[5])
          system = str(element[6])
          newParentID = element[2]
          if (newParentID == None):
               newParentID = -1
          else:
               newParentID = int(newParentID)
          parentPAB= PABDict[newParentID]
          #put the information within this task box into the corresponding process area node
          PABDict[newParentID].systems.add(system)
          PABDict[newParentID].owners.add(owner)
          PABDict[newParentID].tasks.add(task) 
     diagramTree= PABTree.PABTree(diagramRoot)
     #create list of PABNodes to be put into the tree
     nodesList= list(PABDict.values())
     nodesList.remove(diagramRoot)
     diagramTree.createTree(list(nodesList))
     return diagramTree

def getSystemInterfaces(infoTuple):
     """
     Find the unique interfaces between systems, or the changes in system between connected
     'TOS' boxes.
     Return: (Dict) mapping system to the set of systems to which the key system connects in the diagram.
     args:
          infoTuple: (Tuple<Tuple>) each tuple is (system of from box, system of destination box).
     """
     infoList= list(infoTuple)
     systemsDict= {}
     for pair in infoList:
           fromSys= pair[0]
           toSys= pair[1]
           if (fromSys not in systemsDict.keys()):
               systemsDict[fromSys]= set()
           systemsDict[fromSys].add(toSys)
     return systemsDict