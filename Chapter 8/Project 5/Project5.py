from direct.showbase.ShowBase import ShowBase, taskMgr
from panda3d.core import Vec3, NodePath, Loader, Texture, PandaNode, CollisionNode,CollisionSphere, CollisionCapsule,CollisionTraverser,CollisionHandlerPusher, CollisionInvSphere, TransparencyAttrib
from direct.task import Task
import sys
import math,random
## Defense Paths functions
def Cloud(radius = 1):
               x = 2 * random.random() - 1
               y = 2 * random.random() - 1
               z = 2 * random.random() - 1
               unitVec = Vec3(x,y,z)
               unitVec.normalize()
               return unitVec * radius
def BaseballSeams(step,numDrones,B, F = 1):
               time = step / float(numDrones) * 2 * math.pi
               F4 = 0
               R = 1
               xxx = math.cos(time) - B * math.cos(3 * time)
               yyy = math.sin(time) + B * math.sin(3 * time)
               zzz = F * math.cos(2*time) + F4 * math.cos(4 * time)
               rrr = math.sqrt(xxx ** 2 + yyy ** 2 + zzz  ** 2)
               x = R * xxx / rrr
               y = R * yyy / rrr
               z = R * zzz / rrr
               return Vec3(x,y,z)
def CircleY(step, numDrones):
               time = step / float(numDrones) * 2 * math.pi
               x = 0
               y = math.cos(time)
               z = math.sin(time)
               return Vec3(x,y,z)
def CircleZ(step, numDrones):
               time = step / float(numDrones) * 2 * math.pi
               y = 0
               x = math.cos(time)
               z = math.sin(time)
               return Vec3(x,y,z)
def CircleX(step, numDrones):
               time = step / float(numDrones) * 2 * math.pi
               z = 0
               y = math.cos(time)
               x = math.sin(time)
               return Vec3(x,y,z)
## Collision Classes(File Importing does not Work)
class PlacedObject(PandaNode):
     def __init__(self,loader: Loader, modelPath:str, ParentNode: NodePath, nodeName: str):
          self.modelNode: NodePath = loader.loadModel(modelPath)
          if not isinstance(self.modelNode, NodePath):
               raise AssertionError("PlacedObject loader.loadModel("+ modelPath + ") did not return a proper PandaNode!")
          self.modelNode.reparentTo(ParentNode)
          self.modelNode.setName(nodeName)
class CollidableObject(PlacedObject):
     def __init__(self,loader:Loader,modelPath:str,parentNode: NodePath, nodeName:str):
          super(CollidableObject,self).__init__(loader,modelPath,parentNode,nodeName)
          self.collisionNode = self.modelNode.attachNewNode(CollisionNode(nodeName+'_cNode'))
          
class InverseSphereCollideObject(CollidableObject):
     def __init__(self,loader:Loader,modelPath:str, parentNode: NodePath, nodeName: str, colPositionVec: Vec3, colRadius:float):
          super(InverseSphereCollideObject, self).__init__(loader,modelPath,parentNode,nodeName)
          self.collisionNode.node().addSolid(CollisionInvSphere(colPositionVec,colRadius))
class CapsuleCollidableObject(CollidableObject):
     def __init__(self,loader:Loader,modelPath:str,parentNode: NodePath, nodeName: str, ax: float, ay: float, az: float, bx: float, by: float, bz:float, r: float):
          super(CapsuleCollidableObject,self).__init__(loader,modelPath,parentNode,nodeName)
          self.collisionNode.node().addSolid(CollisionCapsule(ax,ay,az,bz,by,bz,r))
