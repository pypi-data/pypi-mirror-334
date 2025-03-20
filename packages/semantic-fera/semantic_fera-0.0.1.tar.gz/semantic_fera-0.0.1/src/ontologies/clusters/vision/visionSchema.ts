
// "dependencies": ["core"],
import { clusterType } from 'common-types';


export const visionCluster = (id): clusterType[] => ([
  {
     "id": id,
     "cluster": "vision",
     "type": "SensedEntity",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "SensedEntity",
           "@documentation": { "@title": "SensedEntity", "@description": "entity that is a sensed, perceived, recognized, or in other words, an anchor entity for recognitions of physical entities (version:v022) (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "TemporalEntity",
           "@key": { "@type": "Lexical", "@fields": ["name"] },
           "actor": {
             "@type": "Optional",
             "@class": "CyberPhysicalActor"
           },
           "anchorState": {
             "@type": "Optional",
             "@class": "xsd:string"
           },
           "physicalEntity": {
             "@type": "Optional",
             "@class": "PhysicalEntity"
           },
           "entityOn": {
             "@type": "Optional",
             "@class": "SensedEntity"
           },
           "entitiesNear": {
             "@type": "Set",
             "@class": "SensedEntity"
           },
           "entityIn": {
             "@type": "Optional",
             "@class": "SensedEntity"
           },
           "entityGeometry": {
             "@type": "Optional",
             "@class": "Geometry"
           },
           // NB! fromData not implemented
           "fromData": {
             "@type": "Optional",
             "@class": "VisionData"
           },
           "recognizedState": {
             "@type": "Set",
             "@class": "EntityState"
           }
       }
  },
  {
    "id": id,
    "cluster": "vision",
    "type": "RecognizedState",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "RecognizedState",
      "@documentation": {
        "@title": "RecognizedState", "@description": "RecognizedState is the type characterizing  sensed state(version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "EntityState",
      "@abstract": []
    }
  },
  {
    "id": id,
    "cluster": "vision",
    "type": "UnRecognizable",
    "version": "v022",
    "woql": {
      "@type": "Class",
      "@id": "UnRecognizable",
      "@documentation": {
        "@title": "Unrecognizable", "@description": "Generic type for all objects that exists in vision but are unrecognizable (version:v022)",
        "@authors": ["William A Coolidge"]
      },
      "@inherits": "PhysicalEntity",
      "@key": { "@type": "Lexical", "@fields": ["name"] }
    }
  },
]);
