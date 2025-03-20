//  "dependencies": ["core"],
import { clusterType, clusterDefFunction } from 'common-types';

//export const policyCluster: clusterType[] = [
export const policyCluster: clusterDefFunction = (id): clusterType[] => ([
  {
    "id": id,
    "cluster": 'policy',
    "type": "JsonLogicVarMap",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "JsonLogicVarMap",
      "@subdocument": [],
      "@documentation": {
        "@title": "JsonLogicVarMap", "@description": "map from var name to property value on an instance (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "variable": "xsd:string",
      "property": "xsd:string",
      "subjectType": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "subjectName": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "subjectId": {
        "@type": "Optional",
        "@class": "xsd:string"
      }
    }
  },
  {
    "id": id,
    "cluster": "policy",
    "type": "TaggedValue",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "TaggedValue",
      "@subdocument": [],
      "@documentation": {
        "@title": "TaggedValue", "@description": " (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "@oneOf": {
        "taggedString": "xsd:string",
        "taggedNumber": "xsd:decimal",
        "taggedBoolean": "xsd:boolean"
      }
    }
  },
  {
    "id": id,
    "cluster": "policy",
    "type": "JsonLogic",
    "version": "v022",
    "woql": {
      "@type": "TaggedUnion",
      "@id": "JsonLogic",
      "@subdocument": [],

      "@documentation": {
        "@title": "JsonLogic", "@description": "outer type for JsonLogic of shape {operator : [values ... ]} (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "taggedString": "xsd:string",
      "taggedNumber": "xsd:decimal",
      "taggedBoolean": "xsd:boolean",
      "var": {
        "@type": "Set",
        "@class": "TaggedValue"
      },
      "missing": {
        "@type": "Set",
        "@class": "JsonLogicVarMap",
        "@cardinality": 1
      },
      "scheduleCron": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 1
      },
      "scheduleDate": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 1
      },
      "if": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@max_cardinality": 3
      },
      "and": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@min_cardinality": 1
      },
      "or": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@min_cardinality": 1
      },
      "==": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 2
      },
      "===": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 2
      },
      "!=": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 2
      },
      "!==": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 2
      },
      "!": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 1
      },
      "!!": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 1
      },
      ">": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 3
      },
      "<": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 3
      },
      ">=": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 3
      },
      "<=": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 3
      },
      "max": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@min_cardinality": 1
      },
      "min": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@min_cardinality": 1
      },
      "+": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@min_cardinality": 1
      },
      "-": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@min_cardinality": 1

      },
      "*": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@min_cardinality": 2
      },
      "/": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 2
      },
      "%": {
        "@type": "Set",
        "@class": "JsonLogic",
        "@cardinality": 2
      },
      "map": {
        "@type": "Set",
        "@class": "JsonLogic",
      },
      "reduce": {
        "@type": "Set",
        "@class": "JsonLogic",
      },
      "filter": {
        "@type": "Set",
        "@class": "JsonLogic",
      },
      "all": {
        "@type": "Set",
        "@class": "JsonLogic",
      },
      "none": {
        "@type": "Set",
        "@class": "JsonLogic",
      },
      "some": {
        "@type": "Set",
        "@class": "JsonLogic",
      },
      "merge": {
        "@type": "Set",
        "@class": "JsonLogic"
      },
      "in": {
        "@type": "Set",
        "@class": "JsonLogic",
      },
      "cat": {
        "@type": "Set",
        "@class": "JsonLogic",
      },
      "substr": {
        "@type": "Set",
        "@class": "JsonLogic",
      },
      "log": {
        "@type": "Set",
        "@class": "JsonLogic",
      },
    }
  },
  {
    "id": id,
    "cluster": "policy",
    "type": "Policy",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "Policy",
      "@documentation": {
        "@title": "Policy", "@description": "abstract policy type for facility cobot (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      //"@inherits": "ProductionOperation",  wac found this error aug 29 when writing report, believe no code change required: todo investigate
      "@inherits": "AbstractEntity",
      "policyOn": {
        "@type": "Set",
        "@class": "PhysicalEntity"
      },
      "policyIn": {
        "@type": "Optional",
        "@class": "PolicySet"
      },
      "enabled": "xsd:boolean",
      "policyOnCompletion": {
        "@type": "Optional",
        "@class": "Policy"
      },
      "policyHolder": {
        "@type": "Optional",
        "@class": "CyberPhysicalActor"
      },
      "condition": "JsonLogic",
      "vars": {
        "@type": "Set",
        "@class": "JsonLogicVarMap",
      },
      "action": "ActionEntity"
    }
  },
  {
    "id": id,
    "cluster": "policy",
    "type": "PolicySet",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "PolicySet",
      "@documentation": {
        "@title": "PolicySet", "@description": "abstract policy set type for facility cobot (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": "Policy"
    }
  },
  {
    "id": id,
    "cluster": "policy",
    "type": "OperationPolicy",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "OperationPolicy",
      "@documentation": {
        "@title": "OperationPolicy", "@description": " policy type and API for operations(version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "Policy",
      "@key": { "@type": "Lexical", "@fields": ["name"] },
    }
  },
  {
    "id": id,
    "cluster": "policy",
    "type": "SubSystemStatePolicy",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "SubSystemStatePolicy",
      "@documentation": {
        "@title": "SubSystemStatePolicy", "@description": "policy for conditions on SubSystemState (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "Policy",
      "@key": { "@type": "Lexical", "@fields": ["name"] }
    }
  },
  {
    "id": id,
    "cluster": "policy",
    "type": "WorkItemTask",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "WorkItemTask",
      "@documentation": {
        "@title": "WorkItemTask", "@description": "WorkItemTask is derived from WorkItemTask.msg with operation and param from Policy.action and Policy.param. It is associated with an entity via PolicyOn (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "Task",
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "parentPolicy": "Policy"
    }
  }
]);
