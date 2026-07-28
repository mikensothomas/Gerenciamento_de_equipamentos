from fastapi import APIRouter, Response, status, Query
from DB import db
from typing import Annotated

itemCardapio_routes = APIRouter(tags=['Cardapio'])
database = db.Database()

@itemCardapio_routes.get("/itens")
def itemCardapio():
    return database.getData()

@itemCardapio_routes.post("/itens", status_code=status.HTTP_201_CREATED)
def cadastroItemCardapio(payload:dict):
    database.insert(
        payload['id'],
        payload
    )
    return Response(status_code=status.HTTP_201_CREATED)

@itemCardapio_routes.get("/itens/dispo")
def getItensDisponiveis(disponivel : Annotated[bool, Query(description="VAlor de query inválido")]):
    disponiveis = database.getData()

    if disponiveis is None:
        return disponiveis

    retorno = {}

    for item in disponiveis:
        if disponiveis[item]["disponivel"] == disponivel:
            retorno[item]=disponiveis[item]
    return retorno