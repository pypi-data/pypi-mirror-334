// "dependencies": ["core","i4", "ros"],
import { clusterType } from 'common-types';

export const urdfCluster = (id): clusterType[] => ([
  {
     "id": id,
     "cluster": "urdf",
     "type": "KinematicNode",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "KinematicNode",
               "@documentation": { "@title": "KinematicNode", "@description": "base type defining a kinematic node, i.e. a joint with links as edges in the graph (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@abstract": [],
               "@inherits": "PhysicalEntity",
               "origin": {
                 "@type"  : "Optional",
                 "@class" : "Origin"
               },
               "parentLink": {
                 "@type"  : "Optional",
                 "@class" : "Link"
               }
               /*,
               "childLink": {
                 "@type"  : "Optional",
                 "@class" : "Link"
               },
               */
       }
  },
  {
    "id": id,
     "cluster": "urdf",
     "type": "Joint",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Joint",
               "@documentation": { "@title": "Joint", "@description": "defines the concrete kinematic node that defines a joint (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": ["KinematicNode", "AssetPart"],
               "@key": { "@type": "Lexical", "@fields": ["name"] },
               "childLink": "Link",
               "axis": {
                 "@type"  : "Optional",
                 "@class" : "Vector3"
               },
               "calibration": {
                 "@type"  : "Optional",
                 "@class" : "Calibration"
               },
               "dynamics": {
                 "@type"  : "Optional",
                 "@class" : "Dynamics"
               },
               "mimic": {
                 "@type"  : "Optional",
                 "@class" : "Mimic"
               },
               "safetyController": {
                 "@type"  : "Optional",
                 "@class" : "SafetyController"
               }
       }
  },
  {
    "id": id,
     "cluster": "urdf",
     "type": "Sensor",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Sensor",
               "@documentation": { "@title": "Sensor", "@description": "URDF type equivalent for a sensor (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": ["KinematicNode", "AssetPart"],
               "@key": { "@type": "Lexical", "@fields": ["name"] },
               "updateRate": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
               /*,
               "camera": {
                 "@type"  : "Optional",
                 "@class" : "Camera"
               },
               "ray": {
                 "@type"  : "Optional",
                 "@class" : "Ray"
               }
               */
       }
  },
  {
    "id": id,
     "cluster": "urdf",
     "type": "Calibration",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Calibration",
               "@subdocument": [],
               "@documentation": { "@title": "Calibration", "@description": "type corresponding URDF Joint Calibration (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@key": { "@type": "ValueHash" },
               "rising": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "falling": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
     "cluster": "urdf",
     "type": "Dynamics",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Dynamics",
               "@subdocument": [],
               "@documentation": { "@title": "Dynamics", "@description": "type corresponding URDF Joint Dynamics (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@key": { "@type": "ValueHash" },
               "damping": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "friction": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
     "cluster": "urdf",
     "type": "Mimic",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Mimic",
               "@subdocument": [],
               "@documentation": { "@title": "Mimic", "@description": "type corresponding URDF Joint Mimic (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@key": { "@type": "ValueHash" },
               "joint": "Joint",
               "multiplier": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "offset": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
     "cluster": "urdf",
     "type": "SafetyController",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "SafetyController",
               "@subdocument": [],
               "@documentation": { "@title": "SafetyController", "@description": "type corresponding URDF Joint SafetyController (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@key": { "@type": "ValueHash" },
               "kVelocity": "xsd:decimal",
               "kPosition": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "softLowerLimit": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "softUpperLimit": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
     "cluster": "urdf",
     "type": "Link",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Link",
               "@documentation": { "@title": "Link", "@description": "defines the edge between the chain (graph) of kinematic nodes (joints) and the associated kinematic properties (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": ["AssetPart"],
               "@key": { "@type": "Lexical", "@fields": ["name"] },
               
               "inertial": {
                 "@type"  : "Optional",
                 "@class" : "Inertial"
               },
               "visual": {
                 "@type"  : "Optional",
                 "@class" : "Visual"
               },
               "collision": {
                 "@type"  : "Optional",
                 "@class" : "Collision"
               }
       }
  },
  {
    "id": id,
     "cluster": "urdf",
     "type": "Inertial",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Inertial",
               "@documentation": { "@title": "Inertial", "@description": "URDF Inertial type (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@subdocument": [],
               "@key": { "@type": "ValueHash" },
               "origin":  {
                 "@type"  : "Optional",
                 "@class" : "Origin"
               },
               "inertia": {
                 "@type"  : "Optional",
                 "@class" : "Inertia"
               },
       }
  },
  {
    "id": id,
     "cluster": "urdf",
     "type": "Inertia",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Inertia",
               "@documentation": { "@title": "Inertia", "@description": "ROS geometry_msgs/Inertia.msg equivalent (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@subdocument": [],
               "@key": { "@type": "ValueHash" },
               "m":  {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "com": {
                 "@type"  : "Optional",
                 "@class" : "Vector3"
               },
               "ixx": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "ixy": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "ixz": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "iyy": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "iyz": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "izz": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
     "cluster": "urdf",
     "type": "Visual",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Visual",
               "@documentation": { "@title": "Visual", "@description": "URDF Visual type (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": ["AbstractEntity"],
               "@subdocument": [],
               "@key": { "@type": "ValueHash" },
               "origin":  {
                 "@type"  : "Optional",
                 "@class" : "Origin"
               },
               "geometry": {
                 "@type"  : "Optional",
                 "@class" : "Box"
               },
               "material": {
                 "@type"  : "Optional",
                 "@class" : "Material"
               }
       }
  },
  {
    "id": id,
     "cluster": "urdf",
     "type": "Collision",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Collision",
               "@documentation": { "@title": "Collision", "@description": "URDF Collision type (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": ["AbstractEntity"],
               "@subdocument": [],
               "@key": { "@type": "ValueHash" },
               "origin":  {
                 "@type"  : "Optional",
                 "@class" : "Origin"
               },
               "geometry": {
                 "@type"  : "Optional",
                 "@class" : "Cylinder"
               },
       }
  },
  {
    "id": id,
  "cluster": "urdf",
  "type": "Material",
  "version":"v022",
  "woql": {
           
               "@type": "Class",
               "@id":"Material",
               "@documentation": { "@title": "Material", "@description": "URDF Material type (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": ["AbstractEntity"],
               "@subdocument": [],
               "@key": { "@type": "ValueHash" },
               "color":  {
                 "@type"  : "Optional",
                 "@class" : "ColorRGBA"
               }
       }
  },
  {
    "id": id,
    "cluster": "urdf",
    "type": "ColorRGBA",
    "version":"v022",
    "woql": 
             {
               "@type": "Class",
               "@id":"ColorRGBA",
               "@documentation": { "@title": "ColorRGBA", "@description": "ROS sts_msgs/ColorRGBA.msg equivalent (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@subdocument": [],
               "@key": { "@type": "ValueHash" },
               "r":  {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "g":  {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "b":  {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "a":  {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
    "cluster": "urdf",
    "type": "Box",
    "version":"v022",
    "woql": 
             {
               "@type": "Class",
               "@id":"Box",
               "@documentation": { "@title": "Box", "@description": "URDF geometry box (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": "Geometry",
               "@subdocument": [],
               "@key": { "@type": "ValueHash" },
               "size":  {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
    "cluster": "urdf",
    "type": "Cylinder",
    "version":"v022",
    "woql": 
             {
               "@type": "Class",
               "@id":"Cylinder",
               "@documentation": { "@title": "Cylinder", "@description": "URDF geometry cylinder (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": "Geometry",
               "@subdocument": [],
               "@key": { "@type": "ValueHash" },
               "radius":  {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "length":  {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
     "cluster": "urdf",
     "type": "Origin",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Origin",
               "inherits":"Geometry",
               "@subdocument": [],
               "@documentation": { "@title": "Origin", "@description": "type corresponding to euler_pose formatted as two vectors (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@key": { "@type": "ValueHash" },
               "xyz": {
                 "@type"  : "Array",
                 "@dimensions": 1,
                 "@class" : "xsd:decimal"
               },
               "rpy": {
                 "@type"  : "Array",
                 "@dimensions": 1,
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
     "cluster": "urdf",
     "type": "JointLimit",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "JointLimit",
               "@subdocument": [],
               "@documentation": { "@title": "JointLimit", "@description": "type from URDF corresponding to limits on revolute and prismatic joints) (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@key": { "@type": "ValueHash" },
               "lower":  {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "upper":  {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "effort":  {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "velocity":  {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  /* dup
  {
     "cluster": "urdf",
     "type": "GroupState",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "GroupState",
               "@documentation": { "@title": "GroupState", "@description": "configuration or data describing a KinematicChain such as a robot arm (version:v022)"},
               "@inherits": "AssetState",
               "@key": { "@type": "Lexical", "@fields": ["name"] },
               "jointGroup": "JointGroup",
       }
  },
  {
     "cluster": "urdf",
     "type": "JointState",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "JointState",
               "@documentation": { "@title": "JointState", "@description": "data type for robot joints (version:v022)"},
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
     "cluster": "urdf",
     "type": "MotorState",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "MotorState",
               "@documentation": { "@title": "MotorState", "@description": "data type for joint motor state (version:v022)"},
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
     "cluster": "urdf",
     "type": "DriveState",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "DriveState",
               "@documentation": { "@title": "DriveState", "@description": "data type for joint drive state (version:v022)"},
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
     "cluster": "urdf",
     "type": "EndEffectorState",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "EndEffectorState",
               "@documentation": { "@title": "EndEffectorState", "@description": "data type for joint end effector group state (version:v022)"},
               "@inherits": "AssetState",
               // timeStamp should be embedded in name
               "@key": { "@type": "Lexical", "@fields": ["name"] },
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
  */
]);
