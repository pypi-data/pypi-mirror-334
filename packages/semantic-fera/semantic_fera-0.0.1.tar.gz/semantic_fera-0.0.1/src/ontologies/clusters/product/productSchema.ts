// "dependencies": ["core"],
import { clusterType } from 'common-types';

export const productCluster = (id): clusterType[] => ([
  {
     "id": id,
     "cluster": "product",
     "type": "ProductInformation",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "ProductInformation",
           "@documentation": { "@title": "ProductInformation", "@description": "abstract product information model for an asset (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@abstract": [],
           "@inherits": "AbstractEntity",
           "make": {
             "@type"  : "Optional",
             "@class" : "xsd:string"
           },
           "model": {
             "@type"  : "Optional",
             "@class" : "xsd:string"
           },
           "version": {
             "@type"  : "Optional",
             "@class" : "xsd:string"
           }
       }
  },
]);
