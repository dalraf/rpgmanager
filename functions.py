from browser import document, bind


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


soma_pontos()
