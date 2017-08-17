#PABTree.py
#Michael Alban
# Jul 27, 2017

class PABTree:
     """
     A tree of PABNodes where each child is a contained process area in a visio diagram.
     
     Attributes:
          root (PABNode): The root of the tree, the largest process area.
          
     """
     def __init__(self, root):
          """
          Creates an instance of PABTree.
          
          Args:
               root (PABNode): the root of this tree
          """
          self.root = root
          
     def addNode(self, node):
          """
          Add node to this tree.
          
          Args:
               node is a PABNode.
          
          Return: True if successful add, false if unsuccessful.
          """
          root = self.root
          #add if the node is child of root
          if (root.identity == node.parentID):
               root.addChild(node)
               return True
          #check children of root
          elif (root.hasChildren):
               children = root.children
               for child in children:
                    childTree = PABTree(child)
                    successCheck = childTree.addNode(node)
                    #return true for the first child that returns true
                    if (successCheck):
                         return True
          #if node cant be added to tree
          return False
     
     def createTree(self, nodeList):
          """
          create full PABTree given a root-only PABTree.
          Args
          Precondition: This tree contains only one node, the root.
          
          Return: TODO.
          """
          while (len(nodeList)>0):
               for node in nodeList:
                    if (self.addNode(node)):
                         nodeList.remove(node)
          
     def itemsInPAB(self, dataType):
          """
          Determine the unique items of dataType in this process area tree.
          Return: set of unique items of the requested dataType.
          Args:
               dataType (String): a string that describes what thing is being asked about.
                    'owners', 'tasks', systems'.
          """
          #if the root of the tree or subtree then return the set of the items
          if (not self.root.hasChildren()):
               if (dataType == "owners"):
                    return self.root.owners
               elif (dataType == "tasks"):
                    return self.root.tasks
               #DEFAULT TO GIVING SYSTEMS IF DATATYPE ARG IS NOT CORRECT
               else:
                    return self.root.systems
          #this is the root with children so count up the children's with its own
          else:
               mySetOfStuff = set()
               if (dataType == "owners"):
                    mySetOfStuff = self.root.owners
               elif (dataType == "tasks"):
                    mySetOfStuff = self.root.tasks
               #DEFAULT TO GIVING SYSTEMS IF DATATYPE ARG IS NOT CORRECT
               else:
                    mySetOfStuff = self.root.systems
               for child in self.root.children:
                    #create the tree of the child
                    childTree= PABTree(child)
                    childItems= childTree.itemsInPAB(dataType)
                    mySetOfStuff= mySetOfStuff.union(childItems)
               return mySetOfStuff
               
     def itemsPerPAB(self, dataType):
          """
          Determine the unique items of dataType per process area
          Return: Dictionary of the following structure:
               {"root PAB": {"Major PAB 1": {"minor PAB 1.1": { "self":(items)
                                                              },
                                             "minor PAB 1.2": {etc...},
                                             "self": (items)
                                            },
                             "Major PAB 2": {"minor PAB 2.1": {etc...},
                                             "self": (items)
                                            },
                            "self": (items)
                            }
               }
               "Self" indicates the items contained at the lowest level by the PAB
               that maps to the dictionary containing "self". This structure is to represent
               the tree structure.
          Args:
               dataType (String): a string that describes what thing is being asked about.
                    'owners', 'tasks', systems'.
          """
          thisRoot= self.root
          #base case: return a dictionary of the name of this process area mapped to its self dictionary,
          #     mapping "self" to the items it contains
          if (not thisRoot.hasChildren()):
               return {thisRoot.name : {"self":self.itemsInPAB(dataType)}}
          #recursive case: merge the dictionary of {root name:unique systems} with the dictionaries returned
          #     by calling itemsPerPAB on each child of root
          else:
               mySetOfStuff = set()
               if (dataType == "owners"):
                    mySetOfStuff = self.root.owners
               elif (dataType == "tasks"):
                    mySetOfStuff = self.root.tasks
               #DEFAULT TO GIVING SYSTEMS IF DATATYPE ARG IS NOT CORRECT
               else:
                    mySetOfStuff = self.root.systems
               topDict= {thisRoot.name: {"self":mySetOfStuff}}
               allChildrenDict= {}
               #go through the process for children then add their information
               for child in thisRoot.children:
                    childTree = PABTree(child)
                    childDict = childTree.itemsPerPAB(dataType)
                    allChildrenDict.update(childDict)
               topDict[thisRoot.name].update(allChildrenDict)
               return topDict
     def numItemsPerPAB(self, dataType):
          """
          Determine the number of unique items of dataType per process area.
          Return: Dictionary of the following structure:
               {"root PAB": {"Major PAB 1": {"minor PAB 1.1": { "self":(num items)
                                                              },
                                             "minor PAB 1.2": {etc...},
                                             "self": (num items)
                                            },
                             "Major PAB 2": {"minor PAB 2.1": {etc...},
                                             "self": (num items)
                                            },
                            "self": (num items)
                            }
               }
               "Self" indicates the number of items contained at the lowest level by the PAB
               that maps to the dictionary containing "self". This structure is to represent
               the tree structure.
          Args:
               dataType (String): a string that describes what thing is being asked about.
                    'owners', 'tasks', systems'.
          """
          itemPerPABDict= self.itemsPerPAB(dataType)
          thisRoot= self.root
          #Base case: a leaf.
          if (not thisRoot.hasChildren):
               keys= list(itemPerPABDict.keys())
               leaf= thisRoot.name
               leafDict= itemPerPABDict[leaf]
               leafDict["self"]= len(leafDict["self"])
               return itemPerPABDict
          #recursive case: find len of self then do numItemsPerPAB for every other entry
          else:
               #do the process for each child
               for child in thisRoot.children:
                    childName= child.name
                    itemPerPABDict[thisRoot.name][childName]= PABTree(child).numItemsPerPAB(dataType)[childName]
               itemPerPABDict[thisRoot.name]["self"]= len(itemPerPABDict[thisRoot.name]["self"])
               return itemPerPABDict
     
     def maxDepth(self):
          """
          Find the maximum depth of the tree, or the longest path between root and leaf.
          Depth is 0 at root, 1 at first generation, 2 at second, etc...
          Return (Integer): The depth.
          Args:
          
          """
          #base Case: a leaf or childless root
          if (not self.root.hasChildren()):
               return 0
          #recursive case: add one to the max depth of the deepest child tree
          else:
               maxChildDepth= 0
               for child in self.root.children:
                    childTree= PABTree(child)
                    childDepth= childTree.maxDepth()
                    maxChildDepth= max(childDepth, maxChildDepth)
               return 1+maxChildDepth
     
