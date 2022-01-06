from browser import document, bind, html, alert
from browser.local_storage import storage
import json


class Personagem:
    def __init__(self, storage):
        self.storage = storage
        if self.storage.get('dados'):
            self.dados = json.loads(self.storage['dados'])
        else:
            self.dados = {}
        self.nome = self.dados.get('nome') or ''
        self.nivel = self.dados.get('nivel') or 1
        self.forca = self.dados.get('forca') or 8
        self.inteligencia = self.dados.get('inteligencia') or 8
        self.carisma = self.dados.get('carisma') or 8
        self.constituicao = self.dados.get('constituicao') or 8
        self.destreza = self.dados.get('destreza') or 8
        self.armas = self.dados.get('armas') or {}

    def salvar(self):
        self.dados['nome'] = self.nome
        self.dados['nivel'] = self.nivel
        self.dados['forca'] = self.forca
        self.dados['inteligencia'] = self.inteligencia
        self.dados['carisma'] = self.carisma
        self.dados['constituicao'] = self.constituicao
        self.dados['destreza'] = self.destreza
        self.dados['armas'] = self.armas
        self.storage['dados'] = json.dumps(self.dados)
        alert('Personagem salvo com sucesso!')

    def deletar(self):
        del self.storage['dados']
        self.dados = {}
        self.nome = ''
        self.nivel = 1
        self.forca = 8
        self.inteligencia = 8
        self.carisma = 8
        self.constituicao = 8
        self.destreza = 8
        self.armas = {}
        alert('Personagem apagado com sucesso!')

    def cacl_pontos_restantes(self):
        self.pontos_restantes = 50 - \
            (self.forca + self.inteligencia +
             self.carisma + self.constituicao + self.destreza)


personagem = Personagem(storage)


def update_formulario_personagem():
    document['nome'].value = personagem.nome
    document['nivel'].value = personagem.nivel
    document['nivelout'].textContent = document['nivel'].value
    document['forca'].value = personagem.forca
    document['forcaout'].textContent = document['forca'].value
    document['inteligencia'].value = personagem.inteligencia
    document['inteligenciaout'].textContent = document['inteligencia'].value
    document['carisma'].value = personagem.carisma
    document['carismaout'].textContent = document['carisma'].value
    document['constituicao'].value = personagem.constituicao
    document['constituicaoout'].textContent = document['constituicao'].value
    document['destreza'].value = personagem.destreza
    document['destrezaout'].textContent = document['destreza'].value
    for nome, dano in personagem.armas.items():
        coluna1 = html.TD(nome)
        coluna2 = html.TD(dano)
        coluna3 = html.TD(html.BUTTON(
            'Remover', Class='button is-info', **{'id': nome + "action", 'value': nome}))
        linha = html.TR(**{'id': nome})
        linha <= coluna1
        linha <= coluna2
        linha <= coluna3
        document['listarma'] <= linha
        document[nome + "action"].bind('click', removerarma)


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
def changeinteligencia(evs):
    document['inteligenciaout'].textContent = document['inteligencia'].value
    personagem.inteligencia = int(document['inteligencia'].value)
    verifica_soma_pontos()


@bind(document['forca'], "change")
def changeforca(evs):
    document['forcaout'].textContent = document['forca'].value
    personagem.forca = int(document['forca'].value)
    verifica_soma_pontos()


@bind(document['destreza'], "change")
def changedestreza(evs):
    document['destrezaout'].textContent = document['destreza'].value
    personagem.destreza = int(document['destreza'].value)
    verifica_soma_pontos()


@bind(document['carisma'], "change")
def changecarisma(evs):
    document['carismaout'].textContent = document['carisma'].value
    personagem.carisma = int(document['carisma'].value)
    verifica_soma_pontos()


@bind(document['constituicao'], "change")
def changeconstituicao(evs):
    document['constituicaoout'].textContent = document['constituicao'].value
    personagem.constituicao = int(document['constituicao'].value)
    verifica_soma_pontos()


@bind(document['armadano'], "change")
def changedanoarma(evs):
    document['armadanoout'].textContent = document['armadano'].value


@bind(document['addarma'], "click")
def addarma(evs):
    if document['armanome'] != '':
        personagem.armas[document['armanome'].value] = document['armadano'].value
        coluna1 = html.TD(document['armanome'].value)
        coluna2 = html.TD(document['armadano'].value)
        coluna3 = html.TD(html.BUTTON(
            'Remover', Class='button is-info', **{'id': document['armanome'].value + "action", 'value': document['armanome'].value}))
        linha = html.TR(**{'id': document['armanome'].value})
        linha <= coluna1
        linha <= coluna2
        linha <= coluna3
        document['listarma'] <= linha
        document[document['armanome'].value +
                 "action"].bind('click', removerarma)


@ bind(document['deletar'], "click")
def deletar(evs):
    personagem.deletar()
    update_formulario_personagem()


@bind(document['salvar'], "click")
def salvar(evs):
    personagem.salvar()


def removerarma(evs):
    del document[evs.target.value]
    del personagem.armas[evs.target.value]


update_formulario_personagem()

verifica_soma_pontos()
