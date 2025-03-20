// "dependencies": ["core"],
import { clusterType } from 'common-types';

export const rosCluster = (id): clusterType[] => ([
  {
    "id": id,
    "cluster": "ros",
    "type": "Geometry",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Geometry",
      "@documentation": {
        "@title": "Geometry", "@description": "Generic base for expressing geometric information for entity position, location, orientation, shape (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": "AbstractEntity"
    }
  },
  {
    "id": id,
    "cluster": "ros",
    "type": "Polygon",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Polygon",
      "@documentation": { "@title": "Polygon", "@description": "Polygon is the abstract type for the coordinates of a contour (Table)" },
      "@abstract": [],
      "@inherits": "Geometry",
      "points": {
        "@type": "Array",
        "@dimensions": 1,
        "@class": "Point"
      }
      /*
      "contour": {
        "@type": "Array",
        "@dimensions": 2,
        "@class": "xsd:decimal"
      }
      */
    }
  },
  {
    "id": id,
    "cluster": "ros",
    "type": "Orientation",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Orientation",
      "@documentation": { "@title": "Orientation", "@description": "The orientation component of Pose" },
      "@abstract": [],
      "@inherits": "Geometry",
      "orientation": "Quaternion"
    }
  },
  {
     "id": id,
     "cluster": "ros",
     "type": "Pose",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Pose",
               "@documentation": { "@title": "Pose", "@description": "Pose data model for expressing pose information (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@abstract": [],
               "@inherits": "Location"
       }
  },
  {
    "id": id,
    "cluster": "ros",
     "type": "Pose3D",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Pose3D",
               "@documentation": { "@title": "Pose3D", "@description": "data model equivalent of ROS geometry_msgs/Pose.msg (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": "Pose",
               "@subdocument": [],
               "@key": { "@type": "ValueHash" },
               "position": "Point",
               "orientation": "Quaternion"
       }
  },
  
  {
    "id": id,
     "cluster": "ros",
     "type": "Location",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Location",
               "@documentation": { "@title": "Location", "@description": "Base model for expressing tuple or cartesian definition of location (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@abstract": [],
               "@inherits": "Geometry",
               "locationOf": {
                 "@type"  : "Optional",
                 "@class" : "PhysicalEntity"
               },
               "locationIn": {
                 "@type"  : "Optional",
                 "@class" : "Polygon"
               }
       }
  },
  

  /*
  {
    "id": id,
    "cluster": "ros",
    "type": "Transform",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Transform",
      "@documentation": { "@title": "Transform", "@description": "data type equivalent for ROS geometry_msgs/Transform.msg" },
      "@inherits": "AssetState",
      // timeStamp should be embedded in name
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "translation": "Vector3",
      "rotation": "Quaternion"
    }
  },
  */
  {
    "id": id,
     "cluster": "ros",
     "type": "Orientation",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Orientation",
               "@documentation": { "@title": "Orientation", "@description": "The orientation component of Pose (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@abstract": [],
               "@inherits": "Geometry",
               "orientation": "Quaternion"
       }
  },
  {
    "id": id,
     "cluster": "ros",
     "type": "Quaternion",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Quaternion",
               "@subdocument": [],
               "@documentation": { "@title": "Quaternion", "@description": "Quaternion equivalent to geomerty_msgs.Quaternion (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@key": { "@type": "ValueHash" },
               "x": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "y": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "z": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "w": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
     "cluster": "ros",
     "type": "Transform",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Transform",
               "@documentation": { "@title": "Transform", "@description": "data type equivalent for ROS geometry_msgs/Transform.msg (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@inherits": "EntityState", // AssetState
               // timeStamp should be embedded in name
               "@key": { "@type": "Lexical", "@fields": ["name"] },
               "translation": "Vector3",
               "rotation":  "Quaternion"
       }
  },
  {
    "id": id,
     "cluster": "ros",
     "type": "Pose2D",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Pose2D",
               "@inherits": "Pose",
               "@subdocument": [],
               "@documentation": { "@title": "Pose2D", "@description": "subdocument (local) corresponding to geometry_msgs/Pose2D (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@key": { "@type": "ValueHash" },
               "x": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "y": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "theta": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
     "cluster": "ros",
     "type": "Vector3",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Vector3",
               "@subdocument": [],
               "@documentation": { "@title": "Vector3", "@description": "type corresponding to geometry_msgs/Vector3 (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@key": { "@type": "ValueHash" },
               "x": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "y": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "z": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },
  {
    "id": id,
     "cluster": "ros",
     "type": "Point",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Point",
               "@subdocument": [],
               "@documentation": { "@title": "Point", "@description": "type corresponding to geometry_msgs/Point (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@key": { "@type": "ValueHash" },
               "x": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "y": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               },
               "z": {
                 "@type"  : "Optional",
                 "@class" : "xsd:decimal"
               }
       }
  },

  /*
  {
    "id": id,
    "cluster": "core",
    "type": "Pose",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Pose",
      "@documentation": { "@title": "Pose", "@description": "Pose data model for expressing pose information" },
      "@abstract": [],
      "@inherits": "Location"
    }
  },
  */

 
  {
    "id": id,
     "cluster": "ros",
     "type": "Cartesian",
     "version":"v022",
     "woql": {
               "@type": "Class",
               /* 
                 Should this be Location? i think location should be an abstract type that supports tuples as well as Point
                 todo synch with ROS: 
                 current proposal:
                                   add Location base
                                   add Point as object format {x y z}
                                   Cartesian is then array of Point
               */
               "@id": "Cartesian",
               "@documentation": { "@title": "Point", "@description": "Point is the abstract type for the cartesian coordinates of a point (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@abstract": [],
               "@inherits": "Location",
               /*
               "coordinates": {
                 "@type": "Array",
                 "@dimensions": 1,
                 "@class": "Point"
               }
               */
               "point": "Point"
       }
  },
  {
    "id": id,
     "cluster": "ros",
     "type": "Polygon",
     "version":"v022",
     "woql": {
               "@type": "Class",
               "@id": "Polygon",
               "@documentation": { "@title": "Polygon", "@description": "Polygon is the abstract type for the coordinates of a contour (Table) (version:v022)",
               "@authors": ["William A Coolidge"]},
               "@abstract": [],
               "@inherits": "Geometry",
               "points": {
                 "@type": "Array",
                 "@dimensions": 1,
                 "@class": "Point" 
               }
               /*
               "contour": {
                 "@type": "Array",
                 "@dimensions": 2,
                 "@class": "xsd:decimal"
               }
               */
              }
  }
             
]);
