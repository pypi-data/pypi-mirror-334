// "dependencies": ["core","policy", "ros", "vision"],
import { clusterType } from 'common-types';

export const usdValueCluster = (id): clusterType[] => ([
 
/*
  low level USD data types :
  Array's can be large and the thinking is that they should not be subdocuments for performance reasons
  conversely, literal types are assumed to be more efficiently handled as subdocuments
  can't be subdocuments and have lexical URIs, currently not subdocuments
*/
/*
{
  "id": id,
  "cluster": "usd",
  "type": "UsdObjectValue",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "UsdObjectValue",
    "@abstract": [],
    "@documentation": { "@title": "UsdObjectValue", "@description": "" },
    */
/*
    use polymorphic type rather than oneOf 
    
    "@oneOf": {
      "stringValue": "xsd:string",
      "numberValue": "xsd:number",
      "booleanValue": "xsd:boolean",
      "float3ArrayValue": "float3Array",
      "matrix4dValue": "matrix4d",usd
      "dictionaryValue" :"UsdDictionary"
   }
      */
     /*
  }
},
*/

{
  "id": id,
  "cluster": "usdValue",
  "type": "GraphicFoundations",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "GraphicFoundations",
    "@documentation": {
      "@authors": ["William A Coolidge"]
    },
  
    "@abstract": [],
    "@inherits": "UsdObjectValue",
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "ValueType",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "ValueType",
    "@documentation": {
      "@authors": ["William A Coolidge"]
    },
  
    "@abstract": [],
    "@inherits": ["UsdObjectValue"/*, "TemporalEntity" */],
    // todo: change to enum ?
    "roleName": {
      "@type": "Optional",
      "@class": "xsd:string"
    },
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "VtInt",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "VtInt",
    "@documentation": {
      "@authors": ["William A Coolidge"]
    },
  
    "@inherits": "ValueType",
    "@unfoldable": [],
    "@key": { "@type": "Lexical", "@fields": ["name"] },
    "vtInt": "xsd:int"
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "VtString",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "VtString",
    "@documentation": {
      "@authors": ["William A Coolidge"]
    },
  
    "@inherits": "ValueType",
    "@unfoldable": [],
    "@key": { "@type": "Lexical", "@fields": ["name"] },
    "vtString": "xsd:string"
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "VtBoolean",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "VtBoolean",
    "@documentation": {
      "@authors": ["William A Coolidge"]
    },
  
    "@inherits": "ValueType",
    "@unfoldable": [],
    "@key": { "@type": "Lexical", "@fields": ["name"] },
    "vtBoolean": "xsd:boolean"
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "VtFloat",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "VtFloat",
    "@documentation": {
      "@authors": ["William A Coolidge"]
    },
    /*
        Currently all ValueTypes are TemoralEntities 
        I wouild like to avoid doubleing up on data types to include temporality. This may be required, but I would prefer mixin but need value for lexical key generation, 
        However, mixin only works under inheritance, not delegation and besides, the delegated value may not be available when generating id
        effectively, the value type has to be one and the same type as the time interval to use this value in the lexical id
        currently have to provide default value for 'first', that is, provide a value 'static' if first is not defined
    */
  
    "@inherits": "ValueType",
    //"@inherits":["ValueType", "TemporalEntity"],
    "@unfoldable": [],
    "@key": { "@type": "Lexical", "@fields": ["name"] },
    "vtFloat": "xsd:float"
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "TemporalVtFloat",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "TemporalVtFloat",
    "@documentation": {
      "@authors": ["William A Coolidge"]
    },
    /*
        The following statement: 'Currently all ValueTypes are TemoralEntities' has been changed ! 
        and we are now doubleing up on data types to include temporality when needed to avoid changing the USD types. 

    */
  
    "@inherits": ["VtFloat", "TemporalEntity"],
    "@unfoldable": [],
    "@key": { "@type": "Lexical", "@fields": ["name", "first"] },
    "vtFloat": "xsd:float"
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "VtDouble",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "VtDouble",
    "@documentation": {
      "@authors": ["William A Coolidge"]
    },
  
    "@inherits": "ValueType",
    "@unfoldable": [],
    "@key": { "@type": "Lexical", "@fields": ["name"] },
    "vtDouble": "xsd:string"
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "VtVec3fArray",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "VtVec3fArray",
    "@documentation": {
      "@title": "VtVec3fArray", "@description": "VtVec3fArray: valueTypeToken: float3[] (version:v001)",
      "@authors": ["William A Coolidge"]
    },
    "@inherits": "ValueType",
    "@key": { "@type": "Lexical", "@fields": ["name"] },
    "@unfoldable": [],
    //"@key": { "@type": "ValueHash" },
  
    "vtVec3fArray": {
      "@type": "Array",
      "@class": "GfVec3f"
    }
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "VtVec3dArray",
  "version": "v001",
  "woql": {
    /*
      This is understood as the basic USD Pose type that is euler angle, no quaternion based
      To be verified !
    */
    "@type": "Class",
    "@id": "VtVec3dArray",
    "@documentation": {
      "@title": "VtVec3dArray", "@description": "VtVec3dArray: valueTypeToken: double3[] (version:v001)",
      "@authors": ["William A Coolidge"]
    },
    "@inherits": ["ValueType", "Pose"],
    "@key": { "@type": "Lexical", "@fields": ["name"] },
    "@unfoldable": [],
    //"@key": { "@type": "ValueHash" },
  
    "vtVec3dArray": {
      "@type": "Array",
      "@class": "GfVec3d"
    }
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "GfVec3f",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "GfVec3f",
    "@documentation": {
      "@title": "GfVec3f", "@description": "float3  (version:v001)",
      "@authors": ["William A Coolidge"]
    },
    
    "@inherits": ["GraphicFoundations"/*, "Location"*/],
     
    //"@key": { "@type": "ValueHash" },
    "@key": { "@type": "Lexical", "@fields": ["name"] },
    
    "gfVec3f": {
      "@type": "Array",
      "@dimensions": 1,
      "@cardinality": 3,
      "@class": "xsd:float"
    }
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "GfVec3d",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "GfVec3d",
    "@documentation": {
      "@title": "GfVec3d", "@description": "float3  (version:v001)",
      "@authors": ["William A Coolidge"]
    },
    
    "@inherits": ["GraphicFoundations"/*, "Location"*/],
    "@unfoldable": [],
    //"@key": { "@type": "ValueHash" },
    "@key": { "@type": "Lexical", "@fields": ["name"] },
    
    "gfVec3d": {
      "@type": "Array",
      "@dimensions": 1,
      "@cardinality": 3,
      "@class": "xsd:double"
    }
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "VtIntArray",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "VtIntArray",
    "@documentation": {
      "@title": "VtIntArray", "@description": "valueTypeToken: int[] (version:v001)",
      "@authors": ["William A Coolidge"]
    },
    
    "@inherits": "ValueType",
    "@unfoldable": [],
    //"@key": { "@type": "ValueHash" },
    "@key": { "@type": "Lexical", "@fields": ["name"] },

    "vtIntArray": {
      "@type": "Array",
      "@class": "xsd:int"
    }
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "VtFloatArray",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "VtFloatArray",
    "@documentation": {
      "@title": "VtFloatArray", "@description": "VtArrayFloat: valueTypeToken: float[] (version:v001)",
      "@authors": ["William A Coolidge"]
    },
    
    "@inherits": "ValueType",

    "@unfoldable": [],
    //"@key": { "@type": "ValueHash" },
    "@key": { "@type": "Lexical", "@fields": ["name"] },

    "vtFloatArray": {
      "@type": "Array",
      "@class": "xsd:float"
    }
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "VtDoubleArray",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "VtDoubleArray",
    "@documentation": {
      "@title": "VtFloatArray", "@description": "VtArrayDouble: valueTypeToken: float[] (version:v001)",
      "@authors": ["William A Coolidge"]
    },
    
    "@inherits": "ValueType",

    "@unfoldable": [],
    //"@key": { "@type": "ValueHash" },
    "@key": { "@type": "Lexical", "@fields": ["name"] },

    "vtDoubleArray": {
      "@type": "Array",
      "@class": "xsd:double"
    }
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "VtTfTokenArray",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "VtTfTokenArray",
    "@documentation": {
      "@title": "VtTfTokenArray", "@description": "VtTfTokenArray valueTypeToken: token[] (version:v001)",
      "@authors": ["William A Coolidge"]
    },
    
    "@inherits": "ValueType",
   
    "@unfoldable": [],
    //"@key": { "@type": "ValueHash" },
    "@key": { "@type": "Lexical", "@fields": ["name"] },
    
    "vtTfTokenArray": {
      "@type": "Array",
      "@class": "xsd:string"
    }
  }
},

{
  "id": id,
  "cluster": "usdValue",
  "type": "GfMatrix4d",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "GfMatrix4d",
    "@documentation": {
      "@title": "GfMatrix4d", "@description": "valueTypeToken: matrix4d: (version:v001)",
      "@authors": ["William A Coolidge"]
    },
    
    "@inherits": "GraphicFoundations",
   
    "@unfoldable": [],
    //"@key": { "@type": "ValueHash" },
    "@key": { "@type": "Lexical", "@fields": ["name"] },
    
    "gfMatrix4d": {
      "@type": "Array",
      "@dimensions": 1,
      "@cardinality": 4,
      "@class": "GfVector4d"
    }
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "GfVector4d",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "GfVector4d",
    "@documentation": {
      "@title": "GfVector4d", "@description": "valueTypeToken: double4: (version:v001)",
      "@authors": ["William A Coolidge"]
    },
    
    "@inherits": "GraphicFoundations",
   
    "@unfoldable": [],
    //"@key": { "@type": "ValueHash" },
    "@key": { "@type": "Lexical", "@fields": ["name"] },
    
    "gfMatrix4d": {
      "@type": "Array",
      "@dimensions": 1,
      "@cardinality": 4,
      "@class": "xsd:double"
    }
  }
},
{
  "id": id,
  "cluster": "usdValue",
  "type": "Range3d",
  "version": "v001",
  "woql": {
    "@type": "Class",
    "@id": "Range3d",
    "@documentation": {
      "@title": "Range3d", "@description": " range3d (version:v001)",
      "@authors": ["William A Coolidge"]
    },
    
    "@inherits": "GraphicFoundations",
  
    "@unfoldable": [],
    //"@key": { "@type": "ValueHash" },
    "@key": { "@type": "Lexical", "@fields": ["name"] },

    "max": "GfVec3d",
    "min": "GfVec3d"
  }
}

/*
class GfRange3d;
class GfMatrix4d;
*/
/*
pxr/base/gf/declare.h
todo: partition primitives from composite types
class GfBBox3d;
class GfDualQuatd;
class GfDualQuatf;
class GfDualQuath;
class GfFrustum;
class GfInterval;
class GfMultiInterval;
class GfLine;
class GfLineSeg;
class GfPlane;
class GfQuatd;
class GfQuatf;
class GfQuath;
class GfQuaternion;
class GfRay;
class GfRect2i;
class GfRect2i;
class GfRotation;
class GfSize2;
class GfSize3;
class GfMatrix2d;
class GfMatrix2f;
class GfMatrix3d;
class GfMatrix3f;
class GfMatrix4d;
class GfMatrix4f;
class GfRange1d;
class GfRange1f;
class GfRange2d;
class GfRange2f;
class GfRange3d;
class GfRange3f;
class GfVec2d;
class GfVec2f;
class GfVec2h;
class GfVec2i;
class GfVec3d;
class GfVec3f;
class GfVec3h;
class GfVec3i;
class GfVec4d;
class GfVec4f;
class GfVec4h;
class GfVec4i;
*/
]);
