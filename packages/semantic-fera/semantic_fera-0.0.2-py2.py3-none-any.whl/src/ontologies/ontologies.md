
## 3 Ontologies

This [curated list](https://github.com/ozekik/awesome-ontology?tab=readme-ov-file) is a reasonable listing of ontology related items. 

We are following a subset of the [SOMA Ontology](https://ease-crc.github.io/soma/) in the FERA project. The OWL for SOMA can be found [here](https://github.com/ease-crc/soma/tree/master/owl). The related research articles out of M Beetz's Bremman group can be found [here](https://ease-crc.org/publications/).

The [NEEM Handbood](https://ease-crc.org/publications/) is recommended reading as it does a good job of addressing issues concerning the design and use of the ontology.

Most ontologies are defined in OWL and a parser to generate a schema of types (not triples) is in progress. The current DUL ontology that follows was translated manually from [SOMA DUL](https://github.com/ease-crc/soma/blob/master/owl/DUL.owl)

With the excpetion of FFU and the initial I4 effort which were defined in one monolithic schema, ontologies are defined here by an ordered array of clusters, each cluster containing one or more type definitions.

Types (and hence its cluster) may inherit from another cluster or contain a predicate where the object type is defined in another cluster.

Clusters are a convenient way of layering and partioning concerns. 

Care should be made to try and avoid blurring horizontal sibling or parallel concerns, nor mixing in the vertical layers and placing an abstraction at the wrong level.

***Postulate***: Each cluster level should use abstract types from parent layers to create either abstract, or concrete types for the specialized layer, only adding abstract types to the parent layer if the generalization belongs there.

In the following we use the term ***schema*** to refer to a specific ontology that defines a database schema.

A schema is an ontology built as original types, or an edited set of types from other ontologies, that targets a specific use-case or world model.  

Each schema is identified by a schema name, a schema version and a set a clusters, each with one or more types.

A database instance is created and populated with the clusters corresponding to the this schema's name and version. 

A database instance includes and extra database instance identifier `schemaName-schemaVersion-instanceName` to handle multiple database instances for the same `schemaName-SchemaVersion` ontology.

The following sub-sections name the current schemas that have been developed, followed by sub-sections on the clusters that make up these schemas.


#### 3.1 FFU
The first project was the FFU (BioBanking) where ontologies were targeted for:
 - safety critical system (for FDA device approval), both developmental and operational
 - ontologically defined authorization policies securing various levels of access to biobank resources
 - medical ontologies defiing biobank content

The FFU was based on the core [IHMC Ontologies](https://ontology.ihmc.us/ontology.html)

The FFU project demonstrated the need for maintainable and lightweight middleware (KaOS was neither).

#### 3.2 FERA

The FERA schema is defined in 7 clusters [base](clusters/base/base.md/#base-cluster), [dul](clusters/dul/dul.md/#dul-cluster), [usd](clusters/usd/usd.md/#usd-cluster), [usdvalue](clusters/usdValue/usdValue.md/#usdvalue-cluster), [fera](clusters/fera/fera.md/#fera-cluster), [assembly](clusters/assembly/assembly.md/#fera-assembly-cluster), and [machine-tending](clusters/tbd/tbd.md/#tbd-cluster).

The clusters are layered:    

**base** &rarr; **usd** &rarr;  **dul** &rarr;  **fera** &rarr; [**assembly**, **machine-tending**];

where **usd** has a local dependency on **usd-value**

The cluster for **assembly** and **machine-tending** are layered under **fera** and can either be used in one **fera** schema assuming no type collisions, or split into two schemas **fera-assembly**, and **fera-machine-tending**


#### 3.3 Facility Cobot

Prior to FERA the root cluster was the [core](clusters/core/core.md/#core-cluster) cluster such that all clusters prior to FERA are interoperable. 

The equivalents in DUL to core are conceptually similar such the non FERA clusters can be ported to use under DUL and USD.

The Facility Cobot schema is defined in 5 clusters [core](clusters/core/core.md/#core-cluster), [vision](clusters/vision/vision.md/#vision-cluster), [policy](clusters/policy/policy/#policy-cluster), [ros](clusters/ros/ros.md/#ros-cluster), and [fc](clusters/fc/fc.md/#fc-cluster).



#### 3.4 Digitech

The Digitech  schema is defined in 5 clusters [core](clusters/core/core.md/#core-cluster), [product](clusters/product/product.md/#product-cluster), [i4](clusters/i4/i4.md/#i4-cluster), [ros](clusters/ros/ros.md/#ros-cluster),  [urdf](clusters/urdf/urdf.md/#urdf-cluster), [plant](clusters/plant/plant.md/#plant-cluster), and [digitech](clusters/digitech/digitech.md/#digitech-cluster).

#### 3.3 All: Additional Core based Clusters

In addition to the clusters of the schemas `Facility Cobot` and `Digitech`, there are 6 other clusters that can be mixed in.

[srdf](clusters/srdf/srdf.md/#srdf-cluster), [plant](clusters/plant/plant.md/#plant-cluster), [bdd](clusters/bdd/bdd.md/#bdd-cluster), [sw](clusters/sw/sw.md/#sw-cluster), [metric](clusters/metric/metric.md/#metric-cluster), [otlp](clusters/otlp/otlp.md/#otlp-cluster)