class SphereCollideObject(CollidableObject):
     def __init__(self, loader:Loader, modelPath:str, parentNode: NodePath, nodeName: str, colPositionVec: Vec3, colRadius: float):
          super(SphereCollideObject,self).__init__(loader,modelPath,parentNode,nodeName)
          self.collisionNode.node().addSolid(CollisionSphere(colPositionVec,colRadius))

     
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.Universe = PoorlyRenderedUniverse(self.loader, "./Assets/Universe/Universe.x",self.render,"Universe","./Assets/Universe/Universe.jpg",(0,0,0), 10000)
        self.Planet1 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet1/protoPlanet.x",self.render,"Planet1","./Assets/Planets/Planet1/Planet1.png", (1150, 5000, 7), 250)
        self.Planet2 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet2/protoPlanet.x",self.render,"Planet2","./Assets/Planets/Planet2/Planet2.png", (500, 9000, 700), 400)
        self.Planet3 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet3/protoPlanet.x",self.render,"Planet3","./Assets/Planets/Planet3/Planet3.png", (-1000, 2000, 174), 100)
        self.Planet4 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet4/protoPlanet.x",self.render,"Planet4","./Assets/Planets/Planet4/Planet4.png", (850, 7000, 270), 400)
        self.Planet5 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet5/protoPlanet.x",self.render,"Planet5","./Assets/Planets/Planet5/Planet5.png", (450, 3000, 245), 600)
        self.Planet6 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet6/protoPlanet.x",self.render,"Planet6","./Assets/Planets/Planet6/Planet6.png", (1500, 5000, 800), 500)
        self.Player = Player(self.loader, "./Assets/Spaceships/Phaser/phaser.x",self.render,"Player","./Assets/Spaceships/Phaser/phaserII.jpg", (100, 100, 100), 60)
        self.Spacestation = TheISSIGuess(self.loader, "./Assets/SpaceStation/spaceStation.x", self.render, "Space Station", "./Assets/SpaceStation/SpaceStation1_Dif2.png", (3000, 2000, 1000),300)
        self.accept("escape",self.quit)
        fullCycle = 60
        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.Player.collisionNode, self.Player.modelNode)
        self.pusher.addCollider(self.Spacestation.collisionNode, self.Spacestation.modelNode)
        self.pusher.addCollider(self.Planet1.collisionNode, self.Planet1.modelNode)
        self.pusher.addCollider(self.Planet2.collisionNode, self.Planet2.modelNode)
        self.pusher.addCollider(self.Planet3.collisionNode, self.Planet3.modelNode)
        self.pusher.addCollider(self.Planet4.collisionNode, self.Planet4.modelNode)
        self.pusher.addCollider(self.Planet5.collisionNode, self.Planet5.modelNode)
        self.pusher.addCollider(self.Planet6.collisionNode, self.Planet6.modelNode)
        self.cTrav.addCollider(self.Player.collisionNode, self.pusher)
        self.cTrav.showCollisions(self.render)
        for j in range(fullCycle):
               Drone.droneCount += 1
               nickName = "Drone" + str(Drone.droneCount)
               self.DrawCloudDefense(self.Planet1, nickName)
               self.DrawBaseballSeams(self.Spacestation, nickName, j, fullCycle, 2)
               self.DrawCircleXDefense(self.Planet2, nickName, j, fullCycle, 2)
               self.DrawCircleYDefense(self.Planet3, nickName, j, fullCycle, 2)
               self.DrawCircleZDefense(self.Planet4, nickName, j, fullCycle, 2)
               self.SetCamera(self.Player)
    
    
    def quit(self):
            sys.exit()
    def DrawBaseballSeams(self,centralObject, droneName, step, numDrones, radius = 1):
         unitVec = BaseballSeams(step,numDrones, B = 0.4)
         unitVec.normalize()
         position = unitVec * radius * 250 + centralObject.modelNode.getPos()
         drone = Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)
         self.pusher.addCollider(drone.collisionNode, drone.modelNode)
         self.cTrav.addCollider(drone.collisionNode, self.pusher)
    def DrawCloudDefense(self, centralObject, droneName):
         unitVec = Cloud()
         unitVec.normalize()
         position = unitVec * 500 + centralObject.modelNode.getPos()
         drone = Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 10)
         self.pusher.addCollider(drone.collisionNode, drone.modelNode)
         self.cTrav.addCollider(drone.collisionNode, self.pusher)
    def DrawCircleZDefense(self, centralObject, droneName, step, numDrones, radius = 1):
         unitVec = CircleZ(step, numDrones)
         unitVec.normalize()
         position = unitVec * radius * 250 + centralObject.modelNode.getPos()
         drone = Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)
         self.pusher.addCollider(drone.collisionNode, drone.modelNode)
         self.cTrav.addCollider(drone.collisionNode, self.pusher)
    def DrawCircleYDefense(self, centralObject, droneName, step, numDrones, radius = 1):
         unitVec = CircleY(step, numDrones)
         unitVec.normalize()
         position = unitVec * radius * 250 + centralObject.modelNode.getPos()
         drone = Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)
         self.pusher.addCollider(drone.collisionNode, drone.modelNode)
         self.cTrav.addCollider(drone.collisionNode, self.pusher)
    def DrawCircleXDefense(self, centralObject, droneName, step, numDrones, radius = 1):
         unitVec = CircleX(step, numDrones)
         unitVec.normalize()
         position = unitVec * radius * 250 + centralObject.modelNode.getPos()
         drone = Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)
         self.pusher.addCollider(drone.collisionNode, drone.modelNode)
         self.cTrav.addCollider(drone.collisionNode, self.pusher)
    def SetCamera(self, player):
         self.disableMouse()
         self.camera.reparentTo(player.modelNode)
         self.camera.setFluidPos(0,1,0)
               


