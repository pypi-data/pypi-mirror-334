//  "dependencies": ["core","i4"],
import { clusterType } from 'common-types';

export const srdfCluster = (id): clusterType[] => ([
  {
     "id": id,
     "cluster": "srdf",
     "type": "Robot",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Robot",
               "@documentation": { "@title": "Robot", "@description": "robot model (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": "AssetStructure",
               "@abstract": [],
               "jointGroup": {
                 "@type"  : "Optional",
                 "@class" : "JointGroup"
               },
               "endEffectorGroup":{
                 "@type"  : "Optional",
                 "@class" : "EndEffectorGroup"
               },
               "groupState":  {
                 "@type"  : "Optional",
                 "@class" : "GroupState"
               }
               //"virtualJoint": "",
               //"disableCollisions": "",
       }
  },
  {
    "id": id,
     "cluster": "srdf",
     "type": "JointGroup",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "JointGroup",
               "@inherits": "AssetStructure",
               "@documentation": { "@title": "JointGroup", "@description": "SRDF Group equivalent (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@key": { "@type": "Lexical", "@fields": ["name"] },
               "links":  {
                 "@type"  : "Set",
                 "@class" : "Link"
               },
               "joints":  {
                 "@type"  : "Set",
                 "@class" : "Joint"
               },
               "kinematicChain":  {
                 "@type"  : "Optional",
                 "@class" : "KinematicChain"
               },
               "jointGroup":  {
                 "@type"  : "Optional",
                 "@class" : "JointGroup"
               }
       }
  },
  {
    "id": id,
     "cluster": "srdf",
     "type": "EndEffectorGroup",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "EndEffectorGroup",
               "@inherits": "AssetStructure",
               "@documentation": { "@title": "JointGroup", "@description": "SRDF Group equivalent (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@key": { "@type": "Lexical", "@fields": ["name"] },
               "jointGroup":  {
                 "@type"  : "Optional",
                 "@class" : "JointGroup"
               },
               "parentLink":  {
                 "@type"  : "Optional",
                 "@class" : "Link"
               },
               "parentJointGroup":  {
                 "@type"  : "Optional",
                 "@class" : "JointGroup"
               }
       }
  },
  {
    "id": id,
     "cluster": "srdf",
     "type": "AssetState",
     "version":"v022",
     "woql": {
                     "@type": "Class",
                     "@id": "AssetState",
                     "@inherits": "EntityState",
                     "@documentation": { "@title": "AssetState", "@description": "SRDF GroupState base class (version:v022)",
                     "@authors": ["William A Coolidge"]},
                     "@key": { "@type": "Lexical", "@fields": ["name"]},
                     "groupState": {
                       "@type"  : "Optional",
                       "@class" : "GroupState"
                     },
                     "physicalEntity": {
                       "@type"  : "Optional",
                       "@class" : "PhysicalEntity"
                     }
       }
  },
  {
    "id": id,
     "cluster": "srdf",
     "type": "GroupState",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "GroupState",
               "@inherits": "AssetState",
               "@documentation": { "@title": "GroupState", "@description": "SRDF GroupState equivalent (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@key": { "@type": "Lexical", "@fields": ["name"] },
               "jointGroup": {
                 "@type"  : "Optional",
                 "@class" : "JointGroup"
               }
       }
  },
  {
    "id": id,
     "cluster": "srdf",
     "type": "JointState",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "JointState",
               "@documentation": { "@title": "JointState", "@description": "data type for robot joints (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": "AssetState",
               // timeStamp should be embedded in name
               "@key": { "@type": "Lexical", "@fields": ["name"] },
               "position": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "velocity": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
     "cluster": "srdf",
     "type": "MotorState",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "MotorState",
               "@documentation": { "@title": "MotorState", "@description": "data type for robot joints (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": "AssetState",
               // timeStamp should be embedded in name
               "@key": { "@type": "Lexical", "@fields": ["name"] },
           
               "motorPosition": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "motorVelocity": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "torque": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "torqueDerivative": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
     "cluster": "srdf",
     "type": "DriveState",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "DriveState",
               "@documentation": { "@title": "DriveState", "@description": "data type for robot joints (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": "AssetState",
               // timeStamp should be embedded in name
               "@key": { "@type": "Lexical", "@fields": ["name"] },
               "current": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "boardVoltage": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
     "cluster": "srdf",
     "type": "PowerState",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "PowerState",
               "@documentation": { "@title": "PowerState", "@description": "data type for robot joints (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": "AssetState",
               // timeStamp should be embedded in name
               "@key": { "@type": "Lexical", "@fields": ["name"] },
               "robotVoltage": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "robotCurrent": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "rmsVoltage": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "rmsCurrent": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "power": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "rmsPower": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "powerFactor": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "voltageRange": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "currentRange": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "phasor": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "reactivePower": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "totalHarmonicDistortion": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
       }
  },
  {
    "id": id,
     "cluster": "srdf",
     "type": "EndEffectorState",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "EndEffectorState",
               "@documentation": { "@title": "EndEffectorState", "@description": "data type for robot joints (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": "AssetState",
               // timeStamp should be embedded in name
               "@key": { "@type": "Lexical", "@fields": ["name"] },
               "position": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "pose": {
                 "@type"  : "Optional",
                 "@class" : "Pose"
               },
               "force": {
                 "@type"  : "Optional",
                 "@class" : "Vector3"
               },
               "momentum": {
                 "@type"  : "Optional",
                 "@class" : "Vector3"
               },
               "actualMomentum": {
                 "@type"  : "Optional",
                 "@class" : "Vector3"
               },
               "transform": {
                 "@type"  : "Optional",
                 "@class" : "Transform"
               }
       }
  },
  {
    "id": id,
     "cluster": "srdf",
     "type": "KinematicChain",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "KinematicChain",
               "@documentation": { "@title": "KinematicChain", "@description": "kinematic group defining a manipulator or kinematic chain (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": "AssetStructure",
               "@key": { "@type": "Lexical", "@fields": ["name"] },
               "baseLink": {
                 "@type"  : "Optional",
                 "@class" : "Link"
               },
               "tipLink": {
                 "@type"  : "Optional",
                 "@class" : "Link"
               },
               //"joints": {
               //  "@type"  : "Set",
               //  "@class" : "Joint"
               //},
       }
  },
]);
