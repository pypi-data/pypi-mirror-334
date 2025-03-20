// "dependencies": ["core","policy", "ros", "vision"],
import { clusterType } from 'common-types';

export const feraCluster = (id): clusterType[] => ([
  // name-value

  {
    "id": id,
    "cluster": "fera",
    "type": "NamedValue",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "NamedValue",
      "@documentation": {
        "@title": "NamedValue", "@description": "base type for named-values (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["ConfigurationDictionary"],
    
      // "dictionaryName": "xsd:string",
      
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "StringValue",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "StringValue",
      "@documentation": {
        "@title": "StringValue", "@description": "a value type for named values (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "NamedValue",
      "@unfoldable": [],
      "@key": { "@type": "Lexical", "@fields": ["name"/*, "dictionaryName"*/] },
      
      "value": "xsd:string",
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "IntValue",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "IntValue",
      "@documentation": {
        "@title": "IntValue", "@description": "a value type for named values (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "NamedValue",
      "@unfoldable": [],
      "@key": { "@type": "Lexical", "@fields": ["name"/*, "dictionaryName"*/] },
      
      "value": "xsd:integer",
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "FloatValue",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "FloatValue",
      "@documentation": {
        "@title": "FloatValue", "@description": "a value type for named values (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "NamedValue",
      "@unfoldable": [],
      "@key": { "@type": "Lexical", "@fields": ["name"/*, "dictionaryName"*/] },
      
      "value": "xsd:float",
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "DoubleValue",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "DoubleValue",
      "@documentation": {
        "@title": "DoubleValue", "@description": "a value type for named values (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "NamedValue",
      "@unfoldable": [],
      "@key": { "@type": "Lexical", "@fields": ["name"/*, "dictionaryName"*/] },
      
      "value": "xsd:double",
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "BooleanValue",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BooleanValue",
      "@documentation": {
        "@title": "BooleanValue", "@description": "a value type for named values (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "NamedValue",
      "@unfoldable": [],
      "@key": { "@type": "Lexical", "@fields": ["name"/*, "dictionaryName"*/] },
      
      "value": "xsd:boolean",
    }
  },
 
  // Regions
  {
    "id": id,
    "cluster": "fera",
    "type": "SampledEntity",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "SampledEntity",
      "@documentation": {
        "@title": "SampledEntity", "@description": "base type for all sampled entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": "TimeInterval",
      "timeStamp": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "sampleIndex": {
        "@type": "Optional",
        "@class": "xsd:unsignedLong"
      },
     "samplePeriod": {
        "@type": "Optional",
        "@class": "SampledTimePeriod"
      }
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "SampledTimePeriod",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "SampledTimePeriod",
      "@documentation": {
        "@title": "SampledTimePeriod", "@description": "base type for sampled time period (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Configuration"],
      //"@abstract": [],

      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "sampledTimePeriod": {
        "@type": "Optional",
        "@class": "xsd:float"
      },
      "sampledTimeUnit" : {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      
    }
  },
 
  {
    "id": id,
    "cluster": "fera",
    "type": "TemporalEntity",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "TemporalEntity",
      "@documentation": {
        "@title": "TemporalEntity", "@description": "base type for all temporal entities (characterized by values over time) (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      //"@inherits": "AbstractEntity",
      "@inherits": "SampledEntity",
      "first": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "last": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "count": {
        "@type": "Optional",
        "@class": "xsd:integer"
      }
    }
  },


  {
    "id": id,
    "cluster": "fera",
    "type": "WayPoint",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "WayPoint",
      "@documentation": {
        "@title": "WayPoint", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Location"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "hasLocation": {
        "@type": "Array",
        "@dimensions": 1,
        "@cardinality": 3,
        "@class": "xsd:double"
      }
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "ProfiledEntity",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ProfiledEntity",
      "@documentation": {
        "@title": "ProfiledEntity", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Region"],
      "@abstract": [],
      "hasProfile": {
        "@type": "Set",
        "@class": "Profile"
      }
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "Profile",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Profile",
      "@documentation": {
        "@title": "Profile", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": [/*"TemporalEntity", */"Description"],
      "@key": { "@type": "Lexical", "@fields": ["name"/*, "first"*/] },
      "version": {
        "@type": "Optional",
        "@class": "xsd:string"
      }
    
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "Pose",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Pose",
      "@documentation": {
        "@title": "Pose", "@description": " alias for Localization (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Localization"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      
    }
  },

  // Situations
  /*
  {
    "id": id,
    "cluster": "fera",
    "type": "PenAssemblySituation",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PenAssemblySituation",
      "@documentation": {
        "@title": "PenAssemblySituation", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["RobotUseSituation"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "MachineTendingSituation",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "MachineTendingSituation",
      "@documentation": {
        "@title": "MachineTendingSituation", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["FeraSituation"],
      "@key": { "@type": "Lexical", "@fields": ["name"] }
    }
  },
*/
  {
    "id": id,
    "cluster": "fera",
    "type": "ProductionSituation",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ProductionSituation",
      "@documentation": {
        "@title": "ProductionSituation", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Situation"],
      "@abstract": [],
      "deployedIn" : "DeploymentContext"
      //"deployment" : "xsd:string"
    }
  },
  
  {
    "id": id,
    "cluster": "fera",
    "type": "DeploymentContext",
    "version": "v001",
    "woql": {
      "@type": "Enum",
      "@id": "DeploymentContext",
      "@documentation": {
        "@title": "DeploymentContext", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@value" : ["I4Lab", "Production"]
    }
  },

  // Goals
  
  {
    "id": id,
    "cluster": "fera",
    "type": "ProjectGoal",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ProjectGoal",
      "@documentation": {
        "@title": "ProjectGoal", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits" : ["Goal"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "expectedGoal":  {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "nonFunctionalGoal": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
    }
  },

  // Plans
  
  {
    "id": id,
    "cluster": "fera",
    "type": "ProductionPlan",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ProductionPlan",
      "@documentation": {
        "@title": "ProductionPlan", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Plan"],
      "@key": { "@type": "Lexical", "@fields": ["name"] }
      
    }
  },

  // PhysicalObjects

  {
    "id": id,
    "cluster": "fera",
    "type": "WorkItem",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "WorkItem",
      "@documentation": {
        "@title": "WorkItem", "@description": "base type for all work items (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["PhysicalObject"],
      "@abstract": []
      
    }
  },
  /*
  {
    "id": id,
    "cluster": "fera",
    "type": "NovoPen",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "NovoPen",
      "@documentation": {
        "@title": "NovoPen", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["WorkItem"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "PenBody",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PenBody",
      "@documentation": {
        "@title": "PenBody", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["WorkItem"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
     // "isComponentOf": {
      "isPartOf": {
        "@type": "Optional",
        "@class": "NovoPen"
      }
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "PenCap",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PenCap",
      "@documentation": {
        "@title": "PenCap", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["WorkItem"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "isPartOf": {
        "@type": "Optional",
        "@class": "NovoPen"
      }
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "BodyLiner",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BodyLiner",
      "@documentation": {
        "@title": "BodyLiner", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["WorkItem"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "isPartOf": {
        "@type": "Optional",
        "@class": "NovoPen"
      }
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "CartridgeHolder",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "CartridgeHolder",
      "@documentation": {
        "@title": "CartridgeHolder", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["WorkItem"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "isPartOf": {
        "@type": "Optional",
        "@class": "NovoPen"
      }
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "PistonRod",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PistonRod",
      "@documentation": {
        "@title": "PistonRod", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["WorkItem"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "isPartOf": {
        "@type": "Optional",
        "@class": "NovoPen"
      }
    }
  },
  */
  {
    "id": id,
    "cluster": "fera",
    "type": "URRobot",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "URRobot",
      "@documentation": {
        "@title": "URRobot", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Agent", "PhysicalObject"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "Camera",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Camera",
      "@documentation": {
        "@title": "Camera", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Agent", "PhysicalObject"],
      "@abstract":[],
      "isConstituentOf": {
        "@type": "Optional",
        "@class": "URRobot"
      },
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "ArmCamera",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ArmCamera",
      "@documentation": {
        "@title": "ArmCamera", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Camera"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "StaticCamera",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "StaticCamera",
      "@documentation": {
        "@title": "StaticCamera", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Camera"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
     
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "Processor",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Processor",
      "@documentation": {
        "@title": "Processor", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Agent", "PhysicalObject"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "isConstituentOf": {
        "@type": "Optional",
        "@class": "URRobot"
      },

    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "Gripper",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Gripper",
      "@documentation": {
        "@title": "Gripper", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Agent", "PhysicalObject"],
      //"@key": { "@type": "Lexical", "@fields": ["name"] },
      "@abstract": [],
      "isPartOf": {
        "@type": "Optional",
        "@class": "URRobot"
      },
    }
  },
  

  // Tasks
  {
    "id": id,
    "cluster": "fera",
    "type": "ProfiledTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ProfiledTask",
      "@documentation": {
        "@title": "ProfiledTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Task", "TemporalEntity", "ProfiledEntity"],
      "@abstract":[]
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "RobotTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "RobotTask",
      "@documentation": {
        "@title": "RobotTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Task", "ProfiledTask"],
      "@abstract":[]
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "SoftwareTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "SoftwareTask",
      "@documentation": {
        "@title": "SoftwareTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Agent", "ProfiledEntity"],
      "@abstract":[],
      "hasEffect": {
        "@type": "Optional",
        "@class": "RobotTask"
      },
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "Dictionary",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Dictionary",
      "@documentation": {
        "@title": "ConfigurationDictionary", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
     "@inherits": ["Region"],
      "@abstract":[],
  
      "namedValues": {
        "@type": "Set",
        "@class": "NamedValue"
      }
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "ContextDescription",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ContextDescription",
      "@documentation": {
        "@title": "ContextDescription", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Description", "Dictionary"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "ConfigurationDictionary",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ConfigurationDictionary",
      "@documentation": {
        "@title": "ConfigurationDictionary", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
     "@inherits": ["Configuration", "Dictionary"],
      "@abstract":[],
      "isConfigurationOf": {
        "@type": "Optional",
        "@class": "Entity"
      },
 
    }
  },
{
    "id": id,
    "cluster": "fera",
    "type": "TaskConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "TaskConfiguration",
      "@documentation": {
        "@title": "TaskConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
     "@inherits": ["ConfigurationDictionary"],
      "@abstract":[],
     // "isConfigurationOf": "SoftwareTask"
    }
  },
  /*
  {
    "id": id,
    "cluster": "fera",
    "type": "PenAssemblyTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PenAssemblyTask",
      "@documentation": {
        "@title": "PenAssemblyTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "followsPlan": "PenAssemblyPlan",

    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "InsertionTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "InsertionTask",
      "@documentation": {
        "@title": "InsertionTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "inhandPose": "InitialInHandPoseEstimationState",
      "fixtureID": "xsd:string",
      "success": "xsd:int",
      "height" : "xsd:int",
      "fixturePose": "Pose",
      "isSubTaskOf": "PenAssemblyTask"
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "InsertionInspectionTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "InsertionInspectionTask",
      "@documentation": {
        "@title": "InsertionInspectionTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "success": "xsd:int",
      "isSubTaskOf": "PenAssemblyTask"
    }
  },

 
  {
    "id": id,
    "cluster": "fera",
    "type": "BinPickTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BinPickTask",
      "@documentation": {
        "@title": "BinPickTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "isSubTaskOf": "PenAssemblyTask"
    }
  },

  {
    "id": id,
    "cluster": "fera",
    "type": "ProcessingTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ProcessingTask",
      "@documentation": {
        "@title": "ProcessingTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "isSubTaskOf": "PenAssemblyTask"
    }
  },
*/
  // Configurations
  /*
    todo: distinguish Task from the equivalent of SWTask, what is that?
    a configuration is of a SWTask, not the logical concept Task for the effect of the SWTask


  */


  {
    "id": id,
    "cluster": "fera",
    "type": "TaskConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "TaskConfiguration",
      "@documentation": {
        "@title": "TaskConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
     "@inherits": ["ConfigurationDictionary"],
      "@abstract":[],
     // "isConfigurationOf": "SoftwareTask"
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "RobotConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "RobotConfiguration",
      "@documentation": {
        "@title": "RobotConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
     "@inherits": ["ConfigurationDictionary"],
     "@key": { "@type": "Lexical", "@fields": ["name"] },
     // "@abstract":[],
     // "isConfigurationOf": "URRobot"
    }
  },
  /*
  {
    "id": id,
    "cluster": "fera",
    "type": "PenAssemblyConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PenAssemblyConfiguration",
      "@documentation": {
        "@title": "PenAssemblyConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyConfiguration"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
   
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "InsertionConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "InsertionConfiguration",
      "@documentation": {
        "@title": "InsertionConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyConfiguration"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
     
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "InsertionInspectionConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "InsertionInspectionConfiguration",
      "@documentation": {
        "@title": "InsertionInspectionConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyConfiguration"],
  
    }
  },

 
  {
    "id": id,
    "cluster": "fera",
    "type": "BinPickConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BinPickConfiguration",
      "@documentation": {
        "@title": "BinPickConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyConfiguration"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    
    }
  },

  {
    "id": id,
    "cluster": "fera",
    "type": "ProcessingConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ProcessingConfiguration",
      "@documentation": {
        "@title": "ProcessingConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyConfiguration"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
  
    }
  },
*/
  // Actions
  {
    "id": id,
    "cluster": "fera",
    "type": "URMove",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "URMove",
      "@documentation": {
        "@title": "URMove", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Action"],
      "@abstract":[],
      "hasOrigin": {
        "@type": "Optional",
        "@class": "WayPoint"
      },
      "hasTarget": {
        "@type": "Optional",
        "@class": "WayPoint"
      },
      "executesTask": "RobotTask"
    }
  },
  
  {
    "id": id,
    "cluster": "fera",
    "type": "MoveP",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "MoveP",
      "@documentation": {
        "@title": "MoveP", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["URMove"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "Movel",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Movel",
      "@documentation": {
        "@title": "Movel", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["URMove"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "MoveJ",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "MoveJ",
      "@documentation": {
        "@title": "MoveJ", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["URMove"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    }
  },
  /*
  {
    "id": id,
    "cluster": "fera",
    "type": "PoseValidationTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PoseValidationTask",
      "@documentation": {
        "@title": "PoseValidationTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "isSubTaskOf": "PenAssemblyTask"
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "GraspValidationTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "GraspValidationTask",
      "@documentation": {
        "@title": "GraspValidationTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "isSubTaskOf": "PenAssemblyTask"
    }
  },*/


  // States
  {
    "id": id,
    "cluster": "fera",
    "type": "ProfiledState",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ProfiledState",
      "@documentation": {
        "@title": "ProfiledState", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["State", "TemporalEntity", "ProfiledEntity"],

    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "TaskState",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "TaskState",
      "@documentation": {
        "@title": "TaskState", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["State"],
      "isStateOf": {
        "@type": "Optional",
        "@class": "Task"
      },
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "JointState",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "JointState",
      "@documentation": {
        "@title": "JointState", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      //"@abstract": [],
      "@key": { "@type": "Lexical", "@fields": ["name", "first"] },
      "@inherits": ["TaskState", "ProfiledState"],
      /*
      "hasJointVelocity":  {
        "@type": "Optional",
        "@class": "GfVec3d"
      },
      "hasJointAcceleration":  {
        "@type": "Optional",
        "@class": "GfVec3d"
      },
      "hasJointEffort":  {
        "@type": "Optional",
        "@class": "GfVec3d"
      },
      "hasJointForce":  {
        "@type": "Optional",
        "@class": "GfVec3d"
      },
      */
     "hasJointPosition":  {
        "@type": "Optional",
        "@class": "xsd:double"
      },
      "hasJointVelocity":   {
        "@type": "Optional",
        "@class": "xsd:double"
      },
      "hasJointAcceleration":  {
        "@type": "Optional",
        "@class": "xsd:double"
      },
      "hasJointEffort":  {
        "@type": "Optional",
        "@class": "xsd:double"
      },
      "hasJointForce": {
        "@type": "Optional",
        "@class": "xsd:double"
      }
    }
    
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "ToolCenterPointState",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ToolCenterPointState",
      "@documentation": {
        "@title": "ToolCenterPointState", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
     // "@abstract": [],
     "@key": { "@type": "Lexical", "@fields": ["name", "first"] },
      "@inherits": ["TaskState", "ProfiledState"],
      "hasTCPSpeed":  {
       "@type": "Array",
      "@dimensions": 1,
      "@cardinality": 6,
      "@class": "xsd:double"
    },
      /*
      "hasTCPPose":  {
        "@type": "Optional",
        //"@class": "VtVec3dArray"
        "@class": "Pose"
      },
      */
      "hasTCPPose":{
        "@type": "Array",
        "@dimensions": 1,
        "@cardinality": 6,
        "@class": "xsd:double"
      },
      /*
      "hasTCPForce":  {
        "@type": "Optional",
        "@class": "GfVec3d"
      },
      */
      "hasTCPForce": {
        "@type": "Array",
        "@dimensions": 1,
        "@cardinality": 6,
        "@class": "xsd:double"
      }
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "MovementState",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "MovementState",
      "@documentation": {
        "@title": "MovementState", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      //"@abstract": [],
      "@key": { "@type": "Lexical", "@fields": ["name", "first"] },
      "@inherits": ["TaskState", "ProfiledState", "WayPoint"],
      
    }
    
  },
  /*
  {
    "id": id,
    "cluster": "fera",
    "type": "GraspTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "GraspTask",
      "@documentation": {
        "@title": "GraspTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "id" : "xsd:int",
      "isSubTaskOf": "PenAssemblyTask"
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "GraspState",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "GraspState",
      "@documentation": {
        "@title": "GraspState", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["TaskState"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "id" : "xsd:int",
      "poseEstimation" : "PoseEstimationState",
      "attemptNr": "xsd:int",
      "runTime": "xsd:float",
      "collision": "xsd:int",

      "expectedType": "xsd:int",
      "initialSuccess": "xsd:int",
      "success": "xsd:int",
      "intendedPose": "Pose",
      "expectedPose": "Pose",
      "isGraspStateOf": "GraspTask"
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "PoseEstimationTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PoseEstimationTask",
      "@documentation": {
        "@title": "PoseEstimationTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "id" : "xsd:int",
      "isSubTaskOf": "PenAssemblyTask",
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "PoseEstimationState",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PoseEstimationState",
      "@documentation": {
        "@title": "PoseEstimationState", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["TaskState"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "id" : "xsd:int",
      "pointCloud" : "PointCloud",
      "objName": "xsd:string",
      "runTime": "xsd:float",
      "score": "xsd:float",
      "camPose": "Pose",
      "basePose": "Pose",
      "isPoseEstimationStateOf": "PoseEstimationTask"
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "PointCloud",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PointCloud",
      "@documentation": {
        "@title": "PointCloud", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["TaskState"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "id" : "xsd:int",
      "isPointCloudOf": "PoseEstimationTask",
      "bin": "xsd:string"
      
    }
  },

  {
    "id": id,
    "cluster": "fera",
    "type": "GraspValidationTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "GraspValidationTask",
      "@documentation": {
        "@title": "GraspValidationTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AssemblyTask"],
      "@abstract": [],
      "id" : "xsd:int",
      "isSubTaskOf": "PenAssemblyTask"
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "GraspValidationState",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "GraspValidationState",
      "@documentation": {
        "@title": "GraspValidationState", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["TaskState"],
      "@abstract": [],
      "id" : "xsd:int",
      "success": "xsd:int",
      "runTime": "xsd:float",
      "score": "xsd:float",
      "pose": "Pose",
      "graspState": "GraspState",
      "isGraspValidationStateOf": "GraspValidationTask"
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "InitialInHandPoseEstimationState",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "InitialInHandPoseEstimationState",
      "@documentation": {
        "@title": "InitialInHandPoseEstimationState", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["GraspValidationState"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    }
  },
  {
    "id": id,
    "cluster": "fera",
    "type": "RotInHandPoseEstimationState",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "RotInHandPoseEstimationState",
      "@documentation": {
        "@title": "RotInHandPoseEstimationState", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["GraspValidationState"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "initialInHandPoseEstimationState": "InitialInHandPoseEstimationState",
    }
  },
  */
  
  /*
  {
    "id": id,
     "cluster": "fera",
     "type": "MachineTender",
     "version":"v001",
     "woql": {
               "@type": "Class",
               "@id": "MachineTender",
               "@documentation": { "@title": "MachineTender Robot", "@description": "MachineTender model (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": ["Robot", "Asset"],
         
               "@key": { "@type": "Lexical", "@fields": ["name"] },
         
       }
  },
  {
    "id": id,
     "cluster": "fera",
     "type": "FeraShell",
     "version":"v001",
     "woql": {
               "@type": "Class",
               "@id": "FeraShell",
               "@documentation": { "@title": "FeraShell Robot", "@description": "FeraShell model (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": ["AssetShell"],
         
               "@key": { "@type": "Lexical", "@fields": ["name"] },
         
       }
  },
  {
    "id": id,
     "cluster": "fera",
     "type": "MachineTending",
     "version":"v001",
     "woql": {
               "@type": "Class",
               "@id": "MachineTending",
               "@documentation": { "@title": "MachineTending Operations", "@description": "MachineTending model (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": ["SubModel"],
         
               "@key": { "@type": "Lexical", "@fields": ["name"] },
         
       }
  },
  {
    "id": id,
     "cluster": "fera",
     "type": "LoadCNC",
     "version":"v001",
     "woql": {
               "@type": "Class",
               "@id": "LoadCNC",
               "@documentation": { "@title": "LoadCNC Robot", "@description": "LoadCNC model (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": ["ShellOperation"],
         
               "@key": { "@type": "Lexical", "@fields": ["name"] },
         
       }
  },
  {
    "id": id,
     "cluster": "fera",
     "type": "MachineTenderBehavior",
     "version":"v001",
     "woql": {
               "@type": "Class",
               "@id": "MachineTenderBehavior",
               "@documentation": { "@title": "MachineTenderBehavior Robot", "@description": "MachineTenderBehavior model (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": ["BDDBehavior"],
         
               "@key": { "@type": "Lexical", "@fields": ["name"] },
         
       }
  },
  {
    "id": id,
     "cluster": "fera",
     "type": "MachineTenderSW",
     "version":"v001",
     "woql": {
               "@type": "Class",
               "@id": "MachineTenderSW",
               "@documentation": { "@title": "MachineTenderSW Robot", "@description": "MachineTenderSW model (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": ["SWAsset"],
         
               "@key": { "@type": "Lexical", "@fields": ["name"] },
         
       }
  }
  */
]);
