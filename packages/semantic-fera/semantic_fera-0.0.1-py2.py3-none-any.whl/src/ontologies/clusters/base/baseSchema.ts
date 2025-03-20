import { clusterType } from 'common-types';

export const baseCluster = (id): clusterType[] => ([

  {
    "id": id,
    "cluster": "base",
    "type": "NamedType",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "NamedType",
      "@abstract": [],
      "@documentation": {
        "@title": "NamedType",
        "@description": "",
        "@authors": ["William A Coolidge"]
      },
      "name": "xsd:string"
    }
  },
/*
  {
    "id": id,
    "cluster": "usd",
    "type": "TemporalEntity",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "TemporalEntity",
      "@documentation": {
        "@title": "TemporalEntity", "@description": "base type for all temporal entities (characterized by values over time) (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      //"@inherits": "AbstractEntity",
      "@inherits": "UsdMultiAppliedAPI",
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
      },
      "samplePeriod": {
        "@type": "Optional",
        "@class": "xsd:float"
      }
    }
  },
*/
  /*
  {
    "id": id,
    "cluster": "core",
    "type": "Thing",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Thing",
      "@documentation": {
        "@title": "owl:Thing", "@description": "OWL Thing root (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": []
    }
  },
  {
    "id": id,
    "cluster": "core",
    "type": "IndexedEntity",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "IndexedEntity",
      "@documentation": {
        "@title": "IndexedEntity", "@description": "IndexedEntity data model (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "index": {
        "@type": "Optional",
        "@class": "xsd:unsignedLong",
      }
    }
  },
  {
    "id": id,
    "cluster": "core",
    "type": "CommonEntity",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "CommonEntity",
      "@documentation": {
        "@title": "CommonEntity", "@description": "CommonEntity data model (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": ["Thing", "IndexedEntity"],
      "name": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
    
      "value": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "number": {
        "@type": "Optional",
        "@class": "xsd:decimal"
      },
      "description": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "notation": {
        "@type": "Optional",
        "@class": "xsd:string"
      }
    }
  },
  {
    "id": id,
    "cluster": "core",
    "type": "Label",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Label",
      "@documentation": {
        "@title": "Label", "@description": "generic name value pair for custom properties of string type (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "@inherits": "CommonEntity",
      "labelOf": {
        "@type": "Optional",
        "@class": "CommonEntity"
      }
    }
  },
  {
    "id": id,
    "cluster": "core",
    "type": "AbstractEntity",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "AbstractEntity",
      "@documentation": {
        "@title": "AbstractEntity", "@description": "base type for all logical entities (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": "CommonEntity",
    }
  },
  {
    "id": id,
    "cluster": "core",
    "type": "PhysicalEntity",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "PhysicalEntity",
      "@documentation": {
        "@title": "PhysicalEntity", "@description": "base type for all physical entities (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": "AbstractEntity"
    }
  },
  {
    "id": id,
    "cluster": "core",
    "type": "Set",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Set",
      "@documentation": {
        "@title": "Set", "@description": "Abstract Set type (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": "AbstractEntity",
      "includes": {
        "@type": "Set",
        "@class": "AbstractEntity",
      },
    }
  },
  {
    "id": id,
    "cluster": "core",
    "type": "EntitySet",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "EntitySet",
      "@documentation": {
        "@title": "RoomEntity", "@description": "concrete set for room entities (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["Set", "PhysicalEntity"],
    }
  },
  {
    "id": id,
    "cluster": "core",
    "type": "SampledEntity",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "SampledEntity",
      "@documentation": {
        "@title": "Entity", "@description": "base type for all sampled entities (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": "AbstractEntity",
      "timeStamp": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "sampleIndex": {
        "@type": "Optional",
        "@class": "xsd:unsignedLong"
      }
    }
  },
  {
    "id": id,
    "cluster": "core",
    "type": "TemporalEntity",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "TemporalEntity",
      "@documentation": {
        "@title": "TemporalEntity", "@description": "base type for all temporal entities (characterized by values over time) (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": "AbstractEntity",
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
    "cluster": "core",
    "type": "CyberPhysicalActor",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "CyberPhysicalActor",
      "@documentation": {
        "@title": "CyberPhysicalActor", "@description": "abstract actors (robots, personnel, etc) (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": "AbstractEntity"
    }
  },
  {
    "id": id,
    "cluster": "core",
    "type": "SampledData",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "SampledData",
      "@documentation": {
        "@title": "SampledData", "@description": "data model for SampledData (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": "SampledEntity",
      "sampledDataOf": {
        "@type": "Optional",
        "@class": "PhysicalEntity"
      },
      "unit": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "dataValue": "xsd:decimal",
    }
  },
  {
    "id": id,
    "cluster": "core",
    "type": "VisionData",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "VisionData",
      "@documentation": {
        "@title": "VisionData", "@description": "data model for VisionData (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": "SampledEntity"
    }
  },
  
  {
    "id": id,
    "cluster": "core",
    "type": "ActionEntity",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "ActionEntity",
      "@documentation": {
        "@title": "ActionEntity", "@description": "base action type(version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": "TemporalEntity"
    }
  },

  {
    "id": id,
    "cluster": "core",
    "type": "Person",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Person",
      "@abstract": [],
      "@documentation": {
        "@title": "Person", "@description": "Person type (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["CyberPhysicalActor"]
    }
  },
  */
]);
