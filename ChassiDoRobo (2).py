from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from Anexos import Garra
from umath import pi, cos
hub = PrimeHub()

class Chassi():
    def __init__(self):
        self.motor_dir = Motor(Port.B)
        self.motor_esq = Motor(Port.F,Direction.COUNTERCLOCKWISE)
        self.sensor_linha = ColorSensor(Port.A)

        self.velMax = 900
        self.velMin = 150
        self.distDesacelera = 15
        self.angDesacelera = 50

        self.referencia = 48
        self.reflexao = self.sensor_linha.hsv().v

        self.diam = 56
        self.circunferenciaRoda = self.diam * pi

        self.erro_anterior = 0
        self.cronometro = StopWatch()
        self.ultimo_print = 0

        
    def autopilot(self,vel_inicial,dist_alvo,ang_alvo):
        self.motor_dir.reset_angle(0)
        self.motor_esq.reset_angle(0)
        vel = vel_inicial * (dist_alvo / abs(dist_alvo))
        dist_atual = self.conversor_cm()
        dist_inicial = self.conversor_cm()
        porcentagemF_total = 0
        porcentagemF = 0
        while porcentagemF_total < 1:
            porcentagemF_total = (dist_atual - dist_inicial) / (dist_alvo - dist_inicial)
            print(porcentagemF_total , dist_atual)
            dist_final = dist_inicial + dist_alvo
            ponto_desacelera = dist_final - self.distDesacelera * (dist_alvo / abs(dist_alvo))
            if dist_alvo < self.distDesacelera:
                ponto_desacelera = 0  
            correcao = self.PID_autopliot(ang_alvo,hub.imu.heading())
            dist_atual = abs(self.conversor_cm())
            if dist_atual < abs(ponto_desacelera):
                vel = vel_inicial *  (dist_alvo / abs(dist_alvo))
            else:
                porcentagemF = ((abs(dist_atual) - abs(ponto_desacelera)) / self.distDesacelera)
                vel = (vel_inicial * (dist_alvo / abs(dist_alvo))) - porcentagemF * (vel_inicial * (dist_alvo / abs(dist_alvo)))
                correcao = correcao / 2
            if abs(vel) < self.velMin:
                vel = self.velMin * (dist_alvo / abs(dist_alvo))
            self.motor_dir.run(vel - correcao)
            self.motor_esq.run(vel + correcao)
        self.motor_dir.brake()
        self.motor_esq.brake()
        print(f' dist atual: {dist_atual - dist_inicial}, dist atual B:{dist_atual} angulo_atual: {hub.imu.heading()}, ponto desa{ponto_desacelera}, % feita {porcentagemF_total}')

    def autopilot_ang(self,vel_inicial,dist_alvo,ang_alvo):
        vel = vel_inicial * ( dist_alvo / abs(dist_alvo))
        self.motor_dir.reset_angle(0)
        self.motor_esq.reset_angle(0)
        dist_atual = (self.motor_dir.angle() + self.motor_esq.angle()) / 2
        print(dist_atual)
        while abs(dist_atual) < abs(dist_alvo):
            correcao = self.PID_autopliot(ang_alvo,hub.imu.heading())
            dist_atual = abs(self.motor_dir.angle())
            self.motor_dir.run(vel - correcao)
            self.motor_esq.run(vel + correcao)
        self.motor_dir.brake()
        self.motor_esq.brake()

    def curva(self,vel, ang):
        ang_inicial = hub.imu.heading()
        vel = vel_inicial
        if ang_alvo > ang_inicial: #Sentido horario
            ponto_desaceleraHorario = ang_alvo - self.angDesacelera
            ang_atual = hub.imu.heading()
            percurso_feito = ang_alvo - ang_atual
            percurso_final = ang_alvo - ang_inicial
            while ang_atual < ang_alvo:
                ang_atual = hub.imu.heading()
                if ang_atual >= ponto_desaceleraHorario:
                    vel = vel_inicial / 4
                else:
                    vel = vel_inicial 
                self.motor_dir.run(-vel)
                self.motor_esq.run(vel)
            self.motor_dir.brake()
            self.motor_esq.brake()
        elif ang_alvo < ang_inicial: #Sentido antihorario
            ang_atual = hub.imu.heading()
            ponto_desaceleraAntiHora = ang_alvo + self.angDesacelera
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
            kp_linha =  5.3
            ki = 0
            kd = 4.1
            self.reset_pid()
            self.posicao_cm_robo()
            self.dist_inicial = self.pos_atual
            while (self.pos_atual - self.dist_inicial) < distancia:
                self.telemetria_tick()
                self.calcular_pid()
                if lado.lower() == "direita" or lado.lower() == "direito":
                    self.motor_dir.run(vel - self.pid * 1)
                    self.motor_esq.run(vel + self.pid * 1)
                elif lado.lower() == "esquerda" or lado.lower() == "esquerdo":
                    self.motor_dir.run(vel - self.pid * -1)
                    self.motor_esq.run(vel + self.pid * -1)
                self.posicao_cm_robo()
            self.motor_dir.brake()
            self.motor_esq.brake()
            wait(5)

#---------------------------------------------------------#
    def PID_autopliot(self,ang_alvo,ang_atual):
        kp_ang = 2.5
        ki_ang = 0
        kd_ang = 1.2

        last_error = 0
        error = ang_alvo - ang_atual
        derivada = (error - last_error) * kd_ang
        proporcinal = error * kp_ang
        last_erro = error
        return proporcinal + derivada

    def conversor_cm(self):
        pos_dir = (self.motor_dir.angle() * 17.58 ) / 360
        pos_esq = (self.motor_esq.angle() * 17.58 ) / 360
        pos_atual = (pos_dir + pos_esq) / 2
        return pos_atual

    def reset_PID(self):
        self.erro = 0
        self.pid = 0

    def PID_seguidor(self):
        self.erro = self.referencia - self.reflexao
        self.derivativo = self.erro - self.erro_anterior
        self.pid = (self.erro * self.kp) + (self.derivativo * self.kd)
        self.erro_anterior = self.erro

    def calcular_pid(self):
        self.erro = self.referencia - self.reflexao
        self.derivativo = self.erro - self.erro_anterior
        self.pid = (self.erro * self.kp) + (self.derivativo * self.kd)
        self.erro_anterior = self.erro

    def telemetria_tick(self):
        tempo_atual = self.cronometro.time()
        if tempo_atual - self.ultimo_print >= 400:
            self.calcular_pid()
            print(f"Reflexão: {self.reflexao} ref: {self.referencia}")
            print(f"P: {self.erro * self.kp} D: {self.derivativo * self.kd} PID: {self.pid}")
            self.ultimo_print = tempo_atual





    
