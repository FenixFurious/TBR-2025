from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

class Garra:
    def __init__(self):
        self.motor = Motor(Port.F)

    def fechar(self,grau = 70):
        self.motor.run_angle(600,grau,Stop.HOLD)

    def abrir(self):
        pass

    def subir(self):
        pass

    def descer(self):
        pass

class Rede:
    def __init__(self):
        self.motor = Motor(X)
        pass

    def sobe(self):
        pass

    def desce(self):
        pass
