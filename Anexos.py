from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

class Garra:
    def __init__(self):
        self.motor = Motor(Port.D,Direction.COUNTERCLOCKWISE)

    def pegaCaixa(self,grau):
        self.motor.run_angle(700,grau,Stop.HOLD)

    def deixaCaixa(self,grau):
        self.motor.run_angle(700,grau)
