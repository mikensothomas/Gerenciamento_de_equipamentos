from fastapi import FastAPI
from routes import alunoRoute, cardapioRoutas
import random
from datetime import datetime, date
from entidades.Agenda import Agendar

from config.Config import Settings

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application with a custom title and description.",
    version="1.0.0",
)

@app.get("/config")
def consfig():
    return Settings

app.include_router(alunoRoute.alunoRoutes)
app.include_router(cardapioRoutas.itemCardapio_routes)

@app.get("/")
def read_root():
    return {"message": "Welcome to My FastAPI Application!"}

@app.get("/saudacao")
def saudacao(name):
    return {"Olá": name}

@app.get("/status")
def status():
    return {"Servidor rodando"}

@app.get("/api/version")
def version():
    return {"Versão": "v1.0.0"}

@app.get("/mensagem/inspiracao")
def inspiração():
    return {"Programação dá muito dinheiro"}

@app.get("/matematica/pi")
def calcularPI():
    pi = 3.14
    return pi

@app.get("/matematica/quadrado-de-oito")
def calcularQuadrado():

    valor = 8
    valorQuadrodado = pow(valor, 2)

    return valorQuadrodado

@app.get("/matematica/area-quadrado")
def areaQuadrado():
    lado = 15
    area = lado * lado
    return f"Àrea: {area}"

@app.get("/matematica/expressao")
def expressao():
    valor1 = 10
    valor2 = 5
    valorTotal = (valor1 + valor2) * 2
    return valorTotal

@app.get("/jogos/dado")
def calcularValorAleatorio():
    return random.randint(1, 6)

@app.get("/jogos/moeda")
def jogoMoeda():

    palavra1 = 'Cara'
    palavra2 = 'Coroa'

    return random.choice([palavra1, palavra2])

@app.get("/jogos/numero-sorte")
def calcularValor1a100():
    return random.randint(1, 100)

@app.get("/seguranca/senha-aleatoria")
def gerarPassword():
    password = ''.join(str(random.randint(0, 9)) for _ in range(4))
    return password

@app.get("/aleatorio/fruta")
def escolherFruto():
    frutas = ['Manga', 'Maçã', 'Batata', 'Malancia']

    return random.choice(frutas)

@app.get("/aleatorio/verdadeiro-falso")
def gerarTrueFalse():
    valor = ['True', 'False']
    return random.choice(valor)

@app.get("/relogio/data")
def gerarDataAtual():
    return date.today().strftime("%d/%m/%Y")

@app.get("/relogio/hora")
def gerarDataAtual():
    return datetime.now().time().strftime("%H:%M")

@app.get("/relogio/ano")
def getYear():
    return date.today().strftime("%Y")

@app.get("/relogio/mes")
def getMonth():
    return date.today().strftime("%m")

@app.get("/listas/vogais")
def getVogais():
    return ['A', 'E', 'I', 'O', 'U']

@app.get("/curiosidades/arco-iris")
def getCuriosidades():
    return ['Vermelho', 'Laranja', 'Amarelo', 'Verde', 'Azul', 'Anil', 'Violeta']

@app.get("/texto/maiusculas")
def getTextUpCase():
    text = 'programação'
    return text.upper()

@app.get("/listas/dias-semana")
def getListaDaSemana():
    return ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']

@app.get("/texto/tamanho")
def getTamanho():
    frase = 'Desenvolvimento de APIs'
    return len(frase)

# LISTA 2

@app.get("/listas/alfabeto")
def pegarAlfabeto():
    return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

@app.get("/api/geometria/retangulo/{base}/{altura}")
def fazerSoma(base: float, altura: float):
    return base * altura

@app.get("/api/listas/somar")
def somarArray():
    contador = 0
    valores = [1, 2, 3, 4, 5]

    for valor in valores:
        contador += valor
    return contador

@app.get("/api/escola/media-turma")
def mediaTurma():
    contador = 0
    valores = [7.5, 8.0, 6.5, 9.0]

    for valor in valores:
        contador += valor
    return contador / 4

@app.get("/api/matematica/tabuada/{numero}/{limite}")
def tabuada(numero: int, limite: int):
    resultado = [numero * i for i in range(1, limite + 1)]

    return (f"Tabuada: {resultado}")

@app.get("/api/listas/maior-valor")
def maiorNumero():
    maior = 0
    valores = [45, 12, 99, 3, 88]

    for valor in valores:
        if maior < valor:
            maior += valor
            maior = valor
    return maior

@app.get("/api/social/saudacoes")
def comprimentar():
    nomes = ["Ana", "Bruno", "Carlos"]

    mensagem = [f"Olá, {nome}" for nome in nomes]

    return mensagem

@app.get("/api/listas/inverter")
def inverte():
    valores = [10, 20, 30, 40]
    invertido = valores[::-1]
    return invertido

@app.post("/agenda")
def agenda(contato: Agendar):
    return {"Contato": contato}
