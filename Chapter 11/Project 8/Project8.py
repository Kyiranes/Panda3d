
from direct.showbase.ShowBase import ShowBase, taskMgr
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Vec3, NodePath, Loader, PandaNode, CollisionNode, CollisionSphere, CollisionCapsule, CollisionTraverser, CollisionHandlerPusher, CollisionInvSphere
from panda3d.core import TransparencyAttrib, CollisionHandlerEvent, ClockObject
from direct.interval.IntervalGlobal import Sequence
import re,time
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
def RockRing(step, numRocks, radius):
               time = step / float(numRocks) * 2 * math.pi
               x = radius * math.sin(time)
               y = radius * math.cos(time)
               z = 0
               return Vec3(x,y,z)
## Collision Classes(File Importing does not Work)
class PlacedObject(PandaNode):
     def __init__(self,loader: Loader, modelPath:str, ParentNode: NodePath, nodeName: str):
          super(PlacedObject, self).__init__(nodeName)
          self.modelNode: NodePath = loader.loadModel(modelPath)
          if not isinstance(self.modelNode, NodePath):
               raise AssertionError("PlacedObject loader.loadModel("+ modelPath + ") did not return a proper PandaNode!")
          self.modelNode.reparentTo(ParentNode)
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
          self.collisionNode.node().addSolid(CollisionCapsule(ax, ay, az, bx, by, bz, r))
