//   "dependencies": ["state","product"],
import { clusterType } from 'common-types';

export const stateCluster = (id): clusterType[] => ([
    
  {
    "id": id,
    "cluster": "state",
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
    "cluster": "state",
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
      /*
      "operation": {
        "@type": "Optional",
        "@class": "ERStateOperation"
      },
      */
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
      /*
      "availableOperations": {
        "@type": "Set",
        "@class": "ERStateOperation"
      },
      */
      "error": {
        "@type": "Optional",
        "@class": "Error"
      },
    }
  },
  /* TODO: move to new cluster
  {
    "id": id,
    "cluster": "state",
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
      */
      /* TODO: Explore this: (note change in logic under typeMap insertion for parents)
      "@inherits": {
        "@id": "ProductionOperation",
        "@context": { "@vocab": "state-v022" }
      },
      */
     /*
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
  {
    "id": id,
    "cluster": "state",
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
    "cluster": "state",
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
    "cluster": "state",
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

]);
