from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from umath import pi, cos
hub = PrimeHub()

class Chassi():
    def __init__(self, common=None):
        self.motor_dir = Motor(Port.D)
        self.motor_esq = Motor(Port.C, Direction.COUNTERCLOCKWISE)
        self.sensor_linha = ColorSensor(Port.E)
        self.common = common
        self.check = 0
        self.velMax = 900
        self.velMin = 150
        self.distDesacelera = 15
        self.angDesacelera = 50

        # Constantes PID para correção angular
        self.kp_ang = 2.5
        self.ki_ang = 0
        self.kd_ang = 1.2
        self.last_error = 0

    def proporcional_derivada(self, ang_alvo, ang_atual):
        error = ang_alvo - ang_atual
        derivada = (error - self.last_error) * self.kd_ang
        proporcional = error * self.kp_ang
        self.last_error = error
        return proporcional + derivada

    def autopilot_ang(self, vel_inicial, dist_alvo, ang_alvo):
        vel = vel_inicial * (dist_alvo / abs(dist_alvo))
        self.motor_dir.reset_angle(0)
        self.motor_esq.reset_angle(0)
        dist_atual = 0
        while abs(dist_atual) < abs(dist_alvo):
            correcao = self.proporcional_derivada(ang_alvo, hub.imu.heading())
            dist_atual = (self.motor_dir.angle() + self.motor_esq.angle()) / 2
            self.motor_dir.run(vel - correcao)
            self.motor_esq.run(vel + correcao)
        self.motor_dir.brake()
        self.motor_esq.brake()


    def curva(self, vel_inicial, ang_alvo):
        ang_inicial = hub.imu.heading()
        vel = vel_inicial
        if ang_alvo > ang_inicial:  # Sentido horário
            ponto_desaceleraHorario = ang_alvo - self.angDesacelera
            ang_atual = hub.imu.heading()
            while ang_atual < ang_alvo:
                ang_atual = hub.imu.heading()
                if ang_atual >= ponto_desaceleraHorario:
                    vel = vel_inicial / 4
                else:
                    vel = vel_inicial
                self.motor_dir.run(-vel)
                self.motor_esq.run(vel)
        elif ang_alvo < ang_inicial:  # Sentido anti-horário
            ponto_desaceleraAntiHora = ang_alvo + self.angDesacelera
            ang_atual = hub.imu.heading()
            while ang_atual > ang_alvo:
                ang_atual = hub.imu.heading()
                if ang_atual < ponto_desaceleraAntiHora:
                    vel = vel_inicial / 4
                else:
                    vel = vel_inicial
                self.motor_dir.run(vel)
                self.motor_esq.run(-vel)
        self.motor_dir.brake()
        self.motor_esq.brake()
        print(f'dist final: {hub.imu.heading()}')

    def segue_linha(self, vel, distancia, lado):
        self.common.posicao_cm_robo()
        self.common.dist_inicial = self.common.pos_atual
        while (self.common.pos_atual - self.common.dist_inicial) < distancia:
            self.common.telemetria_tick()
            self.common.calcular_pid()
            if lado.lower() == "direita" or lado.lower() == "direito":
                self.motor_dir.run(vel - self.common.pid * 1)
                self.motor_esq.run(vel + self.common.pid * 1)
            elif lado.lower() == "esquerda" or lado.lower() == "esquerdo":
                self.motor_dir.run(vel - self.common.pid * -1)
                self.motor_esq.run(vel + self.common.pid * -1)
            self.common.posicao_cm_robo()
        

class Common:
    def __init__(self, chassi):
        self.chassi = chassi
        self.kp =  5.3
        self.ki = 0
        self.kd = 4.1
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

    def calcular_pid(self):
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
            print(f"Reflexão: {self.reflexao} ref: {self.referencia}")
            print(f"P: {self.erro * self.kp} D: {self.derivativo * self.kd} PID: {self.pid}")
            self.ultimo_print = tempo_atual

    def posicao_cm_robo(self):
        pos_dir = (self.chassi.motor_dir.angle() * 17.58) / 360
        pos_esq = (self.chassi.motor_esq.angle() * 17.58) / 360
        self.pos_atual = (pos_dir + pos_esq) / 2

    def segue_linha(self, vel, distancia, lado):
        self.reset_pid()
        self.posicao_cm_robo()
        self.dist_inicial = self.pos_atual
        while (self.pos_atual - self.dist_inicial) < distancia:
            self.telemetria_tick()
            self.calcular_pid()
            if lado.lower() == "direita" or lado.lower() == "direito":
                self.chassi.motor_dir.run(vel - self.pid * 1)
                self.chassi.motor_esq.run(vel + self.pid * 1)
            elif lado.lower() == "esquerda" or lado.lower() == "esquerdo":
                self.chassi.motor_dir.run(vel - self.pid * -1)
                self.chassi.motor_esq.run(vel + self.pid * -1)
            self.posicao_cm_robo()
        self.chassi.motor_dir.brake()
        self.chassi.motor_esq.brake()
        wait(5)


chassi = Chassi()
common = Common(chassi)
chassi.common = common  

chassi.autopilot_ang(300,10,-90)
common.chassi.sensor_linha(600,80,"esquerda")

