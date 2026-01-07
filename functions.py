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

# --- UI Helpers (Toasts) ---

def show_notification(message, type='is-info'):
    existing = document.select('.notification-toast')
    for el in existing:
        el.remove()

    box = html.DIV(Class=f"notification {type} notification-toast")
    box.style = {
        "position": "fixed",
        "top": "70px", # Abaixo do header sticky se houver
        "right": "20px",
        "left": "20px", # Centralizado no mobile
        "zIndex": "1000",
        "boxShadow": "0 2px 10px rgba(0,0,0,0.2)"
    }
    
    btn_close = html.BUTTON(Class="delete")
    btn_close.bind("click", lambda ev: box.remove())
    
    box <= btn_close
    box <= html.DIV(message)
    
    document.body <= box
    window.setTimeout(lambda: box.remove() if box.parent else None, 3000)

# --- Tab Navigation Logic ---

def switch_tab(tab_name):
    # Tabs buttons
    tabs = ['perfil', 'atributos', 'combate']
    for t in tabs:
        # Update Tab Styling
        li = document[f"tab-btn-{t}"]
        if t == tab_name:
            li.classList.add("is-active")
        else:
            li.classList.remove("is-active")
            
        # Update Content Visibility
        content = document[f"view-{t}"]
        if t == tab_name:
            content.classList.add("is-active")
        else:
            content.classList.remove("is-active")

@bind(document["tab-btn-perfil"], "click")
def nav_perfil(ev): switch_tab('perfil')

@bind(document["tab-btn-atributos"], "click")
def nav_atributos(ev): switch_tab('atributos')

@bind(document["tab-btn-combate"], "click")
def nav_combate(ev): switch_tab('combate')

# --- Stepper Logic (Plus/Minus) ---

def update_display(attr_id, value):
    # Atualiza tanto o span visual quanto o input hidden
    if f"{attr_id}out" in document:
        document[f"{attr_id}out"].textContent = value
    if attr_id in document:
        document[attr_id].value = value

def change_value(attr_id, delta, min_val, max_val):
    current = int(document[attr_id].value)
    new_val = current + delta
    
    if new_val < min_val: return
    if new_val > max_val: return
    
    # Atualiza modelo
    if attr_id in personagem.dados:
        personagem.dados[attr_id] = new_val
    
    update_display(attr_id, new_val)
    
    # Verifica pontos se for atributo
    if attr_id in ATRIBUTOS:
        verifica_soma_pontos()

def create_stepper_handlers(attr_id, min_v, max_v):
    # Bind Minus
    @bind(document[f"btn-minus-{attr_id}"], "click")
    def minus(ev):
        change_value(attr_id, -1, min_v, max_v)
        
    # Bind Plus
    @bind(document[f"btn-plus-{attr_id}"], "click")
    def plus(ev):
        change_value(attr_id, 1, min_v, max_v)

# Setup Atributos Steppers
for attr in ATRIBUTOS:
    create_stepper_handlers(attr, MIN_ATRIBUTO, MAX_ATRIBUTO)

# Setup Nivel e HP Steppers
create_stepper_handlers(NIVEL, 1, 20)
create_stepper_handlers(HP, 1, 999)

# Setup Arma Temp Stepper
@bind(document["btn-minus-arma"], "click")
def minus_arma(ev):
    curr = int(document["armadano"].value)
    if curr > 1:
        document["armadano"].value = curr - 1
        document["armadanoout"].textContent = curr - 1

@bind(document["btn-plus-arma"], "click")
def plus_arma(ev):
    curr = int(document["armadano"].value)
    if curr < 50:
        document["armadano"].value = curr + 1
        document["armadanoout"].textContent = curr + 1

# --- Core Functions ---

def update_armas():
    lista_armas = document['listaarmas']
    lista_armas.clear() # Limpa tudo para reconstruir (mais simples para Mobile Table)
    
    for nome, dano in personagem.dados[ARMAS].items():
        row = html.TR()
        
        # Coluna Nome (com data-label para CSS mobile)
        c_nome = html.TD(nome, **{'data-label': 'Nome'})
        
        # Coluna Dano
        c_dano = html.TD(dano, **{'data-label': 'Poder'})
        
        # Coluna Acao
        c_acao = html.TD(**{'data-label': 'Ação'})
        btn_remove = html.BUTTON(Class='button is-small is-danger is-outlined')
        icon = html.SPAN(Class="icon is-small")
        icon <= html.I(Class="fas fa-trash")
        btn_remove <= icon
        btn_remove.bind('click', lambda ev, n=nome: remover_arma(n))
        c_acao <= btn_remove
        
        row <= c_nome
        row <= c_dano
        row <= c_acao
        lista_armas <= row

