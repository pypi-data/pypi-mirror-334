// "dependencies": ["core","policy", "ros", "vision"],
import { clusterType } from 'common-types';

export const fcCluster = (id): clusterType[] => ([
  {
     "id": id,
     "cluster": "fc",
     "type": "ERRobotLocation",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "ERRobotLocation",
           "@documentation": { "@title": "ERRobotLocation", "@description": "ERRobotLocation corresponding to ERRobotLocation.msg i.e. geometry_msgs/Pose2D (version:v022)",
           "@authors": ["William A Coolidge"]},
           /*
             timeStamp from header
             robotId in name with timeStamp, chosen not to duplicate data in a property as per ros.msg equivalent
           */
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "@inherits": "Pose",
           "mobileRobotPose": "Pose2D"
       }
  },
  {
    "id": id,
     "cluster": "fc",
     "type": "FCPose",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "FCPose",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "@documentation": { "@title": "FCPose", "@description": "FCPose is the concrete type defining the coordinates and cleaning state of an object Presence, i.e. a SensedEntity (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": ["Pose", "Cartesian", "Orientation"],
           /*
           "orientation": {
             "@type": "Array",
             "@dimensions": 2,
             "@class": "xsd:decimal"
           }
           */
       }
  },
  {
    "id": id,
     "cluster": "fc",
     "type": "FCContour",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "FCContour",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "@documentation": { "@title": "FCContour", "@description": "FCContour is the concrete type defining the contour coordinates of a shape (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": ["Polygon", "Location"]
       }
  },
  {
    "id": id,
     "cluster": "fc",
     "type": "Zone",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "Zone",
           "@documentation": { "@title": "Zone", "@description": "Zone is the abstract type for the 4 corner x,y coordinates of a rectangle (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@abstract": [],
           "@inherits": "Geometry",
           "rectangle": {
             "@type": "Array",
             "@dimensions": 1,
             "@class": "Point"
           }
           /*
           "rectangle": {
             "@type": "Array",
             "@dimensions": 2,
             "@class": "xsd:decimal"
           }
           */
       }
  },
  {
    "id": id,
     "cluster": "fc",
     "type": "FCZone",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "FCZone",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "@documentation": { "@title": "FCZone", "@description": "FCZone is the concrete type defining the coordinates and cleaning state of a zone and the aggregate of FCPoses in that zone (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": ["Zone", "EntitySet"]
       }
  },
    /* duplicate
  {
     "cluster": "fc",
     "type": "AssetState",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "AssetState",
           "@documentation": { "@title": "AssetState", "@description": "AssetState is the type characterizing the status of the entities of work for the facility cobot (version:v022)"},
           "@inherits": "TemporalEntity",
           "@abstract": [],
           "asset": {
             "@type"  : "Optional",
             "@class" : "PhysicalEntity"
           }
       }
  },
   */

  {
    "id": id,
     "cluster": "fc",
     "type": "ServiceState",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "ServiceState",
           "@documentation": { "@title": "ServiceState", "@description": "ServiceState is the type characterizing the service status of the entities of work for the facility cobot (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "EntityState",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "wasClearedAt": {
             "@type": "Optional",
             "@class": "xsd:string"
           },
           "wasCleanedAt": {
             "@type": "Optional",
             "@class": "xsd:string"
           },
           "serviceStateOf": {
             "@type": "Set",
             "@class": "PhysicalEntity"
           }
       }
  },
  {
    "id": id,
    "cluster": "fc",
    "type": "FCAssetShell",
    "version":"v022",
    "woql": {
          "@type": "Class",
          "@id": "FCAssetShell",
          "@documentation": { "@title": "FCAssetShell", "@description": "Asset Admin Shell for FacilityCobot, the type model for world services per se (version:v022)",
          "@authors": ["William A Coolidge"]},
          "@inherits": "AssetShell",
          "@key": { "@type": "Lexical", "@fields": ["name"] },
          /*"state": "State",
          "heathSummary": {
            "@type": "Optional",
            "@class": "xsd:string"
          },*/
          "availableOperations": {
            "@type": "Array",
            "@dimensions": 1,
            "@class": "ERStateOperation"
          },
          //"asset": "PhysicalEntity"
      }
 },
  {
    "id": id,
     "cluster": "fc",
     "type": "FCShellOperation",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "FCShellOperation",
           "@documentation": { "@title": "FCShellOperation", "@description": "FC ShellOperation models operations for configuration, capability/skill matching, monitoring, and specification  (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "ShellOperation",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "action": "ERStateOperation",
          /*
           "param": {
            "@type": "Optional",
            "@class": "xsd:string"
            },
            "actor": "AssetShell"
          */
       }
  },
  {
    "id": id,
     "cluster": "fc",
     "type": "WorkItemTask",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "WorkItemTask",
           "@documentation": { "@title": "WorkItemTask", "@description": "WorkItemTask is derived from WorkItemTask.msg with operation and param from Policy.action and Policy.param. It is associated with an entity via PolicyOn (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "Task",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "parentPolicy": "Policy"
       }
  },
  {
    "id": id,
     "cluster": "fc",
     "type": "ProductionOperation",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "ProductionOperation",
           "@documentation": { "@title": "ProductionOperation", "@description": "abstract operation type for facility cobot (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@abstract": [],
           "@inherits": "AbstractEntity"
       }
  },
  {
    "id": id,
     "cluster": "fc",
     "type": "FCState",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "FCState",
           "@documentation": { "@title": "FCState", "@description": "abstract type for reporting on the engine of application state (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "State",
           "@key": { "@type": "Lexical", "@fields": ["subSystem", "state", "operation"] },
           /*
           "actor": {
             "@type": "Optional",
             "@class": "CyberPhysicalActor"
           },
           "subSystem": "xsd:string",
           "state": {
             "@type": "Optional",
             "@class": "xsd:string"
           },
           */
           "operation": {
             "@type": "Optional",
             "@class": "ERStateOperation"
           },
           /*
           "message": {
             "@type": "Optional",
             "@class": "xsd:string"
           },
           "progress": {
             "@type": "Optional",
             "@class": "xsd:decimal"
           },
           "workItem": {
             "@type": "Optional",
             "@class": "PhysicalEntity"
           },
           */
           "availableOperations": {
             "@type": "Set",
             "@class": "ERStateOperation"
           },
           /*
           "error": {
             "@type": "Optional",
             "@class": "Error"
           },
           */
       }
  },
  {
    "id": id,
     "cluster": "fc",
     "type": "FCSubSystemState",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "SubSystemState",
           "@documentation": { "@title": "ERState", "@description": "concrete type for reporting on ER's engine of application state (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "State",
           //"@subdocument": [],
           "@key": { "@type": "Lexical", "@fields": ["name"] },
       }
  },
  {
    "id": id,
     "cluster": "fc",
     "type": "ERRobotState",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "ERRobotState",
           "@documentation": { "@title": "ERRobotState", "@description": "concrete type for reporting on ER's engine of application state (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "State",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
       
           "subSystems": {
             "@type": "Set",
             "@class": "SubSystemState"
           },
           "robotId": {
             "@type": "Optional",
             "@class": "xsd:string"
           },
           "batteryPercentage": {
             "@type": "Optional",
             "@class": "xsd:decimal"
           }
       }
  },
  {
    "id": id,
     "cluster": "fc",
     "type": "FCPolicies",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "FCPolicies",
           "@documentation": { "@title": "FCPolicies", "@description": "the policy sets for the facility cobot (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "PolicySet",
           "@key": { "@type": "Lexical", "@fields": ["name"] }
       }
  },
  {
    "id": id,
     "cluster": "fc",
     "type": "FCFleetPolicies",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "FCFleetPolicies",
           "@inherits": "PolicySet",
           "@key": { "@type": "Lexical", "@fields": ["name"] }
       }
  },
  /*
  {
    "id": id,
     "cluster": "fc",
     "type": "Operation",
     "version":"v022",
     "woql": {
           "@type": "Enum",
           "@id": "Operation",
           "@documentation": { "@title": "Operation", "@description": "abstract enum type defining the operation API (version:v022)"},
           "@abstract": []
       }
  },
  */
  {
    "id": id,
     "cluster": "fc",
     "type": "ERStateOperation",
     "version":"v022",
     "woql": {
           "@type": "Enum",
           "@id": "ERStateOperation",
           "@inherits": "Operation",
           "@documentation": { "@title": "ERStateOperation", "@description": "enum type defining the operation set supported by the FC ER API (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@value": [
             "goto",
             "clean",
             "clear",
             "scan",
             "clear-n-clean",
             "start",
             "stop",
             "no-op",
             "reset",
             "resume",
             "abort",
             "unknown",
             "notify-stopped"
           ]
       }
  },
  {
    "id": id,
     "cluster": "fc",
     "type": "USSamplingOperation",
     "version":"v022",
     "woql": {
           "@type": "Enum",
           "@id": "USSamplingOperation",
           "@documentation": { "@title": "USSamplingOperation", "@description": "enum type defining the service API configuring US Sensors (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@value": [
             "heatMap",
             "occupancyMap",
             "tableMap"
           ]
       }
  },
  {
    "id": id,
     "cluster": "fc",
     "type": "OperationPolicy",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "OperationPolicy",
           "@documentation": { "@title": "OperationPolicy", "@description": "FC ER policy type and API for the operation of the facility cobot (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "Policy",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "action": "ERStateOperation"
       }
  },
  /*
    do not need to differentiate cleaning, clearing, etc policies  usr FCOperationPolicy

  {
        "id": id,
     "cluster": "fc",
     "type": "OperationPolicy",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "OperationPolicy",
           "@documentation": { "@title": "OperationPolicy", "@description": "cleaning policy type for the fleet of facility cobot actors (could be human) (version:v022)"},
           "@inherits": "Policy",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           
           "param":  {
             "@type"  : "Optional",
             "@class" : "xsd:string"
           }
       }
  },
  {
        "id": id,
     "cluster": "fc",
     "type": "ClearingPolicy",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "ClearingPolicy",
           "@documentation": { "@title": "ClearingPolicy", "@description": "clearing policy type for the fleet of facility cobot actors (could be human) (version:v022)"},
           "@inherits": "Policy",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "action": "Operation",
           "param":  {
             "@type"  : "Optional",
             "@class" : "xsd:string"
           }
       }
  },
  {
        "id": id,
     "cluster": "fc",
     "type": "Newspaper",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "LocationPolicy",
           "@documentation": { "@title": "LocationPolicy", "@description": "location (goto) policy type for facility cobot (version:v022)"},
           "@inherits": "Policy",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "action": "Operation",
           "param":  {
             "@type"  : "Optional",
             "@class" : "s",
           "@id": "RoutingPolicy",
           "@documentation": { "@title": "RoutingPolicy", "@description": "routing policy type for facility cobot (version:v022)"},
           "@inherits": "Policy",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "action": "Operation",
           "param":  {
             "@type"  : "Optional",
             "@class" : "xsd:string"
           }
         },
    */
         {
          "id": id,
          "cluster": "fc",
          "type": "USSamplingPolicy",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "USSamplingPolicy",
                       "@documentation": { "@title": "SamplingPolicy", "@description": "sampling policy type for US Sensors (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "Policy",
                       "@key": { "@type": "Lexical", "@fields": ["name"] },
                       "action": "USSamplingOperation",
                       "period": {
                         "@type": "Optional",
                         "@class": "xsd:unsignedInt"
                       },
                       "repetitions": {
                         "@type": "Optional",
                         "@class": "xsd:unsignedInt"
                       }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "SubSystemStatePolicy",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "SubSystemStatePolicy",
                       "@documentation": { "@title": "SubSystemStatePolicy", "@description": "policy for conditions on SubSystemState (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "Policy",
                       "@key": { "@type": "Lexical", "@fields": ["name"] },
                       "action": "ERStateOperation"
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "ERRobotStatePolicy",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "ERRobotStatePolicy",
                       "@documentation": { "@title": "ERRobotStatePolicy", "@description": "policy for conditions on ERRobotState (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "Policy",
                       "@key": { "@type": "Lexical", "@fields": ["name"] },
                       "action": "ERStateOperation",  // to be refined when ER uses ERRobotState
                       /*
                       "param":  {
                         "@type"  : "Optional",
                         "@class" : "xsd:string"
                       }
                       */
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Grip",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Grip",
                       "@documentation": { "@title": "Grip", "@description": "grip operation (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@abstract": [],
                       "@inherits": "ProductionOperation",
                       "gripOn": {
                         "@type": "Optional",
                         "@class": "Grippable"
                       },
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "USData",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "USData",
                       "@documentation": { "@title": "USData", "@description": "Data type for US data (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "VisionData",
                       "@key": { "@type": "Lexical", "@fields": ["name"] },
                       "organizationId": {
                         "@type": "Optional",
                         "@class": "xsd:integer"
                       },
                       "locationId": {
                         "@type": "Optional",
                         "@class": "xsd:integer"
                       },
                       "sensorId": {
                         "@type": "Optional",
                         "@class": "xsd:integer"
                       },
                       "usDataOf": {
                         "@type": "Set",
                         "@class": "SensedEntity",
                       },
                       "tables": {
                         "@type": "Array",
                         "@class": "USTable",
                       }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "USHeatMap",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "USHeatMap",
                       "@documentation": { "@title": "USHeatMap", "@description": "Data type for US Heat map data (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@inherits": "TemporalEntity",
                       "@key": { "@type": "Lexical", "@fields": ["name"] },
                       "organizationId": {
                         "@type": "Optional",
                         "@class": "xsd:integer"
                       },
                       "locationId": {
                         "@type": "Optional",
                         "@class": "xsd:integer"
                       },
                       "usHeatMapOf": {
                         "@type": "Set",
                         "@class": "SensedEntity",
                       },
                       "period": {
                         "@type": "Optional",
                         "@class": "xsd:integer"
                       },
                       "positions": {
                         "@type": "Array",
                         "@dimensions": 1,
                         "@class": "USPosition",
                       }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "USPosition",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "USPosition",
                       "@inherits": "IndexedEntity",
                       "@subdocument": [],
                       "@key": { "@type": "Lexical", "@fields": ["index"] },
                       "@documentation": { "@title": "USPosition", "@description": "base US heat map type (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "position": "Point",
                       "count": "xsd:integer",
                       "posture": "xsd:string"
                   
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "USDataElement",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "USDataElement",
                       "@abstract": [],
                       "@inherits": "IndexedEntity",
                       "@documentation": { "@title": "USTable", "@description": "Common data type of USData arrays (version:v022)",
           "@authors": ["William A Coolidge"]},
                       // re-used from Common Entity !!!
                       // "index" : "xsd:unsignedInt",
                       "points": {
                         "@type": "Array",
                         "@dimensions": 2,
                         "@class": "xsd:decimal"
                       },
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "USTable",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "USTable",
                       "@subdocument": [],
                       "@inherits": "USDataElement",
                       "@documentation": { "@title": "USTable", "@description": "Array element data type of USData tables (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@key": { "@type": "Lexical", "@fields": ["index"] },
                       "objects": {
                         "@type": "Array",
                         "@class": "USObject",
                       }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "USObject",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "USObject",
                       "@subdocument": [],
                       "@inherits": "USDataElement",
                       "@documentation": { "@title": "USTable", "@description": "Data type array element of USData tables (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@key": { "@type": "Lexical", "@fields": ["index"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "RoomEntity",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "RoomEntity",
                       "@documentation": { "@title": "RoomEntity", "@description": "Logical and physical entities associated with a Room (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@abstract": [],
                       "@inherits": "PhysicalEntity"
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Passage",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Passage",
                       "@documentation": { "@title": "Passage", "@description": "Passage is an area in a room that supports routes that are not blocked by a room object (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "RoomEntity",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Route",
          "version":"v022",
          "woql": {
                   
                       "@type": "Class",
                       "@id": "Route",
                       "@documentation": { "@title": "Route", "@description": "Route is a path, i.e array of coordinates, through a Passage (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "Passage",
                       "@key": { "@type": "Lexical", "@fields": ["name"] },
                       "wayPoints": "FCPose"
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Room",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Room",
                       "@documentation": { "@title": "Room", "@description": "The physical room and volume of control for operations and objects (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "FCZone",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Gripper",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Gripper",
                       "@documentation": { "@title": "Gripper", "@description": "The gripper on ER (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "PhysicalEntity",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Chair",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Chair",
                       "@documentation": { "@title": "Chair", "@description": "Chair type (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": ["RoomEntity", "Grippable"],
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       
       {
        "id": id,
          "cluster": "fc",
          "type": "FCPerson",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "FCPerson",
                       "@documentation": { "@title": "FCPerson", "@description": "facility cobot Person type (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": ["RoomEntity", "NoTouchObject", "Person"],
                       "@key": { "@type": "Lexical", "@fields": ["name"] },
            }
       },
       
       {
        "id": id,
          "cluster": "fc",
          "type": "Obstacle",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Obstacle",
                       "@documentation": { "@title": "Obstacle", "@description": "Obstacle type (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "RoomEntity",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Table",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Table",
                       "@documentation": { "@title": "Table", "@description": "Table type (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "RoomEntity",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "AGV",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "AGV",
                       "@documentation": { "@title": "AGV", "@description": "AGV type (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": ["NoTouchObject", "CyberPhysicalActor"],
                       "@abstract": [],
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "ERMobileRobot",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "ERMobileRobot",
                       "@documentation": { "@title": "ER AGV", "@description": "ER mobile robot (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "AGV",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "NoTouchObject",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "NoTouchObject",
                       "@documentation": { "@title": "NoTouchObject", "@description": "abstract NoTouchObject type (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@abstract": [],
                       "@inherits": "RoomEntity"
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "MobilePhone",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "MobilePhone",
                       "@documentation": { "@title": "MobilePhone", "@description": "MobilePhone type (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "NoTouchObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Clothing",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Clothing",
                       "@documentation": { "@title": "Clothing", "@description": "Clothing type (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "NoTouchObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Book",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Book",
                       "@documentation": { "@title": "Book", "@description": "Book type (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "NoTouchObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "A4Sheet",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "A4Sheet",
                       "@documentation": { "@title": "A4Sheet", "@description": "A4Sheet type (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "NoTouchObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Laptop",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Laptop",
                       "@documentation": { "@title": "Laptop", "@description": "Laptop type (version:v022)",
           "@authors": ["William A Coolidge"]},
                       "@inherits": "NoTouchObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Grippable",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Grippable",
                       "@documentation": { "@title": "Grippable", "@description": "Grippable type (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@inherits": "AbstractEntity"
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "TableObject",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "TableObject",
                       "@documentation": { "@title": "TableObject", "@description": "abstract TableObject type (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@abstract": [],
                       "@inherits": ["Grippable", "RoomEntity"]
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Utinesel",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Utinesel",
                       "@documentation": { "@title": "Utinesel", "@description": "Utinesel type (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@inherits": "TableObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Glass",
          "version":"v022",
          "woql": {
                   
                       "@type": "Class",
                       "@id": "Glass",
                       "@documentation": { "@title": "Glass", "@description": "Glass type (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@inherits": "TableObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Bottle",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Bottle",
                       "@documentation": { "@title": "Bottle", "@description": "Bottle type (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@inherits": "TableObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Can",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Can",
                       "@documentation": { "@title": "Can", "@description": "Can type (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@inherits": "TableObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Plate",
          "version":"v022",
          "woql": {
                      "@type": "Class",
                       "@id": "Plate",
                       "@documentation": { "@title": "Plate", "@description": "Plate type (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@inherits": "TableObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Cup",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Cup",
                       "@documentation": { "@title": "Cup", "@description": "Cup type (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@inherits": "TableObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Napkin",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Napkin",
                       "@documentation": { "@title": "Napkin", "@description": "Napkin type (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@inherits": "TableObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "OtherObject",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "OtherObject",
                       "@documentation": { "@title": "OtherObject", "@description": "OtherObject type (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@abstract": [],
                       "@inherits": ["RoomEntity", "Grippable"]
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "UnRecognizable",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "UnRecognizable",
                       "@documentation": { "@title": "Unrecognizable", "@description": "Generic type for all objects that exists in vision but are unrecognizable (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@inherits": "OtherObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Bag",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Bag",
                       "@documentation": { "@title": "Bag", "@description": "Bag type (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@inherits": "OtherObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
          "cluster": "fc",
          "type": "Newspaper",
          "version":"v022",
          "woql": {
                       "@type": "Class",
                       "@id": "Newspaper",
                       "@documentation": { "@title": "Newspaper", "@description": "Newspaper type (version:v022)",
                       "@authors": ["William A Coolidge"]},
                       "@inherits": "OtherObject",
                       "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
       },
       {
        "id": id,
        "cluster": "fc",
        "type": "FCRecognizedState",
        "version": "v022",
        "woql": {
          "@type": "Class",
          "@id": "RecognizedState",
          "@documentation": {
            "@title": "RecognizedState", "@description": "RecognizedState is the type characterizing the sensed status of the entities of work for the facility cobot (version:v022)",
            "@authors": ["William A Coolidge"]
          },
          "@inherits": "RecognizedState",
          "@key": { "@type": "Lexical", "@fields": ["name"] },
          "period": {
            "@type": "Optional",
            "@class": "xsd:integer"
          },
          "heatScore": {
            "@type": "Optional",
            "@class": "xsd:integer"
          },
          "accumulatedHeat": {
            "@type": "Optional",
            "@class": "xsd:integer"
          },
          "resetAt": {
            "@type": "Optional",
            "@class": "xsd:string"
          }
        }
      },
]);
