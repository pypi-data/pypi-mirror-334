// "dependencies": ["core","policy", "ros", "vision"],
import { clusterType } from 'common-types';

export const swCluster = (id): clusterType[] => ([
  {
    "id": id,
    "cluster": "sw",
    "type": "SWEntity",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "SWEntity",
      "@documentation": {
        "@title": "SWEntity", "@description": "Base for all sw entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "AbstractEntity",
      "@abstract": []
    }
  },
  {
    "id": id,
    "cluster": "sw",
    "type": "SWEffect",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "SWEffect",
      "@documentation": {
        "@title": "SWEffect", "@description": "Base for sw effects (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "ActionEntity",
      "@abstract": [],
      "actionEntity": {
        "@type": "Optional",
        "@class": "ActionEntity"
      }
      /*,
      "conceptDescription": {
        "@type": "Optional",
        "@class": "ConceptDescription"
      }
      */
    }
  },
  {
    "id": id,
    "cluster": "sw",
    "type": "ASTEntity",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "ASTEntity",
      "@documentation": {
        "@title": "ASTEntity", "@description": "Base for deconstructing sw to an AST (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "SWEntity",
      "@abstract": [],
      "edges": {
        "@type": "Set",
        "@class": "ASTEntity"
      }
    }
  },
  {
    "id": id,
    "cluster": "sw",
    "type": "PureFunctional",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PureFunctional",
      "@documentation": {
        "@title": "PureFunctional", "@description": "Base pure functions, no effect (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "SWAssetElement",
      "@abstract": [],
      "argList": {
        "@type": "Set",
        "@class": "xsd:string"
      },
      "return": {
        "@type": "Optional",
        "@class": "xsd:string"
      }
    }
  },
  {
    "id": id,
    "cluster": "sw",
    "type": "SWAsset",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "SWAsset",
      "@documentation": {
        "@title": "SWAsset", "@description": "Source code or code path (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "SWEntity",
      "@abstract": [],
     // "@key": { "@type": "Lexical", "@fields": ["name"] },
      "dirPath": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "fileName": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "src": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "origin": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "ast": {
        "@type": "Optional",
        "@class": "ASTEntity"
      },
    }
  },
  {
    "id": id,
    "cluster": "sw",
    "type": "SWAssetElement",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "SWAssetElement",
      "@documentation": {
        "@title": "SWAssetElement", "@description": "Base for functions with effects (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      "@inherits": "SWEntity",
      "swAsset": "SWAsset",
      "lineNumber": {
        "@type": "Optional",
        "@class": "xsd:integer"
      }
    }
  },
  {
    "id": id,
    "cluster": "sw",
    "type": "EffectFunctional",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "EffectFunctional",
      "@documentation": {
        "@title": "EffectFunctional", "@description": "Base for functions with effects (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "SWAssetElement",
      "@abstract": [],
      "argList": {
        "@type": "Set",
        "@class": "xsd:string"
      },
      "effects": {
        "@type": "Set",
        "@class": "SWEffect"
      },
      "return": {
        "@type": "Optional",
        "@class": "xsd:string"
      }
    }
  },
  {
    "id": id,
    "cluster": "sw",
    "type": "EffectProcedure",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "EffectProcedure",
      "@documentation": {
        "@title": "EffectProcedure", "@description": "Base for procedures with effects (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "SWAssetElement",
      "@abstract": [],
      "argList": {
        "@type": "Set",
        "@class": "xsd:string"
      },
      "effects": {
        "@type": "Set",
        "@class": "SWEffect"
      }
    }
  },
  {
    "id": id,
    "cluster": "sw",
    "type": "EffectProgram",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "EffectProgram",
      "@documentation": {
        "@title": "EffectProgram", "@description": "SW Program with effects type (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["ASTEntity", "EffectProcedure"],
      "@key": { "@type": "Lexical", "@fields": ["name", "index"] },

    }
  },
  {
    "id": id,
    "cluster": "sw",
    "type": "PureProgram",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PureProgram",
      "@documentation": {
        "@title": "Program", "@description": "SW Program with no effects type (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["ASTEntity", "PureFunctional"],
      "@key": { "@type": "Lexical", "@fields": ["name", "index"] },

    }
  },
 
  {
    "id": id,
    "cluster": "sw",
    "type": "Procedure",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Procedure",
      "@documentation": {
        "@title": "Procedure", "@description": "Concrete SW Procedure type (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["ASTEntity", "EffectProcedure"],
      "@key": { "@type": "Lexical", "@fields": ["name", "index"] },
    }
  },
  {
    "id": id,
    "cluster": "sw",
    "type": "PureFunction",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PureFunction",
      "@documentation": {
        "@title": "PureFunction", "@description": "Concrete SW Function type with no effects (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["ASTEntity", "PureFunctional"],
      "@key": { "@type": "Lexical", "@fields": ["name", "index"] },
    }
  },
  {
    "id": id,
    "cluster": "sw",
    "type": "EffectFunction",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "EffectFunction",
      "@documentation": {
        "@title": "EffectFunction", "@description": "Concrete SW Function type with effects (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["ASTEntity", "EffectFunctional"],
      "@key": { "@type": "Lexical", "@fields": ["name", "index"] },
    }
  },
  {
    "id": id,
    "cluster": "sw",
    "type": "Statement",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Statement",
      "@documentation": {
        "@title": "Statement", "@description": "Concrete SW Statement type (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["ASTEntity","SWAssetElement"],
      "@key": { "@type": "Lexical", "@fields": ["name", "index"] }
    }
  },
  {
    "id": id,
    "cluster": "sw",
    "type": "Expression",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Expression",
      "@documentation": {
        "@title": "Expression", "@description": "Concrete SW Expression type (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["ASTEntity","SWAssetElement"],
      "@key": { "@type": "Lexical", "@fields": ["name", "index"] }
    }
  },


]);
