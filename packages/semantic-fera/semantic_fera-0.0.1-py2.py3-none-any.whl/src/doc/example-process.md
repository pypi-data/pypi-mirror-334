
# Examples

#### Process main

```
    from semantic.api.semantic_api import semantic
    from semantic.common.utils import defineSchemaId
    from semantic.api.config import brokerIP, dbUri, batch_size, topics
    from semantic.fera.fera_types.type_constructors import joint_state, tool_center_point_state, pathMap

    async def main(api):
    query = api.query_constructor()
```

#### example body 1: simple query to match on UsdPrim with segmentName 'base_link', return the whole semantic data instance
```
    base_link_frame = {
                            "@type": 'UsdPrim',
                            "segmentName": 'base_link'
                      }
    query_result = await api.chain(base_link_frame, query,chain_out)
```

#### example body 2: same query, return only the apiSchemas (the USD multiple applied schemas that the base link is derived from)

```
    select_frame = {
                        "apiSchemas": 'value is wild-card under select'
                   }
    apiSchemas = api.select_constructor(select_frame)
    process_result = await api.chain(base_link_frame, query, apiSchemas, chain_out)
```
#### example body 3: get a ToolCenterPoint data set and perform user-defined processing on it

 ```   
    #get all ToolCenterPointState instances (use constrained query for large number of instances)
    tcp_frame = {
                    "@type": "ToolCenterPointState"
                }
    # better: get a constrained set of ToolCenterPointState instances 
    # where the first timestamp is an int formatted as a string and >= 100, <=1000
    tcp_frame = {
                    "@type": "ToolCenterPointState",
                    "first" : { ">=" : "100"},
                    "last" : { "<=" : "1000"}
                }      

    # define a processing function that returns an object (dict)

    def hasTCPForce_mean(args):
     average = list[float]
     count = 0

     try:
        force = list[float]
        force = [0,0,0,0,0,0]

        for tcpState in args['@graph']:
            count = count + 1
            force[0]= force[0] + tcpState['hasTCPForce'][0]
            force[1]= force[1] + tcpState['hasTCPForce'][1]
            force[2]= force[2] + tcpState['hasTCPForce'][2]
            force[3]= force[3] + tcpState['hasTCPForce'][3]
            force[4]= force[4] + tcpState['hasTCPForce'][4]
            force[5]= force[5] + tcpState['hasTCPForce'][5]

        average = [force[0]/count,force[1]/count,force[2]/count,force[3]/count,force[4]/count,force[5]/count]

     except Exception as e:
        redMsg(f"hasTCPForce_mean : {e}  {traceback.format_exc()}")
     return {
             'average-force':average,
             'sample-size' : count
             }

    # use function_constructor to create an async promised either function for use in the processing chain:
     tcp_force_mean = function_constructor(hasTCPForce_mean)
  
    process_result = await api.chain(tcp_frame, query, tcp_force_mean, chain_out)
```
#### end of example bodies of main
```
    if __name__ == "__main__":
       
        currentSchemaId = await api.client.getSchemaId()
        yourSchemaId = defineSchemaId(schemaName, schemaVersion, yourInstanceName, dbUri)
        await api.client.setSchemaId(yourSchemaId)

        api = semantic(brokerIp, defineSchemaId(schemaName, schemaVersion, instanceName, dbUri), batch_size, topics)

        loop = api.get_loop()
        loop.run_until_complete(main(api))

        await api.client.setSchemaId(currentSchemaId)
```