class PoorlyRenderedUniverse(InverseSphereCollideObject):
      def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          super(PoorlyRenderedUniverse,self).__init__(loader,modelPath,parentNode,nodeName, Vec3(0,0,0),1.1)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
class GalaxyPlanet(SphereCollideObject): 
     def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          super(GalaxyPlanet,self).__init__(loader,modelPath,parentNode,nodeName, Vec3(0,0,0),1)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
          
class Player(SphereCollideObject, ShowBase):
     def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          super(Player,self).__init__(loader,modelPath,parentNode,nodeName, Vec3(0,0,0),0.5)
          self.loader = loader
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
          self.render = parentNode
          self.SetKeyBinding()
          self.taskManager = taskMgr
          self.reloadTime = .25
          self.missileDistance = 4000
          self.missileBay = 1
          self.taskManager.add(self.checkIntervals, 'checkMissiles', 34)
          self.EnableHUD()
     def checkIntervals(self, task):
           for i in list(Missile.Intervals):
                     if not Missile.Intervals[i].isPlaying():
                         Missile.fireModels[i].detachNode()
                         Missile.cNodes[i].detachNode()
                         del Missile.Intervals[i]
                         del Missile.fireModels[i]
                         del Missile.cNodes[i]
                         del Missile.collisionSolids[i]
           return Task.cont
     def Thrust(self, keyDown):
          if keyDown:
              self.taskManager.add(self.ApplyThrust, "forward-thrust")
          else: 
              self.taskManager.remove("forward-thrust")
     def ApplyThrust(self,task):
          rate = 5
          trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
          trajectory.normalize()
          self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
          return task.cont
     def SetKeyBinding(self):
          self.accept('space', self.Thrust, [1])
          self.accept('space-up', self.Thrust, [0])
          self.accept("w", self.Thrust, [1])
          self.accept("w-up", self.Thrust, [0])
          self.accept("up", self.Thrust, [1])
          self.accept("up-up", self.Thrust, [0])
          self.accept("left", self.LeftTurn, [1])
          self.accept("left-up", self.LeftTurn, [0])
          self.accept("a", self.LeftTurn, [1])
          self.accept("a-up", self.LeftTurn, [0])
          self.accept("right", self.RightTurn, [1])
          self.accept("right-up", self.RightTurn, [0])
          self.accept("d", self.RightTurn, [1])
          self.accept("d-up", self.RightTurn, [0])
          self.accept("s", self.DownTurn, [1])
          self.accept("s-up", self.DownTurn, [0])
          self.accept("down", self.DownTurn, [1])
          self.accept("down-up", self.DownTurn, [0])
          self.accept("r", self.UpTurn, [1])
          self.accept("r-up", self.UpTurn, [0])
          self.accept("e", self.RollRight, [1])
          self.accept("e-up", self.RollRight, [0])
          self.accept("q", self.RollLeft, [1])
          self.accept("q-up", self.RollLeft, [0])
          self.accept("f", self.Fire)
     def LeftTurn(self,keyDown):
          if keyDown:
              self.taskManager.add(self.ApplyLeftTurn, 'left-turn')
          else:
              self.taskManager.remove('left-turn')
     def ApplyLeftTurn(self,task):
          rate = .5
          self.modelNode.setH(self.modelNode.getH() + rate)
          return task.cont
     def RightTurn(self,keyDown):
           if keyDown:
               self.taskManager.add(self.ApplyRightTurn, 'right-turn')
           else:
               self.taskManager.remove('right-turn')
     def ApplyRightTurn(self,task):
          rate = .5
          self.modelNode.setH(self.modelNode.getH() - rate)
          return task.cont
     def UpTurn(self,keyDown):
           if keyDown: 
               self.taskManager.add(self.ApplyUpTurn, 'up-turn')
           else:
               self.taskManager.remove('up-turn')
     def ApplyUpTurn(self,task):
          rate = .5
          self.modelNode.setP(self.modelNode.getP() + rate)
          return task.cont
     def DownTurn(self,keyDown):
           if keyDown:
               self.taskManager.add(self.ApplyDownTurn, 'down-turn')
           else:
               self.taskManager.remove('down-turn')
     def ApplyDownTurn(self,task):
          rate = .5
          self.modelNode.setP(self.modelNode.getP() - rate)
          return task.cont
     def RollRight(self,keyDown):
           if keyDown:
               self.taskManager.add(self.ApplyRollRight, 'roll-right')
           else:
               self.taskManager.remove('roll-right')
     def ApplyRollRight(self,task):
          rate = .5
          self.modelNode.setR(self.modelNode.getR() - rate)
          return task.cont
     def RollLeft(self,keyDown):
           if keyDown:
               self.taskManager.add(self.ApplyRollLeft, 'roll-left')
           else:
               self.taskManager.remove('roll-left')
     def ApplyRollLeft(self,task):
          rate = .5
          self.modelNode.setR(self.modelNode.getR() + rate)
          return task.cont
     def Fire(self):
           if self.missileBay:
                 travRate = self.missileDistance
                 aim = self.render.getRelativeVector(self.modelNode, Vec3.forward())
                 aim.normalize()
                 fireSolution = aim * travRate
                 inFront = aim*150
                 travVec = fireSolution + self.modelNode.getPos()
                 self.missileBay -= 1
                 tag = 'Missile' + str(Missile.missileCount)
                 posVec = self.modelNode.getPos() + inFront
                 currentMissile = Missile(self.loader, "./Assets/Missile/phaser.x", self.render, tag, "./Assets/Missile/phaserII.jpg", posVec, 4.0)
                 Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
                 Missile.Intervals[tag].start()
           else:
                 if not self.taskManager.hasTaskNamed('reload'):
                      print('Starting Reload')
                      self.taskManager.doMethodLater(0, self.Reload, 'reload')
     def Reload(self, task):
           if task.time > self.reloadTime:
                 self.missileBay += 1
                 if self.missileBay > 1:
                      self.missileBay = 1
                 print('Reloaded')
                 return Task.done
           elif task.time <= self.reloadTime:
                 print('Reloading')
                 return Task.cont
     def EnableHUD(self):
           from direct.gui.OnscreenImage import OnscreenImage
           self.Hud = OnscreenImage(image = "./Assets/Hud/Reticle3b.png", pos = Vec3(0,0,0), scale = 0.1)
           self.Hud.setTransparency(TransparencyAttrib.MAlpha)


class TheISSIGuess(CapsuleCollidableObject):
      def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          super(TheISSIGuess,self).__init__(loader,modelPath,parentNode,nodeName,1,-1,5,1,-1,-5,5)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
          
class Drone(SphereCollideObject):
      droneCount = 0
      def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          super(Drone, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 2)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
class Missile(SphereCollideObject):
      fireModels = {}
      cNodes = {}
      collisionSolids = {}
      Intervals = {}
      missileCount = 0
      def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          super(Missile,self).__init__(loader,modelPath,parentNode,nodeName, Vec3(0,0,0),1)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
          Missile.missileCount += 1
          Missile.fireModels[nodeName] = self.modelNode
          Missile.cNodes[nodeName] = self.collisionNode
          Missile.collisionSolids[nodeName] = self.collisionNode.node().getSolid(0)
          Missile.cNodes[nodeName].show()
          print("Fire torpedo #" + str(Missile.missileCount))
app = MyApp()
app.run()