from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from Missoes import Executa_missoes
from Anexos import Garra
from ChassiDoRobo import Chassi

hub = PrimeHub()
class Robo():
    def __init__(self):
        self.garra = Garra()
        self.chassi = Chassi()
        self.executarMissoes = Executa_missoes(self.chassi)

    
    def setor_1(self):
        self.chassi.autopilot_ang(600,300,0)


caranga = Robo()
caranga.setor_1()
 
        


       

