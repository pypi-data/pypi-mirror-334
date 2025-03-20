// "dependencies": ["core","policy", "ros", "vision"],
import { clusterType } from 'common-types';

export const dulCluster = (id): clusterType[] => ([
  {
    "id": id,
    "cluster": "dul",
    "type": "Entity",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Entity",
      "@documentation": {
        "@title": "Entity", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["UsdMultiAppliedAPI"],

      "name": "xsd:string"
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Abstract",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Abstract",
      "@documentation": {
        "@title": "Abstract", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Entity"],


    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Quality",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Quality",
      "@documentation": {
        "@title": "Quality", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Entity"]
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "PhysicalQuality",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PhysicalQuality",
      "@documentation": {
        "@title": "PhysicalQuality", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Quality"]
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Extrinsic",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Extrinsic",
      "@documentation": {
        "@title": "Extrinsic", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["PhysicalQuality"]
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Localization",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Localization",
      "@documentation": {
        "@title": "Localization", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Extrinsic", "Location"]
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Region",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Region",
      "@documentation": {
        "@title": "Region", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Abstract"]
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "SpaceRegion",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "SpaceRegion",
      "@documentation": {
        "@title": "SpaceRegion", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Abstract"]
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Location",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Location",
      "@documentation": {
        "@title": "Location", "@description": "Currently a pure alias to SpaceRegion (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["SpaceRegion"]
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "TimeInterval",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "TimeInterval",
      "@documentation": {
        "@title": "TimeInterval", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Region"]
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Event",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Event",
      "@documentation": {
        "@title": "Event", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Entity"],
      "isOccuranceOf": {
        "@type": "Optional",
        "@class": "EventType"
      },
      "hasPhase": {
        "@type": "Optional",
        "@class": "Event"
      },
      "hasParticipant": {
        "@type": "Optional",
        "@class": "Object"
      },
      "hasTimeInterval": {
        "@type": "Optional",
        "@class": "TimeInterval"
      },
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Action",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Action",
      "@documentation": {
        "@title": "Action", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Event"],
      "isExecutedBy": {
        "@type": "Optional",
        "@class": "Agent"
      },
      "hasParticipant": {
        "@type": "Optional",
        "@class": "Agent"
      },
      "executesTask": {
        "@type": "Optional",
        "@class": "Task"
      },
    "hasOrigin": {
        "@type": "Optional",
        "@class": "Location"
      },
      "hasDestination": {
        "@type": "Optional",
        "@class": "Location"
      },
    }
  },
  {
    "id": id,
    "cluster": "dul",

    "type": "Object",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Object",
      "@documentation": {
        "@title": "Object", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Entity"]

    }
  },
  {
    "id": id,
    "cluster": "dul",

    "type": "PhysicalObject",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PhysicalObject",
      "@documentation": {
        "@title": "PhysicalObject", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Object"],
      "hasLocation": {
        "@type": "Optional",
        "@class": "Location"
      },
      "hasLocalization": {
        "@type": "Optional",
        "@class": "Localization"
      },
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "SocialObject",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "SocialObject",
      "@documentation": {
        "@title": "SocialObject", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Object"]
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Agent",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Agent",
      "@documentation": {
        "@title": "Agent", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Object"]
    }
  },

  {
    "id": id,
    "cluster": "dul",
    "type": "Concept",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Concept",
      "@documentation": {
        "@title": "Concept", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["SocialObject"],
      "isDefinedIn": {
        "@type": "Optional",
        "@class": "Description"
      },
      "hasPart": {
        "@type": "Optional",
        "@class": "Concept"
      },



    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "EventType",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "EventType",
      "@documentation": {
        "@title": "EventType", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Concept"],
      "classifies": {
        "@type": "Optional",
        "@class": "Event"
      }
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Role",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Role",
      "@documentation": {
        "@title": "Role", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Concept"],
      "isRoleOf": {
        "@type": "Optional",
        "@class": "Object"
      },
      "classifies": {
        "@type": "Optional",
        "@class": "Object"
      },




    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Process",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Process",
      "@documentation": {
        "@title": "Process", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Event"],




    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Collection",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Collection",
      "@documentation": {
        "@title": "Collection", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["SocialObject"],




    }
  }, {
    "id": id,
    "cluster": "dul",
    "type": "Configuration",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Configuration",
      "@documentation": {
        "@title": "Configuration", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Collection"],




    }
  },

  {
    "id": id,
    "cluster": "dul",
    "type": "State",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "State",
      "@documentation": {
        "@title": "State", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Configuration"],

    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "State",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "State",
      "@documentation": {
        "@title": "State", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Configuration"],




    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Task",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Task",
      "@documentation": {
        "@title": "Task", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["EventType"],
      /*
      "hasPart": {
        "@type": "Optional",
        "@class": "Task"
      },
      */
      "isExecutedIn": {
        "@type": "Optional",
        "@class": "Action"
      },
      "isTaskDefinedIn": {
        "@type": "Optional",
        "@class": "Description"
      },
      "isTaskOf": {
        "@type": "Optional",
        "@class": "Role"
      },
      "isSubTaskOf": {
        "@type": "Optional",
        "@class": "Task"
      },
      "followsPlan": {
        "@type": "Optional",
        "@class": "Plan"
      },





    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Description",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Description",
      
      "@documentation": {
        "@title": "Description", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      //"@subdocument": [],
      "@unfoldable": [],
      "@key": { "@type": "ValueHash" },
      "@inherits": ["SocialObject"],
      "description": "xsd:string"
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Goal",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Goal",
      "@documentation": {
        "@title": "Goal", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Description"],




    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Plan",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Plan",
      "@documentation": {
        "@title": "Plan", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Description"],
      "hasComponent": {
        "@type": "Optional",
        "@class": "Plan"
      },
      "definesTask": {
        "@type": "Optional",
        "@class": "Task"
      },
      "hasParticipant": {
        "@type": "Optional",
        "@class": "Agent"
      },
      /*
      "executesTask": {
        "@type": "Optional",
        "@class": "Task"
      },
      */
      "hasSetting": {
        "@type": "Optional",
        "@class": "Situation"
      },
      "hasMainGoal": {
        "@type": "Optional",
        "@class": "Goal"
      },
    }
  },
  {
    "id": id,
    "cluster": "dul",
    "type": "Situation",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Situation",
      "@documentation": {
        "@title": "Situation", "@description": " (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Entity"],
      "isSettingFor": {
        "@type": "Optional",
        "@class": "Entity"
      },
      "satisfies": {
        "@type": "Optional",
        "@class": "Description"
      }

    }
  },


]);
