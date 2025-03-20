//   "dependencies": ["i4","product"],
import { clusterType } from 'common-types';

export const i4Cluster = (id): clusterType[] => ([
    {
     "id": id,
     "cluster": "i4",
     "type": "Asset",
     "version":"v022",
     "woql": {
           "@type": "Class",
           //"@id": "AssetStructure",
           "@id": "Asset",
           "@documentation": { "@title": "Asset", "@description": "abstract data model for a high level asset (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": ["PhysicalEntity"/*, "ProductInformation"*/],
           "@abstract": []
       }
  },
  /* TODO: Move to new cluster
  {
    "id": id,
     "cluster": "i4",
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
     "cluster": "i4",
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
  */
  {
    "id": id,
    "cluster": "i4",
    "type": "ProductionEntity",
    "version":"v022",
    "woql": {
          "@type": "Class",
          "@id": "ProductionEntity",
          "@documentation": { "@title": "ProductionEntity", "@description": "abstract shell entity, effectively the AAS SubModel type (version:v022)",
          "@authors": ["William A Coolidge"]},
          "@inherits": ["AbstractEntity"],
          "@abstract": []
      }
 },
  {
    "id": id,
    "cluster": "i4",
    "type": "AssetShell",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@abstract": [],
      "@id": "AssetShell",
      "@documentation": {
        "@title": "AssetShell", "@description": "Abstract Asset Shell (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "CyberPhysicalActor",
      /*
        assetName is used in lexical id of derived types, lexical id of ConceptDictionary and SubModel instances
      */
      "assetName" : "xsd:string",
      "asset": "Asset",
      "availableOperations": {
        "@type": "Array",
        "@dimensions": 1,
        "@class": "ProductionOperation"
      },
      /*
      "conceptDictionary": {
        "@type": "Optional",
        "@class": "ConceptDictionary"
      },
      */
      "subModels": {
        "@type": "Set",
        "@class": "SubModel"
      },
      /*
        non-standard
      */
      "state": {
        "@type": "Optional",
        "@class": "State"
      },
      "heathSummary": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
    }
  },
  {
    "id": id,
    "cluster": "i4",
    "type": "SubModel",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@abstract": [],
      "@id": "SubModel",
      "@documentation": {
        "@title": "SubModel", "@description": "Abstract SubModel type (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "ProductionEntity",
      /*
        assetName is used in lexical id of derived types, lexical id of ConceptDictionary and SubModel instances
      */
      "assetName" : "xsd:string",
      "capabilities": {
        "@type": "Set",
        "@class": "Capability"
      },
      "skills": {
        "@type": "Set",
        "@class": "ProductionOperation"
      }
    }
  },
  {
    "id": id,
    "cluster": "i4",
    "type": "SubModelElement",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@abstract": [],
      "@id": "SubModelElement",
      "@documentation": {
        "@title": "SubModelElement", "@description": "Abstract SubModelElement type (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "ProductionEntity",

    }
  },
  {
    "id": id,
    "cluster": "i4",
    "type": "Capability",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@abstract": [],
      "@id": "Capability",
      "@documentation": {
        "@title": "Capability", "@description": "Abstract Capability type (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["SubModelElement"],
      "bddBehavior": {
        "@type": "Optional",
        "@class": "BDDBehavior"
      },

    }
  },
  {
    "id": id,
    "cluster": "i4",
    "type": "CapabilityMap",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "CapabilityMap",
      "@documentation": {
        "@title": "CapabilityMap", "@description": "Capability mapped to Skill (realization) (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "SubModelElement",
      "@abstract": [],
      //"@key": { "@type": "Lexical", "@fields": ["name", "capabilityName", "skillName"] },
      "capability": "Capability",
      "skill": "ShellOperation",
    }
  },
  /*
  {
    "id": id,
    "cluster": "i4",
    "type": "ConceptDescription",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ConceptDescription",
      "@documentation": {
        "@title": "ConceptDescription", "@description": "Abstract Asset Shell (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AbstractEntity","BDDBehavior"],
      "@key": { "@type": "Lexical", "@fields": ["name", "assetName"] },
      "assetName" : "xsd:string",
    }
  },
  {
    "id": id,
    "cluster": "i4",
    "type": "ConceptDictionary",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ConceptDictionary",
      "@documentation": {
        "@title": "ConceptDictionary", "@description": "Abstract Asset Shell (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["AbstractEntity"],
      "@key": { "@type": "Lexical", "@fields": ["name", "assetName"] },
      "assetName" : "xsd:string",
      "conceptDescriptions": {
        "@type": "Set",
        "@class": "ConceptDescription"
      },
    }
  },
  */
  {
    "id": id,
    "cluster": "i4",
    "type": "ProductionOperation",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "ProductionOperation",
      "@documentation": {
        "@title": "ProductionOperation", "@description": "abstract production operation type (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["ActionEntity", "SubModelElement"]
    }
  },
 
  {
    "id": id,
    "cluster": "i4",
    "type": "ShellOperation",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "ShellOperation",
      "@documentation": {
        "@title": "ShellOperation", "@description": "Abstract ShellOperation models operations for configuration, capability/skill matching, monitoring, and specification  (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["ProductionOperation"],
      "@abstract": [],
      //"action": "Operation",
      "param": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "actor": "AssetShell",
      "swAsset": {
        "@type": "Optional",
        "@class": "SWAsset"
      },
      "bddBehavior": {
        "@type": "Optional",
        "@class": "BDDBehavior"
      },
    }
  },
  /* move to state cluster 
  {
    "id": id,
    "cluster": "i4",
    "type": "EntityState",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "EntityState",
      "@documentation": { "@title": "EntityState", "@description": "EntityState is the type characterizing the status of the entities of work" },
      "@inherits": "TemporalEntity",
      "@abstract": [],
      "physicalEntity": {
        "@type": "Optional",
        "@class": "PhysicalEntity"
      }
    }
  },

  {
    "id": id,
    "cluster": "i4",
    "type": "State",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "State",
      "@documentation": {
        "@title": "State", "@description": "abstract type for reporting on the engine of application state (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "TemporalEntity",
      "@abstract": [],
      //"@key": { "@type": "Lexical", "@fields": ["subSystem", "state", "operation"] },
      "actor": {
        "@type": "Optional",
        "@class": "CyberPhysicalActor"
      },
      "subSystem": "xsd:string",
      "state": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      
      "operation": {
        "@type": "Optional",
        "@class": "ERStateOperation"
      },
      
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
      
      "availableOperations": {
        "@type": "Set",
        "@class": "ERStateOperation"
      },
      
      "error": {
        "@type": "Optional",
        "@class": "Error"
      },
    }
  },
  {
    "id": id,
    "cluster": "i4",
    "type": "Task",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Task",
      "@abstract": [],
      "@documentation": {
        "@title": "Task", "@description": "Task type (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      // TODO: Explore this: (note change in logic under typeMap insertion for parents)
     // "@inherits": {
     //   "@id": "ProductionOperation",
     //   "@context": { "@vocab": "i4-v022" }
     // },
      
      "@inherits": "ProductionOperation",
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "start": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "completion": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "operationInfo": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "operation": "ShellOperation"
    }
  },
  {
    "id": id,
    "cluster": "i4",
    "type": "Error",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Error",
      "@documentation": {
        "@title": "Error", "@description": "concrete type for reporting on error state (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "AbstractEntity",
      "@subdocument": [],
      "@key": { "@type": "ValueHash" },
      "health": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "message": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "stackTrace": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "isBlocking": {
        "@type": "Optional",
        "@class": "xsd:boolean"
      }
    }
  },
  {
    "id": id,
    "cluster": "i4",
    "type": "ServiceState",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "ServiceState",
      "@documentation": {
        "@title": "ServiceState", "@description": "ServiceState is the type characterizing the service status of the entities of work for the facility cobot (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "EntityState",
      "@abstract": [],

    }
  },
  {
    "id": id,
    "cluster": "i4",
    "type": "SubSystemState",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "SubSystemState",
      "@documentation": {
        "@title": "SubSystemState", "@description": "concrete type for reporting on an engine of application state (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "State",
      //"@subdocument": [],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    }
  },
  */

  /*

  
  {
          "id": id,
     "cluster": "i4",
     "type": "Task",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "Task",
           "@documentation": { "@title": "Task", "@description": "Task is the generic task type (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "ProductionOperation",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "start": {
             "@type": "Optional",
             "@class": "xsd:string"
           },
           "completion": {
             "@type": "Optional",
             "@class": "xsd:string"
           },
           "operationInfo": {
             "@type": "Optional",
             "@class": "xsd:string"
           },
           "operation": "ShellOperation"
       }
  },
  */
 /*
  {
          "id": id,
    "cluster": "i4",
    "type": "AssetShell",
    "version":"v022",
    "woql": {
          "@type": "Class",
          "@id": "AssetShell",
          "@documentation": { "@title": "AssetShell", "@description": "Asset Admin Shell for FacilityCobot, the type model for world services per se (version:v022)",
          "@authors": ["William A Coolidge"]},
          "@inherits": "CyberPhysicalActor",
          "@key": { "@type": "Lexical", "@fields": ["name"] },
          "state": "State",
          "heathSummary": {
            "@type": "Optional",
            "@class": "xsd:string"
          },
          "availableOperations": {
            "@type": "Array",
            "@dimensions": 1,
            "@class": "ERStateOperation"
          },
          "asset": "PhysicalEntity"
      }
 },
  {
          "id": id,
     "cluster": "i4",
     "type": "ShellOperation",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "ShellOperation",
           "@documentation": { "@title": "ShellOperation", "@description": "ShellOperation models operations for configuration, capability/skill matching, monitoring, and specification  (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": ["Operation", "ProductionOperation"],
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "action": "ERStateOperation",
           "param": {
             "@type": "Optional",
             "@class": "xsd:string"
           },
           "actor": "AssetShell"
       
       }
  },
  
  {
          "id": id,
     "cluster": "i4",
     "type": "Error",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "Error",
           "@documentation": { "@title": "Error", "@description": "concrete type for reporting on error state (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "AbstractEntity",
           "@subdocument": [],
           "@key": { "@type": "ValueHash" },
           "health": {
             "@type": "Optional",
             "@class": "xsd:string"
           },
           "message": {
             "@type": "Optional",
             "@class": "xsd:string"
           },
           "stackTrace": {
             "@type": "Optional",
             "@class": "xsd:string"
           },
           "isBlocking": {
             "@type": "Optional",
             "@class": "xsd:boolean"
           }
       }
  },
  
  {
    "id": id,
    "cluster": "i4",
    "type": "ProductionOperation",
    "version":"v022",
    "woql": {
          "@type": "Class",
          "@id": "ProductionOperation",
          "@documentation": { "@title": "ProductionOperation", "@description": "abstract operation type  (version:v022)",
          "@authors": ["William A Coolidge"]},
          "@abstract": [],
          "@inherits": "AbstractEntity"
      }
  },
  {
    "id": id,
    "cluster": "i4",
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
  */
]);
