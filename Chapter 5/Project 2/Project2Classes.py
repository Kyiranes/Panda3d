from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
class PoorlyRenderedUniverse(ShowBase):
      def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          self.modelNode = loader.loadModel(modelPath)
          self.modelNode.reparentTo(parentNode)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
class GalaxyPlanet(ShowBase): 
     def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          self.modelNode = loader.loadModel(modelPath)
          self.modelNode.reparentTo(parentNode)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
          
class Player(ShowBase):
      def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          self.modelNode = loader.loadModel(modelPath)
          self.modelNode.reparentTo(parentNode)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
class TheISSIGuess(ShowBase):
      def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          self.modelNode = loader.loadModel(modelPath)
          self.modelNode.reparentTo(parentNode)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
class Drone(ShowBase):
      droneCount = 0
      def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          self.modelNode = loader.loadModel(modelPath)
          self.modelNode.reparentTo(parentNode)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)

          