// "dependencies": ["core","policy", "ros", "vision"],
import { clusterType } from 'common-types';

export const plantCluster = (id): clusterType[] => ([
  {
    "id": id,
    "cluster": "plant",
    "type": "Zone",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Zone",
      "@documentation": {
        "@title": "Zone", "@description": "Zone is the abstract type for the 4 corner x,y coordinates of a rectangle (version:v022)",
        "@authors": ["William A Coolidge"]
      },
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


  /* duplicate
{
   "cluster": "plant",
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
    "cluster": "plant",
    "type": "Grip",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Grip",
      "@documentation": {
        "@title": "Grip", "@description": "grip operation (version:v022)",
        "@authors": ["William A Coolidge"]
      },
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
    "cluster": "plant",
    "type": "Gripper",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Gripper",
      "@documentation": {
        "@title": "Gripper", "@description": "The gripper (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "PhysicalEntity",
      "@key": { "@type": "Lexical", "@fields": ["name"] }
    }
  },
  {
    "id": id,
    "cluster": "plant",
    "type": "Grippable",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Grippable",
      "@documentation": {
        "@title": "Grippable", "@description": "Grippable type (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "AbstractEntity"
    }
  },
  {
    "id": id,
    "cluster": "plant",
    "type": "Obstacle",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Obstacle",
      "@documentation": {
        "@title": "Obstacle", "@description": "Obstacle type (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "RoomEntity",
      "@key": { "@type": "Lexical", "@fields": ["name"] }
    }
  },

  {
    "id": id,
    "cluster": "plant",
    "type": "AGV",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "AGV",
      "@documentation": {
        "@title": "AGV", "@description": "AGV type (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["NoTouchObject", "CyberPhysicalActor"],
      "@abstract": [],
    }
  },

  {
    "id": id,
      "cluster": "plant",
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
      "cluster": "plant",
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
      "cluster": "plant",
      "type": "Route",
      "version":"v022",
      "woql": {
               
                   "@type": "Class",
                   "@id": "Route",
                   "@documentation": { "@title": "Route", "@description": "Route is a path, i.e array of coordinates, through a Passage (version:v022)",
       "@authors": ["William A Coolidge"]},
                   "@inherits": "Passage",
                   "@key": { "@type": "Lexical", "@fields": ["name"] },
                   "wayPoints": "Pose"
        }
   },
   {
    "id": id,
      "cluster": "plant",
      "type": "Room",
      "version":"v022",
      "woql": {
                   "@type": "Class",
                   "@id": "Room",
                   "@documentation": { "@title": "Room", "@description": "The physical room and volume of control for operations and objects (version:v022)",
       "@authors": ["William A Coolidge"]},
                   "@inherits": "Zone",
                   "@key": { "@type": "Lexical", "@fields": ["name"] }
        }
   },
   {
    "id": id,
      "cluster": "plant",
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
     "cluster": "plant",
     "type": "AssetGroup",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "AssetGroup",
           "@abstract": [],
           "@documentation": { "@title": "AssetGroup", "@description": "aggregate data model for cell or group of assets (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "Asset",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "assets": {
             "@type": "Set",
             "@class": "Asset"
           }
       }
  },
  {
    "id": id,
     "cluster": "plant",
     "type": "AssetPart",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "AssetPart",
           "@documentation": { "@title": "AssetPart", "@description": "physical asset part data model' (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": ["PhysicalEntity", "ProductInformation"],
           "@abstract": [],
           "partOf": {
             "@type": "Optional",
             "@class": "Asset"
           }
       }
  },
  {
    "id": id,
    "cluster": "plant",
    "type": "AGV",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "AGV",
      "@documentation": {
        "@title": "AGV", "@description": "AGV type (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "CyberPhysicalActor",
      "@abstract": [],
    },
  }
]);
