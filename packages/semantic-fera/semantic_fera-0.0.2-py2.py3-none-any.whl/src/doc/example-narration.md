
# Examples


#### Narration main

```
    from semantic.api.semantic_api import semantic
    from semantic.common.utils import defineSchemaId
    from semantic.api.config import brokerIP, dbUri, batch_size, topics
    from semantic.fera.fera_types.type_constructors import joint_state, tool_center_point_state, pathMap

    async def main(api):
    pMap = pathMap(api)

    ...

    # get parent reference that this state is an attribute of

    ref_either : Either = await pMap.refForSegment('base_link')
    ref = ref_either.either(lambda e: f'refForSegment(base_link) Error : {e}', lambda x: x)
        if ref_either.is_right() and ref is not None:
            parent = ref
        else:
            redMsg(ref)

  #use name from USD Prim that it modifies (the robot's base link in this case)
  name = 'base_link'  

  #string version of time stamp representing sample instance (can be int in string format)
  first: str = <time-stamp> 

  #duplicate of first unless you are doing your own history filter
  last: str = <time-stamp> 

  # sample index/count
  count: int = <sameple-count> 

  # termtinusdb emulated reference to the USD object that this the state of
  parentObject: TerminusRef = parent 

  # convert native data to 6 dim arrays of float

  hasTCPSpeed: list[float] = [speed_data[0], speed_data[1], speed_data[2], speed_data[3], speed_data[4], speed_data[5]] 
  hasTCPPose: list[float] = [pose_data[0], pose_data[1], pose_data[2], pose_data[3], pose_data[4], pose_data[5]] 
  hasTCPForce: list[float] = [force_data[0], force_data[1], force_data[2], force_data[3], force_data[4], force_data[5]] 

  # create type constructor instance

  tcp_instance = tool_center_point_state(name, timestamp, timestamp, count, parent, hasTCPSpeed, hasTCPPose, hasTCPForce)

  # use narration in sample loop (caches type instances and auto inserts when number of instances equals 100)
  # note that multiple (comma separated) type constructor instances can be made in a single narration call

  await api.narrate(tcp_instance)

  ...

  #end sample loop

  # insert any left over type instances that have not been inserted automatically into the database
  api.insert()

  if __name__ == "__main__":

        currentSchemaId = await api.client.getSchemaId()
        yourSchemaId = defineSchemaId(schemaName, schemaVersion, yourInstanceName, dbUri)
        await api.client.setSchemaId(yourSchemaId)

        api = semantic(brokerIp, defineSchemaId(schemaName, schemaVersion, instanceName, dbUri), batch_size, topics)

        loop = api.get_loop()
        loop.run_until_complete(main(api))

        await api.client.setSchemaId(currentSchemaId)
```
