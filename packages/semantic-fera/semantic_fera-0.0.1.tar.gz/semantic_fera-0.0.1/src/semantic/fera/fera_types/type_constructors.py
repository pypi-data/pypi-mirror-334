import json
from typing_extensions import Final
from pyrsistent import m,  PMap
from pymonad.either import Either, Left, Right
from pydantic import  ValidationError
from semantic.api.semantic_api import semantic
from semantic.common.utils import msg, redMsg, refForPath
from semantic.common.common_types import NamedType, TerminusRef



class pathMap:
    def __init__(self, semantic):
       self.usdPathMap: PMap = m()
       self.semantic = semantic

    def get(self, segment):
       return self.usdPathMap.get(segment)
    

    async def refForSegment(self,  segmentName: str):
      path = self.usdPathMap.get(segmentName)
      if path is None:
          path_either : Either = await self.pathForSegment(segmentName)
          path = path_either.either(lambda e: f'refForSegment: Error: querying for segmentName: {segmentName}: {e}', lambda x: x)

          if path_either.is_right() and path is not None:
              ref = refForPath("UsdPrim", path, "SpecifierDef")
              #greenMsg('refForSegment: '+json.dumps(ref, indent=6))
              return Right(ref)
          else:
              return Left(ref)
      else:
          ref = refForPath("UsdPrim", path, "SpecifierDef")
          #greenMsg(f'refForSegment {ref}')
          return Right(ref)
   

    async def setPathForSegment(self, segmentName: str):
        key = segmentName
        either_path: Either = await self.pathForSegment(segmentName)
        
        if either_path.is_right():
          path = either_path.either(lambda e: f'Error: shoulder_pan_name: {e}', lambda x: x)
          self.usdPathMap = self.usdPathMap.update({ key: path})
          #greenMsg(f'setPathForSegment: segmentName: {key} path: {path}')
        else:
          redMsg(f'pathForSegment: Prim with {key} not found in db')
        return self
     
    async def pathForSegment(self, segmentName: str) -> Either:
          result: Either
          frame = {
                    "@type": "UsdPrim",
                    "segmentName": segmentName
                  }
          
          prim_either = await self.semantic.client.frame(frame)

          if (prim_either is None or prim_either.is_left()):
            txt = f'failure in query (not empty query) for frame @type: UsdPrim segmentName: {segmentName} '
            result = Left(txt)
            redMsg('pathForSegment: '+txt)
          else:
            prim = prim_either.either(lambda e: f'Error: pathForSegment: {e}', lambda x: x)
            '''
                an empty query will have a context object and nothing else in it
                so we have naught yet caught an empty query
            '''
            name = prim.get('name')
            if name is not None:
              result = Right(name)
              #greenMsg('pathForSegment: '+name)
            else:
              txt = f'frame @type: UsdPrim segmentName: {segmentName} returned empty'
              result = Left(txt)
              redMsg('pathForSegment: '+txt)
         
          return result

    '''
    def primUri(self, segmentName: str) -> str:
            key = segmentName
            path = self.usdPathMap.get(key)
            if path is None:
                redMsg(f' primUri: {key} is not found in usdPathMap')
            else:
                joint_uri = refForPath("UsdPrim", path, "SpecifierDef")
                greenMsg(f'primUri {joint_uri}')
                return joint_uri
    '''


class JointState(NamedType):
  '''
      "@key": { "@type": "Lexical", "@fields": ["name", "first"] },
      "@inherits": ["TaskState", "ProfiledState"],
  '''
  #type: str
  #name: str 
  first: str
  last: str
  count: int
  parentObject: TerminusRef
  hasJointEffort: float
  hasJointPosition: float
  hasJointVelocity: float
  

def joint_state(name:str, first:str, last:str, count:int, parent: TerminusRef, joint_effort:float, joint_position:float, joint_velocity:float) -> JointState:
  #todo make the following JointState (not dict) and validate_type_object generic
  js: JointState = {
      "type" : 'JointState',
      "name" : name,
      "first" : first,
      "last" : last,
      "count" : count,
      "parentObject" : parent,
      "hasJointEffort" : joint_effort,
      "hasJointPosition" : joint_position,
      "hasJointVelocity" : joint_velocity
      }
  try:
     JointState(**js)
     result = Right(js)
  except ValidationError as e:
     txt = 'Error: ' + str(e)
     redMsg("joint_state "+txt)
     result = Left(txt)
  '''
    NB: on use in chain/pipeline:
    for the partial function version required for use in a chain where the pipe arg
    is the input to the lambda function:
    shift the validation above into the lambda body
    the whole point of the partial function is that in a pipe, data arrives as input
    i.e. the data is late and the validation will then also have to be late
    
    return lambda arg: 
      for key in arg:
        js[key] = arg[key]
      try:
        JointState(**js)
        return Right(js)
      except ValidationError as e:
        txt = txt + 'Error: ' + str(e)
        redMsg("joint_state "+txt)
        return Left(txt)
  '''
  return lambda *arg: result


class ToolCenterPointState(NamedType):
  '''
     "@key": { "@type": "Lexical", "@fields": ["name", "first"] },
      "@inherits": ["TaskState", "ProfiledState"],
  '''

  '''
      The speed of the TCP retuned in a pose structure. The first three values
      are the cartesian speeds along x,y,z, and the last three define the
      current rotation axis, rx,ry,rz, and the length |rz,ry,rz| defines the angular
      velocity in radians/s
  '''
  first: str
  last: str
  count: int
  parentObject: TerminusRef
  hasTCPSpeed: list[float]
  hasTCPPose: list[float]
  hasTCPForce: list[float]
    

def tool_center_point_state(name:str, first:str, last:str, count:int, parent: TerminusRef, speed_f6 :list[float], pose_f6: list[float], force_f6: list[float]) -> ToolCenterPointState:
  tcps: ToolCenterPointState = {
      "type" : 'ToolCenterPointState',
      "name" : name,
      "first" : first,
      "last" : last,
      "count" : count,
      "parentObject" : parent,
      "hasTCPSpeed": speed_f6,
      "hasTCPPose": pose_f6,
      "hasTCPForce": force_f6
      }
  try:
     ToolCenterPointState(**tcps)
     result = Right(tcps)
  except ValidationError as e:
     txt = 'Error: ' + str(e)
     redMsg("tool_center_point_state "+txt)
     result = Left(txt)
  return lambda *arg: result


    