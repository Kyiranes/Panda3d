from direct.showbase.ShowBase import ShowBase
from panda3d.core import TransparencyAttrib
import sys
import random
class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.Universe = PoorlyRenderedUniverse(self.loader,self.render)
        self.Planet1 = GalaxyPlanet(self.loader,self.render,"1", (1150, 5000, 7))
        self.Planet2 = GalaxyPlanet(self.loader,self.render,"2", (500, 9000, 700))
        self.Planet3 = GalaxyPlanet(self.loader,self.render,"3", (1000, 2000, 174))
        self.Planet4 = GalaxyPlanet(self.loader,self.render,"4", (850, 7000, 270))
        self.Planet5 = GalaxyPlanet(self.loader,self.render,"5", (450, 3000, 245))
        self.Planet6 = GalaxyPlanet(self.loader,self.render,"6", (1500, 5000, 800))
        # I could do loops too if you'd prefer though idk how to avoid overlapping with this
        # planetCount = x
        # for i in range(planetCount):
        # self.Planet = GalaxyPlanet(self.loader, self.render, i, (random.randint(-9000, 9000), random.randint(-9000, 9000), random.randint(-9000, 9000)
        self.Player = Player(self.loader,self.render)
        self.Spacestation = TheISSIGuess(self.loader,self.render)
        self.accept("escape",self.quit)

    def quit(self):
            sys.exit()
class PoorlyRenderedUniverse:
     def __init__(self,loader,render):
          self.model = loader.loadModel("./Assets/Universe/Universe.x")
          self.model.reparentTo(render)
          self.model.setScale(15000)
          tex = loader.loadTexture("./Assets/Universe/Universe.jpg")
          self.model.setTexture(tex, 1)
class GalaxyPlanet: 
     def __init__(self,loader,render,PlanetNum, pos):
          self.model = loader.loadModel("./Assets/Planets/Planet" + PlanetNum +"/protoPlanet.x")
          self.model.reparentTo(render)
          self.model.setPos(pos)
          self.model.setScale(350)
          tex = loader.loadTexture("./Assets/Planets/Planet" + PlanetNum + "/Planet" + PlanetNum + ".png")
          self.model.setTexture(tex, 1)
          self.model.setTransparency(TransparencyAttrib.MAlpha)
          # Even after removing the backgrounds, the textures are STILL full of holes
          # Im going insane
class Player:
     def __init__(self,loader,render):
          self.model = loader.loadModel("./Assets/Spaceships/Phaser/phaser.x")
          self.model.reparentTo(render)
          self.model.setPos(3000, 1000, 50)
          self.model.setScale(50)
          tex = loader.loadTexture("./Assets/Spaceships/Phaser/phaser_auv.jpg")
          self.model.setTexture(tex, 1)
class TheISSIGuess:
     def __init__(self,loader,render):
          self.model = loader.loadModel("./Assets/SpaceStation/spaceStation.x")
          self.model.reparentTo(render)
          self.model.setPos(2000, 1000, 250)
          self.model.setScale(50)
          tex = loader.loadTexture("./Assets/SpaceStation/SpaceStation1_Dif2.png")
          self.model.setTexture(tex, 1)
          
app = MyApp()
app.run()