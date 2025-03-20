// "dependencies": ["core","policy", "ros", "vision"],
import { clusterType } from 'common-types';
/*
  terminus constraints:
      / in strings is permitted, but not searchable in properites (name) used as lexical fields for id generation
      no special char such as / or even + can be the lead char in a name when used in a lexical field
      terminus url encodes special chars used in urls ==> emulated urls shall be url encoded
  usd constraints:
    path defined as / separated segments in usd can be stored but not searched in terminus
    url encoded path will get double encoded when used as a field used in uri generation, complicating url emulation 
  comprimise is to:
        store path as / separated segments and forgo searching on path
        replace / with + for name which means that clients have to search on + separated paths
        design decision: + separated paths is a lesser evil than %2F separated 
        leading root symbol has to be left out of name equivalent of path assuming / is replaced with +
*/

export const usdCluster = (id): clusterType[] => ([
  {
    "id": id,
    "cluster": "usd",
    "type": "UsdStage",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdStage",
      "@documentation": {
        "@title": "UsdStage", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "@inherits": ["UsdObject", "NamedType"],
      "usdaHeader": "xsd:string",
      "usdaFilePath": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      // name is alias to defaultPrim, defaultPrim is maintained as is and not defaultPrimName due to USD conventions
      "defaultPrim": "xsd:string",
      // "defaultPrimObject" :  "UsdPrim"
      /* 
        forward "defaultPrimObject" :  "UsdPrim"
        back "defaultPrimsStage" : "UsdStage"
        back requires URI generation on prim to stage, defaultPrim is effectively forward URI from stage to prim
      */

    }
  },
  {
    "id": id,
    "cluster": "usd",
    "type": "UsdPrim",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdPrim",
      "@documentation": {
        "@title": "UsdPrim", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@key": { "@type": "Lexical", "@fields": ["name", "specifier"] },
      "@unfoldable": [],
      "@inherits": ["UsdSegment", "UsdObject", "UsdTyped"/*, "PrimDictionary"*/],

      "typeName": {
        "@type": "Optional",
        "@class": "xsd:string"
      },

      "apiSchemas": {
        "@type": "Set",
        //"@class": "UsdAPISchemaBase"
        "@class": "xsd:string"
      },
      "specializesName": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "specifier": "UsdSpecifier",

      "active": "xsd:boolean",
      /*
      "specifier" :  {
        "@type": "Optional",
        "@class":"UsdSpecifier"
      },
      */
      "kind": {
        "@type": "Optional",
        "@class": "UsdKind"
      },
      "referenceNames": {
        "@type": "Set",
        "@class": "xsd:string"
      },
      /*
      "usdTyped": {
        "@type": "Optional",
        "@class": "UsdTyped"
      },
      */


      /*
      covered by parentObject
      "inherits" :   {
        "@type": "Optional",
        "@class": "UsdPrim"
      },
      */

      /* commented out for child-to-parent
      "attributes": {
        "@type": "Set",
        "@class": "UsdAttribute"
      },
      */
      /*
        added for child-to-parent
      
      "parentPrim": {
        "@type": "Set",
        "@class": "UsdPrim"
      },
      */
      /*
         NB: attributes contains set of UsdAttribute names for use in framing
         @graph contains set of UsdAttribute objects for processing/insertion, but not part of schema
      */
      "relationships": {
        "@type": "Set",
        "@class": "UsdRelationship"
      },
      "variants": {
        "@type": "Set",
        "@class": "StringPair"
      },
      "variantSet": {
        "@type": "Set",
        // "@class": "PrimDictionary"
        "@class": "UsdPrim"
      },
      "variability": {
        "@type": "Optional",
        "@class": "UsdVariability"
      },
    }
  },
  /*
  commented out for child 
  {
    "id": id,
    "cluster": "usd",
    "type": "PrimDictionary",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "PrimDictionary",
      "@abstract": [],
     
      //"@key": { "@type": "ValueHash" },
      //"@key": { "@type": "Lexical", "@fields": ["name"] },
      "@documentation": { "@title": "PrimDictionary", "@description": "Embedded Generic Ordered Map, PrimDictionary, or Record type: requires API to convert entries array to object map for lookup efficiency" },
      
      "@inherits": "UsdSegment",
      "childPrims" : {
        "@type": "Set",
        "@class": "UsdPrim"
        //"@class": "xsd:string"
      }
      
         NB: childPrims contains set of child UsdPrim names for use in framing
         @graph contains set of child UsdPrim objects for insertion, but not part of schema
      

    }
  },
  */
  {
    "id": id,
    "cluster": "usd",
    "type": "UsdAttribute",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdAttribute",
      "@documentation": {
        "@title": "UsdAttribute", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "UsdProperty",
      "@unfoldable": [],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      // the default
      /*
      "segmentValue": {
        "@type": "Optional",
        "@class": "UsdObjectValue"
      },
      */
      // time samples as the map of sample frame to value
      /*
      "timeSamples":  {
        "@type": "Set",
        "@class": "UsdObjectValue"
      },
      */
      "appliedSchema": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "roleName": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      /*
        added for child-to-parent
      */
      // "parentPrim": "UsdPrim",

      //"timeFrame": "xsd:double"
      /*     
      "valueType": valueTypeName,

      "value": prop.Get(),
      "metaData": prop.GetMetadata(name)
      */


    }
  },

  {
    "id": id,
    "cluster": "usd",
    "type": "UsdObject",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdObject",
      "@documentation": {
        "@title": "UsdObject", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "UsdDictionary",
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "@unfoldable": [],
      // "@key": { "@type": "ValueHash" },

      // diplayName may be UsdTyped only?
      "definedIn": {
        "@type": "Optional",
        "@class": "DefinitionSource"
      },

      "parentObject": {
        "@type": "Optional",
        "@class": "UsdObject"
      },




      "displayName": {
        "@type": "Optional",
        "@class": "xsd:string"
      },

      /*
      "customData" : {
        "@type": "Optional",
        "@class": "UsdObjectDictionary"
      },
      "assetInfo" : {
        "@type": "Optional",
        "@class": "UsdObjectDictionary"
      },
      */
      /*
      "@oneOf": {
        "documentation": "xsd:string",
        "doc": "xsd:string"
     }
      */
      "doc": {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "documentation": {
        "@type": "Optional",
        "@class": "xsd:string"
      }
    }
  },
  /*
    {
      "id": id,
      "cluster": "usd",
      "type": "TypeB",
      "version": "v001",
      "woql": {
        "@type": "Class",
        "@id": "TypeB",
        "@unfoldable": [],
        "@documentation": {
          "@title": "TypeB", "@description": "Base for all entities (version:v001)",
          "@authors": ["William A Coolidge"]
        },
        "@key": { "@type": "Lexical", "@fields": ["name"] },
        "@inherits": "NamedType"
      }
    },
    {
      "id": id,
      "cluster": "usd",
      "type": "TypeA",
      "version": "v001",
      "woql": {
        "@type": "Class",
        "@id": "TypeA",
        "@documentation": {
          "@title": "TypeA", "@description": "Base for all entities (version:v001)",
          "@authors": ["William A Coolidge"]
        },
        "@unfoldable": [],
        "@key": { "@type": "Lexical", "@fields": ["name"] },
        "@inherits": "NamedType",
        "notes": "xsd:string",
        "typeB": "TypeB"
      }
    },
    */
  /*
  {
    "id": id,
    "cluster": "usd",
    "type": "UsdChildObject",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdChildObject",
      "@documentation": {
        "@title": "UsdChildObject", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
    
      "@abstract": [],
    
    }
  },
  */

  /* 
  candidate to generic schema, not under usd
  nov 2024 replaced inheritance from NamedType with AbstractEntity
  
  {
    "id": id,
    "cluster": "usd",
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

  {
    "id": id,
    "cluster": "usd",
    "type": "TemporalEntity-",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "TemporalEntity-",
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
  {
    "id": id,
    "cluster": "usd",
    "type": "UsdDictionary",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdDictionary",

      "@abstract": [],
      "@inherits": "NamedType",
      //"@key": { "@type": "ValueHash" },
      // "@key": { "@type": "Lexical", "@fields": ["name"] },
      "@documentation": { "@title": "UsdDictionary", "@description": "Embedded Generic Ordered Map, UsdDictionary, or Record type: requires API to convert entries array to object map for lookup efficiency" },


      "dictionaryIsEmpty": {
        "@type": "Optional",
        "@class": "xsd:boolean"
      },

      // name is alias for usdObjectKey

      /*
      "usdObjects" : {
        "@type": "Set",
        "@class": "UsdObject"
      },
      */
      /*
      "usdObjectDictionaries" : {
        "@type": "Set",
        "@class": "UsdObjectDictionary"
      }
      */

    }
  },
  {
    "id": id,
    "cluster": "usd",
    "type": "UsdSegment",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdSegment",
      "@abstract": [],
      "@inherits": "UsdDictionary",
      "@documentation": {
        "@title": "UsdSegment",
        "@description": "",
        "@authors": ["William A Coolidge"]
      },
      "segmentName": "xsd:string",
      "path": "xsd:string"
    }
  },

  {
    "id": id,
    "cluster": "usd",
    "type": "UsdObjectValue",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id":"UsdObjectValue",
      "@abstract": [],
     // "@inherits": ["UsdObject","TimeInterval"],
      "@inherits": ["UsdMultiAppliedAPI"],
      
      "@documentation": {
        "@title": "UsdObjectValue",
        "@description": "Base for .. (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "valueTypeToken": "xsd:string"
    }
  },


  /*
  {
    "id": id,
    "cluster": "usd",
    "type": "AttributeValue",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "AttributeValue",
      "@abstract": [],
      "@inherits": "UsdObjectValue",
      "@documentation": {
        "@title": "AttributeValue", 
        "@description": "Base for .. (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "timeFrame": "xsd:double",
  
    }
  },
  */
  /*
   {
     "id": id,
     "cluster": "usd",
     "type": "UsdObjectDictionary",
     "version": "v001",
     "woql": {
       "@type": "Class",
       "@id": "UsdObjectDictionary",
      
       "@abstract": [],
       "@inherits": "UsdDictionary",
       //"@key": { "@type": "ValueHash" },
      // "@key": { "@type": "Lexical", "@fields": ["name"] },
       "@documentation": { "@title": "UsdObjectDictionary", "@description": "Embedded Generic Ordered Map, UsdObjectDictionary, or Record type: requires API to convert entries array to object map for lookup efficiency" },
     
 
     }
   },
   */
  /*
  {
    "id": id,
    "cluster": "usdValue",
    "type": "EmptyUsdObjectDictionary",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "EmptyUsdObject",
      "@documentation": {
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "UsdObjectDictionary",
      "@subdocument": [],
      "@key": { "@type": "ValueHash" }
    }
  },
  */
  /*
  {
     "id": id,
     "cluster": "usd",
     "type": "AttributeDictionary",
     "version": "v001",
     "woql": {
       "@type": "Class",
       "@id": "AttributeDictionary",
       "@abstract": [],
       
       //"@key": { "@type": "ValueHash" },
       //"@key": { "@type": "Lexical", "@fields": ["name"] },
       "@documentation": { "@title": "AttributeDictionary", "@description": "Embedded Generic Ordered Map, AttributeDictionary, or Record type: requires API to convert entries array to object map for lookup efficiency" },
  
       "@inherits": "UsdSegment",
       
 
       "attributes" : {
         "@type": "Set",
         "@class": "UsdAttribute"
       }
 
     }
   },
   */
  /*
  {
    "id": id,
    "cluster": "usd",
    "type": "FieldValuePair",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "FieldValuePair",
      "@subdocument": [],
      "@key": { "@type": "ValueHash" },
      "@documentation": { "@title": "FieldValuePair", "@description": "" },

      "fieldName" : "xsd:string",
      // types may be application specific
      "@oneOf": {
        "stringValue": "xsd:string",
        "numberValue": "xsd:number",
        "booleanValue": "xsd:boolean",
        "float3ArrayValue": "float3Array",
        "matrix4dValue": "matrix4d",
        "dictionaryValue" :"PrimDictionary"
     }
    }
  },
*/
  // end generic schema lib

  // begin USD specific schema
  {
    "id": id,
    "cluster": "usd",
    "type": "DefinitionSource",
    "version": "v001",
    "woql": {
      "@type": "Enum",
      "@id": "DefinitionSource",
      "@documentation": {
        "@title": "DefinitionSource", "@description": "origin of source defininition(version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@value": [
        "usd",
        "rdf",
        "omniverse"
      ]
    }
  },

  {
    "id": id,
    "cluster": "usd",
    "type": "UsdKind",
    "version": "v001",
    "woql": {
      "@type": "Enum",
      "@id": "UsdKind",
      "@documentation": {
        "@title": "UsdKind", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@value": [
        "model",
        "group",
        "assembly",
        "component",
        "subcomponent"
      ]
    }
  },

  {
    "id": id,
    "cluster": "usd",
    "type": "StringPair",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "StringPair",
      "@unfoldable": [],
      "@inherits": "NamedType",
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      "@documentation": {
        "@title": "StringPair", "@description": "filed value pair for string valued dictionaries (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      //alias to name "field": "xsd:string",
      "value": "xsd:string",
    }
  },

  {
    "id": id,
    "cluster": "usd",
    "type": "UsdSpecifier",
    "version": "v001",
    "woql": {
      "@type": "Enum",
      "@id": "UsdSpecifier",
      "@documentation": {
        "@title": "UsdSpecifier", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@value": [
        "SpecifierDef",
        "SpecifierOver",
        "SpecifierClass"
      ]
    }
  },
  /*
  How do we use this? Current answer: not required
  {
    "id": id,
    "cluster": "usd",
    "type": "ListEditTag",
    "version": "v001",
    "woql": {
      "@type": "Enum",
      "@id": "ListEditTag",
      "@documentation": {
        "@title": "ListEditTag", "@description": "List edit tag annotations for composition (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@value": [
        "prepend",
        "append",
        "remove",
        "reset"
      ]
    }
  },
 */
  {
    "id": id,
    "cluster": "usd",
    "type": "UsdProperty",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdProperty",
      "@documentation": {
        "@title": "UsdProperty", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },

      "@inherits": ["UsdObject", "UsdSegment"],
      "@abstract": []
      // "properties": "Usd"
    }
  },
  {
    "id": id,
    "cluster": "usd",
    "type": "UsdVariability",
    "version": "v001",
    "woql": {
      "@type": "Enum",
      "@id": "UsdVariability",
      "@documentation": {
        "@title": "UsdVariability", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@value": [
        "uniform",
        "varying"
      ]
    }
  },

  {
    "id": id,
    "cluster": "usd",
    "type": "UsdRelationship",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdRelationship",
      "@documentation": {
        "@title": "UsdRelationship", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      // dec 06 UsdSegment is redundant in the following
      "@inherits": ["UsdProperty"],
      "@key": { "@type": "Lexical", "@fields": ["name"] },
      //"primObject": "UsdPrim",
      "primObjectPath": "xsd:string"
    }
  },
  {
    "id": id,
    "cluster": "usd",
    "type": "UsdSchemaBase",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdSchemaBase",
      "@documentation": {
        "@title": "UsdSchemaBase", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@abstract": [],
      // dec 06 "@inherits": ["UsdObject", "NamedType"],
     

      // diplayName may be UsdTyped only?
      /*
      "displayName" : {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "customData" : {
        "@type": "Optional",
        "@class": "PrimDictionary"
      },
      "assetInfo" : {
        "@type": "Optional",
        "@class": "PrimDictionary"
      },
      "documentation" : {
        "@type": "Optional",
        "@class": "xsd:string"
      },
      "@oneOf": {
        "documentation": "xsd:string",
        "doc": "xsd:string"
     }
        */
    }
  },
  {
    "id": id,
    "cluster": "usd",
    "type": "UsdTyped",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdTyped",
      "@documentation": {
        "@title": "UsdTyped", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["UsdSchemaBase", "NamedType"],
      "@key": { "@type": "Lexical", "@fields": ["name"] }
    }
  },
  {
    "id": id,
    "cluster": "usd",
    "type": "UsdAPISchemaBase",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdAPISchemaBase",
      "@documentation": {
        "@title": "UsdApiSchemaBase", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": ["UsdObject","UsdSchemaBase"], // dec 6 changed diretion of usdobject inheritance
      "@abstract": []
    }
  },
  {
    "id": id,
    "cluster": "usd",
    "type": "UsdSingleAppliedAPI",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdSingleAppliedAPI",
      "@documentation": {
        "@title": "UsdSingleAppliedAPI", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "UsdAPISchemaBase",
      "@abstract": []
    }
  },
  {
    "id": id,
    "cluster": "usd",
    "type": "UsdMultiAppliedAPI",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "UsdMultiAppliedAPI",
      "@documentation": {
        "@title": "UsdMultiAppliedAPI", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "UsdAPISchemaBase",
      "@abstract": []
    }
  },
  {
    "id": id,
    "cluster": "usd",
    "type": "XForm",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "XForm",
      "@documentation": {
        "@title": "XForm", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "UsdTyped",
      "@abstract": []
    }
  },
  {
    "id": id,
    "cluster": "usd",
    "type": "Cube",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Cube",
      "@documentation": {
        "@title": "Cube", "@description": "Base for all entities (version:v001)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "UsdTyped",
      "@abstract": []
    }
  },

  {
    "id": id,
    "cluster": "usd",
    "type": "Mesh",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "Mesh",
      "@documentation": {
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "UsdTyped",
      "@abstract": []
    }
  },

  /*
    low level USD data types : TODO: move to  different cluster
  
  
  {
    "id": id,
    "cluster": "usd",
    "type": "float3",
    "version": "v001",
    "woql": {
      "@type": "Class",
      "@id": "float3",
      "@documentation": {
        "@title": "float3", "@description": "usda: float3 usd: GfVec3f (version:v001)",
        "@authors": ["William A Coolidge"]
      },
    
      "@subdocument": [],
      "@key": { "@type": "ValueHash" },
  
      "point": {
        "@type": "Array",
        "@dimensions": 1,
        "@cardinality": 3,
        "@class": "xsd:float"
      }
    }
  },
  */
]);
