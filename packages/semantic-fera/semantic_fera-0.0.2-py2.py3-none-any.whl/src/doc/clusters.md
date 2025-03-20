
## 4 Clusters 

### 4.1 FERA Clusters

#### 4.1.1 Base

[`base` cluster diagram](../ontologies/clusters/base/base.md#base-cluster)

[`base` cluster schema](../ontologies/clusters/base/baseSchema.ts)  

The `base` cluster is a just the single type `NamedType` with the `name` property as per the discussion in [Required Core Properties](#required-core).

The `name` property is a required property on all instances as the `type, name` pair is used as the lexical basis for a unique ID for a given schema scope. The `base` cluster could be replaced with the `CommonEnity`of the [core cluster](#61-core) to standardize additional lexical ID fields and the ability to attribute any semantic data instance with a user defined `name-value`pair through the use of `Label`.


#### 4.1.2 DUL

[`dul` cluster diagram](../ontologies/clusters/dul/dul.md#dul-cluster) 

[`dul` cluster schema](../ontologies/clusters/dul/dulSchema.ts)  

`DUL` is a subset of the `SOMA` ontology and this is a human edited selection from `DUL`. 

`DUL` provides the high level dimensions that all subsequent `FERA` ontologies are derived from.


#### 4.1.3 Usd

[`usd` cluster diagram](../ontologies/clusters/usd/usd.md#usd-cluster) 

[`usd` cluster schema](../ontologies/clusters/usd/usdSchema.ts) 


`OpenUSD` provides a semantic API to the programmer in the form of a very extensive collection of libraries by which the user can create and manipulate resentations of entities with associated types. 

The main concept is a `Prim`that is essentially a generic object container to which types are assigned. This indirect, dictionary object approach to realizing type information is why the `USD`cluster is so odd looking. The original intent of `USD`was not to convert it to `RDF`.

`USD`is intended to be used instead to represent structural/physical entities as it is itself a 3D file format so it is well suited for 3D specification as well as rendering and animation of digital twins.

We impart higher level types, and ontological directions not expressed in `USD`, via the `MultiAplliedAPI`of `USD`.

Robot data will typically represent some state that is associated with a physical robot entity that is the state's `parentObject`.  The type constructors from the Python API are intented to help the user with this.


#### 4.1.4 Usd-value

[`usdValue` cluster diagram](../ontologies/clusters/usdValue/usdValue.md#usdValue-cluster) 

[`usdValue` cluster schema](../ontologies/clusters/usdValue/usdValueSchema.ts) 

`UsdAttribute`is the main mechanism in USD for handling literal types and streams of literal types over USD time codes (samples). 

`UsdValue` is the means by which USD data types are mapped onto attributes. Note that in all cases for the sake of efficiency,  it is the child that points to the parent, i.e. the `USDValue` that points to the `USDAttribute`, and `USDAttribute` that points to a `USDPrim`, a `USDPrim` that points to its `parentObject` prim that is one level up in the usd `path`.

#### 4.1.5 Fera

[`fera` cluster diagram](../ontologies/clusters/fera/fera.md#fera-cluster) 


[`fera` cluster schema](../ontologies/clusters/fera/feraSchema.ts) 

`fera`is the cluster that is generic for the fera projects, i.e. effectively a generic Robot cluster.

#### 4.1.6 Assembly

[`FERA assembly` cluster diagram](../ontologies/clusters/assembly/assembly.md#fera-assembly-cluster)

[`FERA assembly` cluster schema](../ontologies/clusters/assembly/feraAssemblySchema.ts) 

`assembly` is the `fera` derived cluster for the FERA robot assembly research.

#### 4.1.7 Machine-tending

`machine-tending` is the `fera` derived cluster for the FERA machine tending research.

tbd

### 4.2 Facility Cobot Clusters


#### 4.2.1 Core 

[`core` cluster diagram](../ontologies/clusters/core/core.md#core-cluster) 

[`core` cluster schema](../ontologies/clusters/core/coreSchema.ts) 
#### 4.2.2 Vision

[`vision` cluster diagram](../ontologies/clusters/vision/vision.md#vision-cluster) 

[`vision` cluster schema](../ontologies/clusters/vision/visionSchema.ts) 

#### 4.2.3 Policy

[`policy` cluster diagram](../ontologies/clusters/policy/policy.md#policy-cluster) 

[`policy` cluster schema](../ontologies/clusters/policy/policySchema.ts) 
#### 4.2.4 ROS

[`ros` cluster diagram](../ontologies/clusters/ros/ros.md#ros-cluster) 

[`ros` cluster schema](../ontologies/clusters/ros/rosSchema.ts) 

#### 4.2.5 Facility Cobot

[`fc` cluster diagram](../ontologies/clusters/fc/fc.md#fc-cluster) 

[`fc` cluster schema](../ontologies/clusters/fc/fcSchema.ts) 

### 4.3 Digitech Clusters


#### 4.3.1 Core 

This is a repeat, included for schema completeness

[`core` cluster diagram](../ontologies/clusters/core/core.md#core-cluster) 

[`core` cluster schema](../ontologies/clusters/core/coreSchema.ts)
#### 4.3.2 Product

[`product` cluster diagram](../ontologies/clusters/product/product.md#product-cluster) 

[`product` cluster schema](../ontologies/clusters/product/productSchema.ts) 

#### 4.3.3 i4

[`i4` cluster diagram](../ontologies/clusters/i4/i4.md#i4-cluster) 

[`i4` cluster schema](../ontologies/clusters/i4/i4Schema.ts) 
#### 4.3.4 ROS

[`ros` cluster diagram](../ontologies/clusters/ros/ros.md#ros-cluster)

[`ros` cluster schema](../ontologies/clusters/ros/rosSchema.ts) 

#### 4.3.5 URDF

[`urdf` cluster diagram](../ontologies/clusters/urdf/urdf.md#urdf-cluster) 

[`urdf` cluster schema](../ontologies/clusters/urdf/urdfSchema.ts) 

#### 4.3.6 Plant

[`plant` cluster diagram](../ontologies/clusters/plant/plant.md#plant-cluster)

[`plant` cluster schema](../ontologies/clusters/plant/plantSchema.ts)

#### 4.3.7 Digitech

[`digitech` cluster diagram](../ontologies/clusters/digitech/digitech.md#digitech-cluster) 

[`digitech` cluster schema](../ontologies/clusters/digitech/digitechSchema.ts) 


### 4.4 Other Clusters

#### 4.4.1 SRDF

[`srdf` cluster diagram](../ontologies/clusters/srdf/srdf.md#srdf-cluster) 

[`srdf` cluster schema](../ontologies/clusters/srdf/srdfSchema.ts) 

#### 4.4.2 Plant

[`plant` cluster diagram](../ontologies/clusters/plant/plant.md#plant-cluster) 

[`plant` cluster schema](../ontologies/clusters/plant/plantSchema.ts) 

#### 4.4.3 BDD

[`bdd` cluster diagram](../ontologies/clusters/bdd/bdd.md#bdd-cluster) 

[`bdd` cluster schema](../ontologies/clusters/bdd/bddSchema.ts) 

#### 4.4.4 SW

[`sw` cluster diagram](../ontologies/clusters/sw/sw.md#sw-cluster) 

[`sw` cluster schema](../ontologies/clusters/sw/swSchema.ts) 

#### 4.4.5 Metric

[`metric` cluster diagram](../ontologies/clusters/metric/metric.md#metric-cluster) 

[`metric` cluster schema](../ontologies/clusters/metric/metricSchema.ts) 


#### 4.4.6 OTLP

[`otlp` cluster diagram](../ontologies/clusters/otlp/otlp.md#otlp-cluster) 


#### 4.4.7 State

[`state` cluster diagram](../ontologies/clusters/state/state.md#state-cluster) 


[NEXT](python-api.md)

[BACK](../README.md)