class SphereCollideObject(CollidableObject):
     def __init__(self, loader:Loader, modelPath:str, parentNode: NodePath, nodeName: str, colPositionVec: Vec3, colRadius: float):
          super(SphereCollideObject,self).__init__(loader,modelPath,parentNode,nodeName)
          self.collisionNode.node().addSolid(CollisionSphere(colPositionVec,colRadius))

     
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.globalClock = ClockObject.getGlobalClock()
        self.orbitPivots = []
        self.Universe = PoorlyRenderedUniverse(self.loader, "./Assets/Universe/Universe.x",self.render,"Universe","./Assets/Universe/Universe.jpg",(0,0,0), 20000)
        self.Sun = Sun(self.loader, "./Assets/Sun/sun.x", self.render, "Sun", "./Assets/Sun/sun.jpg", (7000, 0, 3000), 1500)
        sunPos = self.Sun.modelNode.getPos()
        self.p1Pivot = self.render.attachNewNode("Planet1-Orbit")
        self.p1Pivot.setPos(sunPos)
        self.Planet1 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet1/protoPlanet.x",self.p1Pivot,"Planet1","./Assets/Planets/Planet1/Planet1.png", Vec3(1150, 5000, 7) - sunPos, 250)
        self.p2Pivot = self.render.attachNewNode("Planet2-Orbit")
        self.p2Pivot.setPos(sunPos)
        self.Planet2 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet2/protoPlanet.x",self.p2Pivot,"Planet2","./Assets/Planets/Planet2/Planet2.png", Vec3(500, 9000, 700) - sunPos, 400)
        self.p3Pivot = self.render.attachNewNode("Planet3-Orbit")
        self.p3Pivot.setPos(sunPos)
        self.Planet3 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet3/protoPlanet.x",self.p3Pivot,"Planet3","./Assets/Planets/Planet3/Planet3.png", Vec3(-1000, 2000, 174) - sunPos, 100)
        self.p4Pivot = self.render.attachNewNode("Planet4-Orbit")
        self.p4Pivot.setPos(sunPos)
        self.Planet4 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet4/protoPlanet.x",self.p4Pivot,"Planet4","./Assets/Planets/Planet4/Planet4.png", Vec3(850, 7000, 270) - sunPos, 400)
        self.p5Pivot = self.render.attachNewNode("Planet5-Orbit")
        self.p5Pivot.setPos(sunPos)
        self.Planet5 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet5/protoPlanet.x",self.p5Pivot,"Planet5","./Assets/Planets/Planet5/Planet5.png", Vec3(450, 3000, 245) - sunPos, 600)
        self.p6Pivot = self.render.attachNewNode("Planet6-Orbit")
        self.p6Pivot.setPos(sunPos)
        self.Planet6 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet6/protoPlanet.x",self.p6Pivot,"Planet6","./Assets/Planets/Planet6/Planet6.png", Vec3(1500, 10000, 500) - sunPos, 800)
        self.spPivot = self.render.attachNewNode("Spacestation-Orbit")
        self.spPivot.setPos(sunPos)
        self.Spacestation = TheISSIGuess(self.loader,"./Assets/SpaceStation/spaceStation.x",self.spPivot,"Space Station", "./Assets/SpaceStation/SpaceStation1_Dif2.png", Vec3(1200, 6000, 900) - sunPos, 100)
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.Rock = Rock(self.loader, "./Assets/Rock/Rock.x",self.render, "Rock", "./Assets/Rock/Rock.png", Vec3(100, 100, 100), 60)
        self.Player = Player(self.loader, "./Assets/Spaceships/Phaser/phaser.x",self.render, "Player", "./Assets/Spaceships/Phaser/phaserII.jpg", Vec3(0, 0, 0), 60, self.cTrav)
        self.Wanderer1 = Wanderer(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 3.0, "./Assets/DroneDefender/octotoad1_auv.png", self.Player)
        self.Wanderer2 = Wanderer(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, "Drone", 5.0, "./Assets/DroneDefender/octotoad1_auv.png", self.Player)
        self.accept("escape",self.quit)
        fullCycle = 60
        self.cTrav.traverse(self.render)
        self.pusher.addCollider(self.Player.collisionNode, self.Player.modelNode)
        self.pusher.addCollider(self.Spacestation.collisionNode, self.Spacestation.modelNode)
        self.cTrav.addCollider(self.Player.collisionNode, self.pusher)
        base.cTrav = self.cTrav 
        self.drawRockRing(self.Planet5, "PlanetRock", 20, 4)
        self.drawRockRing(self.Sun, "SunRock", 40, 13)
        self.orbitPivots.append((self.p1Pivot, 0.15))
        self.orbitPivots.append((self.p2Pivot, 0.05))
        self.orbitPivots.append((self.p3Pivot, 0.2))
        self.orbitPivots.append((self.p4Pivot, 0.08))
        self.orbitPivots.append((self.p5Pivot, 0.12))
        self.orbitPivots.append((self.p6Pivot, 0.04))
        self.SetCamera(self.Player)
        taskMgr.add(self.updateAllOrbits, "updateOrbitsTask")
        taskMgr.doMethodLater(1.0, self.launchRock, "launchRockTask")
        self.DrawCloudDefense(self.Planet1, "Cloud", fullCycle)
        self.DrawBaseballSeams(self.Spacestation, "Seams", fullCycle, 7)
        self.DrawCloudDefense(self.Planet2, "Cloud2", fullCycle)
        self.DrawBaseballSeams(self.Planet3, "Seams2", fullCycle, 2)
        self.DrawCircleZDefense(self.Planet4, "CircleZ", fullCycle, 2)
        fps_limit = 60
        self.globalClock.setMode(ClockObject.MLimited)
        self.globalClock.setFrameRate(fps_limit)
    def quit(self):
            sys.exit()
    def DrawBaseballSeams(self, centralObject, groupName, numDrones, radius = 1):
         pivot = centralObject.modelNode.attachNewNode(groupName + "-pivot")
         pivot.setScale(self.render, 1)
         pivot.setPos(0, 0, 0)
         for i in range(numDrones):
              Drone.droneCount += 1
              droneName = groupName + str(Drone.droneCount)
              unitVec = BaseballSeams(i, numDrones, B = 0.4)
              unitVec.normalize()
              relPos = unitVec * radius * 250
              Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", pivot, droneName, "./Assets/DroneDefender/octotoad1_auv.png", relPos, 5)
         self.orbitPivots.append((pivot, 0.02))

    def DrawCloudDefense(self, centralObject, groupName, numDrones):
         pivot = centralObject.modelNode.attachNewNode(groupName + "-pivot")
         pivot.setScale(self.render, 1)
         pivot.setPos(0, 0, 0)
         pivot.setP(random.uniform(0, 360))
         pivot.setR(random.uniform(0, 360))
         for i in range(numDrones):
              Drone.droneCount += 1
              droneName = groupName + str(Drone.droneCount)
              unitVec = Cloud()
              unitVec.normalize()
              relPos = unitVec * 500
              Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", pivot, droneName, "./Assets/DroneDefender/octotoad1_auv.png", relPos, 10)
         self.orbitPivots.append((pivot, 0.02))
         
    def DrawCircleZDefense(self, centralObject, groupName, numDrones, radius = 1):
         pivot = centralObject.modelNode.attachNewNode(groupName + "-pivot")
         pivot.setScale(self.render, 1)
         pivot.setPos(0, 0, 0)
         pivot.setP(random.uniform(0, 360))
         pivot.setR(random.uniform(0, 360))
         for i in range(numDrones):
              Drone.droneCount += 1
              droneName = groupName + str(Drone.droneCount)
              unitVec = CircleZ(i, numDrones)
              unitVec.normalize()
              relPos = unitVec * radius * 250
              Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", pivot, droneName, "./Assets/DroneDefender/octotoad1_auv.png", relPos, 5)
         self.orbitPivots.append((pivot, 0.02))

    def DrawCircleYDefense(self, centralObject, groupName, numDrones, radius = 1):
         pivot = centralObject.modelNode.attachNewNode(groupName + "-pivot")
         pivot.setScale(self.render, 1)
         pivot.setPos(0, 0, 0)
         pivot.setP(random.uniform(0, 360))
         pivot.setR(random.uniform(0, 360))
         for i in range(numDrones):
              Drone.droneCount += 1
              droneName = groupName + str(Drone.droneCount)
              unitVec = CircleY(i, numDrones)
              unitVec.normalize()
              relPos = unitVec * radius * 250
              Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", pivot, droneName, "./Assets/DroneDefender/octotoad1_auv.png", relPos, 5)
         self.orbitPivots.append((pivot, 0.02))

    def DrawCircleXDefense(self, centralObject, groupName, numDrones, radius = 1):
         pivot = centralObject.modelNode.attachNewNode(groupName + "-pivot")
         pivot.setScale(self.render, 1)
         pivot.setPos(0, 0, 0)
         pivot.setP(random.uniform(0, 360))
         pivot.setR(random.uniform(0, 360))
         for i in range(numDrones):
              Drone.droneCount += 1
              droneName = groupName + str(Drone.droneCount)
              unitVec = CircleX(i, numDrones)
              unitVec.normalize()
              relPos = unitVec * radius * 250
              Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", pivot, droneName, "./Assets/DroneDefender/octotoad1_auv.png", relPos, 5)
         self.orbitPivots.append((pivot, 0.02))  
    def drawRockRing(self, centralObject, rockName, numRocks, radius = 1):
        pivot = centralObject.modelNode.attachNewNode(rockName + "-pivot")
        pivot.setScale(self.render, 1)
        pivot.setPos(0, 0, 0)
        pivot.setP(random.uniform(0, 360))
        pivot.setR(random.uniform(0, 360))
        totalRocks = numRocks * 10 
        for i in range(totalRocks):
            unitVec = RockRing(i, totalRocks, radius)
            relPos = unitVec * radius * 62.75
            Rock(self.loader, "./Assets/Rock/Rock.x", pivot, rockName + str(i), "./Assets/Rock/Rock.png", relPos, 60)
        self.orbitPivots.append((pivot, 0.01))

    def launchRock(self, task):
        rocks = self.render.findAllMatches("**/*Rock*")
        if not rocks.isEmpty():
            rock = rocks[random.randint(0, rocks.getNumPaths() - 1)]
            if "-pivot" in rock.getParent().getName():
                playerPos = self.Player.modelNode.getPos(self.render)
                rockPos = rock.getPos(self.render)
                trajectory = playerPos - rockPos
                trajectory.normalize()
                rock.wrtReparentTo(self.render)
                taskMgr.add(self.rockShooting, rock.getName() + "-fly", extraArgs=[rock, trajectory], appendTask=True)
        
        return task.again

    def rockShooting(self, rockNode, trajectory, task):
        if rockNode.isEmpty():
            return task.done
        speed = 400.0
        rockNode.setPos(rockNode.getPos() + trajectory * speed * self.globalClock.getDt())
        if rockNode.getDistance(self.Player.modelNode) > 15000:
            rockNode.removeNode()
            return task.done
            
        return task.cont
          

    def updateAllOrbits(self, task):
        for node, speed in self.orbitPivots:
            node.setH(node.getH() + speed)
        return task.cont

    def SetCamera(self, player):
         self.disableMouse()
         self.camera.reparentTo(player.modelNode)
         self.camera.setFluidPos(0,1,0)
               

