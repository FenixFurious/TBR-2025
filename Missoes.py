from Anexos import Garra, Rede
from ChassiDoRobo import Chassi



class Executa_missoes:
    def __init__(self):
        self.sensor_cor = ColorSensor(Port.X)
        self.garra = Garra()
        self.chassi = Chassi()
        self.rede = Rede() 

        self.carrinhos = []
        self.ultimo_carrinho = 0

    def pegaCaixa(self):
        self.robo.chassi.autopilot(500,360)
        self.robo.garra.fechar(190)

    def deixaCaixa(self):
        self.robo.chassi.autopilot(-500,360)
        self.robo.garra.fechar(0)

    def cor_carrinho(self):
        carrinho_lido = 0
        hue = self.sensor_carro.hsv().h
        if hue >= 210 and hue <= 240:
            carrinho_lido = carrinho _lido + 1
            self.carrinhos.append('azul')
        elif hue >= 40 and hue <= 90:
            self.carrinhos.append("amarelo")
            carrinho_lido = carrinho_lido + 1
        elif hue <= 140 and hue >=90: 
            self.carrinhos.append("verde")
            carrinho_lido = carrinho_lido + 1
        elif hue >= 240 and hue <= 270:
            cor = 
            self.carrinhos.append("cinza")
            carrinho_lido = carrinho_lido + 
        return carrinho_lido



        

