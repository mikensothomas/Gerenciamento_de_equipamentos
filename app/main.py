from fastapi import FastAPI
import random
from datetime import datetime, date

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application with a custom title and description.",
    version="1.0.0",
)

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