def update_formulario_personagem():
    # Campos Texto
    document[NOME].value = personagem.dados[NOME]
    document[RACA].value = personagem.dados[RACA]
    document[DESCRICAO].value = personagem.dados[DESCRICAO]
    
    # Steppers
    update_display(NIVEL, personagem.dados[NIVEL])
    update_display(HP, personagem.dados[HP])
    
    for attr in ATRIBUTOS:
        update_display(attr, personagem.dados[attr])
        
    update_armas()
    verifica_soma_pontos()

def verifica_soma_pontos():
    personagem.calc_pontos_restantes()
    span_pontos = document['somapontos']
    
    if personagem.pontos_restantes > 0:
        span_pontos.textContent = f'{personagem.pontos_restantes}'
        span_pontos.className = 'tag is-medium is-warning'
    elif personagem.pontos_restantes == 0:
        span_pontos.textContent = 'OK'
        span_pontos.className = 'tag is-medium is-success'
    else:
        span_pontos.textContent = f'{personagem.pontos_restantes}'
        span_pontos.className = 'tag is-medium is-danger'

# --- Event Listeners Inputs Texto ---

@bind(document[NOME], "change")
def changenome(ev):
    personagem.dados[NOME] = document[NOME].value

@bind(document[RACA], "change")
def changeraca(ev):
    personagem.dados[RACA] = document[RACA].value

@bind(document[DESCRICAO], "change")
def changedescricao(ev):
    personagem.dados[DESCRICAO] = document[DESCRICAO].value

# --- Actions ---

@bind(document['addarma'], "click")
def addarma(ev):
    nome_arma = document['armanome'].value.strip()
    dano_arma = document['armadano'].value
    
    if not nome_arma:
        show_notification('Digite o nome da arma.', 'is-warning')
        return
        
    personagem.dados[ARMAS][nome_arma] = dano_arma
    document['armanome'].value = ''
    update_armas()
    show_notification('Arma adicionada!', 'is-success')

def remover_arma(nome_arma):
    if nome_arma in personagem.dados[ARMAS]:
        del personagem.dados[ARMAS][nome_arma]
        update_armas()

@bind(document['deletar'], "click")
def deletar(ev):
    if window.confirm("Apagar tudo?"):
        personagem.deletar()
        update_formulario_personagem()
        show_notification('Resetado!', 'is-success')

@bind(document['salvar'], "click")
def salvar(ev):
    personagem.calc_pontos_restantes()
    if personagem.pontos_restantes < 0:
        show_notification('Limite de pontos excedido!', 'is-danger')
    else:
        personagem.salvar()
        show_notification('Salvo!', 'is-success')

@bind(document['rolar'], "click")
def rolar(ev):
    caracter_name = document['caracter'].value
    mapa_atributos = {
        'Inteligência': INTELIGENCIA, 'Força': FORCA, 'Destreza': DESTREZA,
        'Carisma': CARISMA, 'Constituição': CONSTITUICAO
    }
    
    chave_attr = mapa_atributos.get(caracter_name)
    if not chave_attr: return

    valor_atributo = personagem.dados[chave_attr]
    dado = random.randint(1, 20)
    resultado = valor_atributo - (20 - dado)
    diferenca = abs(resultado * personagem.dados[NIVEL])
    
    msg = ""
    tipo = ""
    
    if resultado > 0:
        msg = f'SUCESSO! (Dado: {dado}) Saldo: {diferenca}'
        tipo = 'is-success'
    elif resultado < 0:
        msg = f'FALHA! (Dado: {dado}) Dano: {diferenca}'
        tipo = 'is-danger'
    else:
        msg = f'NEUTRO (Dado: {dado})'
        tipo = 'is-info'
        
    show_notification(msg, tipo)

# Inicializacao
update_formulario_personagem()
