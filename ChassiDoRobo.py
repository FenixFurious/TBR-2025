from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from umath import pi, cos
hub = PrimeHub()

class Chassi():
    def __init__(self):
        self.motor_dir = Motor(Port.D)
        self.motor_esq = Motor(Port.C,Direction.COUNTERCLOCKWISE)
        self.sensor_linha = ColorSensor(Port.E)

        self.velMax = 900
        self.velMin = 150
        self.distDesacelera = 15
        self.angDesacelera = 50

        self.ref = 45
        self.kp_linha = 3
        

    def autopilot(self,vel,dist):
        self.motor_esq.reset_angle(0)
        self.motor_dir.reset_angle(0)
        dist_atual = (self.motor_dir.angle() + self.motor_esq.angle()) /2
        while dist_atual < dist:
            dist_atual = (self.motor_dir.angle() + self.motor_esq.angle()) /2
            self.motor_dir.run(vel)
            self.motor_esq.run(vel)
        self.motor_dir.brake()
        self.motor_esq.brake()

    def autopilot_ang(self):
        pass

    def curva(self,vel, ang):
        pass

 
class Common:
    def __init__(self,chassi):
        self.chassi = chassi
        self.kp = 7
        self.ki = 0
        self.kd = 9
        self.referencia = 48
        self.reflexao = self.chassi.sensor_linha.hsv().v
        self.diam = 56
        self.circunferenciaRoda = self.diam * pi
        self.erro_anterior = 0
        self.cronometro = StopWatch()
        self.ultimo_print = 0
         
       
    def reset_pid(self):
        self.erro = 0
        self.pid = 0

    def calcular_pid(self): #colca um verbo
        
        self.reflexao = self.chassi.sensor_linha.hsv().v
        self.erro = self.referencia - self.reflexao
        self.derivativo = self.erro - self.erro_anterior
        self.pid = (self.erro * self.kp) + (self.derivativo * self.kd)
        self.erro_anterior = self.erro
    
    def telemetria_tick(self):
        
        
        tempo_atual = self.cronometro.time()

        if tempo_atual - self.ultimo_print >= 400:
            self.calcular_pid()

            self.reflexao = self.chassi.sensor_linha.hsv().v

            print(f"Reflexão:{self.reflexao} ref:{self.referencia}")
            print(f"p{self.erro*self.kp} D:{self.derivativo*self.kd} Pid:{self.pid}")
            self.ultimo_print = tempo_atual
        
       

       
    

    def posicao_cm_robo(self): #diga melhor o que ela faz
        pos_dir = (self.chassi.motor_dir.angle() * 17.58 ) / 360
        pos_esq = (self.chassi.motor_esq.angle() * 17.58 ) / 360
        self.pos_atual = (pos_dir + pos_esq) / 2
        
    
    def segue_linha(self, vel,distancia,lado):
        self.reset_pid()
        self.posicao_cm_robo()
        self.dist_inicial = self.pos_atual
        lado == str
        
        while (self.pos_atual - self.dist_inicial) < distancia:
            self.telemetria_tick()
            self.calcular_pid()
            if (lado ==  "direita") or (lado =="Direito"):
                self.chassi.motor_dir.run(vel - self.pid*(1))
                self.chassi.motor_esq.run(vel + self.pid*(1))
            elif (lado == "esquerda") or (lado =="Esquerda") :
                self.chassi.motor_dir.run(vel - self.pid*(-1))
                self.chassi.motor_esq.run(vel + self.pid*(-1))
            self.posicao_cm_robo()
            

        self.chassi.motor_dir.brake()
        self.chassi.motor_esq.brake()
        wait(5)# mais
chassi = Chassi()
common = Common(chassi)
common.segue_linha(350,150,"direita")
