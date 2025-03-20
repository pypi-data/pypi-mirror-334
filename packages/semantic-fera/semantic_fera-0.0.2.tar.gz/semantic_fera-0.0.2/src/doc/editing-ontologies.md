# Editing Ontologies

## Background Assumptions

The following assumes that the user is concerned with the ontological modeling and subequent programatic use in systems rather than the semantic-web representation of the system. The difference is subtle, but significant, as the concerns of system wide exploitation of a taxonomy used to define the system are different than that of an interface to a semantic-web application. 

The system-wide defintion of types is assumed to be a requirement in the following, with the exposure to the semantic-web as secondary to client and system services usage.

In the ideal case, all aspects of the sytem are staticlly typed such that the ontology serves as a system wide definition that the compiler checks at build time on every signature and return type.

In the worst case, the data types are only validated on insertion to the database for programming languages with little or no type support.

The central postulate of the author is that modeling is a infinite task that implies continuous change to type definitions throughout the system. The approach taken here, is not to resist type change through standardization, or containment to an API or external interfaces,  but to assume and embrace type change through the system programming. 

The central postulate is that an ontolgogicaly defined system requires an environment that supports type change and that this is best achieved with system libraries that are compliled for the ontologies at hand. Statically typed languages are the obvious choice under these requirements but this type centric approach should be maintained for non-statically-typed languages such as Python.

In all cases, the type definitions for the ontology should be local such that code generation is available to the programmer. This can be realized via the native type definitions of statically type languages, definition language for schemas or ontolgies, a DSL for types, or a combination of paths.  Regardless of the means, some form of definition becomes the internal representation that results in compiled type definitions to allow for type validation, code generation, and reasoning. This can be thought of as a ***typed-client*** analogous to a ***thick-client*** where services (in this case types) are available directly on the client.

Versioning shall be applied such that type evolution can be discerned at the type, cluster, and schema levels.

The following documents the current state of this development from the user's point of view.

## Current Implementation

TerminusDB uses JSON-LD as its RDF format for both storage and serialization of data. They have extended the syntax of JSON-LD using the ```@``` symbol (a common, but bad practice since this is a reserved symbol in JSON-LD).

We are currently using TerminusDB's schema definition language as our internal representation. TerminusDB supports a datalog known as WOQL that can be used for both insertion and queries and they support a document (JSON-LD) oriented schema definition that is their current prefered method. 

In our current implementation of a ***typed-client***, ontologies/schemas are defined in terms of custers, each cluster consisting of a set of type definitions that are imported as a package.

Users should be able to import a clusters and create their own clusters.  

Currently clusters from all projects are in a single mono-repo and are being split out into project repositories and distributed as NPM packages.

### Temporary use

Until the availability of NPM based clusters and library for handling clusters, users will have to use the NVIDIA Server for development.