class PoorlyRenderedUniverse(InverseSphereCollideObject):
      def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          super(PoorlyRenderedUniverse,self).__init__(loader,modelPath,parentNode,nodeName, Vec3(0,0,0),.8)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
class GalaxyPlanet(SphereCollideObject): 
     def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          super(GalaxyPlanet,self).__init__(loader,modelPath,parentNode,nodeName, Vec3(0,0,0),1.0)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
          taskMgr.add(self.Rotation, nodeName + '-rotation')
     def Rotation(self, task):
          self.modelNode.setH(self.modelNode.getH() + 0.1)
          return Task.cont
class Player(SphereCollideObject, DirectObject):
     def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, traverser):
          super(Player,self).__init__(loader,modelPath,parentNode,nodeName, Vec3(0,0,0),3)
          DirectObject.__init__(self)
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
          self.cntExplode = 0
          self.explodeIntervals = {}
          self.traverser = traverser
          self.handler = CollisionHandlerEvent()
          self.handler.addInPattern('into')
          self.accept('into', self.HandleInto)
          self.EnableHUD()
          ## self.SetParticles()
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
                 inFront = aim*300
                 travVec = fireSolution + self.modelNode.getPos()
                 self.missileBay -= 1
                 tag = 'Missile-' + str(Missile.missileCount)
                 posVec = self.modelNode.getPos() + inFront
                 currentMissile = Missile(self.loader, "./Assets/Missile/phaser.x", self.render, tag, "./Assets/Missile/phaserII.jpg", posVec, 4.0)
                 Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
                 Missile.Intervals[tag].start()
                 self.traverser.addCollider(currentMissile.collisionNode, self.handler)
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
     def HandleInto(self, entry):
           fromNode = entry.getFromNodePath().getName()
           print("fromNode: " + fromNode)
           intoNode = entry.getIntoNodePath().getName()
           print("intoNode: " + intoNode)
           intoPosition = Vec3(entry.getSurfacePoint(self.render))
           tempVar = fromNode.split("_")
           print("tempVar: " + str(tempVar))
           shooter = tempVar[0]
           print("Shooter: " + str(shooter))
           tempVar = intoNode.split("_")
           print("TempVar1: " + str(tempVar))
           victim = tempVar[0]
           print("Victim: " + str(victim))
           pattern = r'[0-9]'
           strippedString = re.sub(pattern, '', victim)
           validTargets = ["Drone", "Planet", "Space Station", "Rock", "Cloud", "Seams", "CircleX", "CircleY", "CircleZ", "PlanetRock", "SunRock"]
           if strippedString in validTargets:
                 print(victim, " was hit at ", intoPosition)
                 self.DestroyObject(victim, intoPosition)
           print(shooter  + "is done shooting.")
           Missile.Intervals[shooter].finish()
     def DestroyObject(self, hitID, hitPosition):
          nodeID = self.render.find("**/" + hitID)
          if not nodeID.isEmpty():
               nodeID.detachNode()
     ## def Explode(self):
     ##      self.cntExplode += 1
     ##      tag = 'particles-' + str(self.cntExplode)
     ##      self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, duration = 4.0)
     ##      self.explodeIntervals[tag].start()
     ## def ExplodeLight(self, t):
     ##     if t >= 1.0 and self.explodeEffect:
     ##          self.explodeEffect.disable()
     ##     elif t == 0:
     ##          self.explodeEffect.start(self.explodeNode)
     ## def SetParticles(self):
     ##      base.enableParticles()
     ##      self.explodeEffect = ParticleEffect()
     ##      self.explodeEffect.loadConfig("./Assets/Particles/basicxpldefx.ptf")
     ##      self.explodeEffect.setScale(20)
     ##      self.explodeNode = self.render.attachNewNode("ExplosionEffects")