class PABNode:
     """
     An object containing information about a process area box in a visio diagram
      
     Attributes:
          identity (Integer): The id of this process area box.
          parentID (Integer): The ID of the process area box that contains this one.
          parent (PABNode): The process area that contains this one.
          name (String): The name of the process area.
          children (set<PABNode>): The process areas contained within this one.
          systems (list<String>): The systems within this process area where this process area
               is the closest parent.
          owners (list<String>): The owners within this process area where this process area
               is the closest parent.
          tasks (list<Integer>): The task box id numbers of the task boxes contained within this process area
               where this process area is the closest parent.
          
     """
     
     def __init__(self, iden=-1, parentID= -1,name=""):
          """
          Initializes an PABNode instance.
          
          Args:
               iden (Integer): Identity of this PABNode.
               parentID (Integer): Identity of the process area that contains this one.
               parent (PABNode): Parent of this PABNode.
               name(String): the Name of this process area.
               children (set<PABNode>): The children of this PABNode.
               systems (set<String>)
               owners (set<String>)
               Tasks (set<String>)
          """
          self.identity = iden
          self.parentID = parentID
          self.name = name
          self.parent = None
          self.children = set()
          self.systems = set()
          self.owners = set()
          self.tasks = set()
          
          
     def __eq__(self,other):
          """
          Returns True if the two PABNodes have the same identity and .
          """
          return (self.identity==other.identity and self.parentID==other.parentID) 
     
     def __neq__(self,other):
          """
          Returns True if the two PABNodes have different identity properties.
          """
          return (self.identity!=other.identity or self.parentID!=other.parentID)
     
     def __hash__(self):
          """
          hash for PABNodes is XOR of hash of its identity, hash of its parent, and the tuple of the hashes of those two.
          """
          return (hash(self.identity) ^ hash(self.parentID) ^ hash((hash(self.identity),hash(self.parentID))))
          
          
     def isParentOf(self, other):
          """
          Determines whether self is a parent of other.
          Args:
               other (PABNode): The possible child.
               
          Returns (Boolean):
               Returns True if self is a parent of other, False if not.
          """
          return other.parent==self
         
     def addChild(self,other):
          """
          Makes other a child of self. The child's parentID MUST match the identity of the parent.
          Args:
               other (PABNode)
          
          Return: True if successful, False if unsuccessful
          """
          if (other.parentID==self.identity):
               other.parent = self
               self.children.add(other)
               return True
          return False
          
     def hasChildren(self):
          """
          checks if this node has children.
          
          Return: true if this node has children, false otherwise.
          """
          return len(self.children)>0
          
          
          
          
          
          