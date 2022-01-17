from browser import document, bind, html, alert
from browser.local_storage import storage
import random
import json

nome = 'nome'
raca = 'raca'
nivel = 'nivel'
hp = 'hp'
forca = 'forca'
inteligencia = 'inteligencia'
carisma = 'carisma'
constituicao = 'constituicao'
destreza = 'destreza'
armas = 'armas'


class Personagem:
    def __init__(self, storage):
        self.storage = storage
        if self.storage.get('dados'):
            self.dados = json.loads(self.storage['dados'])
        else:
            self.dados = {}
        self.dados[nome] = self.dados.get(nome) or ''
        self.dados[raca] = self.dados.get(raca) or ''
        self.dados[nivel] = self.dados.get(nivel) or 1
        self.dados[hp] = self.dados.get(hp) or 50
        self.dados[forca] = self.dados.get(forca) or 8
        self.dados[forca] = self.dados.get(forca) or 8
        self.dados[carisma] = self.dados.get(carisma) or 8
        self.dados[constituicao] = self.dados.get(constituicao) or 8
        self.dados[destreza] = self.dados.get(destreza) or 8
        self.dados[armas] = self.dados.get(armas) or {}

    def salvar(self):
        self.storage['dados'] = json.dumps(self.dados, ensure_ascii=False)

    def deletar(self):
        del self.storage['dados']
        self.dados = {}
        self.dados[nome] = ''
        self.dados[raca] = ''
        self.dados[nivel] = 1
        self.dados[hp] = 50
        self.dados[forca] = 8
        self.dados[inteligencia] = 8
        self.dados[carisma] = 8
        self.dados[constituicao] = 8
        self.dados[destreza] = 8
        self.dados[armas] = {}

    def cacl_pontos_restantes(self):
        self.pontos_restantes = 50 - \
            (self.dados[forca] + self.dados[inteligencia] +
             self.dados[carisma] + self.dados[constituicao] + self.dados[destreza])


personagem = Personagem(storage)


def update_armas():
    for nome, dano in personagem.armas.items():
        if nome not in [arma.id for arma in document['listaarmas'].children]:
            coluna1 = html.TD(nome)
            coluna2 = html.TD(dano)
            coluna3 = html.TD(html.BUTTON(
                'Remover', Class='button is-info', **{'id': nome + "action", 'value': nome}))
            linha = html.TR(**{'id': nome})
            linha <= coluna1
            linha <= coluna2
            linha <= coluna3
            document['listaarmas'] <= linha
            document[nome + "action"].bind('click', removerarma)

    for arma in document['listaarmas'].children:
        if arma.id not in list(personagem.armas.keys()):
            arma.remove()


def update_formulario_personagem():
    document['nome'].value = personagem.dados[nome]
    document['racas'].value = personagem.dados[raca]
    document['nivel'].value = personagem.dados[nivel]
    document['nivelout'].textContent = document['nivel'].value
    document['hp'].value = personagem.dados[hp]
    document['hpout'].textContent = document['hp'].value
    document['forca'].value = personagem.dados[forca]
    document['forcaout'].textContent = document['forca'].value
    document['inteligencia'].value = personagem.dados[inteligencia]
    document['inteligenciaout'].textContent = document['inteligencia'].value
    document['carisma'].value = personagem.dados[carisma]
    document['carismaout'].textContent = document['carisma'].value
    document['constituicao'].value = personagem.dados[constituicao]
    document['constituicaoout'].textContent = document['constituicao'].value
    document['destreza'].value = personagem.dados[destreza]
    document['destrezaout'].textContent = document['destreza'].value
    update_armas()


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
    personagem.dados[nivel] = int(document['nivel'].value)


@bind(document['hp'], "change")
def changehp(evs):
    document['hpout'].textContent = document['hp'].value
    personagem.dados[hp] = int(document['hp'].value)


@bind(document['nome'], "change")
def changenome(evs):
    personagem.dados[nome] = document['nome'].value


@bind(document['racas'], "change")
def changeraca(evs):
    personagem.dados[raca] = document['racas'].value


@bind(document['inteligencia'], "change")
def changeinteligencia(evs):
    document['inteligenciaout'].textContent = document['inteligencia'].value
    personagem.dados[inteligencia] = int(document['inteligencia'].value)
    verifica_soma_pontos()


@bind(document['forca'], "change")
def changeforca(evs):
    document['forcaout'].textContent = document['forca'].value
    personagem.dados[forca] = int(document['forca'].value)
    verifica_soma_pontos()


@bind(document['destreza'], "change")
def changedestreza(evs):
    document['destrezaout'].textContent = document['destreza'].value
    personagem.dados[destreza] = int(document['destreza'].value)
    verifica_soma_pontos()


@bind(document['carisma'], "change")
def changecarisma(evs):
    document['carismaout'].textContent = document['carisma'].value
    personagem.dados[carisma] = int(document['carisma'].value)
    verifica_soma_pontos()


@bind(document['constituicao'], "change")
def changeconstituicao(evs):
    document['constituicaoout'].textContent = document['constituicao'].value
    personagem.dados[constituicao] = int(document['constituicao'].value)
    verifica_soma_pontos()


@bind(document['armadano'], "change")
def changedanoarma(evs):
    document['armadanoout'].textContent = document['armadano'].value


@bind(document['addarma'], "click")
def addarma(evs):
    if document['armanome'] != '':
        personagem.armas[document['armanome'].value] = document['armadano'].value
        update_armas()


def removerarma(evs):
    del personagem.armas[evs.target.value]
    update_armas()


@ bind(document['deletar'], "click")
def deletar(evs):
    personagem.deletar()
    alert('Personagem apagado com sucesso!')
    update_formulario_personagem()


@bind(document['salvar'], "click")
def salvar(evs):
    if personagem.pontos_restantes > 0:
        alert('Vc ainda possui pontos restantes!')
    if personagem.pontos_restantes < 0:
        alert('Vc ultrapassou o limite de 50 pontos!')
    if personagem.pontos_restantes == 0:
        personagem.salvar()
        alert('Personagem salvo com sucesso!')
        update_formulario_personagem()


@bind(document['rolar'], "click")
def rolar(env):
    caracter_name = document['caracter'].value
    if caracter_name == 'Inteligência':
        caracter = personagem.dados[inteligencia]
    elif caracter_name == 'Força':
        caracter = personagem.dados[forca]
    elif caracter_name == 'Destreza':
        caracter = personagem.dados[destreza]
    elif caracter_name == 'Carisma':
        caracter = personagem.dados[carisma]
    elif caracter_name == 'Constituição':
        caracter = personagem.dados[constituicao]

    dado = random.randint(1, 20)
    resultado = caracter - (20 - dado)
    difer = abs(resultado * personagem.nivel)
    if resultado > 0:
        alert(f'Você ganhou! Resultado do dado {dado}, saldo de {difer}')
    if resultado < 0:
        alert(f'Você perdeu! Resultado do dado {dado}, débito de {difer}')


update_formulario_personagem()

verifica_soma_pontos()
