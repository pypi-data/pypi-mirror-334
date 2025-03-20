
# Semantic FERA

#### Versions

```0.0.1``` : Intial version with only FERA ontology clusters and minimal set of corresponding type constructors.

| Feature | Element | Status | Comment |
|:--- |:--- |:--- | :--- |
| **type cluster definitions**| | complete in intial form, evolution begins|
|  |USD |✅ | complete |
|  |DUL |✅ | minmal selection |  
|  |FERA |✅ | to-be-evolved |  
|  |FERA assembly   |  | in-process |
|  |FERA machine tending   |  | in-process |
| **type defs, -constructors**| | |
|  | JointState |✅ | |
|  | ToolCenterPointState |✅ | |
| **state decorators**| | ❌ | in-process |
| **semantic-api examples**| | ❌ | in-process |


### Install

```pip3 install semantic-api```

```pip3 install semantic-fera```

### Use Example

#### Import semantic-api
```
    from semantic.api.semantic_api import semantic
    from semantic.common.utils import defineSchemaId
    from semantic.api.config import brokerIP, dbUri, batch_size, topics
```

#### Import semantic-fera
```
    from semantic.fera.fera_types.type_constructors import joint_state, tool_center_point_state, pathMap
```


#### Import semantic.fera.config

Import the default API configuration parameters from the relevant config file. The following steps will change as support for multiple users is added.  

```
    from semantic.fera.config.sweng_nvidia_macine_1 import brokerIp, schemaName, schemaVersion
```
Currently, you need to change the default logical database ```instanceName``` and possibly the ```schemaName-schemaVersion``` and follow the ```SchemaID``` steps in the insertion and query examples.

```
    # define the name of the logical database instance that you are using
    yourInstanceName: str = <your instance name>
```
See the use in the bottom of the following two examples:


#### 1 [Insertion - Narration Example](src/doc/example-narration.md)

#### 2 [Query - Processing Example](src/doc/example-process.md)

#### 3 [Ontologies](src/ontologies/ontologies.md)

#### 4 [Clusters](src/ontologies/clusters/clusters.md)

#### 5 [USD Framing](src/doc/usd-framing.md)



