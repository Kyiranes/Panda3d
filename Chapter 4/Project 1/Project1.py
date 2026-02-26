from direct.showbase.ShowBase import ShowBase
import sys
class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.Universe = Universe(self.loader,self.render)
        self.Planet1 = self.loader.loadModel("./Assets/Planets/Planet1/protoPlanet.x")
        self.Planet1.reparentTo(self.render)
        self.Planet1.setPos(150, 5000, 7)
        self.Planet1.setScale(350)
        tex = self.loader.loadTexture("./Assets/Planets/Planet1/Planet1.jpg")
        self.Planet1.setTexture(tex, 1)

        self.Planet2 = self.loader.loadModel("./Assets/Planets/Planet2/protoPlanet.x")
        self.Planet2.reparentTo(self.render)
        self.Planet2.setPos(1000, 2000, 174)
        self.Planet2.setScale(350)
        tex = self.loader.loadTexture("./Assets/Planets/Planet2/Planet2.jpg")
        self.Planet2.setTexture(tex, 1)

        self.Planet3 = self.loader.loadModel("./Assets/Planets/Planet3/protoPlanet.x")
        self.Planet3.reparentTo(self.render)
        self.Planet3.setPos(850, 1000, 270)
        self.Planet3.setScale(350)
        tex = self.loader.loadTexture("./Assets/Planets/Planet3/Planet3.jpg")
        self.Planet3.setTexture(tex, 1)

        self.Planet4 = self.loader.loadModel("./Assets/Planets/Planet4/protoPlanet.x")
        self.Planet4.reparentTo(self.render)
        self.Planet4.setPos(450, 3000, 245)
        self.Planet4.setScale(350)
        tex = self.loader.loadTexture("./Assets/Planets/Planet4/Planet4.jpg")
        self.Planet4.setTexture(tex, 1)

        self.Planet5 = self.loader.loadModel("./Assets/Planets/Planet5/protoPlanet.x")
        self.Planet5.reparentTo(self.render)
        self.Planet5.setPos(1500, 5000, 800)
        self.Planet5.setScale(350)
        tex = self.loader.loadTexture("./Assets/Planets/Planet5/Planet5.jpg")
        self.Planet5.setTexture(tex, 1)

        self.Planet6 = self.loader.loadModel("./Assets/Planets/Planet6/protoPlanet.x")
        self.Planet6.reparentTo(self.render)
        self.Planet6.setPos(1400, 4000, 1700)
        self.Planet6.setScale(350)
        tex = self.loader.loadTexture("./Assets/Planets/Planet6/Planet6.jpg")
        self.Planet6.setTexture(tex, 1)
        
        self.spaceStation = self.loader.loadModel("./Assets/SpaceStation/spaceStation.x")
        self.spaceStation.reparentTo(self.render)
        self.spaceStation.setPos(2000, 1000, 250)
        self.spaceStation.setScale(50)
        tex = self.loader.loadTexture("./Assets/SpaceStation/SpaceStation1_Dif2.png")
        self.spaceStation.setTexture(tex, 1)
        self.spaceShip = self.loader.loadModel("./Assets/Spaceships/Phaser/phaser.x")
        self.spaceShip.reparentTo(self.render)
        self.spaceShip.setPos(3000, 1000, 50)
        self.spaceShip.setScale(50)
        tex = self.loader.loadTexture("./Assets/Spaceships/Phaser/phaser_auv.jpg")
        self.spaceShip.setTexture(tex, 1)
        self.accept("escape",self.quit)

    def quit(self):
            sys.exit()
class Universe:
     def __init__(self,loader,render):
          self.model = loader.loadModel("./Assets/Universe/Universe.x")
          self.model.reparentTo(render)
          self.model.setScale(15000)
          tex = loader.loadTexture("./Assets/Universe/Universe.jpg")
          self.model.setTexture(tex, 1)
class Planet: 
    
          
app = MyApp()
app.run()