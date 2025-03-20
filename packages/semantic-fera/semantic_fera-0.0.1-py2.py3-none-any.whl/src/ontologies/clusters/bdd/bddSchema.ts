//  "dependencies": ["core"],
import { clusterType, clusterDefFunction } from 'common-types';

//export const bddCluster: clusterType[] = [
export const bddCluster: clusterDefFunction = (id): clusterType[] => ([
  {
    "id": id,
    "cluster": 'bdd',
    "type": "BDDBehavior",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BDDBehavior",
      "@abstract": [],
     //"@key": { "@type": "Lexical", "@fields": ["name"] },
      "@documentation": {
        "@title": "BDDBehavior", "@description": "BDD  (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "feature": "BDDFeature",
      "describes": "AbstractEntity"
    }
  },
  {
    "id": id,
    "cluster": 'bdd',
    "type": "BDDFeature",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BDDFeature",
      "@subdocument": [],
      "@documentation": {
        "@title": "BDDFeature", "@description": "BDD  (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "descriptions": "xsd:string",
      "background" : "BDDBackground",
      "rule": "BDDRule", 
      "scenario": "BDDScenario",
      "scenarioTemplate": "BDDScenarioTemplate"

    }
  },
  {
    "id": id,
    "cluster": 'bdd',
    "type": "BDDBackground",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BDDBackground",
      "@subdocument": [],
      "@documentation": {
        "@title": "BDDBackground", "@description": "BDD  (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "given": "BDDGiven"
    }
  },
  {
    "id": id,
    "cluster": 'bdd',
    "type": "BDDSteps",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BDDSteps",
      "@subdocument": [],
      "@documentation": {
        "@title": "BDDSteps", "@description": "BDD  (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "when":  {
        "@type": "Optional",
        "@class":"BDDWhen"
      },
      "given":  {
        "@type": "Optional",
        "@class":"BDDGiven"
      },
      "then":  {
        "@type": "Optional",
        "@class":"BDDThen"
      },
      "and":  {
        "@type": "Optional",
        "@class":"BDDAnd"
      },
      "but": {
        "@type": "Optional",
        "@class":"BDDBut"
      }
    }
  },
  {
    "id": id,
    "cluster": 'bdd',
    "type": "BDDGiven",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BDDGiven",
      "@subdocument": [],
      "@documentation": {
        "@title": "BDDGiven", "@description": "BDD  (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "and": {
        "@type": "Optional",
        "@class": "BDDAnd"
      },
      "but": {
        "@type": "Optional",
        "@class": "BDDBut"
      },
      "step": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "given": {
        "@type": "Optional",
        "@class": "BDDGiven"
      },
    }
  },
  {
    "id": id,
    "cluster": 'bdd',
    "type": "BDDThen",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BDDThen",
      "@subdocument": [],
      "@documentation": {
        "@title": "BDDThen", "@description": "BDD  (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "and": {
        "@type": "Optional",
        "@class": "BDDAnd"
      },
      "but": {
        "@type": "Optional",
        "@class": "BDDThen"
      },
      "step": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "then": {
        "@type": "Optional",
        "@class": "BDDThen"
      },
    }
  },
  {
    "id": id,
    "cluster": 'bdd',
    "type": "BDDWhen",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BDDWhen",
      "@subdocument": [],
      "@documentation": {
        "@title": "BDDWhen", "@description": "BDD  (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "step": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
    }
  },
  {
    "id": id,
    "cluster": 'bdd',
    "type": "BDDAnd",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BDDAnd",
      "@subdocument": [],
      "@documentation": {
        "@title": "BDDAnd", "@description": "BDD  (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "and": {
        "@type": "Optional",
        "@class": "BDDAnd"
      },
      "but": {
        "@type": "Optional",
        "@class": "BDDAnd"
      },
      "step": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
    }
  },
  {
    "id": id,
    "cluster": 'bdd',
    "type": "BDDBut",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BDDBut",
      "@subdocument": [],
      "@documentation": {
        "@title": "BDDBut", "@description": "BDD  (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "and": {
        "@type": "Optional",
        "@class": "BDDAnd"
      },
      "but": {
        "@type": "Optional",
        "@class": "BDDBut"
      },
      "step": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
    }
  },
  {
    "id": id,
    "cluster": 'bdd',
    "type": "BDDScenario",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BDDScenario",
      "@subdocument": [],
      "@documentation": {
        "@title": "BDDScenario", "@description": "BDD  (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "steps": {
        "@type": "Set",
        "@class": "BDDSteps"
      }
    }
  },
  {
    "id": id,
    "cluster": 'bdd',
    "type": "BDDRule",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BDDRule",
      "@subdocument": [],
      "@documentation": {
        "@title": "BDDRule", "@description": "BDD  (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "scenarios": {
        "@type": "Set",
        "@class": "BDDScenario"
      }
    }
  },
  {
    "id": id,
    "cluster": 'bdd',
    "type": "BDDScenarioTemplate",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "BDDScenarioTemplate",
      "@subdocument": [],
      "@documentation": {
        "@title": "BDDScenarioTemplate", "@description": "BDD  (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "ValueHash" },
      "steps": {
        "@type": "Set",
        "@class": "BDDSteps"
      }
    }
  }
]);
