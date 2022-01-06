from browser import document, bind, html, alert
from browser.local_storage import storage
import json


class Personagem:
    def __init__(self, storage):
        self.storage = storage
        self.dados = json.loads(self.storage.get('dados')) or {}
        self.nome = self.dados.get('nome') or ''
        self.nivel = self.dados.get('nivel') or 1
        self.forca = self.dados.get('forca') or 8
        self.inteligencia = self.dados.get('inteligencia') or 8
        self.carisma = self.dados.get('carisma') or 8
        self.constituicao = self.dados.get('constituicao') or 8
        self.destreza = self.dados.get('destreza') or 8
        self.armas = self.dados.get('armas') or []

    def salvar(self):
        self.storage['dados'] = json.dumps(self.dados)
        alert('Personagem salvo com sucesso!')

    def deletar(self):
        del self.storage['dados']
        self.dados = {}
        alert('Personagem apagado com sucesso!')

    def cacl_pontos_restantes(self):
        self.pontos_restantes = 50 - \
            (self.forca + self.inteligencia +
             self.carisma + self.constituicao + self.destreza)


personagem = Personagem(storage)


def verifica_soma_pontos():

    personagem.cacl_pontos_restantes()

    if personagem.pontos_restantes > 0:
        document['somapontos'].textContent = 'Faltam ' + \
            str(personagem.pontos_restantes) + ' pontos'
        document['somapontos'].style.color = 'black'
    elif personagem.pontos_restantes == 0:
        document['somapontos'].textContent = 'Pontos suficientes'
        document['somapontos'].style.color = 'black'
    else:
        document['somapontos'].textContent = 'Vc ultrapassou o limite de 50 pontos!'
        document['somapontos'].style.color = 'red'


@bind(document['nivel'], "change")
def changenivel(evs):
    document['nivelout'].textContent = document['nivel'].value


@bind(document['sliderinteligencia'], "change")
def slidechangeinteligencia(evs):
    document['outputinteligencia'].textContent = document['sliderinteligencia'].value
    personagem.inteligencia = document['sliderinteligencia'].value
    verifica_soma_pontos()


@bind(document['sliderforca'], "change")
def slidechangeforca(evs):
    document['outputforca'].textContent = document['sliderforca'].value
    personagem.forca = document['sliderforca'].value
    verifica_soma_pontos()


@bind(document['sliderdestreza'], "change")
def slidechangedestreza(evs):
    document['outputdestreza'].textContent = document['sliderdestreza'].value
    personagem.destreza = document['sliderdestreza'].value
    verifica_soma_pontos()


@bind(document['slidercarisma'], "change")
def slidechangecarisma(evs):
    document['outputcarisma'].textContent = document['slidercarisma'].value
    personagem.carisma = document['slidercarisma'].value
    verifica_soma_pontos()


@bind(document['sliderconstituicao'], "change")
def slidechangeconstiruicao(evs):
    document['outputconstituicao'].textContent = document['sliderconstituicao'].value
    personagem.constituicao = document['sliderconstituicao'].value
    verifica_soma_pontos()


@bind(document['armadano'], "change")
def changedanoarma(evs):
    document['armadanoout'].textContent = document['armadano'].value


@bind(document['addarma'], "click")
def addarma(evs):
    personagem.armas.append([document['armanome'].value, document['armadano'].value])
    coluna1 = html.TD(document['armanome'].value)
    coluna2 = html.TD(document['armadano'].value)
    coluna3 = html.TD(html.BUTTON('Remover', Class='button is-info'))
    linha = html.TR()
    linha <= coluna1
    linha <= coluna2
    linha <= coluna3
    document['listarma'] <= linha


@bind(document['deletar'], "click")
def deletar(evs):
    personagem.deletar()


@bind(document['salvar'], "click")
def salvar(evs):
    personagem.salvar()


verifica_soma_pontos()
