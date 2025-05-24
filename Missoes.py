from ChassiDoRobo import Chassi


class Executa_missoes:
    def __init__(self, chassi):
        self.chassi = chassi
        self.carrinhos = []

    def ultimo_Carrinho(self):
        ultimoCar = "none"
        dist = 0
        if 'verde' not in self.carrinhos:
            ultimoCar = "verde"
            dist = 200 #MUDAR VALOR DPS
        if 'azul' not in self.carrinhos:
            ultimoCar = "azul"
            dist = 400 #MUDAR VALOR DPS
        if 'cinza' not in self.carrinhos:
            ultimoCar =  "cinza"
            dist = 300 #MUDAR VALOR DPS
        if 'amarelo' not in self.carrinhos:
            ultimoCar = "amarelo"
            dist = 500 #MUDAR VALOR DPS
            return {
                "dist": dist, 
                "ultimoCarrinho": ultimoCar
            }

    def cor_carrinho(self):
        carrinho_lido = 0
        hue = self.sensor_carro.hsv().h
        if hue >= 210 and hue <= 240:
            dist = 439 #MUDAR VALOR DPS
            carrinho_lido = carrinho_lido + 1
            self.carrinhos.append('azul')
        elif hue >= 40 and hue <= 90:
            dist = 380 #MUDAR VALOR DPS
            self.carrinhos.append("amarelo")
            carrinho_lido = carrinho_lido + 1
        elif hue <= 140 and hue >=90: 
            dist = 300 #MUDAR VALOR DPS
            self.carrinhos.append("verde")
            carrinho_lido = carrinho_lido + 1
        elif hue >= 240 and hue <= 270:
            dist = 300 #MUDAR VALOR DPS
            self.carrinhos.append('cinza')
            carrinho_lido = carrinho_lido + 1
        if len(self.carrinho > 3):
            ultimo_Carrinho()
            return {
                'dist': dist
            }
    def empurra_carrinho(self):
        distancia = cor_carrinho()
        if len(self.carrinho > 3):
            distancia = ultimoCarrinho()['dist']
        self.chassi.curva(distancia)
        self.chassi.autopilot(distancia)
        






        

