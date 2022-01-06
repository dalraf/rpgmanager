from browser import document, bind, html, alert
from browser.local_storage import storage
import json

dados = json.loads(storage.get('dados')) or {}


class Personagem:
    def __init__(self, dados, storage):
        self.dados = dados
        self.storage = storage
        self.nome = dados.get('nome') or ''
        self.nome = dados.get('nivel') or 8
        self.forca = dados.get('forca') or 8
        self.inteligencia = dados.get('inteligencia') or 8
        self.carisma = dados.get('carisma') or 8
        self.constituicao = dados.get('constituicao') or 8
        self.destreza = dados.get('destreza') or 8
        self.destreza = dados.get('armas') or []

    def salvar(self):
        self.storage['dados'] = json.dumps(dados)
        alert('Personagem salvo com sucesso!')

    def deletar(self):
        del self.storage['dados']
        alert('Personagem apagado com sucesso!')


personagem = Personagem(dados, storage)


def soma_pontos():
    pontos = 50 - (int(document['sliderinteligencia'].value) + int(document['sliderforca'].value) +
                   int(document['slidercarisma'].value) + int(document['sliderdestreza'].value) + int(document['sliderconstituicao'].value))

    if pontos > 0:
        document['somapontos'].textContent = 'Faltam ' + \
            str(pontos) + ' pontos'
        document['somapontos'].style.color = 'black'
    elif pontos == 0:
        document['somapontos'].textContent = 'Pontos suficientes'
        document['somapontos'].style.color = 'black'
    else:
        document['somapontos'].textContent = 'Vc ultrapassou o limite de 50 pontos!'
        document['somapontos'].style.color = 'red'


@bind(document['sliderinteligencia'], "change")
def slidechangeinteligencia(evs):
    document['outputinteligencia'].textContent = document['sliderinteligencia'].value
    soma_pontos()


@bind(document['sliderforca'], "change")
def slidechangeforca(evs):
    document['outputforca'].textContent = document['sliderforca'].value
    soma_pontos()


@bind(document['sliderdestreza'], "change")
def slidechangedestreza(evs):
    document['outputdestreza'].textContent = document['sliderdestreza'].value
    soma_pontos()


@bind(document['slidercarisma'], "change")
def slidechangecarisma(evs):
    document['outputcarisma'].textContent = document['slidercarisma'].value
    soma_pontos()


@bind(document['sliderconstituicao'], "change")
def slidechangeconstiruicao(evs):
    document['outputconstituicao'].textContent = document['sliderconstituicao'].value
    soma_pontos()


@bind(document['armadano'], "change")
def changedanoarma(evs):
    document['armadanoout'].textContent = document['armadano'].value


@bind(document['nivel'], "change")
def changenivel(evs):
    document['nivelout'].textContent = document['nivel'].value


@bind(document['addarma'], "click")
def addarma(evs):
    coluna1 = html.TD(document['armanome'].value)
    coluna2 = html.TD(document['armadano'].value)
    linha = html.TR()
    linha <= coluna1
    linha <= coluna2
    document['listarma'] <= linha


@bind(document['deletar'], "click")
def deletar(evs):
    personagem.deletar()


@bind(document['salvar'], "click")
def salvar(evs):
    personagem.salvar()


soma_pontos()
