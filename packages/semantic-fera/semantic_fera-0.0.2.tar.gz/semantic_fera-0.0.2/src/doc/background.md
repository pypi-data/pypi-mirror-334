
## 1 Background

This is an initial attempt to aggregate documentation on semantic technologies based on links to various working directories and repsositories. 

This is intended to be distributed as a tar file, in the future, this is expected to be found in its own repository and/or serviced by a static web page.

### 1.1 Context

The context for this effort is formed by a set of observations or ***postulates***:

 - ***types are the symbolic representations of the system (vocabulary, taxonomy, langauge model)***
 - ***the inter-dependence of system types forms a graph of types which we call an ontology***
 - ***system design and inteface design starts with types***
 - ***these types define the semantics of the system, i.e. form a model of the system***
 - ***specific instances of types are what we call semantic data***
 - ***a function is defined by the mapping between the type of its argument and its return type***
 - ***modeling of the world (system) is an infinite task since our concerns and the world are both continuously changing***
 - ***we need to be able to easily handle the evolution and change of our world models (ontologies)***
 - ***system wide types have a positive effect on the development and the subsequent quality of the system***
 - ***we need to be able to handle the evolution and change of our program types***
 - ***the complexity of programing with semantic data, i.e. defining, creating, querying, formatting, and processing of semantic data is limiting exploitation***
 - ***programming with semantic data (on graphs of type instances) is poorly developed in light of its potential***
 

### 1.2 Goals

The goal is to enable semantic techologies to be exploited in projects. This envolves simplifying:

 - the definition, selection, and layering of ontologies
 - the creation of semantic data
 - the querying, formatting, and processing of semantic data
 

Furthermore, It is an implied requirement is that any semantic middleware, or configuration detail, is kept out of the user's functional, in-band, or business logic.
 

### 1.3 Use and Exploitation Potential

System wide ontologies and local programming with types are expeced to be exploited in:
 - code quality: ensuring instance data is correct at run-time (as well as development and compile time correctness)
 - metadata: model higher level environmental contexts, use-cases, configuration, scenarios, tasks, agents, actors, not just entities, behaviour, and actions
 - state machines: state machine states and events as types
 - observability: full semantic coverage of system and sub-system states and errors
 - availability: provide clients with the list of the current actions/operations that a user can make for the current service/error state (HATEOAS)
 - controllability: model the full plant and control space with parameter, error, and noise effects
 - modeling: address the extra dimensions of concern that are not modeled
 - temporality: model the temporal dimension so that all captured semantic data is unique and represents an event
 - policies: exploit events by using ontologically defined conditions on policy agents
 - reasoning: exploit reasoning on types and type properties to create knowledge bases
 - empirical models: use bottom up techniques, both classical and machine learning techniques to validate if not inform symbolic types

[NEXT](rdf-and-types.md)

[BACK](../README.md)