class TheISSIGuess(CapsuleCollidableObject):
      def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          super(TheISSIGuess, self).__init__(loader, modelPath, parentNode, nodeName, 0, 1, 0, 0, -12, 0, 3)
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
class Rock(SphereCollideObject):
      def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          super(Rock,self).__init__(loader,modelPath,parentNode,nodeName, Vec3(0,0,0),1)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
class Wanderer(SphereCollideObject):
      numWanderers = 0
      def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, modelName: str,  scaleVec: Vec3,texPath: str, staringAt: Vec3):
          super(Wanderer,self).__init__(loader,modelPath,parentNode,modelName, Vec3(0,0,0),3.2)
          self.modelNode.setScale(scaleVec)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)
          self.staringAt = staringAt
          Wanderer.numWanderers += 1
          startPos = Vec3(random.uniform(-5000, 5000), random.uniform(2000, 8000), random.uniform(-2000, 2000))
          randPath1 = Vec3(random.uniform(-5000, 5000), random.uniform(2000, 8000), random.uniform(-2000, 2000))
          randPath2 = Vec3(random.uniform(-5000, 5000), random.uniform(2000, 8000), random.uniform(-2000, 2000))
          posInterval0 = self.modelNode.posInterval(15, randPath1, startPos = startPos)
          posInterval1 = self.modelNode.posInterval(20, randPath2, startPos = randPath1)
          posInterval2 = self.modelNode.posInterval(20, startPos, startPos = randPath2)
          self.travelRoute = Sequence(posInterval0, posInterval1, posInterval2, name = modelName + str(Wanderer.numWanderers))
          self.travelRoute.loop()

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
class Sun(SphereCollideObject):
      def __init__(self,loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
          super(Sun,self).__init__(loader,modelPath,parentNode,nodeName, Vec3(0,0,0),1)
          self.modelNode.setPos(posVec)
          self.modelNode.setScale(scaleVec)
          self.modelNode.setName(nodeName)
          tex = loader.loadTexture(texPath)
          self.modelNode.setTexture(tex,1)

app = MyApp()
app.run()