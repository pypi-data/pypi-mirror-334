// "dependencies": ["core","policy", "ros", "vision"],
import { clusterType } from 'common-types';

export const assemblyCluster = (id): clusterType[] => ([


  // Situations
  {
    "id": id,
    "cluster": "assembly",
    "type": "PenAssemblySituation",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PenAssemblySituation",
      "@documentation": {
        "@title": "PenAssemblySituation", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["ProductionSituation"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    }
  },
 
  /*
  {
    "id": id,
    "cluster": "assembly",
    "type": "MachineTendingSituation",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "MachineTendingSituation",
      "@documentation": {
        "@title": "MachineTendingSituation", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["ProductionSituation"],
      "@key": { "@type": "Lexical", "@fields": ["name"] }
    }
  },
 */
  
  // Goals
  
  

  // Plans
  {
    "id": id,
    "cluster": "assembly",
    "type": "PenAssemblyPlan",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PenAssemblyPlan",
      "@documentation": {
        "@title": "PenAssemblyPlan", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["ProductionPlan"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "hasSetting" : "PenAssemblySituation"
      /*
      "initial": {
        "@type": "Optional",
        "@class": "WayPoint"
      },
      "target": {
        "@type": "Optional",
        "@class": "WayPoint"
      }
        */
    }
  },

  // PhysicalObjects
  {
    "id": id,
    "cluster": "assembly",
    "type": "RobotiqGripper",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "RobotiqGripper",
      "@documentation": {
        "@title": "RobotiqGripper", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Gripper"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    
     
    }
  },

  // work items
  {
    "id": id,
    "cluster": "assembly",
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
    "cluster": "assembly",
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
    "cluster": "assembly",
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
    "cluster": "assembly",
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
    "cluster": "assembly",
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
    "cluster": "assembly",
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
  /*
  {
    "id": id,
    "cluster": "assembly",
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
    "cluster": "assembly",
    "type": "ArmCamera",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ArmCamera",
      "@documentation": {
        "@title": "ArmCamera", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Agent", "PhysicalObject"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "isPartOf": {
        "@type": "Optional",
        "@class": "URRobot"
      },
    }
  },
  {
    "id": id,
    "cluster": "assembly",
    "type": "StaticCamera",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "StaticCamera",
      "@documentation": {
        "@title": "StaticCamera", "@description": " (version:v001)",
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
    "cluster": "assembly",
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
    "cluster": "assembly",
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
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "isPartOf": {
        "@type": "Optional",
        "@class": "URRobot"
      },
    }
  },
  */

  // Tasks
  /*
  {
    "id": id,
    "cluster": "assembly",
    "type": "AssemblyTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "AssemblyTask",
      "@documentation": {
        "@title": "AssemblyTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Task", "TemporalEntity"],
      "@abstract":[]
    }
  },
  */
  {
    "id": id,
    "cluster": "assembly",
    "type": "PenAssemblyTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PenAssemblyTask",
      "@documentation": {
        "@title": "PenAssemblyTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["RobotTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },


    }
  },
  {
    "id": id,
    "cluster": "assembly",
    "type": "InsertionTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "InsertionTask",
      "@documentation": {
        "@title": "InsertionTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["RobotTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "inhandPose": "InitialInHandPoseEstimationState",
      "fixtureID":{
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "success": {
        "@type": "Optional",
        "@class": "xsd:int"
      },
      "height" : {
        "@type": "Optional",
        "@class": "xsd:int"
      },
      "fixturePose": {
        "@type": "Optional",
        "@class": "Pose"
      }
    }
  },
  {
    "id": id,
    "cluster": "assembly",
    "type": "InsertionInspectionTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "InsertionInspectionTask",
      "@documentation": {
        "@title": "InsertionInspectionTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["RobotTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "success": {
        "@type": "Optional",
        "@class": "xsd:int"
      }
    }
  },

 
  {
    "id": id,
    "cluster": "assembly",
    "type": "BinPickTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BinPickTask",
      "@documentation": {
        "@title": "BinPickTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["RobotTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      
    }
  },

  {
    "id": id,
    "cluster": "assembly",
    "type": "ProcessingTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ProcessingTask",
      "@documentation": {
        "@title": "ProcessingTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["RobotTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
     
    }
  },

  // Configurations
/*
  {
    "id": id,
    "cluster": "assembly",
    "type": "AssemblyConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "AssemblyConfiguration",
      "@documentation": {
        "@title": "AssemblyConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
     "@inherits": ["Configuration", "Region"],
      "@abstract":[],
      "isConfigurationOf": "AssemblyTask"
    }
  },
  */
  {
    "id": id,
    "cluster": "assembly",
    "type": "PenAssemblyConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PenAssemblyConfiguration",
      "@documentation": {
        "@title": "PenAssemblyConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["TaskConfiguration"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
   
    }
  },
  {
    "id": id,
    "cluster": "assembly",
    "type": "InsertionConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "InsertionConfiguration",
      "@documentation": {
        "@title": "InsertionConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["TaskConfiguration"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
     
    }
  },
  {
    "id": id,
    "cluster": "assembly",
    "type": "InsertionInspectionConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "InsertionInspectionConfiguration",
      "@documentation": {
        "@title": "InsertionInspectionConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["TaskConfiguration"],
  
    }
  },

 
  {
    "id": id,
    "cluster": "assembly",
    "type": "BinPickConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BinPickConfiguration",
      "@documentation": {
        "@title": "BinPickConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["TaskConfiguration"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    
    }
  },

  {
    "id": id,
    "cluster": "assembly",
    "type": "ProcessingConfiguration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ProcessingConfiguration",
      "@documentation": {
        "@title": "ProcessingConfiguration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["TaskConfiguration"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
  
    }
  },

  // Actions
  /*
  {
    "id": id,
    "cluster": "assembly",
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
      "hasDestination": {
        "@type": "Optional",
        "@class": "WayPoint"
      },
      "executesTask": "AssemblyTask"
    }
  },
  
  {
    "id": id,
    "cluster": "assembly",
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
    "cluster": "assembly",
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
    "cluster": "assembly",
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
  */
  /*
  {
    "id": id,
    "cluster": "assembly",
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
    "cluster": "assembly",
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
  /*
  {
    "id": id,
    "cluster": "assembly",
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
      "@inherits": ["State", "TemporalEntity"],
    }
  },
*/
  {
    "id": id,
    "cluster": "assembly",
    "type": "GraspTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "GraspTask",
      "@documentation": {
        "@title": "GraspTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["RobotTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "id" : "xsd:int",
      
    }
  },
  {
    "id": id,
    "cluster": "assembly",
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
      
      "poseEstimation" : "PoseEstimationState",
      "attemptNr": "xsd:int",
      "runTime": "xsd:float",
      "collision": "xsd:int",

      "expectedType": "xsd:int",
      "initialSuccess": "xsd:int",
      "success": "xsd:int",
      "intendedPose": "Pose",
      "expectedPose": "Pose"
    }
  },
  {
    "id": id,
    "cluster": "assembly",
    "type": "PoseEstimationTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PoseEstimationTask",
      "@documentation": {
        "@title": "PoseEstimationTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["RobotTask"],
      "@key": { "@type": "Lexical", "@fields": ["name"] }
    }
  },
  {
    "id": id,
    "cluster": "assembly",
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
    }
  },
  {
    "id": id,
    "cluster": "assembly",
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
      "bin": "xsd:string"
      
    }
  },

  {
    "id": id,
    "cluster": "assembly",
    "type": "GraspValidationTask",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "GraspValidationTask",
      "@documentation": {
        "@title": "GraspValidationTask", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["RobotTask"],
      "@abstract": [],
      "id" : "xsd:int"
    }
  },
  {
    "id": id,
    "cluster": "assembly",
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
      
    }
  },
  {
    "id": id,
    "cluster": "assembly",
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
    "cluster": "assembly",
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
      
    }
  },
  
  /*
  {
    "id": id,
     "cluster": "assembly",
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
     "cluster": "assembly",
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
     "cluster": "assembly",
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
     "cluster": "assembly",
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
     "cluster": "assembly",
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
     "cluster": "assembly",
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