Packages are managed under [```Rush```](https://rushstack.io/) which is used for handling all dependencies of the monorepo for typescript and javascript modules. 

Each cluster is a module and has it's own package/project defininition in the rush.json file that configures the repo. The following should be added to ```rush.json``` for ```fera-machine-tending-schema```:

```
    {
        "packageName": "fera-machine-tending-schema",
        "projectFolder": "types/fera-machine-tending-schema",
        "reviewCategory": "production"
    },
```

  - copy the directory ```/srv/workspace/services/types/fera-assembly-schema``` and change the name of the copied to ```fera-machine-tending-schema```.
  - change the file name under ```src/``` to ```feraMachineTendingSchema.ts```  and edit ```index.ts``` accordingly.
  - edit the package.json file for name changes, likewise the config/api-extractor.json file
  - rush update (to update dependencies in repo)
  - rush build  (to build repo)

###  Cluster definition

A cluster is defined as an array of ```clusterType``` where ```id```, ```cluster```, ```type```, ```version```, ```woql``` are required for schema definition.

```
        interface clusterType {
        /*  
            concept: clusterType is internal program representation (should) containing all data for generating 
            - woql (or other schema format)
            - stubs
            - visualizations
            - interoperability context/concordance data
            - dependencies are the other clusters where this types dependencies are to be found 
        */
        id: string,
        cluster: string,
        type: string,
        version: string,
        inScope?: boolean,
        woql?: any,
        graphviz?: any,
        children?: any, // { childName: clusterType [] }
        }
```

Example: 
```
        import { clusterType } from 'common-types';

        export const machineTendingCluster = (id): clusterType[] => ([

        // Situations
        {
            "id": id,
            "cluster": "machineTending",
            "type": "MachineTendingSituation",
            "version": "v001",
            "woql": {
            "@type": "Class",
            "@id": "MachineTendingSituation",
            "@documentation": {
                "@title": "MachineTendingSituation", "@description": " (version:v001)",
                "@authors": [""]
            },
            "@inherits": ["ProductionSituation"],
            "@key": { "@type": "Lexical", "@fields": ["name"] }
            }
        },
        ...
        ])
```
### Schema Definition

- import your cluster to ```services/types/schema-defs/src/schemaLibs.ts``` as ```{ machineTendingCluster } from 'machine-tending-schema';```
- Add an entry for your (```machineTending```) cluster to the schema ```fera``` in the following or create your new schema in ```schemaDefs```

```
    export const schemaDefs: SchemaMapDef[] = [
        { name: 'fera', version: 'v001', clusters: [ baseCluster, dulCluster, usdCluster, usdValueCluster, feraCluster, assemblyCluster ] } 
    ]
```
- use these ```name``` and ```version``` values when defining db 
- add an entry for your cluster and each type in ```clusterFormat``` of ```services/types/schema-defs/src/schemaLibs.ts``` 

### Design rules

See schemas under /types for example code and [reference](https://terminusdb.com/docs/schema-reference-guide/)
 - Schemas are defined as a set of clusters
 - A schema is built horizontally with a set of clusters that cover different dimensions
 - A schema is built vertically by refining types from parent clusters
 - Each cluster should be a layer that presents the user with a set of cohesive types
 - It is a good practice to define more narrow abstract types in your cluster rather than re-using wider parent types from other clusters
 - See the Fera cluster and the above as examples of applied ```DUL``` and ```fera``` types
 - the URI for an instance is defined by the db and returned as```@id``` according to the ```@key``` definition
 - Human readiable, i.e. lexical URIs are prefered and would be  ```@type/{name}``` in the above example where ```name``` shall be unique for a type
 - Note that the ```@fields``` array would include ```first``` for ```TemporalEntities``` to disambiguate by timestamps 
 - Abstract types are not instantiated, i.e. they have no instances or @key definitions for their @id
 - Abstract types are denoted by ```@abstract: []```
 

### Usage

A freshly started shell service requires a default schemaId set so that it knows what schema to operate on and which logical db instance to use.
You can have multiple db instances running that have the same or different schemas installed.

See define dbID in the following table to set the schemaId and db instance for whenever a shell is restarted. 

The format shall follow ```<schema name><schema version>-<instance name>``` where ```<schema name>``` and ```<schema version>``` follow from the (yours) approriate entry in ```services/types/schema-defs/src/schemaLibs.ts```


| General tasks | Command |
|:--- |:--- |
| build | ```rush build``` |
| tmux | ```tmux attach -t fc``` |
| stop/start shell | in ```services/services/fera-shell```  or the shell pane of tmux |
| run shell | ```rushx serve``` |
| client | in ```services/apps/semantic-client``` or client pane of tmux : ```rushx serve --help``` |
| view dbId | ```rushx serve -v``` |
| define dbId (*)| ```rushx serve -d <schema name><schema version>-<instance name> ```|

(*) required for all client-shell operations

| DB tasks | Command |
|:--- |:--- |
| create db instance for current dbId | ```rushx serve -c``` |
| insert schema for dbId in db | ```rushx serve -q``` |
| insert usd instances (**) | ```rushx serve -x ../../../../semantic-services/semantic_repo/libraries/usd_to_rdf/usd-files/json/ur10.json``` |

(**) requires that usd and usdValue are included in the schema definition


| Visualization tasks | Command |
|:--- |:--- |
| for the current schema graph clusters a, b, and c (***)| ```rushx serve -g a b c``` |
| show parent dependencies | ```rushx serve -e true``` |
| show cluster boundaries | ```rushx serve -b true``` |

(***) generated .svg files are placed in ```/srv/workspace/artifacts```

 


