//      "dependencies": ["core"],
import { clusterType } from 'common-types';

export const metricCluster = (id): clusterType[] => ([
  {
     "id": id,
     "cluster": "metric",
     "type": "Metric",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "Metric",
           "@documentation": { "@title": "TemporalEntity", "@description": "base type for all Metric types (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@abstract": [],
           "@inherits": "TemporalEntity",
           "comparative": {
             "@type": "Array",
             "@dimensions": 1,
             "@class": "Comparative"
           },
           "environment": {
             "@type": "Array",
             "@dimensions": 1,
             "@class": "Environment"
           },
           "metricOn": {
             "@type": "Set",
             "@class": "AbstractEntity"
           },
       }
  },
  {
    "id": id,
     "cluster": "metric",
     "type": "ContourFitMetric",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "ContourFitMetric",
           "@documentation": { "@title": "TemporalEntity", "@description": "point count fit to contour reference (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "Metric"
       }
  },
  {
    "id": id,
     "cluster": "metric",
     "type": "PositionDistributionFitMetric",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "PositionDistributionFitMetric",
           "@documentation": { "@title": "TemporalEntity", "@description": "distribution fit on the position (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@inherits": "Metric",
           "mean": "xsd:float",
           "variance": "xsd:float"
       }
  },
  {
    "id": id,
     "cluster": "metric",
     "type": "Comparative",
     "version":"v022",
     "woql": {
           "@type": "Enum",
           "@id": "Comparative",
           "@documentation": { "@title": "Comparative", "@description": "enum type defining the Comparative qualifiers for Metrics (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@value": [
             "reference",
             "best",
             "worst",
             "normal",
             "outlier",
           ]
       }
  },
  {
    "id": id,
     "cluster": "metric",
     "type": "Environment",
     "version":"v022",
     "woql": {
           "@type": "Class",
           "@id": "Environment",
           "@subdocument": [],
           "@documentation": { "@title": "JsonLogicVarMap", "@description": "subdocument (local) type defining the environment of a Metric (version:v022)",
           "@authors": ["William A Coolidge"]},
           "@key": { "@type": "ValueHash" },
           "lightQuality": {
             "@type": "Optional",
             "@class": "xsd:decimal"
           },
           "peopleCount": {
             "@type": "Optional",
             "@class": "xsd:decimal"
           },
           "obstructionDegree": {
             "@type": "Optional",
             "@class": "xsd:decimal"
           },
           "timeOfDay": {
             "@type": "Optional",
             "@class": "xsd:decimal"
           }
       }
  },
]);
