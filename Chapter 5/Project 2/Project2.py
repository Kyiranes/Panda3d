from direct.showbase.ShowBase import ShowBase
from panda3d.core import TransparencyAttrib
import sys
import DefensePaths as defensePaths
import Project2Classes as project2Classes
class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.Universe = project2Classes.PoorlyRenderedUniverse(self.loader, "./Assets/Universe/Universe.x",self.render,"Universe","./Assets/Universe/Universe.png",(0,0,0), 10000)
        self.Planet1 = project2Classes.GalaxyPlanet(self.loader,"./Assets/Planets/Planet1/protoPlanet.x",self.render,"Planet1","./Assets/Planets/Planet1/Planet1.png", (1150, 5000, 7), 250)
        self.Planet2 = project2Classes.GalaxyPlanet(self.loader,"./Assets/Planets/Planet2/protoPlanet.x",self.render,"Planet2","./Assets/Planets/Planet1/Planet1.png", (500, 9000, 700), 400)
        self.Planet3 = project2Classes.GalaxyPlanet(self.loader,"./Assets/Planets/Planet3/protoPlanet.x",self.render,"Planet3","./Assets/Planets/Planet1/Planet1.png", (1000, 2000, 174), 100)
        self.Planet4 = project2Classes.GalaxyPlanet(self.loader,"./Assets/Planets/Planet4/protoPlanet.x",self.render,"Planet4","./Assets/Planets/Planet1/Planet1.png", (850, 7000, 270), 700)
        self.Planet5 = project2Classes.GalaxyPlanet(self.loader,"./Assets/Planets/Planet5/protoPlanet.x",self.render,"Planet5","./Assets/Planets/Planet1/Planet1.png", (450, 3000, 245), 1600)
        self.Planet6 = project2Classes.GalaxyPlanet(self.loader,"./Assets/Planets/Planet6/protoPlanet.x",self.render,"Planet6","./Assets/Planets/Planet1/Planet1.png", (1500, 5000, 800), 500)
        self.Player = project2Classes.Player(self.loader, "./Assets/Spaceships/Phaser/phaser.x",self.render,"Player","./Assets/Spaceships/Phaser/phaserll.jpg", (100, 100, 100), 60)
        self.Spacestation = project2Classes.TheISSIGuess(self.loader, "./Assets/SpaceStation/spaceStation.x", self.render, "Space Station", "./Assets/SpaceStation/SpaceStation1_Dif2", (2000, 1000, 250),300)
        self.accept("escape",self.quit)
        fullCycle = 60
        for j in range(fullCycle):
          project2Classes.Drone.droneCount += 1
          nickName = "Drone" + str(project2Classes.Drone.droneCount)
          self.DrawCloudDefense(self.Planet1, nickName)
          self.DrawBaseballSeams(self.Spacestation1, nickName, j, fullCycle, 2)

    def quit(self):
            sys.exit()
    def DrawBaseballSeams(self,centralObject, droneName, step, numSeams, radius = 1):
         unitVec = defensePaths.BaseballSeams(step,numSeams, B = 0.4)
         unitVec.normalize()
         position = unitVec * radius * 250 + centralObject.modelNode.getPos()
         project2Classes.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)
    def DrawCloudDefense(self, centralObject, droneName):
         unitVec = defensePaths.Cloud()
         unitVec.normalize()
         position = unitVec * 500 + centralObject.modelNode.getPos()
         project2Classes.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 10)

         
         
app = MyApp()
app.run()