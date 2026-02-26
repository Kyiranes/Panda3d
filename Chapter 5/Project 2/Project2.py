from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, NodePath, Loader, Texture
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

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.Universe = PoorlyRenderedUniverse(self.loader, "./Assets/Universe/Universe.x",self.render,"Universe","./Assets/Universe/Universe.jpg",(0,0,0), 10000)
        self.Planet1 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet1/protoPlanet.x",self.render,"Planet1","./Assets/Planets/Planet1/Planet1.png", (1150, 5000, 7), 250)
        self.Planet2 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet2/protoPlanet.x",self.render,"Planet2","./Assets/Planets/Planet2/Planet2.png", (500, 9000, 700), 400)
        self.Planet3 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet3/protoPlanet.x",self.render,"Planet3","./Assets/Planets/Planet3/Planet3.png", (1000, 2000, 174), 100)
        self.Planet4 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet4/protoPlanet.x",self.render,"Planet4","./Assets/Planets/Planet4/Planet4.png", (850, 7000, 270), 400)
        self.Planet5 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet5/protoPlanet.x",self.render,"Planet5","./Assets/Planets/Planet5/Planet5.png", (450, 3000, 245), 600)
        self.Planet6 = GalaxyPlanet(self.loader,"./Assets/Planets/Planet6/protoPlanet.x",self.render,"Planet6","./Assets/Planets/Planet6/Planet6.png", (1500, 5000, 800), 500)
        self.Player = Player(self.loader, "./Assets/Spaceships/Phaser/phaser.x",self.render,"Player","./Assets/Spaceships/Phaser/phaserII.jpg", (100, 100, 100), 60)
        self.Spacestation = TheISSIGuess(self.loader, "./Assets/SpaceStation/spaceStation.x", self.render, "Space Station", "./Assets/SpaceStation/SpaceStation1_Dif2.png", (2000, 1000, 250),300)
        self.accept("escape",self.quit)
        fullCycle = 60
        for j in range(fullCycle):
          Drone.droneCount += 1
          nickName = "Drone" + str(Drone.droneCount)
          self.DrawCloudDefense(self.Planet1, nickName)
          self.DrawBaseballSeams(self.Spacestation, nickName, j, fullCycle, 2)
          self.DrawCircleXDefense(self.Planet2, nickName, j, fullCycle, 2)
          self.DrawCircleYDefense(self.Planet3, nickName, j, fullCycle, 2)
          self.DrawCircleZDefense(self.Planet4, nickName, j, fullCycle, 2)
    
    def quit(self):
            sys.exit()
    def DrawBaseballSeams(self,centralObject, droneName, step, numDrones, radius = 1):
         unitVec = BaseballSeams(step,numDrones, B = 0.4)
         unitVec.normalize()
         position = unitVec * radius * 250 + centralObject.modelNode.getPos()
         Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)
    def DrawCloudDefense(self, centralObject, droneName):
         unitVec = Cloud()
         unitVec.normalize()
         position = unitVec * 500 + centralObject.modelNode.getPos()
         Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 10)
    def DrawCircleZDefense(self, centralObject, droneName, step, numDrones, radius = 1):
         unitVec = CircleZ(step, numDrones)
         unitVec.normalize()
         position = unitVec * radius * 250 + centralObject.modelNode.getPos()
         Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)
    def DrawCircleYDefense(self, centralObject, droneName, step, numDrones, radius = 1):
         unitVec = CircleY(step, numDrones)
         unitVec.normalize()
         position = unitVec * radius * 250 + centralObject.modelNode.getPos()
         Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)
    def DrawCircleXDefense(self, centralObject, droneName, step, numDrones, radius = 1):
         unitVec = CircleX(step, numDrones)
         unitVec.normalize()
         position = unitVec * radius * 250 + centralObject.modelNode.getPos()
         Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)


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

          
app = MyApp()
app.run()