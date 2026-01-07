from browser import document, bind, html, window
from browser.local_storage import storage
import random
import json

# Constants
MAX_PONTOS_TOTAIS = 50
MIN_ATRIBUTO = 6
MAX_ATRIBUTO = 15
HP_PADRAO = 50
NIVEL_PADRAO = 1
ATRIBUTO_PADRAO = 8

# Keys
NOME = 'nome'
RACA = 'raca'
NIVEL = 'nivel'
HP = 'hp'
FORCA = 'forca'
INTELIGENCIA = 'inteligencia'
CARISMA = 'carisma'
CONSTITUICAO = 'constituicao'
DESTREZA = 'destreza'
ARMAS = 'armas'
DESCRICAO = 'descricao'

ATRIBUTOS = [FORCA, INTELIGENCIA, CARISMA, CONSTITUICAO, DESTREZA]

class Personagem:
    def __init__(self, storage):
        self.storage = storage
        if self.storage.get('dados'):
            try:
                self.dados = json.loads(self.storage['dados'])
            except:
                self.dados = {}
        else:
            self.dados = {}
            
        self.dados[NOME] = self.dados.get(NOME) or ''
        self.dados[RACA] = self.dados.get(RACA) or ''
        self.dados[DESCRICAO] = self.dados.get(DESCRICAO) or ''
        self.dados[NIVEL] = self.dados.get(NIVEL) or NIVEL_PADRAO
        self.dados[HP] = self.dados.get(HP) or HP_PADRAO
        
        # Atributos
        self.dados[FORCA] = self.dados.get(FORCA) or ATRIBUTO_PADRAO
        self.dados[INTELIGENCIA] = self.dados.get(INTELIGENCIA) or ATRIBUTO_PADRAO
        self.dados[CARISMA] = self.dados.get(CARISMA) or ATRIBUTO_PADRAO
        self.dados[CONSTITUICAO] = self.dados.get(CONSTITUICAO) or ATRIBUTO_PADRAO
        self.dados[DESTREZA] = self.dados.get(DESTREZA) or ATRIBUTO_PADRAO
        
        self.dados[ARMAS] = self.dados.get(ARMAS) or {}

    def salvar(self):
        self.storage['dados'] = json.dumps(self.dados, ensure_ascii=False)

    def deletar(self):
        if 'dados' in self.storage:
            del self.storage['dados']
        self.dados = {
            NOME: '',
            RACA: '',
            DESCRICAO: '',
            NIVEL: NIVEL_PADRAO,
            HP: HP_PADRAO,
            FORCA: ATRIBUTO_PADRAO,
            INTELIGENCIA: ATRIBUTO_PADRAO,
            CARISMA: ATRIBUTO_PADRAO,
            CONSTITUICAO: ATRIBUTO_PADRAO,
            DESTREZA: ATRIBUTO_PADRAO,
            ARMAS: {}
        }

    def calc_pontos_restantes(self):
        soma_atributos = sum(self.dados[attr] for attr in ATRIBUTOS)
        self.pontos_restantes = MAX_PONTOS_TOTAIS - soma_atributos

personagem = Personagem(storage)

# --- UI Helpers ---

def show_notification(message, type='is-info'):
    """
    Exibe uma notificação usando classes do Bulma.
    type: is-info, is-success, is-warning, is-danger
    """
    # Remove notificacao anterior se existir
    existing = document.select('.notification-toast')
    for el in existing:
        el.remove()

    box = html.DIV(Class=f"notification {type} notification-toast")
    box.style = {
        "position": "fixed",
        "top": "20px",
        "right": "20px",
        "zIndex": "1000",
        "maxWidth": "300px",
        "boxShadow": "0 2px 10px rgba(0,0,0,0.2)"
    }
    
    btn_close = html.BUTTON(Class="delete")
    btn_close.bind("click", lambda ev: box.remove())
    
    box <= btn_close
    box <= html.DIV(message)
    
    document.body <= box
    
    # Auto remove apos 4 segundos
    window.setTimeout(lambda: box.remove() if box.parent else None, 4000)

# --- Update Functions ---

def update_armas():
    lista_armas = document['listaarmas']
    
    # Adicionar novas
    for nome, dano in personagem.dados[ARMAS].items():
        if nome not in [child.id for child in lista_armas.children]:
            row = html.TR(id=nome)
            row <= html.TD(nome)
            row <= html.TD(dano)
            
            btn_remove = html.BUTTON('Remover', Class='button is-small is-danger is-outlined')
            btn_remove.bind('click', lambda ev, n=nome: remover_arma(n))
            
            row <= html.TD(btn_remove)
            lista_armas <= row

    # Remover deletadas
    ids_atuais = list(personagem.dados[ARMAS].keys())
    for child in list(lista_armas.children):
        if child.id not in ids_atuais:
            child.remove()

