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


def update_formulario_personagem():
    document['nome'].value = personagem.nome
    document['nivel'].value = personagem.nivel
    document['forca'].value = personagem.forca
    document['inteligencia'].value = personagem.inteligencia
    document['carisma'].value = personagem.carisma
    document['constituicao'].value = personagem.constituicao
    document['destreza'].value = personagem.destreza
    for arma in personagem.armas:
        coluna1 = html.TD(arma[0])
        coluna2 = html.TD(arma[1])
        coluna3 = html.TD(html.BUTTON('Remover', Class='button is-info'))
        linha = html.TR()
        linha <= coluna1
        linha <= coluna2
        linha <= coluna3
        document['listarma'] <= linha


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
    personagem.nivel = int(document['nivel'].value)


@bind(document['nome'], "change")
def changenome(evs):
    personagem.nome = document['nome'].value


@bind(document['raca'], "change")
def changeraca(evs):
    personagem.raca = document['raca'].value


@bind(document['inteligencia'], "change")
def slidechangeinteligencia(evs):
    document['outputinteligencia'].textContent = document['inteligencia'].value
    personagem.inteligencia = int(document['inteligencia'].value)
    verifica_soma_pontos()


@bind(document['forca'], "change")
def slidechangeforca(evs):
    document['outputforca'].textContent = document['forca'].value
    personagem.forca = int(document['forca'].value)
    verifica_soma_pontos()


@bind(document['destreza'], "change")
def slidechangedestreza(evs):
    document['outputdestreza'].textContent = document['destreza'].value
    personagem.destreza = int(document['destreza'].value)
    verifica_soma_pontos()


@bind(document['carisma'], "change")
def slidechangecarisma(evs):
    document['outputcarisma'].textContent = document['carisma'].value
    personagem.carisma = int(document['carisma'].value)
    verifica_soma_pontos()


@bind(document['constituicao'], "change")
def slidechangeconstiruicao(evs):
    document['outputconstituicao'].textContent = document['constituicao'].value
    personagem.constituicao = int(document['constituicao'].value)
    verifica_soma_pontos()


@bind(document['armadano'], "change")
def changedanoarma(evs):
    document['armadanoout'].textContent = document['armadano'].value


@bind(document['addarma'], "click")
def addarma(evs):
    personagem.armas.append(
        [document['armanome'].value, document['armadano'].value])
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


update_formulario_personagem()

verifica_soma_pontos()