def update_formulario_personagem():
    # Campos de texto e sliders gerais
    document[NOME].value = personagem.dados[NOME]
    document[RACA].value = personagem.dados[RACA]
    document[DESCRICAO].value = personagem.dados[DESCRICAO]
    
    document[NIVEL].value = personagem.dados[NIVEL]
    document[f"{NIVEL}out"].textContent = personagem.dados[NIVEL]
    
    document[HP].value = personagem.dados[HP]
    document[f"{HP}out"].textContent = personagem.dados[HP]
    
    # Atributos
    for attr in ATRIBUTOS:
        document[attr].value = personagem.dados[attr]
        document[f"{attr}out"].textContent = personagem.dados[attr]
        
    update_armas()
    verifica_soma_pontos()

def verifica_soma_pontos():
    personagem.calc_pontos_restantes()
    span_pontos = document['somapontos']
    
    if personagem.pontos_restantes > 0:
        span_pontos.textContent = f'Faltam {personagem.pontos_restantes} pontos'
        span_pontos.className = 'tag is-warning is-light is-medium'
    elif personagem.pontos_restantes == 0:
        span_pontos.textContent = 'Pontos suficientes'
        span_pontos.className = 'tag is-success is-light is-medium'
    else:
        span_pontos.textContent = f'Excesso de {abs(personagem.pontos_restantes)} pontos!'
        span_pontos.className = 'tag is-danger is-light is-medium'

# --- Event Handlers ---

# Handler Genérico para Atributos
def create_attr_handler(attr_name):
    def handler(ev):
        val = int(ev.target.value)
        personagem.dados[attr_name] = val
        document[f"{attr_name}out"].textContent = val
        verifica_soma_pontos()
    return handler

# Bind nos atributos
for attr in ATRIBUTOS:
    document[attr].bind("input", create_attr_handler(attr))

@bind(document[NIVEL], "input")
def changenivel(ev):
    val = int(ev.target.value)
    document[f"{NIVEL}out"].textContent = val
    personagem.dados[NIVEL] = val

@bind(document[HP], "input")
def changehp(ev):
    val = int(ev.target.value)
    document[f"{HP}out"].textContent = val
    personagem.dados[HP] = val

@bind(document[NOME], "change")
def changenome(ev):
    personagem.dados[NOME] = document[NOME].value

@bind(document[RACA], "change")
def changeraca(ev):
    personagem.dados[RACA] = document[RACA].value

@bind(document[DESCRICAO], "change")
def changedescricao(ev):
    personagem.dados[DESCRICAO] = document[DESCRICAO].value

@bind(document['armadano'], "input")
def changedanoarma(ev):
    document['armadanoout'].textContent = ev.target.value

@bind(document['addarma'], "click")
def addarma(ev):
    nome_arma = document['armanome'].value.strip()
    dano_arma = document['armadano'].value
    
    if not nome_arma:
        show_notification('O nome da arma não pode estar vazio.', 'is-warning')
        return
        
    personagem.dados[ARMAS][nome_arma] = dano_arma
    document['armanome'].value = ''  # Limpa input
    update_armas()
    show_notification(f'Arma "{nome_arma}" adicionada!', 'is-success')

def remover_arma(nome_arma):
    if nome_arma in personagem.dados[ARMAS]:
        del personagem.dados[ARMAS][nome_arma]
        update_armas()

@bind(document['deletar'], "click")
def deletar(ev):
    # Simples confirmacao via browser nativo por seguranca, ou poderia ser modal customizado
    if window.confirm("Tem certeza que deseja apagar o personagem?"):
        personagem.deletar()
        update_formulario_personagem()
        show_notification('Personagem apagado com sucesso!', 'is-success')

@bind(document['salvar'], "click")
def salvar(ev):
    personagem.calc_pontos_restantes()
    
    if personagem.pontos_restantes > 0:
        show_notification(f'Ainda faltam distribuir {personagem.pontos_restantes} pontos.', 'is-warning')
    elif personagem.pontos_restantes < 0:
        show_notification('Você ultrapassou o limite de 50 pontos!', 'is-danger')
    else:
        personagem.salvar()
        show_notification('Personagem salvo com sucesso!', 'is-success')

@bind(document['rolar'], "click")
def rolar(ev):
    caracter_name = document['caracter'].value
    
    # Mapeamento de nome amigavel para chave interna
    mapa_atributos = {
        'Inteligência': INTELIGENCIA,
        'Força': FORCA,
        'Destreza': DESTREZA,
        'Carisma': CARISMA,
        'Constituição': CONSTITUICAO
    }
    
    chave_attr = mapa_atributos.get(caracter_name)
    if not chave_attr:
        return

    valor_atributo = personagem.dados[chave_attr]
    dado = random.randint(1, 20)
    
    # Logica original mantida: resultado = atributo - (20 - dado)
    # Se dado = 20, resultado = atributo. Se dado = 1, resultado = atributo - 19.
    resultado = valor_atributo - (20 - dado)
    
    diferenca = abs(resultado * personagem.dados[NIVEL])
    
    msg = ""
    tipo = ""
    
    if resultado > 0:
        msg = f'SUCESSO! (Dado: {dado})\nSaldo: {diferenca}'
        tipo = 'is-success'
    elif resultado < 0:
        msg = f'FALHA! (Dado: {dado})\nDébito: {diferenca}'
        tipo = 'is-danger'
    else:
        msg = f'NEUTRO (Dado: {dado})'
        tipo = 'is-info'
        
    show_notification(msg, tipo)

# Inicializacao
update_formulario_personagem()